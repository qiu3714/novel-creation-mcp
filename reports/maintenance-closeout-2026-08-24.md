# Four-week maintenance closeout — 2026-08-24

## Delivery status

The planned four-week maintenance window for `novel-creation-mcp` is complete.
The repository is maintained as `3.0.0-rc.1`, with a documented governance,
quality, client-setup, and release-readiness baseline.

## Delivered work

| Area | Delivered outcome |
| --- | --- |
| Governance and content handling | MIT licence, contribution guide, security policy, code of conduct, content policy, source audit, and issue/PR templates. |
| Quality baseline | Bounded dependencies, a repository virtual environment workflow, 18 regression tests, and a Quality workflow on Ubuntu and Windows with Python 3.11. |
| MCP interface | 12 registered tools with regression coverage for their public routes and key input-normalization cases. |
| Client and release preparation | MCP client setup guide, changelog, `3.0.0-rc.1` release candidate, governance audits, and release-readiness reports. |

## Final verification snapshot

Verified in `D:\栗新康\Documents\使用\novel-creation-mcp` on 2026-08-24:

- Branch: `main`
- Starting commit: `a021ec71efd5cd9a5803d5e6c084ade0f4dd0f4c`
- Dependency check, compilation, setup verification, startup preflight, and
  `pytest` completed successfully with 18 passing tests.
- `server.list_tools()` registered 12 tools.
- `git diff --check` completed successfully before the closeout update.
- The latest completed Quality workflow for the starting commit succeeded on
  Ubuntu and Windows with Python 3.11: run `32721873350`.

## Repository evidence snapshot

- Visibility: public
- Licence: MIT
- Open issues: 0
- Open pull requests: 0
- Releases: 0
- Tags: 0
- Stars, forks, watchers, and subscribers: 0
- Local commit count: 18
- Local-history contributors: 2

These values describe the repository at this snapshot. They do not establish
external adoption, usage volume, or download counts.

## Ongoing release path

The maintenance window closes on the release-candidate line. Before publishing
a stable version, the maintainer should complete the following release
decision:

1. Confirm the source-risk scope recorded in `SOURCE_AUDIT.md` and
   `CONTENT_POLICY.md`.
2. Select the stable version and prepare stable release notes.
3. Run the documented quality checks and publish the reviewed GitHub release.

Future public knowledge imports must retain a source URL, licence or reuse
basis, check date, and transformation note.
