<!-- generated-by: gsd-doc-writer -->
# API

The FastAPI service in `src/main.py` evaluates telemetry and stores observations in SQLite. The separate Streamlit dashboard in `app.py` does not call this API. Paths below are relative to the API server. FastAPI's `/docs`, `/redoc`, and `/openapi.json` routes are disabled.

## Authentication

- `/health` is public.
- `/agent/evaluate` and `/observability` require the `x-api-key` header. Set the server's `AIOS_API_KEY` to the same secret.
- The server key must contain at least 32 characters, have no surrounding whitespace, and not match a listed weak value in `src/auth.py`.
- An absent or invalid server key returns HTTP 503 on private routes. A missing or incorrect request header returns HTTP 401 when the server key is valid.

Keep the secret out of source control. See [Configuration](CONFIGURATION.md) for local setup and persistence settings. No deployed API base URL is defined in the repository.

## Endpoints overview

| Method | Path | Description | Auth Required |
| --- | --- | --- | --- |
| GET | `/health` | Check that the API responds. | No |
| POST | `/agent/evaluate` | Evaluate telemetry and store a new observation unless it replays an existing one. | Yes |
| GET | `/observability` | Read the current observation, recent history, and alert state. | Yes |

## Request/response formats

Requests and responses use JSON. `GET` endpoints take no body. `POST /agent/evaluate` accepts these fields:

| Field | Requirement | Meaning |
| --- | --- | --- |
| `kpi_error` | Required, JSON number from 0 to 1 | KPI alignment error. |
| `embedding_shift` | Required, JSON number from 0 to 1 | Embedding drift. |
| `retrieval_score` | Required, JSON number from 0 to 1 | Retrieval quality. |
| `latency_dev` | Required, JSON number from 0 to 1 | Latency deviation. |
| `observation_id` | Optional UUID string | Caller-supplied observation identity for replay detection. |

Metric values must be finite floating-point numbers. Integers, booleans, strings, nulls, missing fields, and extra fields fail validation. The API field is `latency_dev`, not `latency_deviation`.

Example request body:

```json
{
  "kpi_error": 0.1,
  "embedding_shift": 0.1,
  "retrieval_score": 0.9,
  "latency_dev": 0.1
}
```

`POST /agent/evaluate` returns HTTP 200 with a report. The following response uses an illustrative timestamp; its scores follow the example request:

```json
{
  "timestamp": "2026-01-01T00:00:00+00:00",
  "scores": {"AHI": 0.9, "IHI": 0.9, "DHI": 0.9, "ADSI": 0.9},
  "stability_tier": "Stable",
  "guardrail_flags": "stable"
}
```

`AHI`, `IHI`, and `DHI` are rounded to three decimals. `ADSI` is not rounded in the report. The tier and flag use the same classification with title case and lowercase respectively: `Stable`, `Warning`, `Degrading`, or `Critical`. A report does not include `observation_id`; retrieve its observation entry from `/observability`.

- A new observation without `observation_id` receives a generated UUID.
- Repeating identical metrics without an ID immediately after the matching observation returns that saved report without a new entry.
- Repeating an existing ID with identical metrics returns its saved report, even after it leaves recent history.
- Reusing an existing ID with different metrics returns HTTP 409. Distinct IDs permit separate observations with equal metrics.

`GET /health` returns HTTP 200:

```json
{"status": "AI-OS running"}
```

Before any evaluation, `GET /observability` returns HTTP 200:

```json
{"message": "No evaluations performed yet"}
```

After an evaluation, the response has this shape. The example values are illustrative:

```json
{
  "current": {
    "observation_id": "123e4567-e89b-42d3-a456-426614174000",
    "timestamp": "2026-01-01T00:00:00+00:00",
    "ADSI": 0.9,
    "stability_tier": "Stable",
    "guardrail_flags": "stable",
    "mode": "manual_trigger"
  },
  "history": [
    {
      "observation_id": "123e4567-e89b-42d3-a456-426614174000",
      "timestamp": "2026-01-01T00:00:00+00:00",
      "ADSI": 0.9,
      "stability_tier": "Stable",
      "guardrail_flags": "stable",
      "mode": "manual_trigger"
    }
  ],
  "degradation": "stable",
  "anomaly": false
}
```

`history` is oldest-first and contains at most 20 recent entries. `current` is its newest entry. `degradation` reflects the current ADSI tier in lowercase. `anomaly` reflects stored alert state, not just the current score. Background checks read state without creating observations. Replays do not change history or alerts; two fresh `Stable` observations clear an active alert. SQLite retains older observations beyond the response history limit.

## Error codes

| Status | Condition | Response |
| --- | --- | --- |
| 401 | Missing or incorrect `x-api-key` with a valid server key. | `{"detail":"Unauthorized"}` |
| 409 | Existing `observation_id` reused with different metrics. | `{"detail":"Observation ID already used"}` |
| 422 | Invalid JSON body, missing metric, invalid UUID, out-of-range or non-float metric, or extra field. | FastAPI validation response with a `detail` list. |
| 503 | Server `AIOS_API_KEY` missing or rejected by validation. | `{"detail":"API key not configured"}` |

No custom handler translates SQLite or other unexpected failures into a documented API error envelope. An invalid body does not create an observation.

## Rate limits

No API rate limiter, request window, or maximum request count is configured in the repository. Deployment-layer limits, if any, are not specified here. <!-- VERIFY: Confirm any proxy or hosting-layer rate limits before relying on their absence. -->
