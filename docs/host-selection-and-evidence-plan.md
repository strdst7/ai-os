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
