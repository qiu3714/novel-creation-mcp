# Source and repository audit

Last checked: 2026-07-21

## Scope

This audit covered tracked repository files and public-facing documentation. It
excluded `.git/`, `.venv/`, and local cache directories.

## Checks run

- `git ls-files`
- `rg --hidden --glob '!.git/**' --glob '!.venv/**' --glob '!.pytest_cache/**'`
  for common credential and secret patterns.
- Manual review of `README.md`, `README_自动化任务.md`, `CONTENT_POLICY.md`,
  `CONTRIBUTING.md`, `SECURITY.md`, `.github/`, `knowledge/knowledge-base.json`,
  and `knowledge/collected_content.json`.

## Findings

- No obvious hard-coded credential, token, or private key was found in tracked
  files. Matches were limited to policy wording and batch-script syntax.
- `README.md` previously described bundled IP and mythology coverage with exact
  counts that are not supported by the current tracked knowledge files.
  `knowledge/knowledge-base.json` has no `ip_case_studies` or `mythology`
  section, and `knowledge/collected_content.json` currently has no collected
  content entries.
- `content_report.md` is a generated historical report with platform names and
  short summaries, but it does not include source URLs, licences, permissions,
  or a reuse basis. Treat it as an audit lead, not as redistribution evidence.
- Collection and analysis scripts can create or ingest external content. Any
  generated knowledge content must pass `CONTENT_POLICY.md` before being
  committed to the public repository.

## Open risks

- Static examples refer to third-party titles and IP names as nominative
  examples. Do not expand those references into detailed summaries or excerpts
  without source and reuse evidence.
- The collector documentation lists third-party platforms. Platform names and
  configurations do not establish permission to scrape, store, or redistribute
  content.
- Future imports need source URL, licence or reuse basis, date checked, and a
  concise transformation note before they can be treated as public knowledge
  content.
