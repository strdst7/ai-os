# AI-OS Architecture

AI-OS implements a supervisory monitoring architecture for enterprise AI deployments.

## Core Components

### Stability Engine
Computes the Deployment Stability Index (ADSI).

Inputs:
- KPI error
- Retrieval score
- Latency deviation
- Embedding drift

Outputs:
- AHI
- IHI
- DHI
- ADSI

### Guardrails Layer
Enforces stability tiers:

| ADSI | Tier |
|-----|-----|
| ≥0.85 | Stable |
| 0.75–0.85 | Warning |
| 0.65–0.75 | Degrading |
| <0.65 | Critical |

### Monitoring Service
Maintains telemetry history and detects anomalies.

Recovery currently requires two consecutive fresh Stable observations after an anomaly.
A Warning or Critical observation resets the recovery count; replayed observations do not advance it.
The rule has no elapsed-time requirement. Tests cover one-second and one-day gaps, but no incident data or false-clear analysis supports the threshold.
Treat this as provisional, not statistically validated. Calibrate against labeled incidents and operator requirements before production alerting.

### API Layer
FastAPI exposes monitoring endpoints.

## Observability Flow
Telemetry → Stability Engine → Guardrails → Monitoring → API

## CI Validation

GitHub Actions automatically runs:

- pytest
- coverage analysis
- API integration tests
