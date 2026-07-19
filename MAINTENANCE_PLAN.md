# One-month maintenance plan

## Objective

Make `novel-creation-mcp` a reliable, openly governed MCP server with
reproducible installation, basic regression protection, transparent content
handling, and real maintenance evidence for a future Codex for Open Source
application.

## Four-week delivery plan

### Week 1 — governance and content boundary

- Publish the MIT licence, contribution guide, security policy, and content
  policy.
- Audit public repository files for secrets, personal data, and unverified
  source material; record risks rather than deleting material without evidence.
- Add issue and pull-request templates and make the README's claims precise.
- Acceptance: public project rules exist and no known critical exposure is left
  undocumented.

### Week 2 — installation and quality baseline

- Repair deterministic syntax and runtime defects.
- Create a repeatable development environment and a small core test suite.
- Add CI for compilation and tests.
- Acceptance: a clean clone can install dependencies, compile, run setup
  verification, and execute core regression tests.

### Week 3 — tool contract and first release candidate

- Validate each public MCP tool's input and expected output behaviour.
- Improve error messages, installation examples, and client configuration.
- Create a changelog and versioned release candidate.
- Acceptance: all documented tools have at least one regression assertion and
  release notes accurately describe tested changes.

### Week 4 — community evidence and application readiness

- Triage incoming issues and improve documentation from reproducible feedback.
- Publish a stable release only if all release checks pass.
- Record actual project signals: releases, commits, resolved issues, external
  contributions, and verified adoption. Never manufacture metrics.
- Draft the Open Source application using only those observable facts.

## Operating rules

- Keep changes small, tested, committed, and pushed from `main` only after a
  fast-forward sync.
- Never force-push, rewrite history, change repository visibility, or silently
  delete knowledge content.
- Treat copyright, privacy, dependency, and credential findings as release
  blockers until resolved or explicitly scoped out.

## Automation roles

- Monday: governance and content-compliance maintainer.
- Wednesday: quality engineer for tests, defects, and CI.
- Friday: release and community maintainer for documentation, issue triage,
  release readiness, and evidence tracking.
