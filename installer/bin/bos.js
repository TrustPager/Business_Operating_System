#!/usr/bin/env node
/**
 * @trustpager/bos — one-command installer for the Business Operating System.
 *
 * The npm package is a thin bootstrapper (this file + a postinstall hint). The
 * real system is the public repo at github.com/TrustPager/Business_Operating_System.
 * `bos init` acquires that repo onto disk (git clone, or a tarball download if
 * git is not installed) and runs its own `tools/setup.py`, which does the actual
 * work: install the document libraries, write the ~/.claude/bos-run.py signpost,
 * copy the skills + commands into ~/.claude/, and register the keyless research
 * connector. Setup is idempotent, so re-running init on an existing clone updates.
 *
 * Commands:
 *   bos init      [--dir <path>] [--ref <branch>] [--force] [--skip-deps]
 *   bos update    [--dir <path>] [--ref <branch>]
 *   bos where     print the resolved install location
 *   bos help
 */

"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");
const https = require("https");
const { spawnSync } = require("child_process");

const REPO_SLUG = "TrustPager/Business_Operating_System";
const REPO_URL = `https://github.com/${REPO_SLUG}`;
const DIR_NAME = "Business_Operating_System";
const DEFAULT_REF = "main";

// ── tiny output helpers ──────────────────────────────────────────────────
const c = {
  dim: (s) => `\x1b[2m${s}\x1b[0m`,
  green: (s) => `\x1b[32m${s}\x1b[0m`,
  cyan: (s) => `\x1b[36m${s}\x1b[0m`,
  bold: (s) => `\x1b[1m${s}\x1b[0m`,
  red: (s) => `\x1b[31m${s}\x1b[0m`,
};
function log(msg) {
  console.log(msg);
}
function die(msg) {
  console.error(c.red("bos: ") + msg);
  process.exit(1);
}

// ── environment probes ───────────────────────────────────────────────────
function commandExists(cmd, args = ["--version"]) {
  try {
    const r = spawnSync(cmd, args, { stdio: "ignore" });
    return !r.error && (r.status === 0 || typeof r.status === "number");
  } catch (_) {
    return false;
  }
}

/**
 * Find a usable Python 3.10+. Returns { cmd, prefix } where the invocation is
 * [cmd, ...prefix, <scriptArgs>]. On Windows the `py -3` launcher is preferred
 * because a bare `python` can be the Store shim.
 */
function findPython() {
  const candidates =
    process.platform === "win32"
      ? [["py", ["-3"]], ["python", []], ["python3", []]]
      : [["python3", []], ["python", []]];

  for (const [cmd, prefix] of candidates) {
    const probe = spawnSync(cmd, [...prefix, "--version"], { encoding: "utf8" });
    if (probe.error || typeof probe.status !== "number" || probe.status !== 0) {
      continue;
    }
    const out = `${probe.stdout || ""}${probe.stderr || ""}`;
    const m = out.match(/Python\s+(\d+)\.(\d+)/i);
    if (m) {
      const major = Number(m[1]);
      const minor = Number(m[2]);
      if (major > 3 || (major === 3 && minor >= 10)) {
        return { cmd, prefix };
      }
    }
  }
  return null;
}

// ── repo acquisition ─────────────────────────────────────────────────────
function homeDir() {
  return os.homedir();
}

function readRecordedHome() {
  // setup.py writes ~/.claude/bos.json with bos_home once installed.
  try {
    const cfg = path.join(homeDir(), ".claude", "bos.json");
    const data = JSON.parse(fs.readFileSync(cfg, "utf8"));
    if (data && typeof data.bos_home === "string") return data.bos_home;
  } catch (_) {
    /* not installed yet */
  }
  return null;
}

function isBosClone(dir) {
  return !!dir && fs.existsSync(path.join(dir, "tools", "setup.py"));
}

function resolveDir(explicit) {
  if (explicit) return path.resolve(explicit);
  const recorded = readRecordedHome();
  if (isBosClone(recorded)) return recorded;
  return path.join(homeDir(), DIR_NAME);
}

