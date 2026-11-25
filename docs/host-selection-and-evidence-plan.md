# Stateful API host decision and evidence plan

Status: **Blocked: no eligible stateful API host candidate or operator named.** This record grants no deployment or production approval.

| Decision field | Current value |
| --- | --- |
| Decision owner | User — names both the future candidate and its operator. This does not assign gate ownership. |
| Candidate | Pending — no eligible stateful API host candidate named. |
| Operator | Pending — no operator named. |
| Reopen trigger | User names both a candidate and its operator for assessment against all fixed gates. |
| Actual persistent mount | Pending — inspect the selected host before recording its mount. |
| Actual `AIOS_OBSERVATION_DB` path | Pending — inspect the selected host before recording its database path. |

## Runtime and exposure boundary

- **Proposed API runtime:** Docker/FastAPI `src.main:app` persists observations in SQLite. A future candidate must support one host and one replica for this SQLite writer.
- **Existing demo:** Streamlit Community Cloud runs `app.py` with session-local history. It does not host the Docker/FastAPI service or persist its SQLite observations.
- **Host paths:** `docs/DEPLOYMENT.md` gives `/data` and `/data/observations.db` as container setup examples. Neither is an inspected target-host mount or an actual target-host database path.
- **Exposure:** Keep the API private until target-host evidence satisfies every host gate and separate security approval exists.
- **Evidence:** `docs/operational-readiness-005c.md` records successful disposable CI checks. CI results are background only, not target-host evidence or production approval.

Sources: [deployment constraints](DEPLOYMENT.md) and [disposable-runner readiness results](operational-readiness-005c.md).

## Pending acceptance evidence

Each gate requires its own evidence from the selected target host. Gate owners remain pending until assigned.

| Gate | Owner | Required evidence | Evidence source | Status |
| --- | --- | --- | --- | --- |
| Persistent volume | Pending — gate owner not named | Inspect actual persistent mount, `AIOS_OBSERVATION_DB` database location, ownership, and permissions. Check observation history after host restart and container recreation. | Pending — target host not selected | Pending |
| Scheduled backup | Pending — gate owner not named | Record automated backup frequency, retention, off-volume destination, and failure notification. Check an actual completed scheduled backup. | Pending — target host not selected | Pending |
| Restore drill | Pending — gate owner not named | Restore a real backup into an isolated target. Check history, anomaly state, UUID replay, and `PRAGMA integrity_check`. | Pending — target host not selected | Pending |
| Disk alerts | Pending — gate owner not named | Record disk capacity thresholds. Check delivered alerts and backup-write error handling without filling production storage. | Pending — target host not selected | Pending |
| Security review | Pending — gate owner not named | Record a separate documented security review and explicit approval before public API exposure. | Pending — target host not selected | Pending |

`docs/DEPLOYMENT.md` defines these checks and the private-exposure boundary. `docs/operational-readiness-005c.md` supplies disposable CI background, not acceptance evidence for any row. No target-host checks ran for this decision.

## Flagged unverified assumptions

| Probe | Interpretation and limit |
| --- | --- |
| HOST-01 concurrency | Concerns prospective host evaluation only. It provides no named candidate or host result. |
| HOST-02 concurrency | Concerns prospective host evaluation only. It provides no operator, mount, or database path. |
| GATE-01 adjacency and ordering | Concerns the five independent gates. Neither adjacency nor ordering infers completion from CI. |
| Empty edge probe | Adds no requirement or host acceptance evidence. |
| GATE-02 unclassified | Remains an unverified label, not security approval. |

These mechanical probes imply no operational guarantees or acceptance evidence. Keep the API private. Model-service support and recovery-rule changes remain outside this decision.
