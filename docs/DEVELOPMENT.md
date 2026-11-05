<!-- generated-by: gsd-doc-writer -->
# Development

## Local setup

1. Fork [AI-OS](https://github.com/strdst7/ai-os) if you plan to submit changes. Clone your fork instead of `origin` below.
2. From the repository root, create an isolated Python environment and install dependencies:

   ```bash
   git clone https://github.com/strdst7/ai-os.git
   cd ai-os
   python3.10 -m venv venv
   source venv/bin/activate
   python -m pip install -r requirements.txt
   ```

3. Run the dashboard or start the separate API. Neither needs a compile step.

   ```bash
   streamlit run app.py
   ```

   To use the API's private routes, set a local key before starting it:

   ```bash
   export AIOS_API_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
   uvicorn src.main:app --reload
   ```

   Without `AIOS_API_KEY`, `/health` works, but private routes return HTTP 503. Local API observations default to in-memory SQLite. Set `AIOS_OBSERVATION_DB` to a writable file path to retain them after restart. See [Configuration](CONFIGURATION.md). The Streamlit dashboard uses browser-session state, not the API database.

## Build commands

The repository has no `package.json`, `Makefile`, Python package build configuration, or compile step.

| Command | Description |
| --- | --- |
| `python -m pip install -r requirements.txt` | Install application and test dependencies. |
| `streamlit run app.py` | Start the session-local dashboard. |
| `uvicorn src.main:app --reload` | Start the FastAPI service with development reload. |
| `pytest tests` | Run the Python test suite from the repository root. |
| `pytest tests --cov=src` | Run tests with source coverage, as in GitHub Actions. |
| `docker build -t ai-os-lifecycle:ci .` | Build the FastAPI container image, as in CI. |
| `python3 tests/container_lifecycle.py` | Check container persistence and recovery after building that image; requires Docker. |

GitHub Actions also runs `tests/full_volume.py` only on an explicit opt-in dispatch. It fills a disposable volume. Run it only on an approved Docker host with sufficient free space. See [operational readiness](operational-readiness-005c.md).

## Code style

No linter, formatter, or corresponding configuration or command is present. Follow [CONTRIBUTING.md](../CONTRIBUTING.md): preserve service-layer separation, use typed Pydantic models, keep monitoring logic deterministic, and add tests for new logic. Run `pytest tests` before submitting changes. GitHub Actions and GitLab CI run tests, but neither configures a lint step.

## Branch conventions

The default branch is `main`. GitHub Actions tests pushes to `dev` and pull requests targeting `main`. No branch-name pattern or commit-message format is documented. CONTRIBUTING.md asks for clear commit messages.

## PR process

- Fork the repository and create a branch. Open a pull request targeting `main`.
- Describe the change with a clear commit message and keep documentation accurate.
- Include tests for new features. Avoid breaking existing APIs.
- For monitoring metrics, explain the mathematics and calibration. Keep anomaly detection explainable.
- Check `pytest tests` locally. GitHub Actions runs `pytest tests --cov=src` on pull requests to `main` and builds a container.

No pull-request template or documented approval checklist exists.
