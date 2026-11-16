---
phase: 01-host-selection-and-evidence-plan
verified: 2026-11-16T20:55:00Z
status: human_needed
score: 8/8 must-haves verified
covered_files:
  - .planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md
  - .planning/phases/01-host-selection-and-evidence-plan/01-01-SUMMARY.md
  - docs/api-host-decision.md
covered_digest: "v4:sha256:480560370c243de517ce03b44f71fa39e7f05ba31d146fc514f266b8ff43f8b8"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: human_needed
  previous_score: 3/3
  gaps_closed:
    - "HOST-01: host and operator are now named (peakybuildr, 100.122.194.34; MIA / Nur Amirah Binti Mohd Kamil, strdst7) instead of a blocked host decision"
    - "HOST-02: runtime pinned to the repository Dockerfile (python:3.10-slim, uvicorn src.main:app on 0.0.0.0:8000), LXC guest chosen, one replica, /data with AIOS_OBSERVATION_DB=/data/observations.db"
    - "GATE-01/GATE-02: gate table is now grounded on peakybuildr and the guest, in order, with five separate Pending cells and a provenance row in the verified ledger"
  gaps_remaining: []
  regressions: []
human_verification:
  - test: "MIA assigns a named delegate for peakybuildr operator duties (CONTEXT.md D-02 discretion; record line 53 and 'Next decision' line 67 leave it pending)"
    expected: "One named person, besides MIA, is recorded as the operating contact for the guest; MIA's interim label is then removed or dated"
    why_human: "An assignment is an organisational act by the decision owner; inventing a name would itself be the defect this phase exists to prevent"
  - test: "Collected on the real peakybuildr guest: Host volume gate — mount source, /data/observations.db, ownership/permissions, then one observation, restart, recreate on the same volume with identical history and anomaly state"
    expected: "Fifth gate row status changes from Pending only after the storage inventory, mount/permission record and before/after /observability output are retained"
    why_human: "No guest, volume or mount exists yet and nothing in this repo can observe peakybuildr's guests; the Proxmox reachability check is liveness only"
  - test: "Backup schedule gate — automated frequency, retention, off-volume destination and failure notification, evidenced by a completed scheduled run in the log"
    expected: "Row moves off Pending only on a logged scheduled run, not an on-demand copy"
    why_human: "Requires a scheduler and storage the operator has not provisioned; disposable CI copies are not host evidence"
  - test: "Restore drill gate — restore a real backup into an isolated target, then check history, anomaly state, UUID replay and PRAGMA integrity_check without overwriting the only copy"
    expected: "Row moves off Pending with the backup identifier and restore steps recorded"
    why_human: "Needs a real backup on the named host; the CI restore in operational-readiness-005c.md is disposable-runner evidence"
  - test: "Disk monitoring gate — set capacity thresholds for the volume holding /data, prove an alert is delivered, and show backup-write error reporting without filling production storage"
    expected: "Row moves off Pending on a delivered alert plus error-path evidence; tests/full_volume.py was not run against the real volume"
    why_human: "Alerting does not exist in the repository (DEPLOYMENT.md Monitoring) and the volume does not exist yet"
  - test: "Independent security review — a reviewer other than MIA assesses the host, container network exposure, AIOS_API_KEY handling in src/auth.py, the exposure path and operational controls, and records a written decision tied to the host and image revision before any public exposure"
    expected: "Security row moves off Pending only on that written decision; the API stays private until then"
    why_human: "Independence and security acceptance are human judgments; the reviewer is explicitly unassigned"
  - test: "Task 3 human-check deferred to end-of-phase UAT: read docs/api-host-decision.md beside docs/DEPLOYMENT.md and docs/operational-readiness-005c.md"
    expected: "A reader learns in order that the host is selected and named, what was actually checked on 2026-11-17, and that every gate is Pending with the API private; the record does not read as deployment approval and invents no guest ID, storage name, threshold, delegate or reviewer"
    why_human: "Tone and honesty of prose ('does this read as approval?') cannot be asserted by a string check; the deferred item from the SUMMARY's open deviation"
---

# Phase 1: Host selection and evidence plan Verification Report

**Phase Goal:** Produce one decision record naming an eligible host and operator, or a blocked decision, with explicit host evidence criteria and owners.
**Verified:** 2026-11-16T20:55:00Z
**Status:** human_needed
**Re-verification:** Yes — initial was 2026-11-06T22:14:36Z (`human_needed`, 3/3); the deliverable has since been rewritten on `docs/api-host-readiness` at `030df1e` and re-checked from scratch.

## Goal Achievement

### Observable Truths

