---
phase: 01-host-selection-and-evidence-plan
verified: 2026-11-23T06:51:12Z
status: human_needed
score: 3/5 must-haves verified
covered_files:
  - .planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md
  - .planning/phases/01-host-selection-and-evidence-plan/01-01-SUMMARY.md
  - docs/api-host-decision.md
  - docs/host-gate-evidence-2026-11-17.md
  - .planning/ROADMAP.md
covered_digest: "v4:sha256:aa83916e86b9a8cdfa8b58f1d43574d22dd6550fd68f30b6753fce4db95432f6"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: human_needed
  previous_score: "4/5 must-haves verified"
  gaps_closed:
    - "The all-Pending contradiction is gone from the contract, not just the assertion: `.planning/phases/01-host-selection-and-evidence-plan/01-01-PLAN.md:25` now reads 'either Verified against retained evidence or not yet evidenced', `:27` allows 'a status of Pending, Verified or Partial', `:100` says 'a status cell reading Pending until a target-host check is recorded', `:104`'s 'do not close any row' is replaced by 'A row may read Verified only when the retained-evidence document carries the command output behind it', and `:130`, `:166`, `:179` were reworded to match. T2's *text* is no longer contradicted by the record — see the reset below for why that is not the same as T2 passing."
    - "`docs/api-host-decision.md:9`'s gate miscount is fixed: 'the three executed gates below' now matches the three `Verified 2026-11-17` rows at `:40`, `:41` and `:57` (plus `:59`) and the header count at `:3`."
    - "The prior report's documentation-only items are closed: `01-01-PLAN.md:130` no longer says 'fewer than five Pending cells', `:166` no longer counts Pending cells, and `:166` (T-01-03) no longer claims the verify 'asserts five Pending cells'. One stale copy survives at `01-01-SUMMARY.md:72`."
  gaps_remaining:
    - "T2 is NOT honestly satisfied. The truth text was relaxed to accept `Verified`, but nothing in the phase supplies the 'retained evidence' half of it: the only retained evidence (`docs/host-gate-evidence-2026-11-17.md`) is a prose transcript with no runnable provenance, and the record's status column is not machine-covered in any reliable way (five surviving tampers below). A checker that a single appended cell defeats cannot be the thing that makes a must-have true."
    - "The Task 2 `<automated>` element is malformed markup: it opens three times and closes four. The real body ends mid-script at `01-01-PLAN.md:106` (a 1,433-character one-liner that continues past the closing tag), and `01-01-PLAN.md:107-129` holds 14 lines of orphaned Python that no runner executes, terminated by a stray `</automated>` at `:129`. Anyone reading lines 106-130 believes a `for l in gate:` loop polices status cells; it is inert."
    - "`covered_digest` is bound to `v4:sha256:aa83916e…` per the verification brief. It was NOT recomputed over the covered files in this pass; treat it as supplied, not independently confirmed."
  regressions:
    - "HEAD `20c5ae5` fixed two of the three tampers it advertises and broke a third claim. Observed: (a) Disk monitoring -> `Verified 2026-11-17` with evidence untouched now exits 1; (b) evidence file replaced with `placeholder` now exits 1; (c) **rewriting the evidence-file link still exits 0** — the commit message says it fails. `01-01-PLAN.md:114` asserts the bare substring `'host-gate-evidence-2026-11-17'`, which also appears in the prose at `docs/api-host-decision.md:63` ('The raw command output … is retained in …'), so unlinking the markdown target changes nothing the check can see."
    - "Security review can be closed on nothing: flipping `docs/api-host-decision.md:61` to `Verified 2026-11-17` exits 0, because the required token `'independent security review'` is satisfied by the evidence file's own denial at `docs/host-gate-evidence-2026-11-17.md:142` ('No independent security review exists.'). The check accepts a sentence saying the evidence does not exist as the evidence."
    - "The `need{}` per-gate token sets at `01-01-PLAN.md:106` are free-text substring matches with no structure. Both `findmnt` and `identical` already appear in the honest evidence, so a gate that has no evidence of its own inherits Host volume's. One line of token soup (`findmnt identical systemctl backup_write_failed integrity independent security review alert is delivered`) lets **all five** gates read `Verified 2026-11-17` with every Pending ledger row erased, exit 0."
    - "Status is read as `l.split(\"|\")[-2]`, i.e. whatever sits in the second-to-last cell. Appending `| Pending |` to `docs/api-host-decision.md:60` leaves a row that a human reads as `Verified 2026-11-17` while the machine reads `Pending` — exit 0, no evidence supplied. The check is blind to any status cell that is not positioned exactly where it expects."
