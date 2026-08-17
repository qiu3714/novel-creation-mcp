# Governance and source audit - 2026-08-17

## Scope

Monday governance/source maintenance under `MAINTENANCE_PLAN.md`: public
governance files, issue and pull-request templates, README claim
verifiability, source-policy boundary, sensitive-file scan, and current
repository evidence. No knowledge content was added, modified, or deleted.

## Repository gate

- Target repository: `D:\栗新康\Documents\使用\novel-creation-mcp`
- Checked at: `2026-08-17T20:04:36+08:00`
- Branch before edits: `main`
- Worktree before edits: clean
- `git fetch origin --prune`: completed
- `git pull --ff-only`: `Already up to date.`
- Starting commit: `1eef51d56611da3c9215a8c355fc2db252f87e41`
- Starting `HEAD`, `origin/main`, and `git ls-remote origin refs/heads/main`
  all matched `1eef51d56611da3c9215a8c355fc2db252f87e41`; ahead/behind was
  `0 0`.

## Governance coverage

The repository currently tracks the Week 1 governance surface:

- `LICENSE`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `CODE_OF_CONDUCT.md`
- `CONTENT_POLICY.md`
- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `.github/ISSUE_TEMPLATE/content_source_review.yml`
- `.github/pull_request_template.md`

The issue and pull-request templates warn against credentials, private
manuscripts, personal data, and unlicensed substantial excerpts. The
content-source template asks for affected files, concern type, evidence, and a
proposed resolution.

## README claim audit

- README says the project is an MCP server for Chinese novel-writing
  assistance; this matches `server.py` and the public tool descriptions.
- README says the current maintenance version is `3.0.0-rc.1`; this matches
  `config.MCP_SERVER_CONFIG["version"]`.
- README says 12 MCP tools are registered; `server.list_tools()` returned 12
  tool schemas with matching names.
- README says the public knowledge snapshot has no verified external collected
  entries; `knowledge/collected_content.json` has `0` public
  `collected_content` entries.
- README says there is no verified public snapshot supporting fixed counts of
  IP case-study or mythology data; `knowledge/knowledge-base.json` currently
  has no top-level `ip_case_studies` or `mythology` sections.
- README does not claim users, downloads, external adoption, releases, tags, or
  licence compatibility for third-party content.

## Source and sensitive-file scan

The 2026-08-17 scan covered 50 tracked files and excluded local dependency and
cache state. It searched for sensitive filenames plus common private-key,
OpenAI-style key, GitHub-token, AWS-access-key, and generic credential
assignment patterns while emitting only file, line, and rule labels.

Result: no obvious hard-coded credential, token, private key, password, or
sensitive tracked filename was found.

## Current repository evidence

Observed before this maintenance commit using Git, GitHub CLI, and GitHub REST
for `qiu3714/novel-creation-mcp`:

- Visibility: public
- Default branch: `main`
- Licence: MIT
- Open issues: 0
- Open pull requests: 0
- Releases: none
- Tags: none
- Stars: 0
- Forks: 0
- GitHub REST `watchers_count`: 0
- GitHub REST `subscribers_count`: 0
- Latest pushed timestamp reported by GitHub: `2026-08-14T16:06:04Z`
- Commit count in local `HEAD`: 14
- Contributors in local history: 2 (`栗新康`, `qiu3714`)
- Latest observed `Quality` workflow on `main`: success for
  `1eef51d56611da3c9215a8c355fc2db252f87e41` (run `31817721123`)

No adoption, download, user, deployment, or licence-compatibility claims were
inferred from these repository signals.

## Validation results

The repository's standard local checks succeeded after this documentation-only
update:

- `.venv\Scripts\python.exe -m pip check`: passed
- `.venv\Scripts\python.exe -m compileall -q .`: passed
- `.venv\Scripts\python.exe verify_setup.py`: passed
- `.venv\Scripts\python.exe -m pytest -q`: passed with 18 tests
- `git diff --check`: passed before staging, with only LF/CRLF working-copy
  notices from Git

## Open risks

- Static examples in internal data still contain nominative third-party title
  references. They remain audit leads only and must not be expanded into
  detailed summaries or excerpts without source and reuse evidence.
- Collector scripts and documentation mention third-party platforms. Platform
  names and scraping configuration are not permission to redistribute content.
- `content_report.md` remains historical audit evidence only because it lacks
  source URLs, licences, permissions, and reuse bases.
- Future public knowledge imports still require source URL, licence or reuse
  basis, check date, and transformation notes before publication.
- No stable GitHub release or tag exists. Stable release remains blocked until
  the maintainer explicitly confirms source-risk scope, version decision, and
  stable release notes.
