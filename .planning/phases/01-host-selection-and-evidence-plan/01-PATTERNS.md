# Phase 1: Host selection and evidence plan - Pattern Map

**Mapped:** 2026-11-25
**Files analyzed:** 1 proposed document
**Analogs found:** 1 / 1

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
| --- | --- | --- | --- | --- |
| `docs/host-selection-and-evidence-plan.md` (proposed new decision record) | documentation / decision record | evidence-to-decision, batch | `docs/operational-readiness-005c.md` | role-match |

The proposed path is a planning choice, not a host-specific path. No implementation file is in scope. `01-CONTEXT.md` delegates the document location to the agent. The existing readiness report is the closest tracked record of pending deployment checks. `docs/DEPLOYMENT.md` supplies the deployment constraints.

## Pattern Assignments

### `docs/host-selection-and-evidence-plan.md` (documentation / decision record, evidence-to-decision)

**Analog:** `docs/operational-readiness-005c.md` (tracked source).

**Status and evidence boundary** (`docs/operational-readiness-005c.md:1-6`):

```markdown
# Task 005C — Operational Readiness Report

Status: **all seven checks passed on disposable CI runners. Production deployment not approved.**
PR #8 merged into `main` as `be3c7f436ad65d49d58c96f56fdfd53de3f06137`.
Source: PR #8; source changes at `c2142fe6e62c93acbfa38e433237e8831966adfc`.
Evidence: https://github.com/strdst7/ai-os/actions/runs/41558016110
```

Copy the explicit status and evidence-label structure. Do not copy the old PR, commit, or CI URL as evidence for a selected production host. State **Blocked: no eligible stateful API host candidate or operator named**. The user owns naming a candidate and its operator. The operator remains unknown until named.

**Separate runtimes and open gates** (`docs/operational-readiness-005c.md:62-73`):

```markdown
## Deployment-environment gate

The named host is Streamlit Community Cloud at `https://ai-osdev.streamlit.app/`. Its repository entrypoint is `app.py`: a session-local dashboard. It does not start the Docker/FastAPI service in `src/main.py`, read `AIOS_OBSERVATION_DB`, or write observations to SQLite. The CI volume checks apply to that separate API deployment path. The live URL redirected to Streamlit sign-in during an unauthenticated probe, so live dashboard behavior and deployment source revision remain unconfirmed. No persistent host mount, backup destination, or operator access was established. These four acceptance items remain open for any future stateful API deployment:

| Acceptance item | Required evidence on the deployment environment | Status |
| --- | --- | --- |
| Host-volume validation | Inspect the actual persistent mount, `AIOS_OBSERVATION_DB` path, ownership, and permissions. Check history after restart and recreation. | Pending |
| Backup schedule | Record automated frequency, retention, off-volume destination, and failure notification. Check an actual scheduled backup. | Pending |
| Restore drill | Restore a real backup into an isolated target. Check history, anomaly state, UUID replay, and `PRAGMA integrity_check`. | Pending |
| Disk monitoring | Set capacity thresholds and alerts before exhaustion. Check alert delivery and backup-write error handling. Never fill production storage. | Pending |
```

Copy the four evidence descriptions and pending statuses. Add separate **Owner** and **Evidence source** fields for each gate. Mark both fields **Pending — operator not named** or **Pending — source not available** as appropriate. Do not imply the Streamlit host is a candidate for the API. Add a fifth, separate security-review prerequisite with pending owner, evidence source, and approval status. Cite `docs/operational-readiness-005c.md:73` for the private-until-review constraint.

**Deployment topology and security constraint** (`docs/DEPLOYMENT.md:23-37`):

```markdown
- Set `AIOS_OBSERVATION_DB=/data/observations.db` and mount persistent storage at `/data`. The container rejects missing, relative, and in-memory paths. Check host ownership, permissions, and persistence before use. <!-- VERIFY: Confirm the actual host mount, ownership, permissions, and database path. -->
- Keep one host and one replica for this SQLite writer. The source uses a local lock, not a shared multi-host transaction system.

