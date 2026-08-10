# Source and repository audit

Last checked: 2026-08-10

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
- 2026-07-28 refresh: repeated the sensitive-pattern scan across tracked and
  non-ignored public files, rechecked README public claims against actual MCP
  tool registration, and queried current GitHub issue, pull-request, release,
  tag, and workflow evidence for Week 4 release readiness.
- 2026-07-31 refresh: repeated the sensitive-pattern scan, reviewed README
  installation steps, changelog, MCP client setup documentation, and
  `MCP_SERVER_CONFIG.version`, then queried current GitHub issue, pull-request,
  release, tag, repository, and workflow evidence for Week 4 application
  readiness.
- 2026-08-03 refresh: repeated the sensitive-pattern scan, rechecked README
  examples and MCP tool schema descriptions against actual knowledge files, and
  queried current GitHub repository, release, and tag evidence for Monday
  governance maintenance.
- 2026-08-08 refresh: repeated the sensitive-pattern scan, reviewed README
  installation steps, changelog, MCP client setup documentation,
  `MCP_SERVER_CONFIG.version`, tool schema registration, knowledge-file
  structure, and queried current GitHub issue, pull-request, release, tag,
  repository, and workflow evidence for release/community maintenance.
- 2026-08-10 refresh: repeated the sensitive-pattern scan, reviewed README
  public claims, governance files, issue and pull-request templates, actual MCP
  tool registration, knowledge-file structure, and queried current GitHub issue,
  pull-request, release, tag, repository, and workflow evidence for Monday
  governance/source maintenance.

## Findings

- No obvious hard-coded credential, token, or private key was found in tracked
  files. Matches were limited to policy wording and batch-script syntax.
- The 2026-07-28 rescan again found no obvious hard-coded credential, token,
  private key, or password. Matches were limited to policy wording, audit
  wording, and Windows batch `tokens=*` syntax.
- The 2026-07-31 rescan again found no obvious hard-coded credential, token,
  private key, or password. Matches were limited to policy wording, audit
  wording, release-authorization wording, and Windows batch `tokens=*` syntax.
- The 2026-08-03 rescan again found no obvious hard-coded credential, token,
  private key, or password. Matches were limited to policy wording, audit
  wording, release-authorization wording, and Windows batch `tokens=*` syntax.
- The 2026-08-08 rescan again found no obvious hard-coded credential, token,
  private key, or password. Matches were limited to policy wording, audit
  wording, release-readiness wording, issue-template wording, and Windows batch
  `tokens=*` syntax.
- The 2026-08-10 rescan found no obvious hard-coded credential, token, private
  key, or password in tracked files. The structured scan intentionally reported
  only file, line, and rule names, and produced no matches.
- Governance coverage remains present: `LICENSE`, `CONTRIBUTING.md`,
  `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CONTENT_POLICY.md`, bug/content-source
  issue templates, and a pull-request template are tracked.
- README public claims remain bounded to observable facts: 12 registered MCP
  tools, no bundled verified external collection entries, no fixed count of IP
  case studies or mythology systems, and release-candidate status only.
- README examples and MCP schema descriptions were tightened to avoid implying
  that specific third-party IP cases or mythology systems are bundled as
  redistributable project content.
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
- `knowledge/collected_content.json` retains historical metadata, but its
  current public `collected_content` array is empty and should not be counted
  as public adoption or redistribution evidence.

## Open risks

- Static examples in internal data still refer to third-party titles as
  nominative examples. Do not expand those references into detailed summaries or
  excerpts without source and reuse evidence.
- The collector documentation lists third-party platforms. Platform names and
  configurations do not establish permission to scrape, store, or redistribute
  content.
- Future imports need source URL, licence or reuse basis, date checked, and a
  concise transformation note before they can be treated as public knowledge
  content.
- The 2026-08-10 governance pass did not modify or delete tracked knowledge
  files; the source-risk boundary remains documentation-only until new content
  is reviewed under `CONTENT_POLICY.md`.
