# Stateful API host decision

**Status: Blocked.** No stateful API host or accountable operator has been selected. The decision owner must name an eligible host and assign an operator before the host can be assessed. The operator assignment is Pending. This record is an evidence plan, not approval to deploy or expose the API.

`app.py` on Streamlit Community Cloud is a session-local demo. It is not the FastAPI/SQLite host. The `Dockerfile` starts `src.main:app` in a proposed Python 3.10 container. Registry image publication is not deployment. The actual API host, runtime, persistent mount and access are unverified.

The container sets `AIOS_REQUIRE_PERSISTENCE=1`. An operator must provide a persistent `/data` mount and `AIOS_OBSERVATION_DB=/data/observations.db`. The SQLite writer requires one host and one replica. The API remains private. A separate security review is pending before any public exposure.

## Target-host acceptance evidence

Each check remains Pending. The eventual named operator owns the four host checks. The decision owner must assign that role to a person or team. A separate security reviewer must be assigned for the final row.

| Gate | Owner role | Target-host check | Evidence to retain | Status |
| --- | --- | --- | --- | --- |
| Host volume | API host operator, assignment pending | Inspect actual persistent mount, database path, ownership and permissions. Write an observation, then check identical history and anomaly after restart and container recreation on the same volume. | Host and mount inventory, permission record, restart/recreation commands and before/after observation results. | Pending |
| Backup schedule | API host operator, assignment pending | Define automated frequency and retention, off-volume destination and failure notification. Check an actual scheduled backup, not only an on-demand copy. | Scheduler config, destination and retention policy, completed scheduled-run log and failure-notification result. | Pending |
| Restore drill | API host operator, assignment pending | Restore a real backup into an isolated target. Check history, anomaly state, UUID replay and `PRAGMA integrity_check` without overwriting the only copy. | Backup identifier, isolated restore steps and recorded checks. | Pending |
| Disk monitoring | API host operator, assignment pending | Set capacity thresholds. Check alert delivery and backup-write error reporting without filling production storage. | Threshold and routing config, delivered alert and safe backup-write error evidence. | Pending |
| Security review | Independent security reviewer, assignment pending | Review the identified host, API authentication, exposure path and operational controls. Record written approval before any public exposure. | Reviewer decision and approval record tied to the target host and revision. | Pending |

The [deployment guide](DEPLOYMENT.md) and [operational-readiness report](operational-readiness-005c.md) describe the existing runtime and CI checks. CI lifecycle and full-volume simulations used disposable runners. They are not target-host evidence. Proposed checks and this document are not completed evidence. Do not run `tests/full_volume.py` on local or production storage.

Next, the decision owner must name an eligible host and operator. Gather its host artifacts and separate security approval before making another production decision. Until then, production approval and public API access stay blocked. The recovery rule also remains unchanged pending labeled incidents and an operator-approved false-clear target.
