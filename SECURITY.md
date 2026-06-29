# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Business Operating System, please report it by emailing **security@trustpager.com**.

Include as much detail as you can: what you found, how to reproduce it, and what impact you believe it has. You can expect an acknowledgement within 3 business days and a status update within 10 business days. We will coordinate a fix and disclosure timeline with you.

Please do not open a public GitHub issue for security vulnerabilities. Public issues are fine for everything else.

---

## Security Posture

### BOS runs locally

Business Operating System runs inside the user's Claude Code installation on their own machine. Skills execute as prompts in the local Claude session. Python tool scripts (`tools/`, `skills/*/fetch.py`) run as local processes. No BOS server receives your data.

### The keyless floor needs no account or key

Skills with `requires_credential: none` in their manifest work entirely from the model's reasoning over what the operator types. They make no outbound network calls and store nothing. The keyless floor is the default; every new installation starts here.

### The TrustPager API key is stored locally

If you connect TrustPager, the `setup.py` installer writes your API key to `~/.claude/bos.json` on your local machine. That file:

- Is never committed to the repository (the `.gitignore` excludes it).
- Is never sent to BOS servers (there are no BOS servers).
- Is read at runtime only by the local `tools/trustpager_api.py` library.

### The secret scanner enforces the no-key-in-repo policy

`tools/check-no-secrets.py` scans every tracked file for real credential tokens before any commit can enter CI. CI runs this scan first, before any other step, on every push and pull request. It matches real credential values (not just the bare prefix), so documentation that legitimately mentions the key format is never a false positive.

For pre-commit protection on your local clone, add the scanner as a pre-commit hook:

```sh
# .git/hooks/pre-commit
#!/bin/sh
python tools/check-no-secrets.py || exit 1
```

### Skills ask before destructive actions

Skills that write data (update an opportunity, send a message, create an invoice) confirm intent before acting and journal their writes. The journal is local only.

### The test suite is offline by design

The `BOS_OFFLINE=1` environment variable makes `tools/trustpager_api.py` refuse every authenticated network call before it even reads the API key. CI always runs with this flag set, so a real key can never enter the test environment.

### Supported versions

BOS 1.0.0 is the current supported release. Security fixes will be applied to the latest version on the `main` branch.
