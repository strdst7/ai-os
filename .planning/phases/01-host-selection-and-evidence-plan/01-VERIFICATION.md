---
phase: 01-host-selection-and-evidence-plan
verified: 2026-11-23T06:45:11Z
status: human_needed
score: 4/5 must-haves verified
covered_files:
  - .planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md
  - .planning/phases/01-host-selection-and-evidence-plan/01-01-SUMMARY.md
  - docs/api-host-decision.md
  - docs/host-gate-evidence-2026-11-17.md
  - .planning/PROJECT.md
covered_digest: "v4:sha256:159c3b29aaa99b278707d2106b9e38764c4fd3bb35b25ec677448b1be45017c1"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: human_needed
  previous_score: 4/5 must-haves verified
  gaps_closed:
    - "The previous report's 'gate rows carry no date' finding is closed on the record's own terms: docs/api-host-decision.md:57-61 now carry a dated Status column (`Verified 2026-11-17`, `Verified 2026-11-17 for schedule, destination and run; notification path Pending`, `Partial — no delivery channel`), so the ledger's mount/backup items are no longer undated leaves"
    - "The plan's all-Pending gate contract is retired rather than silently broken: .planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:106 now requires a Pending/Verified/Partial status cell per row plus at least three Pending cells, and .planning/ROADMAP.md:20 adds the anti-shortcut clause 'A gate leaves Pending only on a recorded target-host check, never on CI or reachability evidence'"
    - "The drill-footprint finding is now recorded in-tree: docs/host-gate-evidence-2026-11-17.md:155-176 lists every item left on peakybuildr with its disposition and states the rows are 'present, not removed'"
    - "The 'record still reads as API stays private / not approved' check still holds after the plan edit: docs/api-host-decision.md:3, :9, :63, :67"
  gaps_remaining:
    - "T2 — the clause 'labels every VM/container, mount, backup, alert and review item as not yet evidenced' is still unmet and is NOT retired by the plan edit: docs/api-host-decision.md:40-41 read `Verified 2026-11-17`, :43-44 puts the container and API-key drill results in the Verified column, :45 puts off-volume backup results in the Verified column. The plan edit changed the *assertion* (.planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:106) and the ROADMAP criterion (.planning/ROADMAP.md:20), but the T2 truth text at 01-01-PLAN.md:25 and the Task 2 action at 01-01-PLAN.md:100/102/104 (`Keep exactly four host-gate rows … Status Pending`, `do not close any row`) were left unchanged — so the plan contradicts itself and T2 stays failed"
    - "`covered_digest` is bound (per the verification brief) to `v4:sha256:159c3b29…`; it is not recomputed over the five covered files in this pass, because .planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md was edited in HEAD `84d99fb` while docs/api-host-decision.md and docs/host-gate-evidence-2026-11-17.md were not. The digest therefore cannot have been taken after this HEAD over unchanged content; treat it as supplied, not independently confirmed"
  regressions:
    - "The plan revision lowered the bar where it matters most. Old assertion (.planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:106 at 17fc59b, diff in `84d99fb`) demanded `low.count(\"| pending\")>=5`; the new one accepts a row marked `| verified 2026-11-17` and pads the count with the ledger's ten unrelated `Pending` cells (docs/api-host-decision.md:38-47, 3-5 counted as ten because the gate Status cells are not Pending). Net effect: all four host gates and the security review could read `Verified` with an empty evidence pointer and both assertion and `01-01-PLAN.md:118` would still exit 0 — the check no longer proves 'no gate is closed without retained evidence', which is exactly the clause ROADMAP SC3 gained at .planning/ROADMAP.md:20"
    - "No machine check ties a `Verified` gate cell to a retained-evidence anchor. docs/api-host-decision.md:57-61 name artifacts only in prose; only :63 links the evidence file. A row could flip to `Verified 2026-11-17` with no anchor and nothing in .planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:106 or :118 would notice"
    - "Task 2's `<fails_when>` at .planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:107 still says 'fewer than five Pending cells exist' while the assertion at :106 accepts three; the fail text and the assertion disagree"
    - "Task 3's `<fails_when>` at .planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:119 still says 'or fewer than five Pending cells remain', but the code at :118 no longer counts Pending cells at all"
    - "Threat T-01-03's mitigation at .planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:143 still reads \"Task 2's verify asserts five Pending cells\" — false after the edit, so the threat register no longer describes the shipped check"
    - "Header miscount survives: docs/api-host-decision.md:9 says 'the two executed gates below were measured' while :57-59 mark three gates Verified and :3 says 'Three host gates were measured'"
    - "Plan prose vs ROADMAP: GATE-01 (Record …, no evidence required) is marked `Complete` at .planning/REQUIREMENTS.md:32, which FRESHNESS/REQUIREMENTS reads as satisfied, while .planning/ROADMAP.md:20 requires gates to stay Pending 'until target-host checks pass'. Defensible (the requirement is to record) but the two planning files now read differently on the same rows"
