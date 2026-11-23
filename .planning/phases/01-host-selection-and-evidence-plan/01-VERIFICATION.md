---
phase: 01-host-selection-and-evidence-plan
verified: 2026-11-23T03:11:24Z
status: human_needed
score: 4/5 must-haves verified
covered_files:
  - .planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md
  - .planning/phases/01-host-selection-and-evidence-plan/01-01-SUMMARY.md
  - docs/api-host-decision.md
  - docs/host-gate-evidence-2026-11-17.md
  - .planning/PROJECT.md
covered_digest: "v4:sha256:8660c98668504682078b769eb68d62b09a339bd90072d341bfbcd96580bcbb42"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: human_needed
  previous_score: 3/5 must-haves verified
  gaps_closed:
    - "T2's ledger contradiction is closed: docs/api-host-decision.md:38-39 now read as historical drill facts (`The drill host existed …` / `The drill volume was provisioned …`) and stay `Pending`, and :15 now bounds the reachability check to `a guest exists for the API` and `storage is provisioned for it`, so no Pending prerequisite sits under a Verified row"
    - "The Status-line miscount is closed: docs/api-host-decision.md:3 now says `Three host gates were measured on 2026-11-17 and a fourth is partial`, matching :57-60 and :67"
    - "The evidence-retention regression is closed in substance: docs/host-gate-evidence-2026-11-17.md:31-63, 68-93, 98-122 retains the lvs/findmnt/stat output, restart/recreate results, timer line, backup log, forced `backup_write_failed`, restore integrity and identical-state results, planted UUIDs and replay step, and it carries them past the contract (detailed at Gap 2); :124-136 carries the threshold and the explicit `No delivery channel exists`"
    - "The restore row now names the UUID-replay result: docs/api-host-decision.md:59 and docs/host-gate-evidence-2026-11-17.md:115-118"
    - ".planning/PROJECT.md:26 now says three gates verified and disk monitoring Partial, matching the decision record"
    - "The scaffold factory was removed, so re-running the plan cannot mint a guest ID, storage name, threshold or IP on peakybuildr; the NEW-capability sweep is therefore NOT APPLICABLE"
  gaps_remaining:
    - "T2 — `every VM/container, mount, backup, alert and review item` is still not labelled not-yet-evidenced: the Mount and Ownership rows read `Verified 2026-11-17` (docs/api-host-decision.md:40-41) and the Backup row (:45) and Storage free capacity (:39) carry no date, check or evidence pointer: partial"
  regressions:
    - "Retained evidence narrates state a Pending row denies: docs/host-gate-evidence-2026-11-17.md:61-63, 89, 120-122 describe fixing `/data` ownership and destination permissions and re-running, while docs/api-host-decision.md:40-41 and :45 still label those drill checks Pending with no date"
    - "A repo markdown file records shell commands run as root on the production host against unwritable and forced-threshold paths (docs/host-gate-evidence-2026-11-17.md:82-93, :131-132, :145-152) with no record of the creating or tear-down commands, against Threat T-01-05 and 01-01-PLAN.md:145"
human_verification:
  - test: "Confirm whether the drill destination /srv/bkro and the threshold override at docs/host-gate-evidence-2026-11-17.md:82-93 and :131-132 are still present on peakybuildr, and remove them; then state whether the rules forbidding host-directory ownership changes and threshold edits on the real volume (docs/api-host-decision.md:60 `Do not fill production storage`, 01-01-PLAN.md:102, 01-01-PLAN.md:145 `no provisioning … is authorised by this phase`) still stand"
    expected: "Either the leftovers are removed and the record states the admin-path work honestly, or the rules are formally amended; this cannot be decided from the repo because peakybuildr is outside it"
    why_human: "Only the operator can check and clean the host, and amending a threat-model rule is a project-governance decision, not a document fix"
  - test: "Disk monitoring gate — set capacity thresholds for the volume holding /data, prove an alert is delivered, and show backup-write error reporting without filling production storage"
    expected: "Row moves off `Partial — no delivery channel` only on a delivered alert; tests/full_volume.py was not run against the real volume"
    why_human: "The record states no delivery channel reaches a person (docs/api-host-decision.md:60) and docs/DEPLOYMENT.md:54 confirms no alerting integration exists in the repo"
  - test: "Independent security review — a reviewer other than MIA assesses the host, container network exposure, AIOS_API_KEY handling in src/auth.py, the exposure path and operational controls, and records a written decision tied to the host and image revision before any public exposure"
    expected: "Security row moves off Pending only on that written decision; the API stays private until then"
    why_human: "Independence and security acceptance are human judgments; the reviewer is explicitly unassigned (docs/api-host-decision.md:61)"
