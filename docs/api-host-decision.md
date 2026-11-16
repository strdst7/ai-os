# Stateful API host decision

Status: Selected — host `peakybuildr`, a Linux Proxmox VE host on the tailnet at 100.122.194.34.

Decision owner and operator: MIA / Nur Amirah Binti Mohd Kamil (GitHub `strdst7`), interim operating contact until a named delegate is assigned.

Decision date: 2026-11-17.

This is a decision-only milestone. No container was built or run, no VM, LXC container, ZFS dataset or mount was created, and nothing was deployed to `peakybuildr`. The record fixes the host and the runtime shape; everything else is open.

## The host check, and what it does not prove

Checked on 2026-11-17: ICMP echo replies from 100.122.194.34, HTTPS `HTTP 200` on port 8006, and TCP 22 accepting connections.

That check proves the Proxmox node answers on its management ports. It does not prove that the API runs, that a guest exists, or that storage is provisioned. Port 8006 is the Proxmox web UI, not the API.

## What runs there, and what does not

`app.py` on Streamlit Community Cloud is the session-local demo. It is not the FastAPI/SQLite host. The API is the image built from the repository `Dockerfile`: `python:3.10-slim`, `uvicorn src.main:app` on `0.0.0.0:8000` (the image `CMD`), `EXPOSE 8000`, and `AIOS_REQUIRE_PERSISTENCE=1` set in `ENV`. The image is unchanged by this phase.

## Chosen runtime shape

- One Docker image, built from the repository `Dockerfile`, running as a single LXC container guest on `peakybuildr`. LXC is chosen over a VM for lower overhead on a homelab node; a VM would give a kernel boundary and a Docker daemon inside the guest, and stays the fallback if the container's storage or networking proves awkward. The guest type is a reasoned choice, not an executed one.
- One replica only. `src/services/monitoring_service.py` serialises writes with a local `Lock` around a single SQLite file, so a second replica would split the writer.
- A persistent volume provided by the operator, mounted at `/data`, with `AIOS_OBSERVATION_DB=/data/observations.db`. The image sets `AIOS_REQUIRE_PERSISTENCE=1`; a relative or `:memory:` database path raises `ValueError` at startup, so a wrong mount path fails fast instead of silently writing to memory.
- Open items, deliberately unmade: guest ID, storage backend, CPU and memory, the tailnet address the API answers on, who runs the container, and the container runtime user.

## What is verified, and what is not

A green management-port check is not host evidence, so the two live in separate columns.

| Check | Verified on 2026-11-17 | Not verified |
| --- | --- | --- |
| Node reachability | ICMP echo replies from 100.122.194.34 | — |
| Proxmox web UI | HTTPS `HTTP 200` on port 8006 | — |
| SSH | TCP port 22 accepting connections | — |
| Guest | — | Guest existence and its type/ID. Evidence: `pct list` or `qm list` output for the guest. |
| Storage | — | Guest storage backend and free capacity. Evidence: storage configuration and a capacity listing. |
| Mount | — | The `/data` mount and the database path inside it. Evidence: `pct exec … mount` and `ls -l /data/observations.db`. |
| Ownership | — | Directory ownership and permissions. Evidence: `stat` output for `/data` and the database file. |
| Start policy | — | Container start command and restart policy. Evidence: the compose or `docker run` invocation and the restart policy in effect. |
| Network | — | The tailnet address the API would answer on. Evidence: the guest's tailnet address and a probe from another tailnet node. |
| API key | — | `AIOS_API_KEY` provisioning. Evidence: the variable set in the guest without printing its value. |
| Backup | — | Backup target and schedule. Evidence: see the Backup schedule gate. |
| Alerting | — | Alerting. Evidence: see the Disk monitoring gate. |
| Security | — | Any security review. Evidence: see the Security review row. |

Every Not verified item is Pending.

## Target-host acceptance gates

Each row is Pending. MIA is the interim operator for the four host gates and must assign a named operating contact (delegate) for `peakybuildr`. The security review is not a host gate and cannot be closed by host operations work.

| Gate | Owner | Target-host check on `peakybuildr` | Evidence to retain | Status |
| --- | --- | --- | --- | --- |
| Host volume | MIA, interim operator; named delegate pending | Inspect the guest's persistent volume and the `/data` mount source (ZFS dataset, LVM volume or directory-backed LXC path — open until recorded), the database path `/data/observations.db`, ownership and permissions. Write one observation, restart the container, then recreate it on the same volume; identical history and anomaly state is the pass condition. | Storage inventory, mount and permission record, restart and recreate commands with before/after `/observability` output. | Pending |
| Backup schedule | MIA, interim operator; named delegate pending | Define automated frequency and retention, an off-volume destination that is not the storage the database lives on, and a failure notification path. Pass condition is a completed scheduled run in the log, not an on-demand copy. | Scheduler config, destination and retention policy, completed scheduled-run log, failure-notification result. | Pending |
| Restore drill | MIA, interim operator; named delegate pending | Restore a real backup into an isolated target, then check history, anomaly state, UUID replay and `PRAGMA integrity_check` without overwriting the only copy. | Backup identifier, isolated restore steps, recorded checks. | Pending |
| Disk monitoring | MIA, interim operator; named delegate pending | Set capacity thresholds for the volume holding `/data`, prove an alert is delivered, and show backup-write error reporting. Do not fill production storage; `tests/full_volume.py` must not run on the real volume. | Threshold and routing config, delivered alert, safe backup-write error evidence. | Pending |

| Security review | Independent reviewer, assignment pending | Review the named host, the container network exposure, `AIOS_API_KEY` handling in `src/auth.py` (503 when the server key is unset, short, whitespace-padded or a placeholder; 401 when the client key is missing or mismatched), the exposure path and operational controls. | Written decision tied to the host and image revision. | Pending |

The [deployment guide](DEPLOYMENT.md) remains the runtime contract that governs the container, and its statement that production API deployment remains blocked is still true — deployment itself is not approved; this record selects a host and nothing more. CI lifecycle and full-volume results in the [operational-readiness report](operational-readiness-005c.md) came from disposable runners, including a tmpfs full-volume simulation, and provide no target-host mount or alert evidence. This phase produced no gate evidence at all — the Proxmox reachability check above is infrastructure liveness, not a host gate.

## Next decision

MIA assigns a named operating contact (delegate) for `peakybuildr`, and the four host gates are collected on the real guest before any separate production decision. The API stays private, and public exposure needs the security review plus the gate evidence.
