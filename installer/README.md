# @trustpager/bos

The one-command installer for the **Business Operating System** — the open-source AI operating system for running your business on [Claude Code](https://claude.com/claude-code).

## Install

```
npm install -g @trustpager/bos
bos init
```

Then fully close and reopen Claude Code (skills load at startup) and run:

```
/start-here
```

That's it. No account, no API key.

## What `bos init` does

This npm package is a thin bootstrapper. The real system is the public repo at
[github.com/TrustPager/Business_Operating_System](https://github.com/TrustPager/Business_Operating_System).
`bos init`:

1. Puts the repo on your machine — `git clone` if git is installed, otherwise a
   tarball download (default location `~/Business_Operating_System`, override with `--dir`).
2. Runs the repo's own `tools/setup.py`, which installs the document libraries,
   writes the `~/.claude/bos-run.py` signpost, copies the skills and commands
   into `~/.claude/`, and registers the keyless research connector.

Requires **Node 16+** and **Python 3.10+**.

## Commands

| Command | What it does |
|---|---|
| `bos init` | Install onto this machine and set up Claude Code. |
| `bos update` | Pull the latest version and refresh skills. |
| `bos where` | Print where the system is (or would be) installed. |
| `bos help` | Show help. |

### Options (init / update)

| Option | Default | Meaning |
|---|---|---|
| `--dir <path>` | `~/Business_Operating_System` | Install location. |
| `--ref <branch>` | `main` | Branch / snapshot to install. |
| `--force` | — | Overwrite an existing TrustPager key during setup. |
| `--skip-deps` | — | Skip the document-library install. |

## Connect TrustPager (optional)

The keyless system works on its own. To switch on the always-on workflows
(live pipeline briefings, follow-up radar, missed-call recovery, automations),
connect a [TrustPager](https://trustpager.com) workspace from inside Claude Code:

```
Connect my TrustPager workspace
```

## License

MIT