---

# Phase 1: Host selection and evidence plan Verification Report

**Phase Goal:** Produce one decision record naming the selected host and operator, with explicit host evidence criteria and owners; record a blocked decision only when no eligible host exists (`.planning/ROADMAP.md:14`).
**Verified:** 2026-11-23T03:11:24Z, working tree on HEAD `e0fe598` plus uncommitted fixes (`docs/api-host-decision.md`, `docs/host-gate-evidence-2026-11-17.md`, `.planning/PROJECT.md`)
**Status:** human_needed
**Re-verification:** Yes — previous report (`2026-11-23T03:09:24Z`, `human_needed`, 3/5) found five defects. Every truth is re-decided below against the current files; nothing is carried forward.

## Goal Achievement

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | SC1 — record names the host and operator, or states what is blocked | ✓ VERIFIED | `docs/api-host-decision.md:3` names `peakybuildr` and `100.122.194.34`; `:5` names MIA / Nur Amirah Binti Mohd Kamil (`strdst7`) as interim operator with the delegate still pending; `:7` dates the decision 2026-11-17. No delegate name invented (`:5`, `:67`). |
| 2 | SC2 — Streamlit separated from FastAPI/SQLite; one-host, one-replica topology | ✓ VERIFIED | `docs/api-host-decision.md:19` separates the Streamlit demo from the `Dockerfile` image and matches `Dockerfile:14,26,28,30` (`python:3.10-slim`, `AIOS_REQUIRE_PERSISTENCE=1`, `EXPOSE 8000`, `uvicorn … --host 0.0.0.0 --port 8000`); `:23` one LXC guest; `:24` one replica, justified by `self.lock = Lock()` at `src/services/monitoring_service.py:25` over one SQLite file. |
| 3 | SC3 — four host gates and the security review have owners, evidence requirements and pending status until target-host checks pass | ✓ VERIFIED | Each row carries owner, check and evidence (`docs/api-host-decision.md:57-61`). The "pending until checks pass" clause is discharged exactly as written: three host gates passed their target-host check and read `Verified 2026-11-17` (`:57-59`), Disk monitoring reads `Partial — no delivery channel` because its own check "prove an alert is delivered" is unmet (`:60`), and Security review is `Pending` (`:61`). The checks were run on drill guest 158, not the API guest, and the record says so (`:53`, `:63`). |
| 4 | T1 — peakybuildr (100.122.194.34) with MIA interim, dated by the 2026-11-17 check | ✓ VERIFIED | `docs/api-host-decision.md:3,5,7`; method at `:13`; bound at `:15`, which now limits the reachability check to the management ports. |
| 5 | T2 — states exactly which facts are verified at the Proxmox layer and on which date, and labels every VM/container, mount, backup, alert and review item as not yet evidenced | ⚠️ PARTIAL (both prior defects closed, one clause still unmet) | Proxmox-layer facts are exact and dated (`docs/api-host-decision.md:13`, `:35-37`). Guest and Storage are closed: they read as historical drill facts and stay `Pending` (`:38-39`), and `:15` now says the check proves neither `a guest exists for the API` nor `that storage is provisioned for it`, so no Pending prerequisite sits under a Verified row any more. What remains is the mount/backup half: `:40-41` read `Verified 2026-11-17`, and `:45` (Backup) and `:39` (free capacity) name no date, check or evidence pointer, so those items are neither labelled not-yet-evidenced nor dated as verified. |
| 6 | T3 — one Dockerfile image, one VM or LXC, `/data`, `AIOS_OBSERVATION_DB=/data/observations.db`, `AIOS_REQUIRE_PERSISTENCE=1`, one replica; shape chosen, not executed | ✓ VERIFIED in substance (decision-only tail superseded) | Shape fixed with VM as fallback and open items unmade (`docs/api-host-decision.md:23-26`); persistence claim matches `src/services/monitoring_service.py:19-23`, constructed at import in `src/main.py:29`; replica claim matches `src/services/monitoring_service.py:25`. The "not executed" tail is superseded: a container was run on guest 158 (`:43`, `:44`), and `:9` and `:63` state that plainly while `:38` keeps "No guest is sized or appointed for the API". The plan's own doubt (Task 3 imported `app.py`, `requirements.txt`, `src/agent.py`, `OPERATIONS.md`; `01-01-PLAN.md:116`) was resolved at `docs/api-host-decision.md:19` without editing them. |
| 7 | T4 — gates each carry a Pending status; no gate is closed by CI results or by the reachability check | ✓ VERIFIED in substance (status clause superseded) | Three rows read `Verified 2026-11-17` (`docs/api-host-decision.md:57-59`), so the literal "Pending" clause is superseded, not breached. The anti-shortcut clause holds: the reachability check is not reused as gate evidence (`:35-37` vs `:57-61`), and CI/tmpfs results are excluded (`:63`, `docs/operational-readiness-005c.md:60`); each closure rests on a command in `docs/host-gate-evidence-2026-11-17.md:31-122`. |
| 8 | T5 — API stays private; security review precedes public exposure; no public URL, deployment or approval | ✓ VERIFIED | `docs/api-host-decision.md:61` security review Pending and unassigned; `:9` and `:63` say deployment is not approved and the API is not deployed; `:67` keeps the API private and gates exposure on the review. `:43` binds `127.0.0.1:18000` inside the drill guest; `docs/host-gate-evidence-2026-11-17.md:143` says nothing listens beyond loopback. No public URL or approval anywhere. |

