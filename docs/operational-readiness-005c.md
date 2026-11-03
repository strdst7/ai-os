# Task 005C — Operational Readiness Report

Status: **seven checks completed on the isolated CI runner; production deployment not approved.**
Source: PR #8, tested commit `c2142fe6e62c93acbfa38e433237e8831966adfc`.
Evidence: https://github.com/strdst7/ai-os/actions/runs/41557732710

| Check | Evidence | Result |
| --- | --- | --- |
| Container restart | The CI script wrote a Critical observation, ran `docker restart`, and read identical observability state. | Pass on CI |
| Container recreation | The CI script removed and created a container using the same named Docker volume. History and anomaly remained identical. | Pass on CI |
| SQLite backup | `sqlite3.Connection.backup` copied the live database into the mounted volume. | Pass on CI |
| Restore | A container opened the backup file and recovered the original history and anomaly. New Stable records completed recovery. | Pass on CI |
| Disk exhaustion | `PRAGMA max_page_count` reproduced `database or disk is full`. The write rolled back, the alert stayed unchanged, and the reopened database passed integrity check. | Pass in SQLite test; real full-volume behavior untested |
| SQLite integrity | `PRAGMA integrity_check` returned `ok` for live and backup databases on CI. | Pass on CI |
| Environment config | Missing and relative database paths stopped the Docker container. A file path on `/data` worked. | Pass on CI; mount ownership and host persistence remain operator checks |

The Docker image sets `AIOS_REQUIRE_PERSISTENCE=1`. Set `AIOS_OBSERVATION_DB=/data/observations.db` and mount a persistent volume at `/data`. The script uses an isolated CI volume. CI volumes do not prove a production host's mount, backup schedule, restore runbook, or disk alerts. The local Mac Docker build timed out while the data volume had under 0.5 GiB free. Docker Desktop then reported `unable to start`. No local container lifecycle result is claimed.

CI tests: Python 3.10.22, 47 passed, 97% coverage, one warning. The earlier two FastAPI `on_event` warnings closed through a lifespan hook. The remaining `StarletteDeprecationWarning` originates in the installed FastAPI TestClient importing `httpx`. It is test-client compatibility noise, not an application warning. Keep it visible. Review dependency compatibility before replacing `httpx` or changing the test client.

Production recovery policy remains **pending**. The current count rule is uncalibrated. Obtain labeled incidents, observation cadence, and an operator-approved false-clear target. Compare candidate rules on held-out incidents before modifying recovery logic. No recovery logic changed in 005C.