human_verification:
  - test: "Disk monitoring gate — set capacity thresholds for the volume holding /data, prove an alert is delivered to a person, and show backup-write error reporting without filling production storage"
    expected: "docs/api-host-decision.md:60 moves off `Partial — no delivery channel` only on a recorded delivered alert; tests/full_volume.py was not run against the real volume"
    why_human: "The record states no delivery channel reaches a person (docs/api-host-decision.md:60, docs/host-gate-evidence-2026-11-17.md:135-136) and docs/DEPLOYMENT.md:54 confirms no alerting integration exists in the repo"
  - test: "Independent security review — a reviewer other than MIA assesses the host, container network exposure, AIOS_API_KEY handling in src/auth.py, the exposure path and operational controls, and records a written decision tied to the host and image revision before any public exposure"
    expected: "docs/api-host-decision.md:61 moves off Pending only on that written decision; the API stays private until then"
    why_human: "Independence and security acceptance are human judgments; the reviewer is explicitly unassigned (docs/api-host-decision.md:61) and docs/host-gate-evidence-2026-11-17.md:142 states outright that no independent review exists"
  - test: "Drill footprint cleanup on peakybuildr — decide keep-or-remove for each row of docs/host-gate-evidence-2026-11-17.md:160-168 (guest 158 + LV fourtera/vm-158-data, containers aios-gate/aios-restore, /srv/aios-restore-isolated, /srv/bkro, the drill systemd units and scripts) and execute the removals with the commands listed there"
    expected: "Rows marked remove are gone from the host and docs/host-gate-evidence-2026-11-17.md:174-176's 'stated as present, not as removed' note is replaced by the actual outcome; evidence rows at :164 stay"
    why_human: "peakybuildr is outside the repo and the last cleanup attempt failed on Tailscale SSH re-auth (docs/host-gate-evidence-2026-11-17.md:174-176); only the operator can run `pct destroy` / `lvremove`"
---

# Phase 1: Host selection and evidence plan Verification Report

**Phase Goal:** Produce one decision record naming the selected host and operator, with explicit host evidence criteria and owners; record a blocked decision only when no eligible host exists (`.planning/ROADMAP.md:14`).
**Verified:** 2026-11-23T06:51:12Z, working tree on HEAD `20c5ae5` (dirty only in `tests/.DS_Store`, unrelated).
**Status:** human_needed
**Re-verification:** Yes — previous report (`2026-11-23T06:45:11Z`, `human_needed`, 4/5) ruled T2 still a regression. Every truth is re-decided below from scratch against the current files; nothing is carried forward.

