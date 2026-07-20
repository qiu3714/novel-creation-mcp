# Contributing

## Before opening an issue

1. Confirm the behaviour using the current `main` branch.
2. Include Python version, MCP client, operating system, configuration, and
   reproducible steps.
3. Do not include private manuscripts, credentials, or copyrighted source
   material that you are not permitted to share.

## Pull requests

- Keep each pull request focused on one problem.
- Add or update tests when behaviour changes.
- Update `README.md` when installation, configuration, or a tool contract
  changes.
- Preserve the project content policy; do not submit copied works, extensive
  excerpts, or datasets without a redistributable licence.
- Follow `CODE_OF_CONDUCT.md` in issues, pull requests, and reviews.

## Content-source changes

Every new public knowledge item must record its source URL, licence or reuse
basis, date checked, and a concise statement of what was transformed. If that
evidence is missing, open a content/source review issue instead of adding the
material to the repository.

## Development checks

Run the available checks before requesting review:

```powershell
python -m compileall -q .
python verify_setup.py
python -m pytest -q
```
