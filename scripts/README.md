# Gate ledger check: what it can and cannot prove

`scripts/check_gate_ledger.py` is a lint, not a certificate. It catches a
record that drifts from its own evidence. It cannot tell a real command from
a typed one, because it reads markdown and markdown has no provenance.

## What it enforces

A gate row may read `Verified` only when all of these hold:

- the row sits in the five-row gate table, in order, with no duplicate names
  and a consistent column count;
- the status cell opens with `Pending`, `Partial`, `Verified` or `Not`, and any
  `Verified` cell carries a date;
- the matching `## Gate N` section in
  `docs/host-gate-evidence-2026-11-17.md` exists, is not repeated, and does
  not disclaim its own contents;
- that section contains a fenced block with a `$ ` command line and the
  gate's required output tokens;
- the guest named in a gate section matches the `## Environment` block, and
  both match the guest the record names;
- no heading in the evidence file repeats, no path is a symlink, and the
  record still reads `Status: Selected`, still links the evidence, still says
  the deployment is not approved, and still keeps a `Pending` or `Partial`
  row.

`scripts/test_check_gate_ledger.py` proves each of those with 22 tamper cases.

## What it cannot prove

Two holes have no fix at this layer. Both are named so nobody mistakes the
green check for a held gate.

- **A typed transcript passes.** If someone writes
  `$ findmnt` followed by the expected output by hand, every check above
  passes. Nothing in markdown distinguishes a paste from a fabrication.
- **Swapping two genuine sections passes.** Moving Gate 1's real body under
  Gate 3's heading and back leaves every token present. The check verifies
  that a gate's section shows a command and its output; it does not verify
  that the output belongs to that gate.

Closing either one needs something outside the document: a recorded terminal
session, a checksum over captured output, or an operator signature. Until then
the correct reading of a green check is "the record has not drifted from its
evidence", not "the gate is held".

The independent security review already required by
`docs/api-host-decision.md` is the right place to settle both.