ROADMAP success criteria (3) merged with the PLAN's 5 must-have truths. None of the PLAN truths weakens a roadmap criterion.

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Roadmap SC1 — the record names the host and operator | ✓ VERIFIED | `docs/api-host-decision.md:3` `Status: Selected — host peakybuildr, a Linux Proxmox VE host on the tailnet at 100.122.194.34.` Line 5 names MIA / Nur Amirah Binti Mohd Kamil (GitHub `strdst7`) as interim operator; line 7 dates it 2026-11-17. `peakybuildr` matches the only host facts in evidence (tailnet 100.122.194.34). |
| 2 | Roadmap SC2 — Streamlit separated from FastAPI/SQLite; one-host, one-replica topology | ✓ VERIFIED | Lines 19, 23–25: `app.py` on Streamlit Community Cloud is the session-local demo, not the API; the API is the `Dockerfile` image `python:3.10-slim` with `uvicorn src.main:app` on `0.0.0.0:8000`, `EXPOSE 8000`, `AIOS_REQUIRE_PERSISTENCE=1`; one LXC guest, one replica. Matches `Dockerfile:8,14,19,24,26` exactly. One replica justified from `src/services/monitoring_service.py:25` (`self.lock = Lock()`) and `:26` (single `sqlite3.connect` file). |
| 3 | Roadmap SC3 — four host gates plus security review have owners, evidence requirements and pending status | ✓ VERIFIED | Lines 55–61: five rows in plan order (Host volume, Backup schedule, Restore drill, Disk monitoring, Security review), each with owner, a peakybuildr/guest-specific check, evidence to retain, and `Pending`. Security review row is the fifth row, visually separate in its owner column ("Independent reviewer, assignment pending") and line 53 says it cannot be closed by host operations work. |
| 4 | PLAN T1 — record names peakybuildr (100.122.194.34) with MIA as named operator (interim until a delegate), dated by the 2026-11-17 check | ✓ VERIFIED | Lines 3–7; only that claim is asserted. No delegate name is invented. |
| 5 | PLAN T2 — record states exactly which facts are verified at the Proxmox layer, dated, and labels every VM/container, mount, backup, alert and review item not yet evidenced | ✓ VERIFIED | Lines 13–15 verify exactly ICMP echo, HTTPS `HTTP 200` on 8006, TCP 22 — the same three facts the orchestrator established; line 15 says it does not prove the API runs, a guest exists, or storage is provisioned, and that 8006 is the web UI. Ledger lines 38–47 mark guest, storage, mount, ownership, start policy, network, API key, backup, alerting and security as Not verified; line 49 says every such item is Pending. No measured claim appears in the Verified column. |
| 6 | PLAN T3 — one Docker image from the repo Dockerfile runs in one VM or LXC guest on peakybuildr, persistent `/data`, `AIOS_OBSERVATION_DB=/data/observations.db`, `AIOS_REQUIRE_PERSISTENCE=1`, exactly one replica; shape chosen, not executed | ✓ VERIFIED | Lines 9, 23–26: LXC chosen over VM with reasons, VM kept as fallback, open items (guest ID, storage, CPU/memory, address, operator, runtime user) declared unmade. Line 9 states nothing was built, run, created or deployed. |
| 7 | PLAN T4 — four host gates and a separate security review each name owner, check, evidence and Pending; no gate closed by CI or the reachability check | ✓ VERIFIED | Lines 55–61 as in #3; line 63 explicitly excludes disposable CI results, the tmpfs full-volume simulation and the Proxmox reachability check as gate evidence. Five `Pending` cells confirmed by parsing every table row. |
| 8 | PLAN T5 — API stays private: security review precedes any public exposure; the record names no public URL, deployment or approval | ✓ VERIFIED | Line 63 keeps DEPLOYMENT.md's "production API deployment remains blocked" true and says deployment is not approved; line 67 keeps the API private and requires the security review plus gate evidence before exposure. No URL, IP of a running API, approval or deployment is claimed. |

**Score:** 8/8 truths verified (0 present, behavior-unverified).

### Deferred Items

| # | Item | Addressed In | Evidence |
|---|------|-------------|----------|
| 1 | Five gate statuses moving off Pending | No later phase exists (one-phase roadmap) | Explicitly out of scope for this phase by D-01/D-03; correctly Pending, not deferred work for another phase |

Nothing was moved to `deferred:` from the gap list — no gaps were found.

### Required Artifacts

| Artifact | Expected | Status | Details |
| --- | --- | --- | --- |
| `docs/api-host-decision.md` | Selected-host decision record with ledger, runtime shape, four gates, security review | ✓ VERIFIED | 67 lines, 7.3 KB, substantive prose (no placeholder/stub markers); `query verify.artifacts` → `all_passed: true`, 1/1, exit 0. Not wired into code because it is a document — wiring is checked as key links below. |

