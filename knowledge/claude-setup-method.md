# Claude Code settings: what gets set up and why

This module sets up your global Claude Code configuration. It also explains what each piece does so you understand what you're working with. You can change anything later, and the module shows you exactly where each file lives.

## Two separate CLAUDE.md files: what each one does

Claude Code reads two different instruction files, and they serve different purposes.

**Your global `~/.claude/CLAUDE.md`** (on Mac/Linux) or `%USERPROFILE%\.claude\CLAUDE.md` (on Windows) holds cross-project preferences: how you like Claude to talk to you, your default safety habits, and any content style choices that should apply everywhere. This is what the setup module writes to.

**Your project `CLAUDE.md`** (in each project folder, written by `/start-here`) holds the business profile for that specific project: your business name, products, customers, pipeline, and voice. It is the source of truth for anything business-specific. It takes priority over the global file for that project.

Think of it this way: the global file is your working style, the project file is your business context. They do not overlap and you do not need to duplicate anything between them.

## Why this permissions posture is good

The setup writes a `settings.json` to `~/.claude/` that follows one principle: safe reads should never interrupt you; anything that changes or sends something should always ask.

Here is what that means in practice.

**Pre-allowed (no prompt):** Read, Glob, and Grep let Claude look at your files without stopping to ask every time. These are read-only and cannot change anything, so there is no risk in pre-approving them. If you have TrustPager connected, the `get_*`, `list_*`, `search_*`, `describe_*`, and `preview_*` TrustPager tools are also pre-allowed for the same reason: they only retrieve information. Pre-approving these means your sessions stay fast once you connect.

**Always prompts (intentional):** Anything that sends a message, creates a record, updates data, or runs a bulk action still surfaces a confirmation step. This is a deliberate safety gate. It means Claude will never send an email or SMS on your behalf, create a deal, or trigger an automation without you seeing it first and saying yes. This prompt is your chance to catch anything that does not look right before it reaches a customer.

**Denied outright:** Bulk delete tools (`bulk_delete_*`) and individual delete tools (`delete_*`) for TrustPager are on the deny list. A bulk delete on a CRM is the kind of action that is difficult to reverse. Putting it on the deny list means it will never run, even accidentally, without you explicitly changing this setting.

The full posture is in `settings/recommended-settings.json`. You can add specific write tools to the allow list if you decide you trust a particular workflow to run without prompting. The comment in that file explains how.

## TrustPager read pre-allows: when they activate

The TrustPager tool entries in the allow list (the `mcp__trustpager__get_*` patterns and so on) only match when a TrustPager MCP server is actually connected and named `trustpager`. If you have not connected TrustPager yet, they sit dormant and harmless. Once you do connect it, those reads are already approved so you are not interrupted by permission prompts every time Claude checks your pipeline or looks up a contact.

## How to change anything

Everything the setup module touches is standard text you can edit.

- To update your working-style preferences, open `~/.claude/CLAUDE.md` and edit the block between the BOS markers. The markers keep the block easy to find and update later.
- To adjust the permissions posture, open `~/.claude/settings.json` and edit the allow or deny arrays. The JSON is commented to explain each section.
- To remove the BOS block from your global CLAUDE.md entirely, delete everything between and including the BOS start and end markers. Your project CLAUDE.md files are untouched.

## This module teaches as it sets up

Running the setup skill writes the files and walks you through what each one does. You do not need to read this document first to use it; it is here if you want to go deeper or revisit the reasoning later. To explore further, ask your BOS: "What does my Claude settings file do?" or "How do I pre-allow a specific tool?"
