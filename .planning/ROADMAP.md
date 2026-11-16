# Roadmap: AI-OS production API readiness

## Overview

Decide whether an eligible stateful API host exists, then define host-specific evidence for future production approval. The milestone ends with a decision record, not a deployment.

## Phases

- [x] **Phase 1: Host selection and evidence plan** - Record the host decision and five approval prerequisites.

## Phase Details

### Phase 1: Host selection and evidence plan
**Goal**: Produce one decision record naming the selected host and operator, with explicit host evidence criteria and owners; record a blocked decision only when no eligible host exists.
**Depends on**: Nothing (first phase)
**Requirements**: HOST-01, HOST-02, GATE-01, GATE-02
**Success Criteria** (what must be TRUE):
  1. The record names the host and operator, or states exactly which decision remains blocked.
  2. The record separates Streamlit from FastAPI/SQLite and accounts for one-host, one-replica topology.
  3. Four host gates and security review have owners, evidence requirements, and pending status until target-host checks pass.
**Plans**: 1 plan

Plans:
- [x] 01-01-PLAN.md — Record the selected host `peakybuildr` with a dated evidence ledger and a Pending gate plan.

## Progress

| Phase | Plans Complete | Status | Completed |
| --- | --- | --- | --- |
| 1. Host selection and evidence plan | 1/1 | Awaiting human verification (host gates pending) | - |
