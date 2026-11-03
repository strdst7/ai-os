# External Integrations

Mapped: 2026-11-03. Source: checked local AI-OS checkout.

## Storage

- `src/services/monitoring_service.py` opens a SQLite database through `sqlite3.connect`.
- The file path comes from `AIOS_OBSERVATION_DB`. Docker mode requires an absolute path.
- The image in `Dockerfile` supplies no volume itself. Its operator must mount persistent storage.
- `tests/container_lifecycle.py` uses a disposable Docker named volume for restart, recreation, backup, and restore checks.
- `tests/full_volume.py` uses a disposable 16 MiB tmpfs Docker volume for ENOSPC checks.
- No external managed database or object-storage integration appears in the application source.

## HTTP and authentication

- `src/main.py` exposes `/health`, `/agent/evaluate`, and `/observability` via FastAPI.
- `src/auth.py` checks the `x-api-key` header against `AIOS_API_KEY` with `hmac.compare_digest`.
- `/health` is public; private routes reject missing or invalid credentials.
- API documentation endpoints are disabled in `src/main.py`.
- `app.py` calculates dashboard values locally; it does not fetch the FastAPI service.

## Hosting and automation

- `README.md` links a Streamlit Community Cloud demo, `https://ai-osdev.streamlit.app/`.
- Source code does not prove its deployed revision. An unauthenticated probe redirected to Streamlit sign-in.
- GitHub Actions in `.github/workflows/ci.yml` runs test, Docker lifecycle, and manual opt-in ENOSPC jobs.
- `.gitlab-ci.yml` declares test, container registry build, and GitHub mirror jobs. Those jobs are config, not evidence of successful operation.
- The GitHub repository has a push webhook for Streamlit, but the repo has no GitHub deployment record.

## Operational integrations missing

- No scheduled off-volume backup destination or failure notifier is wired into the application.
- No production disk-capacity metrics or alert destination is wired into this repository.
- `docs/operational-readiness-005c.md` keeps mount, backup schedule, restore drill, and disk alerts pending.
