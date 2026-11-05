# Phase 1: Host and ownership decision - Discussion Log

> Audit trail only. Planning agents use `01-CONTEXT.md`.

**Date:** 2026-11-05
**Phase:** 1-Host and ownership decision
**Areas discussed:** Private access, host selection, operator ownership, team handoff

---

## Private access

| Question | Alternatives | User choice |
| --- | --- | --- |
| Access path | SSH tunnel, private network, undecided | Both paths |
| Primary path | Tunnel first, network first, equal paths | Equal paths |
| Host qualification | One working path, both required | One working path |
| Authorized users | Named operators, operations team, undecided | Undecided |
| Existing availability | Tunnel, private network, both, neither checked | Both work today |
| Candidate-host reachability | Both, one, neither checked, no host | Neither checked against a candidate host |

**Notes:** Existing paths work for other services. No host-specific API reachability is claimed.

## Host and operator

| Question | Alternatives | User choice |
| --- | --- | --- |
| Candidate host | Named host, no host | No candidate host |
| Host selection and operational ownership | User, named operator, undecided | User |

**Notes:** MIA owns storage, backups, alerts, and restore drills when a host exists.

## Team handoff

| Question | Alternatives | User choice |
| --- | --- | --- |
| Decision-record readers | User, named backup operator, operations team, undecided | Operations team |
| Record location | AI-OS repository, existing runbook, undecided | Asked Claude to decide |

## Claude's Discretion

- Store the non-secret decision record in the repository's existing planning area.
- Do not add a parallel runbook without an established operations location.

## Deferred Ideas

- Production-host evidence and recovery calibration remain outside Phase 1.
