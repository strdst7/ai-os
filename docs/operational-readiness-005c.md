# Task 005C — Operational Readiness Report

Status: **all seven checks passed on disposable CI runners. Production deployment not approved.**
Source: PR #8; source changes at `c2142fe6e62c93acbfa38e433237e8831966adfc`.
Evidence: https://github.com/strdst7/ai-os/actions/runs/41558016110

| Check | Evidence | Result |
| --- | --- | --- |
| Container restart | The CI script wrote a Critical observation, ran `docker restart`, and read identical observability state. | Pass on CI |
| Container recreation | The CI script removed and created a container using the same named Docker volume. History and anomaly remained identical. | Pass on CI |
| SQLite backup | `sqlite3.Connection.backup` copied the live database into the mounted volume. | Pass on CI |
| Restore | A container opened the backup file and recovered the original history and anomaly. New Stable records completed recovery. | Pass on CI |
| Disk exhaustion | `PRAGMA max_page_count` reproduced a full database. Task 006 filled an isolated 16 MiB tmpfs. The API returned HTTP 500 without recording the failed observation. Backup also failed. Integrity and retry passed after freeing space. | Simulation and disposable full-volume check passed; production host pending |
| SQLite integrity | `PRAGMA integrity_check` returned `ok` for live and backup databases on CI. | Pass on CI |
| Environment config | Missing and relative database paths stopped the Docker container. A file path on `/data` worked. | Pass on CI; mount ownership and host persistence remain operator checks |

The Docker image sets `AIOS_REQUIRE_PERSISTENCE=1`. Set `AIOS_OBSERVATION_DB=/data/observations.db` and mount a persistent volume at `/data`. The script uses an isolated CI volume. CI volumes do not prove a production host's mount, backup schedule, restore runbook, or disk alerts. An earlier Mac build timed out. A later local build succeeded, then disk space fell to 263 MiB. No local container lifecycle result is claimed.

CI tests: Python 3.10.22, 47 passed, 97% coverage, one warning. The earlier two FastAPI `on_event` warnings closed through a lifespan hook. The remaining `StarletteDeprecationWarning` originates in the installed FastAPI TestClient importing `httpx`. It is test-client compatibility noise, not an application warning. Keep it visible. Review dependency compatibility before replacing `httpx` or changing the test client.

Production recovery policy remains **pending**. The current count rule is uncalibrated. Obtain labeled incidents, observation cadence, and an operator-approved false-clear target. Compare candidate rules on held-out incidents before modifying recovery logic. No recovery logic changed in 005C.

## Task 006 — disposable full-volume result

The [opt-in run](https://github.com/strdst7/ai-os/actions/runs/41561506594) checked commit `696d598a6b51a29db72a6e4bd9d13afda2cd0501`. The GitHub-hosted `ubuntu-latest` runner reported Linux `7.0.0-1017-azure`, x86_64. Docker client and server reported `29.4.2`. The runner reported 93,980,954,624 free bytes before build. `df` showed 88 GiB available on `/dev/root`. The script required at least 4 GiB free and explicit `AIOS_RUN_ENOSPC_TEST=1`.

The script created a unique Docker local-driver volume backed by tmpfs. Inside the container, `/data` reported `tmpfs` and exactly 16,777,216 bytes capacity. The API port bound only to `127.0.0.1`. This volume held test observations only. No production data was mounted. After filling it, available blocks reached zero.

```text
Mount: tmpfs; capacity: 16777216 bytes
Volume free blocks after fill: 0
Observation write HTTP status: 500
Observation write HTTP body: Internal Server Error
History and anomaly unchanged after failed write
Backup on full volume: backup_failed: database or disk is full
Removed filler; volume space restored
Integrity after ENOSPC: ok; observation rows: 1
Retry: HTTP success; history: 2; anomaly: true
Live integrity after retry: ok
Backup after space restoration: ok; integrity: ok
ENOSPC write and backup failed; API rejected write; integrity and recovery passed
Application container exit code: 0
Cleanup exit codes: stop=0, container=0, volume=0
```

The failed observation produced no success response. History and anomaly state stayed unchanged. Its retry succeeded after freeing space. The original row remained readable. SQLite reported `ok` for the live database and backup. The API returned a generic HTTP 500, not a structured storage error. Operators still need a disk alert.

The workflow also injected an error after mounting, before filling. That test process exited `1` as intended. Its application container exited `0` after a normal stop. Cleanup exit codes were `stop=0`, `container=0`, and `volume=0`. The workflow found no matching test container or volume afterward. The real ENOSPC run exited `0` with the same cleanup codes. No unexpected filesystem or transaction behavior appeared.

Only approved disposable Docker hosts can run this check. The script requires `AIOS_RUN_ENOSPC_TEST=1` and at least 4 GiB free on `/`.

```sh
docker build -t ai-os-lifecycle:ci .
AIOS_RUN_ENOSPC_TEST=1 python3 tests/full_volume.py
```

Do not run it on this Mac without enough headroom. At the latest check, the Mac had 710 MiB free. No Docker test or cleanup ran at that level.

This disposable-runner result does not establish production readiness. Production-host mount, backup schedule, disk alerts, and restore drill need separate host checks. The production recovery rule still needs labeled incidents, cadence, and a false-clear target.

## Deployment-environment gate

The deployment target, operator, and volume layout are not identified. Keep the service private and PR #8 open. Record the following on the actual target before approving deployment:

| Gate | Required evidence | Status |
| --- | --- | --- |
| Topology | One host and one replica, or a decision to replace SQLite with a shared transactional store. | Pending |
| Volume | Inspect the real mount, ownership, permissions, and `AIOS_OBSERVATION_DB` path. Restart and recreate against the same volume. | Pending |
| Backup | Set a schedule, retention, and storage outside the database volume. Record a successful online backup. | Pending |
| Restore | Restore into an isolated target. Check history, anomaly state, UUID replay, and `PRAGMA integrity_check`. | Pending |
| Capacity | Check free space, disk alerts, backup-write errors, and response handling on the deployment filesystem. Never fill a production data volume. | Pending |
| Exposure | Keep the API private until a security review checks access, secrets, and network binding. | Pending |

Do not reuse the disposable CI result as evidence for these target-specific gates. Keep the two-Stable recovery rule unchanged until labeled incidents support a policy.
