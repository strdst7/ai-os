# Phase 1: Host and ownership decision — Research

**Researched:** 2026-11-05  
**Domain:** Private API host selection and SQLite topology decision  
**Confidence:** HIGH for repository facts; LOW for host fit until MIA supplies a host

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** No candidate FastAPI host exists yet. Record host selection as open, not approved.
- **D-02:** MIA selects the host and owns storage, backups, alerts, and restore drills.
- **D-03:** The operations team needs the host decision record. This does not grant API access.
- **D-04:** Leave SQLite topology and persistent-volume fit blocked until a host and its process count, replica count, and durable mount are known.
- **D-05:** SSH tunnel and private network are equally acceptable access paths. One checked path is enough for host qualification.
- **D-06:** Both paths work for other services. Neither path has been checked against a candidate FastAPI host.
- **D-07:** Authorized API users remain undecided. Treat access ownership as a blocker before service access.
- **D-08:** Keep the API private. A separate security review must approve any public exposure.

### Claude's Discretion
- Keep the non-secret decision record in this repository's existing planning area. The team can read it alongside the code and readiness report.
- Record access details and evidence without credentials or sensitive network identifiers. Do not create a parallel runbook without an established operations location.

### Deferred Ideas (OUT OF SCOPE)
- Host mount, backup schedule, restore drill, disk alert, and private-exposure checks belong in Phase 2.
- Production approval and recovery-rule calibration require later evidence.
- Streamlit changes and a new database remain outside this milestone.
</user_constraints>

<phase_requirements>
## Phase Requirements
| ID | Description | Research Support |
|---|---|---|
| HOST-01 | Operator can identify a candidate private FastAPI host, owner, and access prerequisites, or record that none exists. | Record **no candidate**; MIA is selection and operations owner; require named operator/contact, intended private path and authorized users before access. [VERIFIED: .planning/REQUIREMENTS.md:10-13; .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:16-26] |
| HOST-02 | Operator can decide whether a single process and persistent SQLite volume fit the candidate topology, or mark the decision blocked until topology is known. | Record **blocked** pending host, process count, replica count, durable mount identity and storage topology. [VERIFIED: .planning/REQUIREMENTS.md:10-13; .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:20-25] |
</phase_requirements>

## Summary

Phase 1 should deliver **one non-secret decision record in this phase directory**, not a deployment. No candidate FastAPI host has been nominated, so host approval and SQLite/volume fit are blocked. MIA chooses the host and owns storage, backups, alerts and restore drills; the operations team receives the record but not API permission. Both SSH tunnel and private network are allowed, but only a host-specific check of one path counts. Authorized users and access owner still require a decision. [VERIFIED: .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:6-31]