## Goal Achievement

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | T1 (`01-01-PLAN.md:24`) — peakybuildr (100.122.194.34) selected with MIA as interim operator, dated by the 2026-11-17 check | ✓ VERIFIED | `docs/api-host-decision.md:3` names host and address; `:5` names MIA / Nur Amirah Binti Mohd Kamil (`strdst7`) as interim, delegate pending; `:7` dates it; `:13` records ICMP/8006/22; `:15` bounds the inference to management ports and denies a guest or storage for the API. No delegate invented (`:5`, `:67`). |
| 2 | T2 (`01-01-PLAN.md:25`) — record states which facts are verified at the Proxmox layer and on which date, and marks every VM/container, mount, backup, alert and review item either Verified **against retained evidence** or not yet evidenced | ✗ FAILED | T2 passes only if "against retained evidence" is a real constraint. Measured against the revised Task 2 check it is not: tamper (e) closes the security review on zero evidence, tamper (p) closes Disk monitoring with no evidence at all, and tamper (g) closes all five on one line of token soup — all three exit 0. The record's own labels are mostly honest (`docs/api-host-decision.md:38`, `:39`, `:42-47` carry a concrete not-yet-evidenced item), but at `:60` the `Partial` classification rests on the human acknowledging "alert is delivered is not met", and the plan's machine check cannot defend any of it. Truth text at `:25` is now internally consistent with `:27`, `:100`, `:104`; the *record* is not backed by a check that can hold the label. |
| 3 | T3 (`01-01-PLAN.md:26`) — one Dockerfile image, one VM or LXC, `/data`, `AIOS_OBSERVATION_DB=/data/observations.db`, `AIOS_REQUIRE_PERSISTENCE=1`, one replica; shape chosen (not executed) | ✓ VERIFIED | Shape fixed at `docs/api-host-decision.md:23-26`, LXC chosen with VM as stated fallback, open items unmade (`:26`). Matches `Dockerfile:8,14,24,26` (`python:3.10-slim`, `AIOS_REQUIRE_PERSISTENCE=1`, `EXPOSE 8000`, `uvicorn src.main:app --host 0.0.0.0 --port 8000`). Persistence claim matches `src/services/monitoring_service.py:20-23`; single-writer reason matches `src/services/monitoring_service.py:25`. "Not executed" is honestly superseded at `docs/api-host-decision.md:9` and `:63`. |
| 4 | T4 (`01-01-PLAN.md:27`) — four host gates plus a separate security review each name an owner, the check, the evidence to retain and a status of Pending / Verified / Partial; a gate reads Verified only against retained evidence; no gate closed by CI or reachability | ✗ FAILED | The structural half holds: `docs/api-host-decision.md:57-61` give five rows in the required order, each with owner, a peakybuildr/guest-specific check and an evidence-to-retain column, and reachability (`:35-37`) is never cited as gate evidence. The evidentiary half does not: "Verified only against retained evidence" is unenforceable as shipped (tampers e, g, p). The check that is supposed to guard it is inert past `01-01-PLAN.md:106`. |
| 5 | T5 (`01-01-PLAN.md:28`) — API stays private; security review precedes public exposure; no public URL, deployment or approval | ✓ VERIFIED | Security review Pending and unassigned (`docs/api-host-decision.md:61`); "deployment is still not approved" (`:3`), "Deployment is not approved" (`:9`), still not deployed (`:63`); `docs/DEPLOYMENT.md:30`'s "Production API deployment remains blocked" kept true; `:67` gates exposure on review plus gate evidence. Only listener is `127.0.0.1:18000` (`:43`, `docs/host-gate-evidence-2026-11-17.md:149`). No public URL or approval anywhere. |

**Score:** 3/5 must-haves verified (T1, T3, T5); T2 and T4 fail.

## SC1-SC3, re-decided

| SC | `.planning/ROADMAP.md` | Verdict |
| --- | --- | --- |
| SC1 | `:18` — record names the host and operator, or states exactly what is blocked | **HOLDS.** `docs/api-host-decision.md:3`, `:5`, `:7`. |
| SC2 | `:19` — separates Streamlit from FastAPI/SQLite, accounts for one-host one-replica | **HOLDS.** `docs/api-host-decision.md:19` (Streamlit is the demo, image is the API), `:23-24` (one LXC guest, one replica, with the `Lock` reason), matching `src/services/monitoring_service.py:25`. |
| SC3 | `:20` — four host gates and security review have owners, evidence requirements, and pending status until target-host checks pass; a gate leaves Pending only on a recorded target-host check, never on CI or reachability | **HOLDS as text, NOT defended in code.** Owners and evidence requirements: `docs/api-host-decision.md:57-61`. Pending-until-checked: three gates have recorded drill evidence (`docs/host-gate-evidence-2026-11-17.md:31-122`), Disk is `Partial` (`:60`), security review is `Pending` (`:61`). The second sentence — "leaves Pending only on a recorded target-host check" — has no machine check that survives the tampers below. |