human_verification:
  - test: "Disk monitoring gate — set capacity thresholds for the volume holding /data, prove an alert is delivered to a person, and show backup-write error reporting without filling production storage"
    expected: "docs/api-host-decision.md:60 moves off `Partial — no delivery channel` only on a recorded delivered alert; `tests/full_volume.py` was not run against the real volume"
    why_human: "The record states no delivery channel reaches a person (docs/api-host-decision.md:60, docs/host-gate-evidence-2026-11-17.md:135-136) and docs/DEPLOYMENT.md:54 confirms no alerting integration exists in the repo"
  - test: "Independent security review — a reviewer other than MIA assesses the host, container network exposure, AIOS_API_KEY handling in src/auth.py, the exposure path and operational controls, and records a written decision tied to the host and image revision before any public exposure"
    expected: "docs/api-host-decision.md:61 moves off Pending only on that written decision; the API stays private until then"
    why_human: "Independence and security acceptance are human judgments; the reviewer is explicitly unassigned (docs/api-host-decision.md:61)"
  - test: "Drill footprint cleanup on peakybuildr — decide keep-or-remove for each row of docs/host-gate-evidence-2026-11-17.md:160-168 (guest 158 + LV fourtera/vm-158-data, containers aios-gate/aios-restore, /srv/aios-restore-isolated, /srv/bkro, the drill systemd units and scripts) and execute the removals with the commands listed there"
    expected: "Rows marked remove are gone from the host and :174-176's 'stated as present, not as removed' note is replaced by the actual outcome; evidence rows (:164) stay"
    why_human: "peakybuildr is outside the repo and the last cleanup attempt failed on Tailscale SSH re-auth (docs/host-gate-evidence-2026-11-17.md:174-176); only the operator can run `pct destroy` / `lvremove`"
---

# Phase 1: Host selection and evidence plan Verification Report

**Phase Goal:** Produce one decision record naming the selected host and operator, with explicit host evidence criteria and owners; record a blocked decision only when no eligible host exists (`.planning/ROADMAP.md:14`).
**Verified:** 2026-11-23T06:45:11Z, working tree on HEAD `84d99fb` (dirty only in `tests/.DS_Store`, unrelated).
**Status:** human_needed
**Re-verification:** Yes — previous report (`2026-11-23T03:11:24Z`, `human_needed`, 4/5) had T2 failing. Every truth is re-decided below from the current files; nothing is carried forward, and the plan edit in `84d99fb` is judged on whether it describes the real end state.