### Key Link Verification

`query verify.key-links` exits 1 (`all_verified: false`, 2/4): it reports "Target not referenced in source" for `docs/DEPLOYMENT.md` and `docs/operational-readiness-005c.md`. That is a checker false negative — the record links them as relative Markdown targets (`[deployment guide](DEPLOYMENT.md)`, `[operational-readiness report](operational-readiness-005c.md)` at line 63), not root-relative strings. Semantically all four links hold:

| From | To | Via | Status | Details |
| ---- | --- | --- | ------ | ------- |
| `docs/api-host-decision.md` | `Dockerfile` | uvicorn src.main:app, EXPOSE 8000, AIOS_REQUIRE_PERSISTENCE=1 unchanged | ✓ WIRED | Checker verified; content matches `Dockerfile:14,24,26` |
| `docs/api-host-decision.md` | `src/services/monitoring_service.py` | Absolute, non-`:memory:` DB enforcement under AIOS_REQUIRE_PERSISTENCE=1 | ✓ WIRED | Checker verified; `monitoring_service.py:20-23` raises `ValueError` for `:memory:` or a non-absolute path |
| `docs/api-host-decision.md` | `docs/DEPLOYMENT.md` | /data mount, env setup, same four gates — no contradiction | ✓ WIRED manually | Line 63 links it; DEPLOYMENT.md:26,30,34–37 agree (mount, blocked statement, four checks); no contradiction found |
| `docs/api-host-decision.md` | `docs/operational-readiness-005c.md` | Disposable-CI evidence insufficient for host acceptance | ✓ WIRED manually | Line 63 links it; operational-readiness-005c.md:3,18,60,64–73 say the same |

### Data-Flow Trace (Level 4)

N/A — static decision record; no rendered dynamic data.

### Behavioral Spot-Checks

All three PLAN assertions run from the repo root, exactly as written in the plan, against HEAD `030df1e`:

| Behavior | Command | Result | Status |
| --- | --- | --- | ------ |
| Task 1 wording/status assertions | `python3 -c '<01-01-PLAN.md Task 1 <automated>>'` | `missing []`, `EXIT=0` | ✓ PASS |
| Task 2 gate-table assertions | `python3 -c '<01-01-PLAN.md Task 2 <automated>>'` | `missing []`, `EXIT=0` | ✓ PASS |
| Task 3 source-reconciliation assertions | `python3 -c '<01-01-PLAN.md Task 3 <automated>>'` | `failed [] pending_cells 5`, `EXIT=0` | ✓ PASS |
| Whitespace hygiene | `git diff --check` | no output, `EXIT=0` | ✓ PASS |
| Decision coverage gate | `query check.decision-coverage-verify <phaseDir> 01-CONTEXT.md` | `total: 4, honored: 4, not_honored: []`, exit 0 | ✓ PASS (non-blocking) |

The SUMMARY (line 138) claims Task 2's shipped assertion "can never pass". That is false at HEAD: commit `d6327ae` turned the ledger label into a real table row (`docs/api-host-decision.md:34`), so the `^\| Not verified` clause is satisfied and Task 2 exits 0. The fact is re-stated as an open "Deviation" in the plan (commit `030df1e`) but is now stale. Non-blocking, listed under Anti-Patterns.

### Source-Claim Verification (PLAN Task 3 reconciliation points)

| Claim in the record | Code as it exists | Verdict |
| --- | --- | --- |
| `python:3.10-slim`, `uvicorn src.main:app`, `0.0.0.0:8000`, `EXPOSE 8000`, `AIOS_REQUIRE_PERSISTENCE=1` in ENV | `Dockerfile:8,14,24,26` — exact match, two-stage build | TRUE |
| A relative or `:memory:` `AIOS_OBSERVATION_DB` raises `ValueError` at startup when `AIOS_REQUIRE_PERSISTENCE=1` | `monitoring_service.py:20-23`; the service is constructed at import time (`src/main.py:29`), so the image fails at startup, before serving | TRUE |
| Writes serialised by a local `Lock` around one SQLite file | `monitoring_service.py:25-26,46,107` | TRUE |
| `503` when the server key is unset, short, whitespace-padded or a placeholder | `src/auth.py:7-9` — `not api_key or len < 32 or api_key != api_key.strip() or in {dev-key, changeme, password, secret, default, test-key}` → 503 | TRUE (placeholder list is finite; "a placeholder" is a fair summary, no stronger claim made) |
| `401` when the client key is missing or mismatched | `src/auth.py:10-11` — `not x_api_key or not compare_digest(...)` → 401 | TRUE |
| Deployment remains blocked; the four gates are unchanged | `DEPLOYMENT.md:30,34-37` | TRUE |
| CI results are disposable runners incl. a tmpfs full-volume simulation | `operational-readiness-005c.md:3,14,24-28,60` | TRUE |
| `app.py` is Streamlit, not the API | `DEPLOYMENT.md:4,8`; `app.py` | TRUE |