**Score:** 4/5 must-haves verified (T1, T3, T4, T5); SC1, SC2 and SC3 additionally verified; T2 partially verified.

## Prior findings, re-decided

| Prior finding | Verdict now | Why |
| --- | --- | --- |
| Status line said "Two" where three gates were measured | **CLOSED** | `docs/api-host-decision.md:3` now says "Three host gates were measured on 2026-11-17 and a fourth is partial", matching `:57-60` and `:67`; the old `Two`/`Three` split is gone. |
| T2 regression — Verified column carried guest/storage/mount/ownership while `:15` denied a guest or storage exists | **PARTIALLY CLOSED** | The contradiction is gone: Guest and Storage are `Pending` historical statements (`:38-39`) and `:15` was narrowed to "for the API" / "for it" (`:15`), and Mount/Ownership (`:40-41`) now sit under rows that describe the drill host as having existed rather than claiming its absence, so the "Verified under Pending prerequisites" defect no longer applies. What is not fixed is T2's second clause: mount and backup items are not labelled not-yet-evidenced, and `docs/host-gate-evidence-2026-11-17.md:61-63` and `:120-122` narrate the ownership repair that `:40-41` and `:45` still call Pending without a date. |
| `:15` overstated what the reachability check proves | **CLOSED** | `docs/api-host-decision.md:15` now reads "does not prove … that a guest exists for the API, or that storage is provisioned for it" and adds the drill-storage qualifier. |
| Restore row dropped the UUID-replay result | **CLOSED** | `docs/api-host-decision.md:59` names the UUID result; `docs/host-gate-evidence-2026-11-17.md:115-118` records the mechanism (`monitoring_service.evaluate` returns the stored report for a known `observation_id`) and `:147-152` is the executable replay step. |
| No retained gate evidence in the repo | **CLOSED** | `docs/host-gate-evidence-2026-11-17.md` contains every artifact the gate table names — see "Evidence retention" below. |
| `.planning/PROJECT.md:26` said all four gates Pending | **CLOSED** | `.planning/PROJECT.md:26` now says three gates verified on a drill guest, disk monitoring Partial, security review and the API guest Pending. |

## Evidence retention

`docs/host-gate-evidence-2026-11-17.md` is real and covers the gate table row by row:

