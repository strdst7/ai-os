# Phase 1: Host selection and evidence plan — Context

## Decisions

- D-01: This is a decision-only milestone. Produce one host decision record, not an app, database, UI, or deployment.
- D-02: No stateful API host is selected. MIA is decision owner and interim operator; the named operating contact remains pending. Record the host decision as blocked until an eligible host and contact are named; never infer a host from the Streamlit demo.
- D-03: Keep production API access private. Four target-host gates and a security review remain pending until actual evidence exists.
- D-04: Use one host and one replica while SQLite is the writer. Do not treat disposable CI results as host evidence.

## Claude's Discretion

- Choose a concise decision-record format and evidence matrix within the existing documentation structure.
- Assign a named operating contact to the selected host; MIA remains interim operator until then.

## Deferred Ideas

- API deployment, public exposure, new infrastructure, new UI or database, and recovery-rule calibration.

## Source

User selected “Production API readiness gates,” “Host not selected yet (plan host selection first),” and a one-phase milestone for host selection and evidence planning. See `docs/DEPLOYMENT.md` and `docs/operational-readiness-005c.md` for the baseline gates.