No Verified-column row lacks a dated check that was actually run against peakybuildr; the three rows are exactly the three facts established on 2026-11-17.

### Probe Execution

N/A — no probe declared; documentation-only phase.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| ----------- | ----------- | ----------- | ------ | -------- |
| HOST-01 | `01-01-PLAN.md` | Record a named stateful API host and operator, or a blocked decision | ✓ SATISFIED | Truths #1, #4 |
| HOST-02 | `01-01-PLAN.md` | Record runtime, persistent mount path, one-host/one-replica constraint, Streamlit's separate role | ✓ SATISFIED | Truths #2, #6 |
| GATE-01 | `01-01-PLAN.md` | Host-volume, backup schedule, restore drill, disk-alert checks with evidence requirements and owners | ✓ SATISFIED | Truths #3, #7 |
| GATE-02 | `01-01-PLAN.md` | Security review separate from public exposure; proposed vs completed evidence distinguished | ✓ SATISFIED | Truths #3, #8 |

**Coverage:** 4/4 mapped, 0 orphaned (REQUIREMENTS.md maps only these four to Phase 1).

### Decision Coverage

All 4 trackable CONTEXT.md decisions (D-01 through D-04) honored by shipped artifacts (`query check.decision-coverage-verify`: 4/4, exit 0). The "Claude's Discretion … assign a named delegate" item is not satisfied — it belongs in moral terms to the human owner and is listed in Human Verification, not counted as a content gap.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| ---- | ---- | ------- | -------- | ------ |
| `01-01-SUMMARY.md` | 138 / 144–149 | Stale claim that Task 2's shipped assertion "can never pass"; false at `d6327ae` (Task 2 exits 0) | ℹ️ Info | Mislabels a later fix as an open deviation; no effect on the deliverable |
| `docs/api-host-decision.md` | 34 | `\| Not verified \| — \| The rows below are the outstanding checks; this row labels them. \|` — a provenance/label row inside a two-column data table | ℹ️ Info | Reads as a data row in the middle of a ledger; it exists only to satisfy Task 2's `^\| Not verified` clause. Harmless but visible overfitting to the check |
| `01-01-PLAN.md` | 84 (truncated in file view) | Truncated action text in the plan file | ℹ️ Info | Pre-existing; does not affect must-haves or checks |

No `TBD`/`FIXME`/`XXX` debt markers in `docs/api-host-decision.md` (grep exit 1). The only "placeholder" hit is the auth-policy description, which matches `src/auth.py`.

### Human Verification Required

All seven items are deliberately Pending or out of the deliverable's reach; none is a documentation gap. Listed above in frontmatter `human_verification`:

1. **Named delegate** — MIA assigns the peakybuildr operating contact.
2. **Host volume gate** — collect on the real guest.
3. **Backup schedule gate** — collect on the real guest.
4. **Restore drill gate** — collect on the real guest.
5. **Disk monitoring gate** — collect on the real guest.
6. **Independent security review** — reviewer unassigned; API stays private.
7. **Task 3 human-check** (deferred end-of-phase UAT) — record reads as a decision, not an approval.

### Gaps Summary

No gaps. Every must-have truth and all four ROADMAP success criteria are verified against the shipped document and the code it cites; the 2026-11-17 ledger evidence is limited to exactly the three Proxmox-layer facts established (ICMP, HTTPS 200 on 8006, TCP 22) and the document says plainly what that does not prove. The three plan assertions exit 0 on their real content (not a modified copy). The phase cannot be `passed` only because the host gates, the security review, the named delegate and the Task 3 prose review are human-only and intentionally Pending — that is `human_needed`.

Out-of-deliverable documentation drift (not phase scope, reported for the orchestrator): `.planning/PROJECT.md:26` still says "No API host is selected", the Key Decisions table row "Select a host before implementation" is `Pending`, and `.planning/ROADMAP.md:24` still describes the plan as "Record the blocked API host decision". `docs/DEPLOYMENT.md` also still reads as host-agnostic — which the record explicitly reconciled rather than edited, as the plan required.

---

_Verified: 2026-11-16T20:55:00Z_
_Verifier: Hermes subagent (gsd-verifier)_