| Gate-table claim (`docs/api-host-decision.md`) | Artifact (`docs/host-gate-evidence-2026-11-17.md`) |
| --- | --- |
| mount source, ext4, rw on `/fourtera/aios-158-data` (`:57`) | `lvs` and both `findmnt` outputs at `:31-39`; `mp0` line at `:23` |
| host `100000:100000 755`, guest `root:root 755`, database `644` (`:57`) | `stat` output at `:41-46` |
| restart and recreate returned identical history/current/anomaly, `integrity_check ok` (`:57`) | `:53-58` (`RESTART_IDENTICAL=yes`, `RECREATE_IDENTICAL=yes`, `live integrity: ok`), and `:143` records nothing exercised the write endpoint, so the 9 rows are the only state |
| timer `aios-backup.timer` daily 02:30, 7-day retention, `/srv/aios-backup` on `pve-root` (`:58`) | `:68-73` timer listing and `findmnt` device; `:89` retention policy |
| completed scheduled run `OK backup=… bytes=28672` (`:58`) | `:76-80` |
| forced `ERROR backup_write_failed` and exit 1 (`:58`) | `:84-87`, with the honest note at `:92-93` that the `chmod 500` attempt was not a valid simulation |
| restore into a separate directory and second container, all identical, live source untouched (`:59`) | `:98-113` |
| UUID replay (`:59`) | `:115-118` mechanism plus `:147-152` replay command |
| threshold `ok disk_use=21% threshold=80%`, alert line on forced threshold, error reporting (`:60`) | `:127-132` |
| "No delivery channel reaches a person yet" (`:60`) | `:135-136` |

What is *not* in the file, and cannot be, is the guest itself: `docs/host-gate-evidence-2026-11-17.md:140` states guest 158 is a drill guest, and keeping it alive, keeping the backup timer installed and keeping the DB readable so future verifiers can re-run `:147-152` is an operator obligation that the repo cannot hold. That is a stated limitation, not a closed claim — but it is not a retention regression either, because the file proves what it asserts and says plainly where the proof stops.

## Behavioral Spot-Checks

All three `<automated>` assertions from `01-01-PLAN.md` re-run verbatim from the repo root against the working tree:

| Behavior | Command | Result | Status |
| --- | --- | --- | --- |
| Task 1 wording/status assertions | `python3 -c '<01-01-PLAN.md:90>'` | `missing []`, exit 0 | ✓ PASS |
| Task 2 gate-table assertions | `python3 -c '<01-01-PLAN.md:106>'` | `missing []`, exit 0 | ✓ PASS |
| Task 3 source-reconciliation assertions | `python3 -c '<01-01-PLAN.md:118>'` | `failed [] pending_cells 9`, exit 0 | ✓ PASS |
| Whitespace hygiene | `git diff --check` | no output, exit 0 | ✓ PASS |

Assertion caveats still worth reporting, unchanged in nature:
- `01-01-PLAN.md:106` counts `| pending` cells across the whole document, so it cannot detect a gate row leaving `Pending`; `docs/api-host-decision.md:38-47` alone supplies the 9 cells.
- The `uuid replay` literal at `01-01-PLAN.md:106` would pass on the check column of `docs/api-host-decision.md:59`; it now matches the evidence column too (`:59`, `docs/host-gate-evidence-2026-11-17.md:115-118`).
- `01-01-PLAN.md:118`'s `auth` check only greps for `503`/`401`; the full 503/401 behaviour is verified separately below.

## Source-Claim Verification

| Claim in `docs/api-host-decision.md` | Source | Verdict |
| --- | --- | --- |
| `python:3.10-slim`, `uvicorn src.main:app`, `0.0.0.0:8000`, `EXPOSE 8000`, `AIOS_REQUIRE_PERSISTENCE=1` (`:19`) | `Dockerfile:2,8,14,18,26,28,30` | TRUE |
| Relative or `:memory:` DB path raises `ValueError` at startup (`:25`) | `src/services/monitoring_service.py:19-23`, constructed at import `src/main.py:29` | TRUE |
| One replica because writes serialise on a local `Lock` over one SQLite file (`:24`) | `src/services/monitoring_service.py:25`, transaction opened per write at `:47-48` | TRUE |
| Security review scope: 503 unset/short/padded/placeholder, 401 missing/mismatched (`:61`) | `src/auth.py:7-11` | TRUE (server-key check line 9, client-key check line 11) |
| Deployment remains blocked; `DEPLOYMENT.md` still governs (`:63`) | `docs/DEPLOYMENT.md:30` | TRUE |
| CI/tmpfs results disposable and excluded (`:63`) | `docs/operational-readiness-005c.md:60,64-70` | TRUE |
| No alerting integration in the repo (`:60` framing) | `docs/DEPLOYMENT.md:54` | TRUE |
| Guest 158, storage, mount and ownership facts (`:38-41`) | `docs/host-gate-evidence-2026-11-17.md:11-59` | TRUE — operator-reported host output; version, container and docker inputs are not in the env block at `:11-18` |
| Backup timer, destination, run and error (`:58`) | `docs/host-gate-evidence-2026-11-17.md:68-87` | TRUE — timer listing shows `LAST -` (`:70`), so no second scheduled fire predates the log line at `:79` |
| Restore results and UUID replay (`:59`) | `docs/host-gate-evidence-2026-11-17.md:98-118` | TRUE — the `False` history value at `:107` has no corresponding `current`/`anomaly` line, which rests a single-state claim on one row |
| `history identical: True` over 9 rows (`:57`, `:59`) | `src/services/monitoring_service.py:55-62,66-69` | TRUE, with a ceiling: `evaluate` returns the stored report when the telemetry fingerprint matches or `observation_id` is known, and `src/agent.py:33` stamps a fresh timestamp, so history can only be compared on ids and scores, never on bytes |

