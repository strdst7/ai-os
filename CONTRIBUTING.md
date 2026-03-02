# Contributing to AI-OS

Thank you for your interest in contributing to AI-OS.

AI-OS is a production-grade AI deployment monitoring system built for enterprise governance and stability evaluation.

---

## Contribution Principles

AI-OS prioritizes:

- Architectural clarity
- Deterministic stability scoring
- Governance discipline
- Production-readiness
- Research-backed modeling

All contributions must preserve these principles.

---

## Development Setup

1. Clone the repository
2. Create a virtual environment
3. Install dependencies:
   pip install -r requirements.txt
4. Run tests:
   pytest

---

## Code Standards

- Maintain service-layer separation
- Use typed models (Pydantic)
- Keep monitoring logic deterministic
- No experimental hacks
- Include tests for new logic

---

## Pull Request Guidelines

- Provide clear commit messages
- Include tests for new features
- Maintain documentation accuracy
- Avoid breaking existing APIs

---

## Research Contributions

If extending monitoring metrics:

- Include mathematical explanation
- Provide calibration logic
- Ensure anomaly detection remains explainable
