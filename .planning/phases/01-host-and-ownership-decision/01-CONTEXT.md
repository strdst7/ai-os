# Phase 1: Host and ownership decision - Context

**Gathered:** 2026-11-05
**Status:** Ready for planning. Host selection remains blocked.

<domain>
## Phase Boundary

Record the candidate private FastAPI host and operator, or identify blockers. Assess single-process SQLite and persistent-volume fit only after topology is known. This phase does not deploy the API or grant production approval.

</domain>

<decisions>
## Implementation Decisions

### Host and ownership
- **D-01:** No candidate FastAPI host exists yet. Record host selection as open, not approved.
- **D-02:** MIA selects the host and owns storage, backups, alerts, and restore drills.
- **D-03:** The operations team needs the host decision record. This does not grant API access.
- **D-04:** Leave SQLite topology and persistent-volume fit blocked until a host and its process count, replica count, and durable mount are known.

### Private access
- **D-05:** SSH tunnel and private network are equally acceptable access paths. One checked path is enough for host qualification.
- **D-06:** Both paths work for other services. Neither path has been checked against a candidate FastAPI host.
- **D-07:** Authorized API users remain undecided. Treat access ownership as a blocker before service access.
- **D-08:** Keep the API private. A separate security review must approve any public exposure.

### Claude's Discretion
- Keep the non-secret decision record in this repository's existing planning area. The team can read it alongside the code and readiness report.
- Record access details and evidence without credentials or sensitive network identifiers. Do not create a parallel runbook without an established operations location.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project scope
- `.planning/PROJECT.md` — service boundary, host constraints, and core value.
- `.planning/REQUIREMENTS.md` — HOST-01 and HOST-02 acceptance scope.
- `.planning/ROADMAP.md` — Phase 1 boundary and success criteria.

### Existing operational evidence
- `docs/operational-readiness-005c.md` — disposable CI results and open target-host gates.
- `.planning/codebase/ARCHITECTURE.md` — API flow, SQLite transaction model, and Streamlit separation.
- `.planning/codebase/INTEGRATIONS.md` — persistence and authentication boundaries.

No external host specification or operations runbook was identified.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `docs/operational-readiness-005c.md`: Reuse its host-gate evidence categories instead of inventing new criteria.
- `tests/container_lifecycle.py`: Its disposable-volume results establish test behavior, not host readiness.

### Established Patterns
- `Dockerfile`: One Uvicorn process requires an absolute `AIOS_OBSERVATION_DB` path.
- `src/services/monitoring_service.py`: SQLite stores observations and anomaly state; no shared remote database exists.
- `app.py`: Streamlit keeps separate session-local history.

### Integration Points
- `.planning/phases/01-host-and-ownership-decision/`: Keep the non-secret decision and blocked-evidence record beside phase planning.
- `docs/operational-readiness-005c.md`: Carry its four open host gates into Phase 2 planning.

</code_context>

<specifics>
## Specific Ideas

- Record one working host-specific private path when a host exists; the other path can remain pending.
- An existing tunnel or private network for unrelated services does not qualify a future host.
- Do not equate operations-team visibility of the record with permission to use the API.

</specifics>

<deferred>
## Deferred Ideas

- Host mount, backup schedule, restore drill, disk alert, and private-exposure checks belong in Phase 2.
- Production approval and recovery-rule calibration require later evidence.
- Streamlit changes and a new database remain outside this milestone.

</deferred>

---

*Phase: 1-Host and ownership decision*
*Context gathered: 2026-11-05*