The checked code starts one Uvicorn process in the image, opens a local SQLite file, and accepts an absolute database path under persistence enforcement. That does **not** attest to a host mount or permit concluding that a proposed multi-process/replica topology fits. Disposable CI checks do not establish host readiness. [VERIFIED: Dockerfile:11-26; src/services/monitoring_service.py:15-39; docs/operational-readiness-005c.md:8-18,62-73] [CITED: https://www.sqlite.org/whentouse.html]

**Primary recommendation:** Planner should create a small decision record with explicit blocked statuses and an evidence/request checklist for MIA; wait for a candidate topology before deciding fit. Do not run host checks or modify code in Phase 1. [VERIFIED: .planning/ROADMAP.md:9-25; .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:80-85]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|---|---|---|---|
| Candidate host and accountable operator | Operations / hosting | Repository planning | MIA must nominate it; planning records the decision, not infrastructure state. [VERIFIED: .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:16-20,28-31] |
| Private access and authorized-user decision | Operations / security | API authentication | Host path remains unchecked; code's key check cannot choose authorized users or prove private networking. [VERIFIED: .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:22-26; src/auth.py:5-11] |
| SQLite and durable-volume fit | Hosting / storage | API / SQLite | Topology and mount must be known before judging a local writer's fit. [VERIFIED: .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:20-25; src/services/monitoring_service.py:24-26] |

## Standard Stack

No new package or installation. Reuse the repository's Markdown planning area and existing readiness report; Phase 1 is a decision artifact. Existing image uses `python:3.10-slim`, Uvicorn and Python `sqlite3`; these are **observed**, not a recommendation to deploy them now. [VERIFIED: Dockerfile:1-26; src/services/monitoring_service.py:1-26; .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:28-31,54-68]

## Architecture Patterns

**Decision flow:** MIA nominates candidate and operator → identify process/replica count and durable mount/storage type → document *one* host-specific checked private path (SSH tunnel **or** private network) and decide authorized users → record HOST-01 and HOST-02 as decided or blocked. This is a future qualification flow, not evidence it has happened. [VERIFIED: .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:16-31; .planning/ROADMAP.md:9-15]

**Decision record fields:** candidate host (or `none identified`), MIA selection responsibility, named on-call/operator contact (pending), intended private path and host-specific evidence status (pending), authorized API users/access owner (undecided), process count (unknown), replica count (unknown), durable mount/storage type (unknown), SQLite/single-process fit (blocked), outstanding inputs and next decision owner. Record only non-secret identifiers; omit credentials and sensitive network addresses. A blank field must not be interpreted as approval. [VERIFIED: .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:16-31,73-77]

**Separation:** `app.py` is a Streamlit demo with session-local history; `Dockerfile` launches the separate API. The named Streamlit URL is not a candidate API host. [VERIFIED: .planning/codebase/ARCHITECTURE.md:5-9,37-45; docs/operational-readiness-005c.md:62-65; Dockerfile:20-26]

**Topology caution:** SQLite's official guidance permits local server-side use and allows only one concurrent writer; its FAQ says multiple processes can open one file, but warns that NFS locking may fail. Therefore one image command is a good default to **evaluate**, not proof that an unspecified host, replica count, or mount is safe. Do not categorically assert SQLite cannot work with multiple processes; examine the actual deployment topology before approving it. [CITED: https://www.sqlite.org/whentouse.html; https://www.sqlite.org/faq.html#q5] [VERIFIED: src/services/monitoring_service.py:24-26,41-49]

## Don't Hand-Roll

| Problem | Avoid | Use instead |
|---|---|---|
| Host readiness evidence | New deployment scripts or parallel runbook in Phase 1 | Existing four open gates in `docs/operational-readiness-005c.md:62-73`, carried into Phase 2. [VERIFIED: .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:28-31,80-85] |
| Topology selection | New database, scheduler, or access framework | Record unknowns and MIA's decision first. [VERIFIED: .planning/REQUIREMENTS.md:28-35; .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:16-26] |

## Common Pitfalls

1. **Equating an absolute path with a persistent mount.** `AIOS_OBSERVATION_DB` only enforces an absolute file path in image mode; the host's mount is unverified. Keep fit blocked. [VERIFIED: src/services/monitoring_service.py:15-26; docs/operational-readiness-005c.md:16-18,66-71]
2. **Promoting disposable CI or Streamlit to API host evidence.** CI has restart/recreation/backup/restore tests on disposable volumes; Streamlit is a separate entrypoint. Neither qualifies a host. [VERIFIED: docs/operational-readiness-005c.md:3-18,62-73]
3. **Confusing record readership with API authorization.** Operations-team visibility is not API permission; named authorized users are unresolved. [VERIFIED: .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:19,25-26,73-77]
4. **Treating a private path proven for another service as FastAPI proof.** Require one check tied to the nominated FastAPI host, not both paths. No check can be asserted yet. [VERIFIED: .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:22-25,73-76]
5. **Branch history drift.** Current `docs/streamlit-readiness-reality` has local planning commits absent from `origin/main`, while upstream carries newer documentation (`docs/API.md`, `CONFIGURATION.md`, `DEPLOYMENT.md`, etc.). Planner must reconcile both histories before implementation; do not switch/reset the branch or overwrite untracked `ai-os-pr8.diff`. [VERIFIED: `git log --left-right HEAD...origin/main` and `git diff --name-status HEAD..origin/main`, 2026-11-05; `git status --short`]

## Code Examples

No application-code change is justified. A **documentation-only** decision status is sufficient: `HOST-01: blocked — no candidate nominated by MIA; HOST-02: blocked — process/replica counts and durable mount unknown`. These are proposed record labels, not runtime constants. [VERIFIED: .planning/REQUIREMENTS.md:10-13; .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:16-25]

## Validation Architecture

| Req ID | Check | Type | Evidence |
|---|---|---|---|
| HOST-01 | Decision record names candidate and owner **or** says no candidate, with private path and access prerequisites explicitly pending. | Manual document review | Match CONTEXT D-01/D-03/D-05/D-07; no network probe possible without a host. [VERIFIED: .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:16-26] |
| HOST-02 | Document process count, replica count and mount **or** mark topology/fit blocked. | Manual document review | Match CONTEXT D-04 and requirement text; do not claim a mount check. [VERIFIED: .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:20-21; .planning/REQUIREMENTS.md:12-13] |

No test framework, test fixture, or package is needed for a decision-only phase. Existing Python tests exercise application behavior, not an unnamed deployment host. [VERIFIED: .planning/ROADMAP.md:9-25; docs/operational-readiness-005c.md:8-18]

## Security Domain

Phase 1 has no service access or security approval. ASVS-related planning boundaries: authentication (V2) uses an existing API key for protected routes, but the authorized population is undecided; session management (V3) is not selected here; access control (V4) requires private path and explicit user ownership; input validation (V5) and cryptography (V6) are not changed in this documentation phase. This is a scope map, **not** an ASVS certification. Public exposure needs a separate security review. [VERIFIED: src/auth.py:5-11; src/main.py:27-44; .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:22-31]

## Open Questions / Blockers for MIA

1. Which candidate private host, if any, and who is the named operating contact? If none, record `none identified`. [VERIFIED: .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:16-20]
2. What process count, replica count, and durable mount/storage topology would the API use? Until known, HOST-02 remains blocked. [VERIFIED: .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:20-21]
3. Who is authorized to use the API and who approves that roster? Which **one** host-specific private path can be checked when the host exists? No credentials or sensitive network identifiers belong in this repo. [VERIFIED: .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:22-31]

## Sources and Confidence

- **HIGH — opened repository source:** `.planning/phases/01-host-and-ownership-decision/01-CONTEXT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/PROJECT.md`, `Dockerfile`, `src/services/monitoring_service.py`, `src/auth.py`, `src/main.py`, `docs/operational-readiness-005c.md`; citations at claims. [VERIFIED: files named]
- **Official SQLite documents (cited, webfetch confidence LOW per `gsd-tools query classify-confidence --provider webfetch`):** https://www.sqlite.org/whentouse.html (last updated 2025-05-31); https://www.sqlite.org/faq.html#q5 (last updated 2024-11-26). These support generic fit cautions, not this host's suitability. [CITED: https://www.sqlite.org/whentouse.html; https://www.sqlite.org/faq.html]
- **Host-specific fit:** LOW, because no candidate or evidence exists. No assumed host details should be promoted to decisions. [VERIFIED: .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:16-26]

**Valid until:** Host nomination/topology change or updated phase context; re-evaluate before planning implementation. [VERIFIED: .planning/phases/01-host-and-ownership-decision/01-CONTEXT.md:16-26]