Production API deployment remains blocked. Complete the four host checks below and a security review before public exposure. <!-- VERIFY: Record host-specific acceptance evidence and security approval before enabling public API access. -->
```

Treat `/data/observations.db` as the documented container example, never a chosen target-host mount. Record the actual host mount and database path as pending. Record the API runtime as Docker/FastAPI `src.main:app`, contingent on a future host decision (`docs/DEPLOYMENT.md:4,8-12`).

**Evidence-not-approval pattern** (`docs/operational-readiness-005c.md:18,60`):

```markdown
CI volumes do not prove a production host's mount, backup schedule, restore runbook, or disk alerts.

This disposable-runner result does not establish production readiness. Production-host mount, backup schedule, disk alerts, and restore drill need separate host checks.
```

Keep CI links as background evidence only. Mark every target-host check pending. Do not convert disposable full-volume results into a target-host disk alert result.

**Decision-record fields to create:** decision status; decision owner; candidate and operator status; reopen trigger; runtime separation; SQLite topology; actual host mount and database path status; one row per four host gates; separate security-review row; each prerequisite's owner, required evidence, evidence source, and status. Use explicit pending values rather than invented names, paths, schedules, approvals, or completed evidence. Reopen when the user names both a candidate and its operator for assessment against fixed gates (`01-CONTEXT.md:16-30`).

## Shared Patterns

### Runtime separation

**Source:** `docs/DEPLOYMENT.md:4,8-12`. **Apply to:** Decision status, host-candidate assessment, and evidence table.

```markdown
AI-OS has two separate runtimes. `app.py` is a Streamlit demo with session-local history. The `Dockerfile` starts `src.main:app`, a FastAPI service with SQLite observations. Neither the container lifecycle checks nor the demo establish production approval for the API.
```

### Evidence-source discipline

**Source:** `docs/operational-readiness-005c.md:3,8-18,60,66-73`. **Apply to:** Every evidence claim and gate row. Identify CI checks as passed on disposable runners only. Require target-host evidence for approval. Leave host-specific evidence source pending until identified.

### Exposure, rollback, and safety

**Source:** `docs/DEPLOYMENT.md:30,39-48,54-55`; `.planning/PROJECT.md:32-36`. **Apply to:** Decision status and security review. Keep the FastAPI service private. Do not treat an image tag as a SQLite rollback. Never run `tests/full_volume.py` on a local or production host.

## Content Constraints and Requirement Coverage

| Requirement | Decision-record content | Source |
| --- | --- | --- |
| HOST-01 | Blocked decision; no eligible candidate; user names future candidate and operator; reopen trigger. | `.planning/REQUIREMENTS.md:8-11`; `01-CONTEXT.md:16-20` |
| HOST-02 | Operator pending; Docker/FastAPI runtime; actual host mount/path pending; Streamlit is only the separate demo. | `.planning/REQUIREMENTS.md:10-12`; `docs/DEPLOYMENT.md:4-12,23-28` |
| GATE-01 | Four distinct pending gates; each has owner, evidence requirement, evidence source, status. | `.planning/REQUIREMENTS.md:13-16`; `docs/operational-readiness-005c.md:66-71` |
| GATE-02 | Separate pending security review with owner, required review evidence, evidence source, status; no public exposure. | `.planning/REQUIREMENTS.md:15-17`; `docs/DEPLOYMENT.md:30` |

Owners of the four gates and security review were not settled (`01-CONTEXT.md:25`). The user owns the decision to name a host candidate, not automatically every gate. The future host operator is unknown. No host or operator placeholder is acceptable. No code, deployment tooling, service behavior, or recovery policy changes belong in this phase.

## No Analog Found

None for the proposed document. Existing documents describe gates, but no tracked document already records the blocked host decision with per-gate owners and evidence sources. The planner must create those fields without inventing their values.

## Metadata

**Analog search scope:** `docs/*.md` (eight documents); canonical `.planning/PROJECT.md`, `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md`, and phase context.
**Files scanned:** Two documentation analogs read; eight documentation paths indexed. Both named analogs are git-tracked.
**Pattern extraction date:** 2026-11-25.
**Research:** No `01-RESEARCH.md` existed at mapping time.
