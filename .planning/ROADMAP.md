# Roadmap: AI-OS production API readiness

## Overview

Decide whether an eligible stateful API host exists, then define the host-specific evidence required for production approval. This milestone ends with a decision record, not a deployment.

## Phases

- [x] **Phase 1: Host selection and evidence plan** - Record the host decision and the five approval prerequisites. (completed 2026-11-25)

## Phase Details

### Phase 1: Host selection and evidence plan
**Goal**: Produce one decision record naming an eligible host and operator, or a blocked decision, with explicit host evidence criteria and owners.
**Depends on**: Nothing (first phase)
**Requirements**: HOST-01, HOST-02, GATE-01, GATE-02
**Success Criteria** (what must be TRUE):
  1. The record names the host and operator, or states exactly which decision remains blocked.
  2. The record separates the Streamlit demo from the FastAPI/SQLite deployment and accounts for one-host, one-replica topology.
  3. All four host gates and the security review have owners, evidence requirements, and honest pending status until checked on the target host.
**Plans**: 1/1 plans complete — `01-01-PLAN.md` (blocked decision record and five pending evidence gates)
- [x] 01-01-PLAN.md

## Progress

| Phase | Plans Complete | Status | Completed |
| --- | --- | --- | --- |
| 1. Host selection and evidence plan | 1/1 | Complete    | 2026-11-25 |
