"""Check the gate ledger in docs/api-host-decision.md against retained evidence.

Run from the repo root:  python3 scripts/check_gate_ledger.py

A gate row may read Verified only when the evidence document carries the
command output behind it. Prose anywhere in the record cannot satisfy a token.
"""

import re
import sys
from pathlib import Path

RECORD = Path("docs/api-host-decision.md")
EVIDENCE = Path("docs/host-gate-evidence-2026-11-17.md")

GATES = ["host volume", "backup schedule", "restore drill", "disk monitoring",
         "security review"]

# Tokens that must appear in the EVIDENCE document, never in the record.
# Each token only appears there when the gate genuinely passed.
PROOF = {
    "host volume": ["findmnt", "RESTART_IDENTICAL", "RECREATE_IDENTICAL"],
    "backup schedule": ["systemctl", "backup_write_failed"],
    "restore drill": ["PRAGMA integrity_check", "identical: True"],
    # No proof exists yet, so this gate can never read Verified.
    "disk monitoring": [],
    "security review": [],
}


def gate_rows(record):
    """Return {gate name: status cell} for the ledger's gate table."""
    found = {}
    for line in record.splitlines():
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        name = cells[0].lower()
        if name in GATES and len(cells) >= 2:
            found[name] = cells[-1]
    return found


def gate_rows_in_order(record):
    """Gate names in the order their table rows appear."""
    seen = []
    for line in record.splitlines():
        cells = [c.strip().lower() for c in line.strip().strip("|").split("|")]
        if line.startswith("| ") and cells and cells[0] in GATES and cells[0] not in seen:
            seen.append(cells[0])
    return seen


def check(record_text, evidence_text):
    """Return a list of failure strings; empty means the ledger is sound."""
    problems = []
    lower = record_text.lower()
    ev = evidence_text.lower()

    rows = gate_rows(record_text)
    order = [g for g in gate_rows_in_order(record_text)]
    if order != [g for g in GATES if g in order]:
        problems.append(f"gate rows out of table order: {order}")

    missing_rows = [g for g in GATES if g not in rows]
    if missing_rows:
        problems.append(f"gate rows missing: {missing_rows}")

    for gate, status in rows.items():
        if "verified" not in status.lower():
            continue
        proofs = PROOF.get(gate, [])
        if not proofs:
            problems.append(
                f"{gate!r} reads {status!r} but no evidence fixture exists for it")
            continue
        lacking = [t for t in proofs if t.lower() not in ev]
        if lacking:
            problems.append(
                f"{gate!r} reads {status!r} but evidence lacks {lacking}")

    if "host-gate-evidence-2026-11-17" not in lower:
        problems.append("record does not link docs/host-gate-evidence-2026-11-17.md")

    if not any("pending" in s.lower() for s in rows.values()):
        problems.append("no gate row is still Pending")

    if "not approved" not in lower:
        problems.append("record no longer says deployment is not approved")

    return problems


def main():
    record = RECORD.read_text()
    evidence = EVIDENCE.read_text()
    problems = check(record, evidence)
    for p in problems:
        print("FAIL:", p)
    if problems:
        return 1
    print("gate ledger ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
