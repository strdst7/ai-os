---
status: partial
phase: 01-host-selection-and-evidence-plan
source:
  - 01-01-SUMMARY.md
started: 2026-11-07T06:15:35+08:00
updated: 2026-11-16T21:03:00.989Z
---

## Current Test

[testing complete]

## Tests

### 1. Selected-host decision reads as a decision, not an approval
expected: Read docs/api-host-decision.md. It names Proxmox VE peakybuildr (100.122.194.34) and MIA as operator, states the deployment is not approved, keeps the API private, and marks every host gate Pending. Nothing in it reads as host readiness or permission to deploy.
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
result: blocked
blocked_by: prior-phase
reason: No guest exists on peakybuildr yet; nothing can be measured.

### 4. Backup, restore and disk-alert gates measured on a real guest
expected: A scheduled off-volume backup completes and is logged, an isolated restore of that backup passes history, anomaly, UUID replay and PRAGMA integrity_check, and a disk threshold alert is delivered with backup-write error reporting.
result: blocked
blocked_by: prior-phase
reason: Depends on the guest and the host volume from test 3.

### 5. Independent security review before any public exposure
expected: A named independent reviewer signs a host and image-revision-specific decision; until then the API stays private.
result: blocked
blocked_by: third-party
reason: No reviewer assigned.

### 6. Verification report matches the shipped document
expected: gsd-tools query verification.status for the phase reports human_needed (not stale), and the report's 8/8 must-haves still describe docs/api-host-decision.md as shipped.
result: pass
source: automated
reported: "verification.status = human_needed after the fingerprint restamp; digest computed over the shipped plan, summary and document"

### 7. Independent read of the record's own claims
expected: A reader who is not the author checks docs/api-host-decision.md, the plan and the verification report, and finds no unverifiable claim presented as established, and no automated check weakened to pass.
result: pass
reported: "pass"
source: human

## Summary

total: 7
passed: 3
issues: 0
pending: 0
skipped: 0
blocked: 4

## Gaps

None caused by the phase output. Tests 2 to 5 are prerequisite gates on a host that has no guest yet. The cold-start check is deferred to the first real start, not a phase defect.

## Deferred Follow-Ups

- test: 8
  idea: "Cold-start smoke test does not apply to a documentation-only phase; run it once the API image is first started on a peakybuildr guest."
  deferred_at: 2026-11-17
