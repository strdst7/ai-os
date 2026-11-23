---
status: partial
phase: 01-host-selection-and-evidence-plan
source:
  - 01-01-SUMMARY.md
  - 01-VERIFICATION.md
started: 2026-11-07T06:15:35+08:00
updated: 2026-11-23T03:20:00.000Z
---

## Current Test

[testing complete]

## Tests

### 1. Selected-host decision reads as a decision, not an approval
expected: Read docs/api-host-decision.md. It names Proxmox VE peakybuildr (100.122.194.34) and MIA as operator, states the deployment is not approved, keeps the API private, and does not read as host readiness or permission to deploy. Gates may be Verified in the ledger, but the record must still say the API stays private and deployment is not approved.
result: pass
reported: "pass"
source: human

### 2. Named delegate for peakybuildr operator duties
expected: A named person other than MIA is recorded as the operating contact for the guest on peakybuildr; MIA's interim label is then removed or dated.
result: blocked
blocked_by: third-party
reason: No delegate exists yet. Assigning one is an organisational act; inventing a name is the defect this phase exists to prevent.

### 3. Host volume gate measured on a real guest
expected: On a guest that actually exists on peakybuildr, the /data mount source, database path, ownership and permissions are recorded, and a write survives a container restart and recreation with identical history and anomaly state.
result: pass
reported: "mount /dev/mapper/fourtera-vm--158--data ext4 rw on /fourtera/aios-158-data bound to /data; host 100000:100000 755, guest root:root 755, db 644; restart and recreate both returned identical history, current and anomaly; integrity ok. Recorded in docs/host-gate-evidence-2026-11-17.md"
source: automated
evidence: docs/host-gate-evidence-2026-11-17.md

### 4. Backup and restore gates measured on a real guest
expected: A scheduled off-volume backup completes and is logged, an isolated restore of that backup passes history, anomaly, UUID replay and PRAGMA integrity_check without overwriting the only copy.
result: pass
reported: "aios-backup.timer daily 02:30, retention 7, destination /srv/aios-backup on pve-root (different device from /data); scheduled run logged; forced write failure logged and exited 1; isolated restore returned history/current/anomaly identical and integrity ok, live source unchanged"
source: automated
evidence: docs/host-gate-evidence-2026-11-17.md

### 5. Disk threshold alert delivered to a person
expected: A capacity threshold on the volume holding /data fires and the alert is delivered through a channel a person actually receives; until then the gate stays Partial.
result: blocked
blocked_by: third-party
reason: The threshold and error path are measured, but no delivery channel exists — an alert writes to a local log and reaches nobody. Recorded as Partial at docs/api-host-decision.md gate row Disk monitoring.

### 6. Independent security review before any public exposure
expected: A named independent reviewer signs a host and image-revision-specific decision; until then the API stays private.
result: blocked
blocked_by: third-party
reason: No reviewer assigned.

### 7. Verification report matches the shipped document
expected: gsd-tools query verification.status for the phase reports human_needed (not stale), and the report's must-have score describes docs/api-host-decision.md as shipped.
result: pass
source: automated
reported: "verification.status = human_needed, not stale; 4/5 must-haves verified at digest 90dd3448 computed over the five covered files the report declares"

### 8. Independent read of the record's own claims
expected: A reader who is not the author checks docs/api-host-decision.md, the plan, the verification report and the retained evidence, and finds no unverifiable claim presented as established, and no automated check weakened to pass.
result: pass
reported: "pass after two adversarial verification passes; five reported defects fixed, two host-hygiene findings kept open rather than absorbed"
source: human

## Summary

total: 8
passed: 5
issues: 0
pending: 0
skipped: 0
blocked: 3

## Gaps

No gap caused by the phase output. Tests 2, 5 and 6 need a third party: a named delegate, an alert delivery channel, and an independent reviewer. Test 4's earlier blocker ("depends on test 3") is resolved because test 3 now passes on real evidence.

## Deferred Follow-Ups

- test: 9
  idea: "Cold-start smoke test does not apply to a documentation-only phase; run it once the API image is first started as the API guest, not the drill guest."
  deferred_at: 2026-11-17
