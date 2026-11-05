# Phase 01: Host and ownership decision — Pattern Map

**Mapped:** 2026-11-05
**Files analyzed:** 1 proposed decision record
**Analogs found:** 1 / 1

## File Classification

| New file (proposed; planner may rename) | Role | Data flow | Closest tracked analog | Match quality |
| --- | --- | --- | --- | --- |
| `.planning/phases/01-host-and-ownership-decision/01-HOST-DECISION.md` | Decision record | Manual evidence → documented status/blockers | `.planning/PROJECT.md:52-59` | Role match; existing decision table, not host-specific |

No application, test, runbook, or Phase 2 check-plan files are required by this phase.

## Pattern Assignments

### Decision record

**Decision/status format — `.planning/PROJECT.md:52-59`:**

```markdown
## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Plan host and operator discovery first | Neither is available yet. | — Pending |
| Keep API private | Security review is incomplete. | — Pending |
```

Use an explicit `blocked`/`pending` outcome rather than an empty approval field. Tie the record to `HOST-01` and `HOST-02` (`.planning/REQUIREMENTS.md:10-13`): no candidate nominated by MIA; named operating contact, authorized API users/access owner, and host-specific private path pending; process count, replica count, and durable mount unknown, so SQLite fit blocked. MIA owns host selection and storage, backups, alerts, and restore drills (`01-CONTEXT.md:16-31`). Operations-team record readership is not API permission. No credentials or sensitive network identifiers.

**Readiness/evidence boundary — `docs/operational-readiness-005c.md:62-73`:**

```markdown
| Acceptance item | Required evidence on the deployment environment | Status |
| --- | --- | --- |
| Host-volume validation | Inspect the actual persistent mount, `AIOS_OBSERVATION_DB` path, ownership, and permissions. Check history after restart and recreation. | Pending |
```

Reference its four open host gates (host-volume validation, backup schedule, restore drill, disk monitoring) as downstream Phase 2 work, not Phase 1 evidence. The report explicitly separates disposable CI checks from target-host proof (`docs/operational-readiness-005c.md:3-18,60-73`); the Streamlit URL is not the FastAPI host (`:64`). Do not duplicate the report or assert checks occurred.

## Shared Patterns

- **Traceability:** Scope only `HOST-01` and `HOST-02` (`.planning/ROADMAP.md:9-15`); Phase 2 owns the runnable host checks (`:17-25`).
- **Validation:** Manually review blocked statuses and absence of invented host evidence; `git diff --check` is the quick document check (`.planning/phases/01-host-and-ownership-decision/01-VALIDATION.md:14-19,40-45`). No auth, runtime error handling, or code validation pattern applies to a Markdown-only decision.

## No Analog Found

No existing tracked host-specific decision record was identified. The project decision table supplies format, not host evidence; `01-CONTEXT.md` supplies the actual decisions.

## Metadata

**Analog search scope:** tracked `.planning/` decision/validation files and `docs/operational-readiness-005c.md`. Both named analogs were verified with `git ls-files`. No source files were changed.
