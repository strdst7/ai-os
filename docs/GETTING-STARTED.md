<!-- generated-by: gsd-doc-writer -->
# Getting started

AI-OS offers a Streamlit research dashboard for exploring deployment stability. Its FastAPI service is a separate, stateful entrypoint and is not production-approved.

## Prerequisites

- Python `>=3.10` with `venv` and `pip`. The Docker image uses Python 3.10.
- Git to clone the repository.
- No Docker installation is needed for the local dashboard.

## Installation steps

1. Clone the repository and enter it:

   ```bash
   git clone https://github.com/strdst7/ai-os.git
   cd ai-os
   ```

2. Create and activate a Python 3.10 virtual environment:

   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the project dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

`requirements.txt` selects Streamlit `>=1.65,<1.66` on Python 3.10 and `>=1.66.1` on Python 3.11 or newer.

## First run

Run the local dashboard from the repository root:

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit. Change the sidebar telemetry sliders to see the ADSI, stability tier, anomaly flag, and trend. The dashboard stores its history in `st.session_state`, not in the FastAPI service's SQLite database.

To check the separate local API, set a strong key and start Uvicorn in another terminal:

```bash
export AIOS_API_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
uvicorn src.main:app --reload
```

Then request its public health endpoint:

```bash
curl http://127.0.0.1:8000/health
```

The health response is `{"status":"AI-OS running"}`. Private routes require the same key in the `x-api-key` header. Without `AIOS_OBSERVATION_DB`, local API observations use an in-memory SQLite database and disappear on restart. Do not expose this research service publicly; see [operational readiness](operational-readiness-005c.md).

## Common setup issues

- `python3.10: command not found`: Install Python 3.10 or use a supported newer Python version. Create the virtual environment with that interpreter.
- `streamlit: command not found` or missing imports: Activate `.venv` and install `requirements.txt` there.
- API requests to `/agent/evaluate` or `/observability` return HTTP 503: Set `AIOS_API_KEY` to at least 32 characters before starting Uvicorn. `/health` does not need a key.
- API startup fails with `AIOS_OBSERVATION_DB must be an absolute persistent file path`: Docker sets `AIOS_REQUIRE_PERSISTENCE=1`. Supply a writable absolute SQLite path on a mounted persistent volume. See [configuration](CONFIGURATION.md).
- Local port already in use: Stop the other service or choose a free port with `uvicorn src.main:app --port 8001`. The dashboard and API run as separate processes.

## Next steps

- [Configuration](CONFIGURATION.md) covers API keys, SQLite persistence, and defaults.
- [Architecture](architecture.md) explains the components.
- [Contributing](../CONTRIBUTING.md) covers development conventions and tests. Run the suite with `pytest`.
- [Operational readiness](operational-readiness-005c.md) lists deployment checks that remain open.
