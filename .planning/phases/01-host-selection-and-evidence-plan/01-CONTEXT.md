# Phase 1: Host selection and evidence plan — Context

## Decisions

- **D-01 — Decision-only milestone:** This is a decision-only milestone. Produce one host decision record, not an app, database, UI, or deployment.
- **D-02 — Host selected 2026-11-17:** The stateful API host is Proxmox VE `peakybuildr` (tailnet `100.122.194.34`, Linux, online). MIA (Nur Amirah Binti Mohd Kamil, `strdst7`) is decision owner and interim operating contact; a named delegate for operator duties remains pending. Reachability was checked 2026-11-17: ICMP echo, HTTPS 200 on port 8006, TCP port 22 open. Port 8006 is the Proxmox web UI and is not the API. Never infer a host from the Streamlit demo; app.py is not the API.
- **D-03 — Private until evidence and review:** Keep production API access private. Four target-host gates and a security review remain pending until actual evidence exists on `peakybuildr`.
- **D-04 — One host, one replica:** The API runs as one Docker image from the repo `Dockerfile` (`uvicorn src.main:app`) inside a single VM or LXC container on `peakybuildr`, one replica only, with a persistent `/data` volume and `AIOS_OBSERVATION_DB=/data/observations.db`. Do not treat disposable CI results as host evidence.

## Claude's Discretion

- Choose a concise decision-record format and evidence matrix within the existing documentation structure.
- Assign a named delegate for `peakybuildr` operator duties; MIA remains interim operator until then.

## Deferred Ideas

- API deployment, public exposure, new infrastructure, new UI or database, and recovery-rule calibration.

## Source

User selected “Production API readiness gates,” “Host not selected yet (plan host selection first),” and a one-phase milestone for host selection and evidence planning. See `docs/DEPLOYMENT.md` and `docs/operational-readiness-005c.md` for the baseline gates.