function download(url, dest, redirects = 0) {
  return new Promise((resolve, reject) => {
    if (redirects > 6) return reject(new Error("too many redirects"));
    const file = fs.createWriteStream(dest);
    https
      .get(url, { headers: { "User-Agent": "trustpager-bos-installer" } }, (res) => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          file.close();
          fs.unlink(dest, () => {});
          return resolve(download(res.headers.location, dest, redirects + 1));
        }
        if (res.statusCode !== 200) {
          file.close();
          fs.unlink(dest, () => {});
          return reject(new Error(`HTTP ${res.statusCode} for ${url}`));
        }
        res.pipe(file);
        file.on("finish", () => file.close(() => resolve()));
      })
      .on("error", (err) => {
        try {
          fs.unlinkSync(dest);
        } catch (_) {}
        reject(err);
      });
  });
}

async function acquireViaTarball(dir, ref) {
  if (!commandExists("tar", ["--version"])) {
    die(
      "neither git nor tar is available. Install git (https://git-scm.com) and re-run `bos init`."
    );
  }
  const parent = path.dirname(dir);
  fs.mkdirSync(parent, { recursive: true });
  const tarUrl = `${REPO_URL}/archive/refs/heads/${ref}.tar.gz`;
  const tmp = path.join(os.tmpdir(), `bos-${ref}-${process.pid}.tar.gz`);
  log(c.dim(`Downloading ${tarUrl}`));
  await download(tarUrl, tmp);
  const extracted = path.join(parent, `${DIR_NAME}-${ref}`);
  try {
    fs.rmSync(extracted, { recursive: true, force: true });
  } catch (_) {}
  const r = spawnSync("tar", ["-xzf", tmp, "-C", parent], { stdio: "inherit" });
  fs.unlink(tmp, () => {});
  if (r.status !== 0) die("failed to extract the downloaded archive.");
  if (!fs.existsSync(extracted)) {
    die(`archive did not contain the expected folder "${DIR_NAME}-${ref}".`);
  }
  fs.renameSync(extracted, dir);
}

async function acquire(dir, ref) {
  if (isBosClone(dir)) {
    log(c.dim(`Using existing install at ${dir}`));
    return;
  }
  if (fs.existsSync(dir) && fs.readdirSync(dir).length > 0) {
    die(
      `${dir} already exists and is not a Business Operating System clone.\n` +
        `Pass --dir <path> to install somewhere else, or remove that folder.`
    );
  }
  if (commandExists("git")) {
    log(c.dim(`Cloning ${REPO_URL}`));
    fs.mkdirSync(path.dirname(dir), { recursive: true });
    const args = ["clone"];
    if (ref !== DEFAULT_REF) args.push("--branch", ref);
    args.push(REPO_URL, dir);
    const r = spawnSync("git", args, { stdio: "inherit" });
    if (r.status !== 0) die("git clone failed.");
  } else {
    log(c.dim("git not found — downloading a snapshot instead."));
    await acquireViaTarball(dir, ref);
  }
}

function runSetup(dir, python, forwardArgs) {
  const setup = path.join(dir, "tools", "setup.py");
  if (!fs.existsSync(setup)) die(`could not find tools/setup.py in ${dir}.`);
  log("");
  log(c.bold("Running Business Operating System setup…"));
  const r = spawnSync(python.cmd, [...python.prefix, setup, ...forwardArgs], {
    stdio: "inherit",
    cwd: dir,
  });
  return r.status === 0;
}

// ── argument parsing ─────────────────────────────────────────────────────
function parseArgs(argv) {
  const opts = { dir: null, ref: DEFAULT_REF, forward: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--dir") opts.dir = argv[++i];
    else if (a === "--ref" || a === "--branch") opts.ref = argv[++i];
    else if (a === "--force") opts.forward.push("--force");
    else if (a === "--skip-deps") opts.forward.push("--skip-deps");
    else if (a === "-h" || a === "--help") opts.help = true;
    else opts.forward.push(a); // anything else passes through to setup.py
  }
  return opts;
}

