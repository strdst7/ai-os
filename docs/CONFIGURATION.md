<!-- generated-by: gsd-doc-writer -->
# Configuration

The FastAPI service (`src.main:app`) and Streamlit dashboard (`app.py`) are separate entrypoints. The dashboard stores ADSI history in `st.session_state`; it does not use the API's SQLite store or API key.

## Environment variables

No `.env.example` or `.env.sample` exists. The source and Dockerfile define these settings:

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `AIOS_API_KEY` | For usable private API routes | None | Secret checked against the `x-api-key` request header. Missing or invalid server keys return HTTP 503 on `/agent/evaluate` and `/observability`; `/health` remains public. The service still starts without it. |
| `AIOS_OBSERVATION_DB` | In container mode | `:memory:` outside container mode | SQLite database path. An empty string always fails initialization. Use an absolute path on persistent storage for the Docker image. |
| `AIOS_REQUIRE_PERSISTENCE` | Set by Dockerfile | Unset outside the image | Only the exact value `1` rejects `:memory:` and relative database paths during service initialization. The image sets `1`. |
| `PYTHONPATH` | Set by Dockerfile | Runtime-dependent outside the image | The image sets `/app` so `src` imports resolve. |
| `PYTHONDONTWRITEBYTECODE` | Set by Dockerfile | Runtime-dependent outside the image | The image sets `1` to avoid bytecode files. |
| `PYTHONUNBUFFERED` | Set by Dockerfile | Runtime-dependent outside the image | The image sets `1` for unbuffered Python output. |

The test harness also reads these opt-in variables. They do not configure the application:

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `AIOS_RUN_ENOSPC_TEST` | For `tests/full_volume.py` only | Unset | Exact value `1` permits the destructive disposable-volume test to proceed after its free-space check. |
| `AIOS_FAIL_AFTER_MOUNT` | No | Unset | Exact value `1` injects a test failure after the isolated mount check. |

## Config file format

There is no JSON, YAML, TOML, or dotenv application config loader. `src/config.py` defines Python class attributes:

| Class | Attribute | Value | Use |
| --- | --- | --- | --- |
| `GuardrailConfig` | `LATENCY_THRESHOLD` | `0.3` | Defined but not referenced by the current application. |
| `GuardrailConfig` | `DRIFT_THRESHOLD` | `0.2` | Defined but not referenced by the current application. |
| `GuardrailConfig` | `COST_VOLATILITY_THRESHOLD` | `0.4` | Defined but not referenced by the current application. |
| `MonitoringConfig` | `HISTORY_LIMIT` | `20` | Caps recent entries returned and scores sampled for anomaly checks; SQLite keeps older rows. |
| `MonitoringConfig` | `MONITOR_INTERVAL_SECONDS` | `10` | Delay between API background checks; those checks read state without adding observations. |

API report tiers come from `src/guardrails.py`. The dashboard and API observability degradation use `src/stability_engine.py`. Neither uses `GuardrailConfig`. Changing these class attributes requires a code change and restart.

## Required vs optional settings

- **API access:** Set `AIOS_API_KEY` to at least 32 characters. Leading or trailing whitespace and listed weak values fail validation. Pass the same value as `x-api-key` on private requests. Keep the secret out of the repository.
- **Container startup:** Set `AIOS_OBSERVATION_DB` to an absolute file path. The image sets `AIOS_REQUIRE_PERSISTENCE=1`; missing, empty, in-memory, or relative paths stop startup.
- **Local API startup:** Without persistence enforcement, the API starts with an in-memory database. Set a writable file path if observations must survive a restart. A missing parent directory or unwritable path raises a SQLite error during initialization.
- **Streamlit dashboard:** It needs none of the `AIOS_*` API settings. Its session history does not survive a browser session reset.

For a disposable local API run, install `requirements.txt`, then set a strong key before starting Uvicorn:

```bash
export AIOS_API_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
uvicorn src.main:app
```

For the Docker image, provide a persistent mount and an absolute path, as tested by `tests/container_lifecycle.py`:

```bash
docker run --mount source=ai-os-data,target=/data \
  -e AIOS_API_KEY="$AIOS_API_KEY" \
  -e AIOS_OBSERVATION_DB=/data/observations.db \
  ai-os-image
```

The command assumes an image named `ai-os-image` and a volume named `ai-os-data`; create and secure them for your host. <!-- VERIFY: Confirm the deployment host's persistent mount, directory ownership, file permissions, backup schedule, and disk alerts. --> SQLite uses one local writer lock; do not share one database file across multiple hosts or replicas. See [operational readiness](operational-readiness-005c.md) before a stateful deployment.

## Defaults

- `AIOS_OBSERVATION_DB` defaults to `:memory:` in `MonitoringService.__init__`. Observations and alert state disappear on restart.
- `AIOS_REQUIRE_PERSISTENCE` has no source default; only `1` enables its path restriction. Docker sets `1`.
- `AIOS_API_KEY` has no fallback key. Invalid or missing values cause HTTP 503 on private routes, not a startup failure.
- `MonitoringConfig` values come from `src/config.py`; the other defined thresholds do not control current guardrail behavior.

## Per-environment overrides

Set environment variables in the process that starts `uvicorn src.main:app`. The Dockerfile fixes `AIOS_REQUIRE_PERSISTENCE=1` unless the container environment overrides it. Do not disable persistence enforcement for stateful deployments. No `.env.development`, `.env.test`, `.env.production`, or environment-specific config loader exists. The Streamlit entrypoint runs independently with session-local state.
