## What changed and why

Brief description of the change. If this closes an issue, link it here.

---

## Checklist

Run all of these locally before submitting. CI will run the same sequence.

### Gates

- [ ] Offline unit tests pass: `BOS_OFFLINE=1 python -m unittest discover -s tests`
- [ ] Secret scan clean: `python tools/check-no-secrets.py`
- [ ] Skill linted (if a skill changed): `python tools/lint-skill.py skills/<name>`
- [ ] Onboarding binding valid: `python tools/check-onboarding-binding.py`
- [ ] Registry regenerated and fresh (if a skill was added or changed):
      `python tools/registry-generator.py && python tools/registry-generator.py --check`
- [ ] Capabilities regenerated and fresh (if the registry changed):
      `python tools/export-capabilities.py && python tools/export-capabilities.py --check`

### Content rules (for any skill or doc changes)

- [ ] No em dashes on customer- or owner-facing surfaces (generated customer documents, email/SMS/social copy, README, INSTALL, CAPABILITIES, templates/). Skill bodies and maintainer docs are exempt; see the scope in CONTRIBUTING.md
- [ ] Customer-facing copy is outcome-led, not pain-led

### Skill additions (complete if this PR adds a new skill)

- [ ] `SKILL.md` frontmatter passes `lint-skill.py` with no errors
- [ ] Skill is keyless (`requires_credential: none`) or correctly declares its driver and credential
- [ ] If `fetch.py` exists: `test-fixture.json` exists and the offline fixture test passes
- [ ] Registry and capabilities regenerated (see gates above)
