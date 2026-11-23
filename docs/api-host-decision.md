# Stateful API host decision

Status: Selected — host `peakybuildr`, a Linux Proxmox VE host on the tailnet at 100.122.194.34. Two host gates were measured on 2026-11-17; the deployment is still not approved.

Decision owner and operator: MIA / Nur Amirah Binti Mohd Kamil (GitHub `strdst7`), interim operating contact until a named delegate is assigned.

Decision date: 2026-11-17.

This record selects the host and fixes the runtime shape. Phase 1 built no image on `peakybuildr` and created no guest; the two executed gates below were measured afterwards on the disposable guest 158. Deployment is not approved.

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

| Check | Verified on 2026-11-17 | Not verified | Status |
| --- | --- | --- | --- |
| Not verified | — | The rows below are the outstanding checks; this row labels them. | — |
| Node reachability | ICMP echo replies from 100.122.194.34 | — | Verified |
| Proxmox web UI | HTTPS `HTTP 200` on port 8006 | — | Verified |
| SSH | TCP port 22 accepting connections | — | Verified |
| Guest | Guest 157 `aios` (LXC, Debian 13, Docker) existing and running; guest 158 `aios-drill` (LXC, Debian 13, unprivileged) created for the gate drill | No guest is sized or appointed for the API. Evidence: `pct config` for the chosen guest. | Pending |
| Storage | `/fourtera/vm-158-data`, ext4 on the 3.6 TB `fourtera` volume group; 10 GB | Storage for the API guest itself. Evidence: storage configuration and a capacity listing. | Pending |
| Mount | `/data` bound from `/fourtera/aios-158-data`; recorded as `mp0` in the guest config and present after restart | — | Verified |
| Ownership | Host `100000:100000 755`, guest `root:root 755 /data`, database file `root:root 644` | — | Verified |
| Start policy | Container recreated on the same volume with an unchanged database path | Restart policy and the compose or `docker run` invocation adopted for the API. Evidence: the invocation and the restart policy in effect. | Pending |
| Network | Container bound `127.0.0.1:18000` inside the drill guest only | The tailnet address the API would answer on. Evidence: the guest's tailnet address and a probe from another tailnet node. | Pending |
| API key | `AIOS_API_KEY` supplied to the drill container without printing its value; absent, the API answers `503 API key not configured` | Provisioning of the key on the API guest. | Pending |
| Backup | Scheduled timer with off-volume destination, completed run logged, forced write-failure logged | The failure-notification path (see Disk monitoring). | Pending |
| Alerting | Threshold evaluated and an alert line written on a forced threshold | Delivery to a person. Evidence: see the Disk monitoring gate. | Pending |
| Security | — | Any security review. Evidence: see the Security review row. | Pending |

Every Not verified item is Pending.

## Target-host acceptance gates

The four host gates are measured on the drill guest 158; the named delegate is still pending. The security review is not a host gate and cannot be closed by host operations work.

| Gate | Owner | Target-host check on `peakybuildr` | Evidence to retain | Status |
| --- | --- | --- | --- | --- |
| Host volume | MIA, interim operator; named delegate pending | Inspect the guest's persistent volume and the `/data` mount source, the database path `/data/observations.db`, ownership and permissions. Write one observation, restart the container, then recreate it on the same volume; identical history and anomaly state is the pass condition. | Mount source `/dev/mapper/fourtera-vm--158--data` (ext4, rw) on `/fourtera/aios-158-data`, bound to `/data`; host `100000:100000 755`, guest `root:root 755`, database `644`. Restart and recreate on the same volume both returned an identical `history`, `current` and `anomaly`, with `PRAGMA integrity_check` = `ok`. | Verified 2026-11-17 |
| Backup schedule | MIA, interim operator; named delegate pending | Define automated frequency and retention, an off-volume destination that is not the storage the database lives on, and a failure notification path. Pass condition is a completed scheduled run in the log, not an on-demand copy. | systemd timer `aios-backup.timer`, daily 02:30, 7-day retention; destination `/srv/aios-backup` on `pve-root`, a different device from the `fourtera` volume holding `/data`; a completed scheduled run logged (`OK backup=… bytes=28672`); a forced write failure logged `ERROR backup_write_failed` and exited 1. Failure notification path still missing. | Verified 2026-11-17 for schedule, destination and run; notification path Pending |
| Restore drill | MIA, interim operator; named delegate pending | Restore a real backup into an isolated target, then check history, anomaly state, UUID replay and `PRAGMA integrity_check` without overwriting the only copy. | Backup restored into a separate directory and a second container; `history identical: True`, `current identical: True`, `anomaly identical: True`, `integrity ok`; live source unchanged at 9 rows and `integrity ok`. A restored copy must be owned by uid 100000, or the container fails with `attempt to write a readonly database`. | Verified 2026-11-17 |
| Disk monitoring | MIA, interim operator; named delegate pending | Set capacity thresholds for the volume holding `/data`, prove an alert is delivered, and show backup-write error reporting. Do not fill production storage; `tests/full_volume.py` must not run on the real volume. | Threshold script at 80% on `/fourtera` logging `ok disk_use=21% threshold=80%`; an alert line written when the threshold was forced; backup-write error reporting shown. No delivery channel reaches a person yet, so "alert is delivered" is not met. | Partial — no delivery channel |
| Security review | Independent reviewer, assignment pending | Review the named host, the container network exposure, `AIOS_API_KEY` handling in `src/auth.py` (503 when the server key is unset, short, whitespace-padded or a placeholder; 401 when the client key is missing or mismatched), the exposure path and operational controls. | Written decision tied to the host and image revision. | Pending |

These gates were measured on guest 158, a disposable LXC container created for the drill. They prove the volume, backup and restore contract holds on this host and this storage. They do not appoint guest 158 as the API guest, and the API is still not deployed. The [deployment guide](DEPLOYMENT.md) remains the runtime contract that governs the container, and its statement that production API deployment remains blocked is still true. CI lifecycle and full-volume results in the [operational-readiness report](operational-readiness-005c.md) came from disposable runners, including a tmpfs full-volume simulation; the drill above adds real target-host mount and storage evidence, and no target-host alert delivery.

## Next decision

MIA assigns a named operating contact (delegate) for `peakybuildr`. Three gates are verified on the drill guest; the disk-monitoring gate needs an alert delivery channel before it can pass. A separate production decision needs the remaining gates plus the security review. The API stays private, and public exposure needs the security review plus that gate evidence.
