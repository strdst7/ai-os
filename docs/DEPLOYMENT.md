<!-- generated-by: gsd-doc-writer -->
# Deployment

AI-OS has two separate runtimes. `app.py` is a Streamlit demo with session-local history. The `Dockerfile` starts `src.main:app`, a FastAPI service with SQLite observations. Neither the container lifecycle checks nor the demo establish production approval for the API. See [operational readiness](operational-readiness-005c.md).

## Deployment targets

- **Streamlit demo:** `app.py` is the dashboard entrypoint. `README.md` names Streamlit Community Cloud at `https://ai-osdev.streamlit.app/`. An unauthenticated probe redirected to sign-in; the live revision and behavior remain unconfirmed. <!-- VERIFY: Confirm the Streamlit project's deployed source revision, access, and live behavior. --> The demo does not use the API's SQLite database or API key.
- **Docker/FastAPI:** `Dockerfile` builds a Python 3.10 image and starts `uvicorn src.main:app --host 0.0.0.0 --port 8000`. `AIOS_REQUIRE_PERSISTENCE=1` requires an absolute `AIOS_OBSERVATION_DB` file path. The operator must supply a persistent mount; the image does not create one.
- **GitLab container registry:** `.gitlab-ci.yml` builds and pushes commit-SHA and `latest` tags on the default branch. This publishes images, not a running service. <!-- VERIFY: Confirm the registry, deployment host, image promotion, and release operator before deployment. -->

No Docker Compose, Kubernetes, or platform deployment manifest exists in the repository. Do not treat the Streamlit dashboard as a host for the FastAPI service.

## Build pipeline

1. GitHub Actions `.github/workflows/ci.yml` tests on pushes to `dev` and pull requests targeting `main`: install `requirements.txt`, install `pytest pytest-cov`, then run `pytest tests --cov=src` with `PYTHONPATH=.`.
2. Its container job runs `docker build -t ai-os-lifecycle:ci .` and `python3 tests/container_lifecycle.py`. An optional manual job runs `tests/full_volume.py` on disposable storage only.
3. GitLab `.gitlab-ci.yml` tests branch and merge-request pipelines with `pytest tests --cov=src --cov-report=term --cov-report=xml --junitxml=report.xml`.
4. On the GitLab default branch, its build job runs `docker build -t "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA" -t "$CI_REGISTRY_IMAGE:latest" .`, then pushes both tags. A separate job mirrors repository refs to GitHub. Neither CI file deploys a container or promotes a Streamlit release.

A local Docker build for evaluation uses `docker build -t ai-os-image .`. This does not satisfy the target-host acceptance gates.

## Environment setup

- Set `AIOS_API_KEY` to a unique secret of at least 32 characters. Supply it as `x-api-key` to private API routes. A missing or invalid server key returns HTTP 503 for those routes; `/health` remains public.
- Set `AIOS_OBSERVATION_DB=/data/observations.db` and mount persistent storage at `/data`. The container rejects missing, relative, and in-memory paths. Check host ownership, permissions, and persistence before use. <!-- VERIFY: Confirm the actual host mount, ownership, permissions, and database path. -->
- Keep one host and one replica for this SQLite writer. The source uses a local lock, not a shared multi-host transaction system.
- `PYTHONPATH=/app`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUNBUFFERED=1`, and `AIOS_REQUIRE_PERSISTENCE=1` come from `Dockerfile`. See [configuration](CONFIGURATION.md) for defaults and local API behavior.

Production API deployment remains blocked. Complete the four host checks below and a security review before public exposure. <!-- VERIFY: Record host-specific acceptance evidence and security approval before enabling public API access. -->

| Open host gate | Evidence required |
| --- | --- |
| Host volume | Inspect the mount and database path; check history after restart and container recreation. |
| Backup schedule | Check frequency, retention, off-volume destination, failure notification, and an actual scheduled backup. |
| Restore drill | Restore a backup into an isolated target; check history, anomaly, UUID replay, and `PRAGMA integrity_check`. |
| Disk monitoring | Check capacity thresholds, alert delivery, and backup-write errors without filling production storage. |

## Rollback procedure

No automated rollback exists in the repository. A previous image tag alone does not revert SQLite state.

1. Stop writes and identify the last approved image tag and compatible database backup. <!-- VERIFY: Confirm the actual release tag, backup, and schema compatibility on the target host. -->
2. Preserve the current database and mount. Restore a verified backup to an isolated target if data recovery is needed; do not overwrite the only copy.
3. Start the selected image against the intended persistent database on one host and one replica. <!-- VERIFY: Confirm the host's stop, start, and traffic-switch commands before an incident. -->
4. Check `/health`, authenticated `/observability`, history, anomaly state, UUID replay, and SQLite integrity. Reopen traffic only after operator review.

`tests/container_lifecycle.py` exercises restart, recreation, backup, and restore on a disposable CI volume. It is not a production rollback procedure.

## Monitoring

- `GET /health` returns `{"status":"AI-OS running"}` without authentication. It does not check disk capacity, backup freshness, or SQLite integrity.
- Authenticated `GET /observability` returns recent history and anomaly state after evaluations. `src/main.py` also runs periodic read-only checks; these do not create observations.
- The image enables unbuffered Python output, but the repository has no alerting integration, backup scheduler, external metrics exporter, or monitoring dashboard configuration. <!-- VERIFY: Confirm host log collection, disk alerts, backup-failure notifications, and incident ownership. -->
- Disposable CI results, including a full-volume failure check, do not validate target-host monitoring. Keep the current two-Stable recovery rule unchanged until labeled incidents, observation cadence, and a false-clear target support calibration.