## Goal Achievement

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | T1 — peakybuildr (100.122.194.34) selected with MIA as interim operator, dated by the 2026-11-17 check | ✓ VERIFIED | `docs/api-host-decision.md:3` names host and address; `:5` names MIA / Nur Amirah Binti Mohd Kamil (`strdst7`) interim, delegate pending; `:7` dates it; `:13` records the method; `:15` bounds it to management ports and denies a guest or storage for the API. No delegate invented (`:5`, `:67`). |
| 2 | T2 — record states which facts are verified at the Proxmox layer and on which date, and labels every VM/container, mount, backup, alert and review item as not yet evidenced | ✗ FAILED | The first half holds: `docs/api-host-decision.md:35-37` are the three Proxmox-layer facts, each `Verified` and dated 2026-11-17 at `:13`. The second half does not: `:40` (Mount) and `:41` (Ownership) read `Verified 2026-11-17`; `:42` (Start policy) and `:43` (Network) and `:44` (API key) put the drill container's results in the Verified column; `:45` (Backup) puts the completed off-volume run in the Verified column; `:46` says the alert line was written. Only Guest, Storage and Security still read as not-yet-evidenced (`:38`, `:39`, `:47`). The plan edit retired the *assertion* (`01-01-PLAN.md:106`), not this truth (`01-01-PLAN.md:25`) nor Task 2's action (`01-01-PLAN.md:100`: `Every row keeps … Status Pending`; `:102` `Do not close any row`; `:104` `Nothing is marked passed`), so the record still departs from the plan it was built to satisfy. |
| 3 | T3 — one Dockerfile image, one VM or LXC, `/data`, `AIOS_OBSERVATION_DB=/data/observations.db`, `AIOS_REQUIRE_PERSISTENCE=1`, one replica; shape chosen (not executed) | ✓ VERIFIED | Shape fixed at `docs/api-host-decision.md:23-26` with VM as fallback and open items unmade. Matches `Dockerfile:8,14,24,26` (`python:3.10-slim`, `AIOS_REQUIRE_PERSISTENCE=1`, `EXPOSE 8000`, `uvicorn src.main:app --host 0.0.0.0 --port 8000`). Persistence claim matches `src/services/monitoring_service.py:20-23`; replica claim matches `src/services/monitoring_service.py:25`. The "not executed" tail is superseded honestly: `docs/api-host-decision.md:9` says what Phase 1 built (nothing) and that gates were measured afterwards on guest 158, and `:26` keeps the API guest unmade. |
| 4 | T4 — four host gates plus a separate security review each name an owner, the check, the evidence to retain and a Pending status; no gate closed by CI or the reachability check | ✓ VERIFIED in substance (status clause superseded by recorded target-host checks) | Every row at `docs/api-host-decision.md:57-61` has owner, a peakybuildr/guest check and an evidence-to-retain column. The literal Pending clause is superseded by `84d99fb` (`.planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:106`, `.planning/ROADMAP.md:20`) and by measurement, not by paperwork. The anti-shortcut clause holds: reachability (`:35-37`) is never cited as gate evidence, and each closure cites retained output in `docs/host-gate-evidence-2026-11-17.md:31-59` (Host volume), `:67-93` (Backup), `:98-122` (Restore); CI/tmpfs results are excluded at `:63` and `docs/operational-readiness-005c.md:60`. One gate sits between states: at `docs/api-host-decision.md:58` the failure-notification path is called both "still missing" and covered by "Verified 2026-11-17 for schedule, destination and run", and `:45` calls the same notification path Pending — a split status on one row, not a closure without evidence. |
| 5 | T5 — API stays private; security review precedes public exposure; no public URL, deployment or approval | ✓ VERIFIED | Security review Pending and unassigned (`docs/api-host-decision.md:61`); "deployment is still not approved" and "Deployment is not approved" (`:3`, `:9`); `:63` keeps `docs/DEPLOYMENT.md:30` true (`Production API deployment remains blocked`); `:67` keeps the API private and gates exposure on review plus gate evidence. Drill bind is `127.0.0.1:18000` (`:43`, `docs/host-gate-evidence-2026-11-17.md:149`). No public URL or approval anywhere. |

**Score:** 4/5 must-haves verified (T1, T3, T4, T5); T2 failed. SC1, SC2 and SC3 additionally hold as stated in `.planning/ROADMAP.md:18-20`.

## Plan revision `84d99fb` — honest retire or lowered bar?

**The edit is honest about the end state and dishonest about the bar.** Two separate questions:

1. *Does it describe what actually happened?* Yes. Host volume (`docs/api-host-decision.md:57`), Backup (`:58`) and Restore drill (`:59`) were measured on guest 158 and retained at `docs/host-gate-evidence-2026-11-17.md:31-122`. Before `84d99fb` the plan asserted five Pending cells that the record could no longer honestly supply; leaving that assertion in place would have forced either a false `Pending` or a failing check. Retiring it was right. `.planning/REQUIREMENTS.md:30-33` and `.planning/ROADMAP.md:20,30` now match the record, and `.planning/phases/01-host-selection-and-evidence-plan/01-01-SUMMARY.md:169-185` annotates the old "no gate evidence exists" line instead of rewriting history.

