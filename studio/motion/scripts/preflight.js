// preflight.js — the one-time "check my setup" gate (design spec §9).
//
// Keyless != frictionless: Remotion's first render fetches a ~150MB headless
// Chrome, needs a working software-GL backend, and takes real time on a modest
// laptop. This gate surfaces all of that in plain English BEFORE the owner sits
// through a full render that might fail opaquely.
//
// What it does, in order:
//   1. Report the Node version (Remotion needs a modern Node).
//   2. Run a real 1-frame test render of a bundled composition with the default
//      swangle backend. That single step exercises the whole fragile chain:
//      bundling, the one-time headless-Chrome fetch (fails opaquely behind a
//      corporate proxy / AV), and the swangle software-GL backend.
//   3. Report pass/fail in plain English, with the render-time and licence notes.
//
// No API key, no network beyond Remotion's own browser fetch. Windows-safe:
// spawns node on the CLI's JS entry (no shell, no npx, no PATH assumptions).

import { spawn } from "node:child_process";
import { mkdtempSync, rmSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.join(__dirname, "..");
const CLI_JS = path.join(
  PROJECT_ROOT,
  "node_modules",
  "@remotion",
  "cli",
  "remotion-cli.js"
);

function line(s = "") {
  console.log(s);
}

line("");
line("Checking your video setup. This runs once and can take a few minutes the");
line("first time, because it downloads the render browser (~150MB).");
line("");

// 1. Node version.
line(`Node:        ${process.version}`);

// 2. Dependencies present?
if (!existsSync(CLI_JS)) {
  line("");
  line("Not ready:   the studio's dependencies are not installed yet.");
  line("Fix:         run `npm install` in studio/motion, then run this again.");
  line("");
  process.exit(1);
}
line("Dependencies: installed.");
line("");
line("Running a small test render (this triggers the one-time browser download");
line("and checks the swangle graphics backend)...");
line("");

// 3. A real 1-frame still render of a bundled comp, with the default backend.
const tmp = mkdtempSync(path.join(tmpdir(), "bos-preflight-"));
const outPng = path.join(tmp, "preflight.png");
const args = [
  CLI_JS,
  "still",
  "src/index.ts",
  "Scaffold",
  outPng,
  "--frame=0",
  "--gl=swangle",
];

const child = spawn(process.execPath, args, {
  cwd: PROJECT_ROOT,
  stdio: "inherit",
});

child.on("close", (code) => {
  const ok = code === 0 && existsSync(outPng);
  try {
    rmSync(tmp, { recursive: true, force: true });
  } catch {}
  line("");
  if (ok) {
    line("All set. Your machine can render video.");
    line("");
    line("Good to know:");
    line("  - A software render is minutes, not seconds. A 60-second clip is a few");
    line("    minutes on a normal laptop, so a working render is not a stuck one.");
    line("  - Remotion is free for teams of up to 3 people. A company of 4 or more");
    line("    needs a paid Remotion Company Licence before publishing commercially.");
    line("");
    process.exit(0);
  }
  line("Not ready yet. The test render did not complete.");
  line("");
  line("Most common cause: the one-time browser download was blocked (a corporate");
  line("proxy or antivirus can stop it). Check your connection and run this again.");
  line("If your screen glitched or the machine restarted, that points to the");
  line("graphics driver, not the video.");
  line("");
  process.exit(1);
});

child.on("error", (err) => {
  try {
    rmSync(tmp, { recursive: true, force: true });
  } catch {}
  line("");
  line(`Not ready:   could not launch the renderer (${err.message}).`);
  line("Fix:         run `npm install` in studio/motion, then run this again.");
  line("");
  process.exit(1);
});
