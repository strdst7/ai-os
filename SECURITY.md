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

The maintainers are not responsible for insecure deployments.