2. *Did it lower the bar in the way that matters?* Yes. The clause ROADMAP SC3 protects — "A gate leaves Pending only on a recorded target-host check, never on CI or reachability evidence" (`.planning/ROADMAP.md:20`) — has no machine check after the edit:
   - The old assertion demanded `low.count("| pending")>=5` (see the `-` line at `.planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:106` in `git show 84d99fb`). The new one demands a status cell be one of three values (`.planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:106`: `any(s in low for s in ("| pending","| verified 2026-11-17","| partial"))`) plus `low.count("| pending")>=3`.
   - Those three Pending cells are not gate cells. They come from `docs/api-host-decision.md:38-47`, which contains ten `| pending` cells. Flipping every gate row in `:57-61` to `Verified 2026-11-17` would still leave ten, and both `01-01-PLAN.md:106` and `:118` would exit 0.
   - The evidence to retain is prose only (`docs/api-host-decision.md:57-61`); only `:63` links the file. A `Verified` cell with no anchor passes.
   - So a gate can now be closed on nothing, including on a reachability check, and no check in the plan would object. That is exactly the shortcut the threat register names (`.planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:132`).

   The lazy fix is one line each: assert the gate table's status column only contains `Pending|Partial|Verified 2026-11-17`, and require any `Verified` row to name `host-gate-evidence-2026-11-17.md` or a dated line. Also update `01-01-PLAN.md:107` and `:119` (`<fails_when>` still says "fewer than five Pending cells") and `:143` (T-01-03 still says "Task 2's verify asserts five Pending cells").

**Verdict on T2:** still a regression, not a superseded expectation. The plan edit retires a *measurement-era* constraint on gate status (Task 2's assertion, ROADMAP SC3's Pending-until-checked phrasing), but T2 is a *labelling* truth — "labels every VM/container, mount, backup, alert and review item as not yet evidenced" (`.planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:25`). That sentence and the action that implements it (`:100`, `:102`, `:104`) are untouched by `84d99fb`, and the record still labels Mount, Ownership, Start policy, Network, API key and Backup as evidenced. Editing only the assertion contradicts the truth and the action it verifies; marking T2 verified would mean grading the document against a check written after the fact.

## Prior findings, re-decided

| Prior finding | Verdict now | Why |
| --- | --- | --- |
| T2 — every mount/backup item must be labelled not-yet-evidenced | **STILL OPEN** | `docs/api-host-decision.md:40-41`, `:43-45` remain Verified-column entries; `.planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:25`, `:100`, `:102` still demand not-evidenced labelling. See above. |
| Retained evidence narrates ownership repair that the ledger called Pending | **CLOSED** | The ledger now dates it: `docs/api-host-decision.md:41` and `:57` read `Verified 2026-11-17` for host `100000:100000`, matching `docs/host-gate-evidence-2026-11-17.md:61-63`. The narrate/deny contradiction is gone; what remains is the T2 labelling question, not a factual drift. |
| Restore row dropped the UUID-replay result | **CLOSED** | `docs/api-host-decision.md:59` names UUID replay; retained at `docs/host-gate-evidence-2026-11-17.md:115-118` and `:147-152`. |
| Gate rows carried no date | **CLOSED** | `docs/api-host-decision.md:57-61` Status column is dated or state-qualified. |
| Host-directory root work with no record (drill footprint) | **CLOSED as a record, OPEN as a host state** | `docs/host-gate-evidence-2026-11-17.md:155-176` lists the guest, LV, containers, `/srv/bkro`, `/srv/aios-restore-isolated`, the drill units and scripts, and the `chown`, with keep/remove guidance; `:170-172` bounds it (`No production storage was filled`, drill volume and throwaway dir only, guest 157 untouched). `:174-176` says outright the rows are "present, not removed". The tree no longer hides anything; removal is the operator's action, carried below. |
| `docs/api-host-decision.md:9` said "two executed gates" | **NEW, open** | `:3` says three were measured, `:57-59` show three `Verified`; `:9` still says "the two executed gates below". Minor count drift. |
| `.planning/phases/01-host-selection-and-evidence-plan/01-01-SUMMARY.md:138` says Task 2 "can never pass" | **CLOSED** | Superseded by `:101` and by the passing run below; `:169-185` annotates the rest. |
| `.planning/ROADMAP.md:30` said "Awaiting human verification (host gates pending)" | **CLOSED** | `.planning/ROADMAP.md:30` now records three gates verified, disk Partial, remaining human items. |
| `.planning/phases/01-host-selection-and-evidence-plan/01-UAT.md:31-38` blocked on "No guest exists" | **CLOSED** | `01-UAT.md:22-52` now records rows 3 and 4 as pass against the retained evidence. |

