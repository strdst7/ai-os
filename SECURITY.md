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

The maintainers are not responsible for insecure deployments.
