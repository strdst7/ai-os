# Roadmap: AI-OS Private API Deployment Readiness

## Overview

This milestone produces a private-host decision and runnable, non-destructive operator checks. No production-readiness claim follows without live host evidence.

## Phases

### Phase 1: Host and ownership decision
**Goal:** Name a candidate private host and owner, or record the missing inputs that block selection.
**Mode:** mvp
**Requirements:** HOST-01, HOST-02
**Success Criteria**:
1. Operator has a decision record with candidate host, owner, private access path, and missing prerequisites.
2. Operator can assess single-process SQLite and durable-volume fit against the selected topology, or sees a documented blocker.

### Phase 2: Host check plan
**Goal:** Give the operator runnable, non-destructive checks for storage, recovery, alerts, and exposure.
**Mode:** mvp
**Requirements:** DATA-01, BACK-01, BACK-02, ALRT-01, SECU-01
**Success Criteria**:
1. Operator can check the mount and database path, then compare observation state across restart and recreation.
2. Operator can inspect scheduled backups and run an isolated restore with history, anomaly, replay, and integrity checks.
3. Operator can check disk alert delivery and storage-error handling without filling production storage.
4. Operator sees an explicit private-exposure gate and an evidence table marked blocked until real host access exists.

## Coverage

| Requirement | Phase |
|-------------|-------|
| HOST-01 | Phase 1 |
| HOST-02 | Phase 1 |
| DATA-01 | Phase 2 |
| BACK-01 | Phase 2 |
| BACK-02 | Phase 2 |
| ALRT-01 | Phase 2 |
| SECU-01 | Phase 2 |

All seven v1 requirements map once. Live host checks and recovery calibration remain deferred.