## T2 — the explicit ruling

**Still a regression, in a narrower and worse-hidden form than at `84d99fb`.**

`20c5ae5` did the thing the last report asked for on the contract side and I confirm it: `01-01-PLAN.md:25` no longer says every item must be "not yet evidenced", `:100` reads "Pending until a target-host check is recorded", and `:104`'s "do not close any row" is replaced by the retained-evidence clause. Nothing was quietly deleted to dodge the question — the four `must_haves.truths` at `:24-28` are all present, `fails_when` at `:130` now describes the retained-evidence rule, T-01-03 at `:166` was rewritten, and the artifacts table at `:179` reads "each with an owned status". The old finding "the plan contradicts itself" is closed.

But the commit claims a check now *enforces* that clause, and it does not. Measured, the enforcement is absent in four distinct ways:

1. **The check is half-dead code.** `01-01-PLAN.md:106` is a 1,433-character `python3 -c '…'` one-liner whose string is closed by `</automated>` while the script continues; the continuation sits at `:107-129` as bare markup with a stray `</automated>` at `:129`. The `for l in gate:` loop that inspects status cells never runs under any tool that reads `<automated>` elements. Only the tokens checked before the break (`requires`, `len(gate)==5`) are live.
2. **The link check checks the wrong text.** `01-01-PLAN.md:114` (inside the inert region, so also moot) would assert the bare substring `host-gate-evidence-2026-11-17`; `docs/api-host-decision.md:63` contains that filename in prose independently of the markdown link, so tamper (c) survives even if the code were live.
3. **The evidence tokens are content-free.** `findmnt` and `identical` are already in the honest Host-volume evidence, and `'independent security review'` is already in the evidence file's own disclaimer at `docs/host-gate-evidence-2026-11-17.md:142`. A substring test cannot distinguish "the evidence supports this" from "the file says this doesn't exist".
4. **Status position is hardcoded to `[-2]`.** One appended cell reorders what the machine reads (tamper p).

So `20c5ae5` moved the bar from "every gate must be Pending" to "a gate may be Verified, and here is a check that is supposed to stop unevidenced closures" — and the second half is not true. A must-have that reads "Verified **against retained evidence**" is not satisfied by a checker that three trivial edits defeat.

## Tamper harness — exact observed results

Harness: `.hermes/cache/scratch/tamper.py` (this session; a fresh `copytree` of `/Users/nuramirahmohdkamil/ai-os/docs` per case, the Task 2 assertion extracted from the plan by regex and run with `cwd` at the scratch root, exit code captured).

| # | Tamper | Expected | Observed |
| --- | --- | --- | --- |
| — | honest tree (baseline) | pass | **exit 0** `gate rows ok 5` ✓ |
| a | `docs/api-host-decision.md:60` status -> `Verified 2026-11-17`, evidence untouched | fail | **exit 1** `[('disk monitoring', 'alert is delivered')]` ✓ |
| b | `docs/host-gate-evidence-2026-11-17.md` replaced with `placeholder` | fail | **exit 1** `AssertionError: [('host volume','findmnt'), …]` ✓ |
| c | markdown link target rewritten to `host-gate-evidence-2099-01-01.md` | fail | **exit 0** ✗ **SURVIVOR** |
| d | all five gate statuses -> `Verified 2026-11-17`, evidence untouched | fail | exit 1 (caught only by the Disk token) ✓ |
| e | `docs/api-host-decision.md:61` Security review -> `Verified 2026-11-17`, evidence untouched | fail | **exit 0** ✗ **SURVIVOR** |
| f | Disk -> `Verified 2026-11-17` + evidence file is one token-soup line | fail | **exit 0** ✗ **SURVIVOR** |
| g | all five -> `Verified 2026-11-17`, every ledger `\| Pending \|` erased, token-soup evidence | fail | **exit 0** ✗ **SURVIVOR** |
| h | evidence file deleted | fail | exit 1 `FileNotFoundError` ✓ |
| i | Disk -> `Not verified` | fail | exit 1 ✓ |
| j | Disk -> bare `Verified` | fail | exit 1 ✓ |
| k | Disk -> `Verified`, row's "delivery not met" caveat removed | fail | exit 1 ✓ |
| l | all five -> `Verified`, all `\| Pending \|` cells erased, soup | fail | exit 1 (`assert "| pending" in low`) ✓ |
| n | evidence file emptied (0 bytes) | fail | exit 1 ✓ |
| p | Disk -> `Verified 2026-11-17 \| Pending \|` (extra trailing cell) | fail | **exit 0** ✗ **SURVIVOR** |

