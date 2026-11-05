# Phase 01 — Private FastAPI host decision

**Decision status:** Open and blocked. No candidate FastAPI host has been identified or approved; this record is not deployment or production-readiness approval. The operations team may read this non-secret record, but readership grants no API access.

| Decision | Status | Evidence or missing input | Decision owner / next action |
| --- | --- | --- | --- |
| HOST-01 / D-01: Select a private FastAPI host | Open / blocked; none identified | No candidate host or host-specific evidence. Disposable CI results and the Streamlit URL are not FastAPI host evidence. | MIA: nominate a candidate or confirm none is available. |
| D-02: Assign operations ownership | Pending named contact | MIA owns host selection, storage, backups, alerts, and restore drills; the named operating contact is missing. | MIA: name the operating contact. |
| D-03: Share the record | Record available to operations; API access not granted | Operations-team readership does not authorize use of the API. | MIA: share this record with operations; keep service access separate. |
| D-05 / D-06: Choose private access | Blocked on a candidate and a host-specific check | SSH tunnel **or** private network is acceptable; one checked path is sufficient. Both paths work for other services, but neither has been checked against a candidate FastAPI host. Other-service checks do not qualify this API. | MIA: identify the intended path and arrange one host-specific check after nomination. |
| D-07: Decide API authorization | Undecided; blocks service access | Authorized API users and access ownership are not defined. | MIA: identify the access decision owner and obtain an approved user roster before service access. |
| HOST-02 / D-04: Assess single-process SQLite and persistent-volume fit | Blocked; no topology approval | Host, process count, replica count, durable mount identity, and storage topology are unknown. `Dockerfile` starts one Uvicorn process; `AIOS_OBSERVATION_DB` must be absolute in image mode (`src/services/monitoring_service.py`). Neither code fact proves a durable host mount or that this topology fits. | MIA: provide the host and topology/mount details, then assess single-process SQLite and persistent-volume fit. |
| D-08: Keep API private | Private-only; public exposure blocked | No public-exposure approval. A separate security review is required before any public exposure. | MIA: maintain the private boundary; request security review if public exposure is proposed. |

## Evidence needed next

MIA should supply a candidate host and named operating contact; its process count, replica count, durable mount identity and storage topology; the intended private path with one host-specific check; and the authorized API users and access decision owner. Until then HOST-01 and HOST-02 remain blocked, not passed. Do not record credentials, keys, private addresses, or sensitive network identifiers here.

Phase 2 should use the four still-open deployment-environment gates in `docs/operational-readiness-005c.md`: host-volume validation, backup schedule, restore drill, and disk monitoring. That report contains the checks; none has been satisfied on a FastAPI deployment host by this decision record. A published image, disposable CI volume, Streamlit dashboard, or unrelated service's private path is not a host qualification.
