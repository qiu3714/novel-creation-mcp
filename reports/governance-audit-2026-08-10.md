# Governance and source audit - 2026-08-10

## Scope

Monday governance/source maintenance under `MAINTENANCE_PLAN.md`: public
governance files, issue and pull-request templates, README claim
verifiability, source-policy boundary, sensitive-file scan, and current
repository evidence. No knowledge content was added, modified, or deleted.

## Repository gate

- Target repository: `D:\栗新康\Documents\使用\novel-creation-mcp`
- Checked at: `2026-08-10T18:05:33+08:00`
- Branch before edits: `main`
- Worktree before edits: clean
- `git fetch origin --prune`: completed
- `git pull --ff-only`: `Already up to date.`
- Starting commit: `a5dca7058c33542c3ea0842e37e2b7a4ad150c30`
- `git ls-remote origin refs/heads/main`: matched the starting commit

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

The issue and pull-request templates explicitly warn against credentials,
private manuscripts, personal data, and unlicensed substantial excerpts. The
content-source template asks for affected files, concern type, and evidence.

## README claim audit

- README says the project is an MCP server for Chinese novel-writing assistance;
  this matches `server.py` and the public tool descriptions.
- README says the current maintenance version is `3.0.0-rc.1`; this matches
  `config.MCP_SERVER_CONFIG["version"]`.
- README says 12 MCP tools are registered; `server.list_tools()` returned 12
  tool schemas with matching names.
- README says the public knowledge snapshot has no verified external collected
  entries; `knowledge/collected_content.json` has `0` public
  `collected_content` entries.
- README does not claim fixed counts of bundled IP cases, mythology systems,
  users, downloads, external adoption, releases, or tags.

## Source and sensitive-file scan

The 2026-08-10 scan covered tracked files and excluded local dependency/cache
state. It searched for common private-key, OpenAI-style key, GitHub-token,
AWS-access-key, and generic credential assignment patterns while emitting only
file, line, and rule labels.

Result: no obvious hard-coded credential, token, private key, or password was
found in tracked files.

## Current repository evidence

Observed before this maintenance commit using Git, GitHub CLI, and GitHub REST:

- Visibility: public
- Default branch: `main`
- Licence: MIT
- Open issues: 0
- Open pull requests: 0
- Releases: 0
- Tags: 0
- Stars: 0
- Forks: 0
- GitHub REST `watchers_count`: 0
- GitHub REST `subscribers_count`: 0
- Latest pushed timestamp reported by GitHub: `2026-08-07T16:08:40Z`
- Commit count in local `HEAD`: 12
- Contributors in local history: 2 (`qiu3714`, `栗新康`)
- Latest observed `Quality` workflow on `main`: success for
  `a5dca7058c33542c3ea0842e37e2b7a4ad150c30` (run `31196134764`)

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
- Future public knowledge imports still require source URL, licence or reuse
  basis, check date, and transformation notes before publication.
- No stable GitHub release or tag exists. Stable release remains blocked until
  the maintainer explicitly confirms source-risk scope, version decision, and
  release notes.
