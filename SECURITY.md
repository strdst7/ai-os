# Security Policy

AI-OS is designed for enterprise AI governance and monitoring.

---

## Supported Versions

| Version | Supported |
|---------|-----------|
| v1.0.x  | Yes       |

---

## Reporting Vulnerabilities

Please report security vulnerabilities privately.

Avoid opening public issues for security-sensitive matters.

---

## Security Design Principles

AI-OS enforces:

- API key authentication
- Environment-based configuration
- Guardrail threshold validation
- Telemetry validation via schema typing

---

## Deployment Responsibility

AI-OS must be deployed:

- Behind authentication
- With secure environment variables
- In a monitored production environment

Set a random `AIOS_API_KEY` with at least 32 characters through the deployment environment or secret manager.
Missing, empty, short, whitespace-padded, and known default keys make private routes return 503.
Send the key in the `x-api-key` header. Never commit it.
Only `/health` is public. API documentation routes are disabled.
Do not publish the service before a security review.

For a single-host, single-replica deployment, set `AIOS_OBSERVATION_DB` to a file on a persistent volume.
The default in-memory store is for tests and local development; it loses observations on restart.
The Docker image requires an absolute file path at startup; missing or in-memory paths stop the service.
Keep the database file private. Back it up and monitor disk space.
SQLite transactions and a unique observation ID prevent concurrent retries from creating duplicate records.
Do not run multiple hosts or replicas against a shared SQLite file. Use a shared transactional store when that deployment exists.

The maintainers are not responsible for insecure deployments.