**Two of the three tampers the commit message claims as fixed do fail (a, b); the third (c) does not.** Four further survivors were found, of which (e), (g) and (p) represent claiming a gate passed with no evidence. (f) is a degenerate (g).

## Does the record still read "API stays private, deployment not approved"?

Yes, unchanged by `20c5ae5` (which touched `docs/api-host-decision.md` by one line only): `:3` "the deployment is still not approved", `:9` "Deployment is not approved", `:63` "the API is still not deployed" and `docs/DEPLOYMENT.md:30` still true, `:67` "The API stays private, and public exposure needs the security review plus that gate evidence".

## Line 9's gate count vs the gate table

Consistent now. `docs/api-host-decision.md:9` says "the three executed gates below were measured … on the disposable guest 158"; the gate table at `:57`, `:58`, `:59` carries three rows reading `Verified 2026-11-17` (the `:58` status is qualified "for schedule, destination and run; notification path Pending", which matches `:9`'s "three … measured"), and `:60` is `Partial`. The previous "two executed gates" miscount is gone.

## Behavioral Spot-Checks

The three `<automated>` commands were extracted from `01-01-PLAN.md` by regex (three opens, four closes — the extra close at `:129` is orphaned) and executed verbatim with `shell=True`, `cwd=/Users/nuramirahmohdkamil/ai-os`:

| Behavior | Source | Result | Status |
| --- | --- | --- | --- |
| Task 1 wording/status assertions | `01-01-PLAN.md:106` block 0 (line 90) | `missing []`, **exit 0** | ✓ PASS |
| Task 2 gate-table assertions | `01-01-PLAN.md:106` block 1 (lines 106-129) | `missing []`, `gate rows ok 5`, **exit 0** | ✓ PASS (exit only — see tampers) |
| Task 3 source-reconciliation assertions | `01-01-PLAN.md:141` block 2 | `failed []`, **exit 0** | ✓ PASS |

All three exit 0 as claimed. The pass is not evidence the checks are adequate, per the tamper table.

## Source-Claim Verification

| Claim in `docs/api-host-decision.md` | Source | Verdict |
| --- | --- | --- |
| `python:3.10-slim`, `uvicorn src.main:app`, `0.0.0.0:8000`, `EXPOSE 8000`, `AIOS_REQUIRE_PERSISTENCE=1` (`:19`) | `Dockerfile:8,14,24,26` | TRUE |
| Relative or `:memory:` DB path raises `ValueError` under `AIOS_REQUIRE_PERSISTENCE=1` (`:25`) | `src/services/monitoring_service.py:20-24` | TRUE |
| One replica because writes serialise on a local `Lock` over one SQLite file (`:24`) | `src/services/monitoring_service.py:25-27` | TRUE |
| Security review scope: 503 on unset/short/padded/placeholder, 401 on missing/mismatched (`:61`) | `src/auth.py:6-11` | TRUE |
| Deployment remains blocked; `DEPLOYMENT.md` governs (`:63`) | `docs/DEPLOYMENT.md:30` | TRUE |
| No alerting integration in the repo (`:60`) | `docs/DEPLOYMENT.md:54` | TRUE |
| Guest 158 / storage / mount / ownership (`:38-41`, `:57`) | `docs/host-gate-evidence-2026-11-17.md:11-59` | TRUE — operator-reported host output; `:11-18` carries an image digest but no build command |
| Backup timer, off-volume destination, run, forced error (`:58`) | `docs/host-gate-evidence-2026-11-17.md:67-93` | TRUE — but the timer's `LAST` is `-` (`:70`); the run at `:79` was started through the unit (`:76`), so "completed scheduled run" is a manual trigger of the scheduled unit, not an unattended fire |
| Restore + UUID replay (`:59`) | `docs/host-gate-evidence-2026-11-17.md:98-118` | TRUE — `history identical: True` at `:108`; the `current`/`anomaly` values behind the flags are not printed |
| `history`/`current`/`anomaly` "byte-identical" (`:57`) | `docs/host-gate-evidence-2026-11-17.md:53-58` | PARTIAL — lines truncated with `…`; identity is asserted by the `_IDENTICAL=yes` flags, not shown |

## Requirements Coverage

| Requirement | Source Plan | Status |
| --- | --- | --- |
| HOST-01 | `01-01-PLAN.md:11` | ✓ SATISFIED — T1 |
| HOST-02 | `01-01-PLAN.md:12` | ✓ SATISFIED — T3; the ledger half is T2's problem, not HOST-02's (`.planning/REQUIREMENTS.md:11` asks only for runtime, mount path, topology and Streamlit's role) |
| GATE-01 | `01-01-PLAN.md:13` | ✓ SATISFIED as recording (`.planning/REQUIREMENTS.md:32` reads Partial — accurate) |
| GATE-02 | `01-01-PLAN.md:14` | ✓ SATISFIED as recording (`.planning/REQUIREMENTS.md:33` reads Pending — accurate) |

`.planning/REQUIREMENTS.md:10-16` checkboxes remain unticked while `:30-33` carries per-line status — bookkeeping inconsistency, reported not edited.

## Out-of-Deliverable Drift (reported, not edited)

- `01-01-PLAN.md:106-129` — malformed `<automated>` element (3 opens, 4 closes; inert Python at `:107-129`).
- `01-01-PLAN.md:132` (`<done>`) still says gates carry "Pending status … Nothing is marked passed", contradicting `:100`/`:104`/`:179` of the same commit.
- `01-01-PLAN.md:143` (`<human-check>`) still expects "every gate is still Pending"; `:145` (`<done>`) still says "every gate Pending".
- `01-01-SUMMARY.md:72` still credits the Task 2 check to "5 pending cells".
- `docs/api-host-decision.md:58` carries a split status on one row (schedule/destination/run verified; failure notification "still missing") while `:45` calls the same notification path Pending.
- `docs/operational-readiness-005c.md:64` still names Streamlit Community Cloud as "the named host"; the record supersedes it without annotation.

## Gaps Summary

`20c5ae5` fixed the contract half it set out to fix and did not fix the check. T1, T3 and T5 verify. T2 and T4 fail because the truth they carry — "Verified **against retained evidence**" — is guarded only by a checker that is half-inert markup and that five tampers defeat, three of them closing a gate with no evidence at all. Status stays `human_needed` for that plus three genuinely human-only items: an alert delivery channel, the independent security review, and the drill footprint still on peakybuildr.

The lazy fix, if wanted: make `<automated>` one well-formed script, parse the gate table's header row to locate the status column by name instead of `[-2]`, require `len(cells) == len(header)` for each row, and require a Verified row to cite a anchor that the evidence file heading names — not a substring that the denial sentence also satisfies. That is one script, ~10 lines, replacing the current 1,433-character line plus 14 orphaned ones.

---

_Verified: 2026-11-23T06:51:12Z_
_Verifier: Hermes subagent (gsd-verifier)_
