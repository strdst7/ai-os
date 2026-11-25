# Phase 1: Host selection and evidence plan - Context

**Gathered:** 2026-11-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Record the blocked stateful API host decision and the evidence required before production approval. This phase does not select an imaginary host, deploy the API, or approve public exposure.

</domain>

<decisions>
## Implementation Decisions

### Host candidates
- **D-01:** No eligible host candidate exists yet. Record the decision as blocked; do not imply a host was selected.
- **D-02:** The user owns the decision to name a host candidate. The future host operator remains unknown.
- **D-03:** Reopen the blocked decision when the user names a host candidate and its operator for assessment against the fixed gates.
- **D-04:** Do not insert a placeholder host, operator, or host-specific path. Mark unknown host-specific details pending.

### Fixed project constraints
- Keep the Streamlit Community Cloud demo separate from the Docker/FastAPI service and its SQLite observations.
- Retain the one-host, one-replica SQLite constraint for any future candidate.
- Record the persistent volume, scheduled backup, restore drill, disk alerts, and security review as pending. Each prerequisite needs an owner and evidence source. Assigning those owners was not settled in this discussion; do not invent names or claim completion.
- Keep the FastAPI service private until target-host evidence and security review exist.

### Agent discretion
- Choose a concise decision-record location and structure that fits the existing documentation. Preserve explicit pending fields rather than inventing host facts.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Scope and acceptance
- `.planning/PROJECT.md` — milestone boundary, core value, and safety constraints.
- `.planning/REQUIREMENTS.md` — HOST-01, HOST-02, GATE-01, and GATE-02.
- `.planning/ROADMAP.md` — Phase 1 goal and success criteria.

### Existing evidence
- `docs/DEPLOYMENT.md` — separate runtimes, blocked deployment, host gates, and rollback limits.
- `docs/operational-readiness-005c.md` — disposable CI results and outstanding target-host checks.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `docs/DEPLOYMENT.md` and `docs/operational-readiness-005c.md`: Existing gate descriptions and evidence boundaries for the decision record.

### Established Patterns
- `src/services/monitoring_service.py`: SQLite state uses a local lock and an absolute persistent path when `AIOS_REQUIRE_PERSISTENCE=1`.
- `src/main.py`: The FastAPI runtime serves the private evaluation and observability routes separately from `app.py`.

### Integration Points
- This decision-only phase updates documentation. It does not modify API behavior or deployment tooling.

</code_context>

<specifics>
## Specific Ideas

- The user selected a blocked decision without a placeholder host.
- The user owns naming a future host candidate and operator.

</specifics>

<deferred>
## Deferred Ideas

- GPT-6-sol model support was requested earlier. Its use in the service remains unspecified and lies outside this decision-only milestone.

</deferred>

---

*Phase: 1-host-selection-and-evidence-plan*
*Context gathered: 2026-11-25*
