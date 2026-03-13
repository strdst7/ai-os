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

### API Layer
FastAPI exposes monitoring endpoints.

## Observability Flow