## Does the record still read "API stays private, deployment not approved"?

Yes, and the plan edit did not weaken it. `docs/api-host-decision.md:3` ("the deployment is still not approved"), `:9` ("Deployment is not approved"), `:63` ("the API is still not deployed", `docs/DEPLOYMENT.md` block still true), `:67` ("The API stays private, and public exposure needs the security review plus that gate evidence"). No public URL, bind or approval appears; the only listener recorded is `127.0.0.1:18000` (`:43`, `docs/host-gate-evidence-2026-11-17.md:143`).

## Behavioral Spot-Checks

All three `<automated>` assertions from `01-01-PLAN.md` re-run verbatim from the repo root at `84d99fb`, extracted from the `<automated>` element and executed as `python3 -c '<body>'` (the element also contains the `python3 -c ` prefix, which was stripped before execution):

| Behavior | Command | Result | Status |
| --- | --- | --- | --- |
| Task 1 wording/status assertions | `.planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:90` | `missing []`, exit 0 | ✓ PASS |
| Task 2 gate-table assertions | `.planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:106` | `missing []`, exit 0 | ✓ PASS |
| Task 3 source-reconciliation assertions | `.planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:118` | `failed []`, exit 0 | ✓ PASS |
| Whitespace hygiene | `git diff --check` | no output, exit 0 | ✓ PASS |

They pass, and that is the problem with Task 2's: passing proves only that the five literals appear and three `| pending` cells exist somewhere. Demonstrated ceiling — replace every gate row's status at `docs/api-host-decision.md:57-61` with `Verified 2026-11-17` and blank the evidence cells; `01-01-PLAN.md:106` and `:118` still exit 0 (10 `| pending` cells remain at `:38-47`). No such edit was made; the point is the check cannot see one.

Other caveats worth reporting:
- `01-01-PLAN.md:107` and `:119` (`<fails_when>`) still describe the five-Pending-cell rule that `:106`/`:118` no longer enforce.
- `01-01-PLAN.md:143` (T-01-03 mitigation) still claims the verify "asserts five Pending cells".
- `01-01-PLAN.md:90`'s `<automated>` element fails with `SyntaxError` if the whole element (including the `python3 -c ` prefix) is passed to `python3 -c`; only the quoted body is executable.

## Source-Claim Verification

