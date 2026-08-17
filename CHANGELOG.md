# Changelog

All notable project maintenance changes are recorded here. This project follows
release-candidate notes until the stable-release gates in `MAINTENANCE_PLAN.md`
are satisfied.

## [Unreleased]

### Added

- Added a Week 4 release-readiness report with current repository signals,
  community evidence, and Open Source application-safe facts.
- Added a 2026-07-31 Week 4 readiness refresh with latest issue, pull-request,
  release, tag, CI, and application-draft evidence.
- Added a 2026-08-08 release/community readiness refresh with latest issue,
  pull-request, release, tag, CI, documentation, and application-draft
  evidence.
- Added a 2026-08-10 governance/source audit report with current README,
  template, source-policy, sensitive-pattern, and repository-signal evidence.
- Added a 2026-08-15 release/community readiness refresh with latest issue,
  pull-request, release, tag, CI, documentation, version, and application-draft
  evidence.
- Added a 2026-08-17 governance/source audit report with current README,
  template, source-policy, sensitive-pattern, and repository-signal evidence.

### Changed

- Refreshed the README release-status link and source audit timestamp for the
  2026-07-28 governance pass.
- Refreshed the README release-status link and source audit timestamp for the
  2026-07-31 release/community pass.
- Replaced README and MCP schema examples that named specific third-party IP or
  mythology entries with source-policy-neutral placeholders.
- Refreshed the README release-status link and source audit timestamp for the
  2026-08-08 release/community pass.
- Updated README Windows PowerShell installation, startup, and verification
  commands to use the virtual-environment Python executable.
- Refreshed the README evidence links and source audit timestamp for the
  2026-08-10 governance/source pass.
- Refreshed the README release-readiness link for the 2026-08-15
  release/community pass.
- Refreshed the README governance/source audit link and source audit timestamp
  for the 2026-08-17 governance/source pass.

### Release status

- No GitHub release or tag was created in this pass because the stable-release
  gates remain unmet.
- Stable release remains blocked pending a stable-version decision, maintainer
  confirmation of source-risk scope, and stable release notes.

## [3.0.0-rc.1] - 2026-07-25

### Added

- Added a dedicated MCP client setup guide with stdio configuration examples
  for Windows and Unix-like environments.
- Added this changelog so release notes can be reviewed before any GitHub
  release is created.
- Added a release-readiness report for the current Week 3 maintenance pass.

### Changed

- Marked the server configuration version as `3.0.0-rc.1` to distinguish the
  tested release candidate from a stable GitHub release.
- Linked README installation notes to the detailed MCP client setup guide and
  release-readiness report.

### Verified

- `pip check`
- `python -m compileall -q .`
- `python verify_setup.py`
- `python -m pytest -q` with 17 passing tests

### Release status

- No GitHub release or tag was created in this pass.
- Stable release remains blocked until the Week 4 community-evidence and
  release-readiness gates are reviewed.