// ── commands ─────────────────────────────────────────────────────────────
async function cmdInit(argv) {
  const opts = parseArgs(argv);
  const python = findPython();
  if (!python) {
    die(
      "Python 3.10+ is required and was not found.\n" +
        "Install it from https://python.org (tick “Add to PATH” on Windows), then re-run `bos init`."
    );
  }
  const dir = resolveDir(opts.dir);
  await acquire(dir, opts.ref);
  const ok = runSetup(dir, python, opts.forward);
  log("");
  if (ok) {
    log(c.green("✓ Business Operating System is installed."));
    log("");
    log(c.bold("One last thing:") + " fully close and reopen Claude Code so the new");
    log("skills load (they load at startup, not mid-session). Then run:");
    log("");
    log("  " + c.cyan("/start-here"));
    log("");
    log(c.dim(`Installed at ${dir}`));
  } else {
    die("setup did not complete. Scroll up for the error, fix it, then re-run `bos init`.");
  }
}

async function cmdUpdate(argv) {
  const opts = parseArgs(argv);
  const dir = resolveDir(opts.dir);
  if (!isBosClone(dir)) {
    die(`no Business Operating System install found at ${dir}. Run \`bos init\` first.`);
  }
  const python = findPython();
  if (!python) die("Python 3.10+ is required and was not found.");
  if (commandExists("git") && fs.existsSync(path.join(dir, ".git"))) {
    log(c.dim("Pulling the latest version…"));
    const r = spawnSync("git", ["-C", dir, "pull", "--ff-only"], { stdio: "inherit" });
    if (r.status !== 0) {
      log(c.red("git pull failed") + " — re-running setup against the current version.");
    }
  } else {
    // Snapshot install (no git): re-fetch the tarball over the top.
    log(c.dim("Refreshing snapshot…"));
    const tmpDir = path.join(os.tmpdir(), `bos-update-${process.pid}`);
    fs.rmSync(tmpDir, { recursive: true, force: true });
    fs.mkdirSync(tmpDir, { recursive: true });
    await acquireViaTarball(path.join(tmpDir, DIR_NAME), opts.ref);
    // Overlay repo-owned files; setup.py handles the ~/.claude refresh + brand safety.
    copyTree(path.join(tmpDir, DIR_NAME), dir);
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }
  const ok = runSetup(dir, python, opts.forward);
  log("");
  log(ok ? c.green("✓ Updated. Restart Claude Code to load any new skills.") : c.red("Update did not complete cleanly."));
}

function copyTree(src, dest) {
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    if (entry.name === ".git") continue;
    const from = path.join(src, entry.name);
    const to = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      fs.mkdirSync(to, { recursive: true });
      copyTree(from, to);
    } else {
      fs.copyFileSync(from, to);
    }
  }
}

function cmdWhere() {
  const dir = resolveDir(null);
  if (isBosClone(dir)) {
    log(dir);
  } else {
    log(c.dim("(not installed yet — run `bos init`)"));
    log(`Would install to: ${dir}`);
  }
}

function help() {
  log(`
${c.bold("Business Operating System")} — installer

  ${c.cyan("bos init")}     Install onto this machine and set up Claude Code.
  ${c.cyan("bos update")}   Pull the latest version and refresh skills.
  ${c.cyan("bos where")}    Print where the system is (or would be) installed.
  ${c.cyan("bos help")}     Show this help.

Options for init / update:
  --dir <path>    Install location (default: ~/${DIR_NAME})
  --ref <branch>  Git branch / snapshot to install (default: ${DEFAULT_REF})
  --force         Overwrite an existing TrustPager key during setup
  --skip-deps     Skip the document-library install

Repo: ${REPO_URL}
`);
}

// ── entry ────────────────────────────────────────────────────────────────
(async () => {
  const [sub, ...rest] = process.argv.slice(2);
  try {
    switch (sub) {
      case "init":
      case undefined:
        await cmdInit(rest);
        break;
      case "update":
      case "upgrade":
        await cmdUpdate(rest);
        break;
      case "where":
        cmdWhere();
        break;
      case "help":
      case "-h":
      case "--help":
        help();
        break;
      default:
        die(`unknown command "${sub}". Run \`bos help\`.`);
    }
  } catch (err) {
    die(err && err.message ? err.message : String(err));
  }
})();