| Claim in `docs/api-host-decision.md` | Source | Verdict |
| --- | --- | --- |
| `python:3.10-slim`, `uvicorn src.main:app`, `0.0.0.0:8000`, `EXPOSE 8000`, `AIOS_REQUIRE_PERSISTENCE=1` (`:19`) | `Dockerfile:2,8,14,24,26` | TRUE |
| Relative or `:memory:` DB path raises `ValueError` at startup (`:25`) | `src/services/monitoring_service.py:19-23` | TRUE |
| One replica because writes serialise on a local `Lock` over one SQLite file (`:24`) | `src/services/monitoring_service.py:5,25` | TRUE |
| Security review scope: 503 on unset/short/padded/placeholder, 401 on missing/mismatched (`:61`) | `src/auth.py:7-11` | TRUE |
| Deployment remains blocked; `DEPLOYMENT.md` governs (`:63`) | `docs/DEPLOYMENT.md:30` | TRUE |
| CI/tmpfs results disposable and excluded (`:63`) | `docs/operational-readiness-005c.md:60` | TRUE |
| No alerting integration in the repo (`:60`) | `docs/DEPLOYMENT.md:54` | TRUE |
| Guest 158, storage, mount, ownership (`:38-41`) | `docs/host-gate-evidence-2026-11-17.md:11-59` | TRUE — operator-reported host output; the env block at `:11-18` carries image digest but no build command |
| Backup timer, destination, run, forced error (`:58`) | `docs/host-gate-evidence-2026-11-17.md:67-93` | TRUE — timer listing shows `LAST -` (`:70`); the run at `:79` was started through the unit (`:76`), so "scheduled path" is accurate but was not an unattended fire |
| Restore and UUID replay (`:59`) | `docs/host-gate-evidence-2026-11-17.md:98-118` | TRUE — `history identical: True` at `:108`; no `current`/`anomaly` value is printed for the restored copy beyond `:110` |
| `history`/`current`/`anomaly` "byte-identical" (`:57`, evidence `:49-50`) | `docs/host-gate-evidence-2026-11-17.md:53-58` | PARTIAL — the lines are truncated with `…`, so identity is asserted by the `_IDENTICAL=yes` flags, not shown byte-for-byte |

## Requirements Coverage

| Requirement | Source Plan | Status | Evidence |
| --- | --- | --- | --- |
| HOST-01 | `01-01-PLAN.md:11` | ✓ SATISFIED | Truth 1, Truth 4 |
| HOST-02 | `01-01-PLAN.md:12` | ✓ SATISFIED | Truth 2 partially, Truth 3 |
| GATE-01 | `01-01-PLAN.md:13` | ✓ SATISFIED (recording) | Truth 4; the "record checks, owners, evidence" obligation at `.planning/REQUIREMENTS.md:15` is met, and `.planning/REQUIREMENTS.md:32` correctly says Partial for the measurement |
| GATE-02 | `01-01-PLAN.md:14` | ✓ SATISFIED (recording) | Truth 5; `.planning/REQUIREMENTS.md:33` correctly says Pending for the review itself |

`.planning/REQUIREMENTS.md:10-16` checkboxes none ticked while `:30-33` reads Complete/Complete/Partial/Pending — bookkeeping inconsistency, reported not edited. GATE-01 `Complete` at `:32` sits awkwardly against `.planning/ROADMAP.md:20`'s Pending-until-measured rule; the requirement text at `:15` only asks for the recording, so both readings survive, but the two files should agree.

## Out-of-Deliverable Drift (reported, not edited)

- `docs/api-host-decision.md:9` says "the two executed gates", `:3` and `:57-59` say three.
- `docs/api-host-decision.md:58` carries a split status on one row (schedule/destination/run verified; failure notification "still missing") while `:45` calls the same notification path Pending.
- `.planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:107`, `:119`, `:143` still describe the retired five-Pending-cell rule.
- `.planning/phases/01-host-selection-and-evidence-plan/01-01-SUMMARY.md:58-74` (coverage block) still credits D4 to "5 pending cells", a check that no longer exists.
- `docs/operational-readiness-005c.md:64` still names Streamlit Community Cloud as "the named host"; the record supersedes it without annotation.

## Gaps Summary

The phase goal holds and the record is a real decision, not an approval. T1, T3, T4 and T5 verify against the tree. T2 does not: the record still places mount, ownership, start policy, network, API key and backup drill results in its Verified column, and the plan text that requires them to read as not-yet-evidenced (`01-01-PLAN.md:25`, `:100`, `:102`, `:104`) was not edited. The `84d99fb` revision changed the assertion instead, and weakened it: three Pending cells drawn from the ledger plus a free choice of three status values means no gate closure — on evidence or on reachability — can be detected. That makes the plan's check describe an end state looser than the document it grades, which is a lowered bar, not an honest retire. Status stays `human_needed` for that plus three genuinely human-only items: an alert delivery channel, the independent security review, and the drill footprint still sitting on peakybuildr.

---

_Verified: 2026-11-23T06:45:11Z_
_Verifier: Hermes subagent (gsd-verifier)_