## Permission and exposure claims

`docs/api-host-decision.md:41` reports `root:root 755` for `/data` and `100000:100000 755` on the host; the same values are in `docs/host-gate-evidence-2026-11-17.md:42,44,46`. Both describe drill guest 158, and `:26` leaves the API container runtime user open, so nothing implies these are API-guest settings. `docs/host-gate-evidence-2026-11-17.md:61-63` says the ownership was changed with `chown 100000:100000` on the host path before the gate passed, yet `docs/api-host-decision.md:40-41` call the result `Verified 2026-11-17` while `:45` leaves the backup check Pending — the drift is listed as a regression below. No public bind, URL or exposure approval appears; `:43` is `127.0.0.1:18000` inside the drill guest only.

## Requirements Coverage

| Requirement | Source Plan | Status | Evidence |
| --- | --- | --- | --- |
| HOST-01 | `01-01-PLAN.md:11` | ✓ SATISFIED | Truth 1, Truth 4 |
| HOST-02 | `01-01-PLAN.md:12` | ✓ SATISFIED | Truth 2, Truth 6 |
| GATE-01 | `01-01-PLAN.md:13` | ✓ SATISFIED | Truth 3, Truth 7, Truth 5 with the mount/backup labelling gap noted |
| GATE-02 | `01-01-PLAN.md:14` | ✓ SATISFIED | Truth 8; `docs/api-host-decision.md:61`, `:63`, `:67` |

Planning bookkeeping is still stale and is reported, not edited: all four boxes unticked and `Pending` in `.planning/REQUIREMENTS.md:10-16,30-33`.

## Out-of-Deliverable Drift (reported, not edited)

- `.planning/ROADMAP.md:30` still reads "Awaiting human verification (host gates pending)".
- `.planning/phases/01-host-selection-and-evidence-plan/01-UAT.md:31-38` still records tests 3 and 4 blocked on "No guest exists on peakybuildr yet".
- `.planning/phases/01-host-selection-and-evidence-plan/01-01-SUMMARY.md:138` still claims Task 2's assertion "can never pass", contradicted by `:101` in the same file and by the passing run above.
- `docs/operational-readiness-005c.md:64` still names Streamlit Community Cloud as "the named host"; the decision record supersedes it but the report was not annotated.

## Gaps Summary

The phase goal holds and the author's five fixes are real: the status line, the guest/storage labelling, the `:15` scope, the UUID-replay result, the retained evidence file and `.planning/PROJECT.md:26` all check out. T2 is not fully closed — mount and backup items are still not labelled not-yet-evidenced or dated, and the evidence file narrates an ownership repair that the ledger still calls Pending. Beyond that, the evidence file itself records root-level host administration (`chown` on the mount path, `chmod`/immutable tricks on a backup destination, a forced threshold on the real volume, `pct exec`) directly on `peakybuildr`, with tree-level reports and a rule at `docs/api-host-decision.md:60` that forbids filling production storage and at `01-01-PLAN.md:145` that forbids host-path mounting. That is a governance question for the operator, not a document typo, so it is carried as a human item rather than silently absorbed. `status` stays `human_needed` for that question plus the two human-only gates that genuinely remain: disk-monitoring delivery and the independent security review.

---

_Verified: 2026-11-23T03:11:24Z_
_Verifier: Hermes subagent (gsd-verifier)_
