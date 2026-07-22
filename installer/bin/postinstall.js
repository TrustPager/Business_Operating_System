#!/usr/bin/env node
/**
 * Runs after `npm install -g @trustpager/bos`. We deliberately do NOT clone or
 * run setup here — a full install as a global postinstall is fragile (Python
 * detection, permissions) and a failure would abort the npm install itself.
 * Instead we print the one next step, matching the site's two-line card.
 */
"use strict";

// Stay quiet inside CI and nested/dependency installs. A global CLI install is
// the case we want to greet; npm signals it via npm_config_global (older) or
// npm_config_location (npm 9+). If neither says global, assume a dependency
// install and stay silent.
const isGlobal =
  process.env.npm_config_global === "true" ||
  process.env.npm_config_location === "global";
if (process.env.CI || !isGlobal) {
  process.exit(0);
}

const cyan = (s) => `\x1b[36m${s}\x1b[0m`;
const bold = (s) => `\x1b[1m${s}\x1b[0m`;

console.log(`
${bold("Business Operating System")} is ready to install.

Next, run:

  ${cyan("bos init")}

It sets everything up and plugs the skills into Claude Code.
`);
