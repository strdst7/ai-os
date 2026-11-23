"""Check the gate ledger in docs/api-host-decision.md against retained evidence.

Run from the repo root:  python3 scripts/check_gate_ledger.py

A gate row may read Verified only when the evidence document carries, inside
that gate's own section, a dated command and its output. A bare word anywhere
in the file does not count: not a denial, not a bullet list, not a phrase the
record itself supplies.
"""

import re
import sys
from pathlib import Path

RECORD = Path("docs/api-host-decision.md")
EVIDENCE = Path("docs/host-gate-evidence-2026-11-17.md")

# Gate name in the record's ledger -> (heading in the evidence doc, required
# output tokens). An empty token list means no evidence fixture exists yet, so
# the gate can never read Verified.
GATES = {
    "host volume": ("Gate 1 — Host volume",
                    ["findmnt", "RESTART_IDENTICAL", "RECREATE_IDENTICAL"]),
    "backup schedule": ("Gate 2 — Backup schedule",
                        ["systemctl", "backup_write_failed"]),
    "restore drill": ("Gate 3 — Restore drill",
                      ["PRAGMA integrity_check", "identical: True"]),
    "disk monitoring": ("Gate 4 — Disk monitoring", []),
    "security review": ("Security review", []),
}

ORDER = list(GATES)
STATUSES = {"pending", "partial", "verified", "not verified"}


def ledger_rows(record):
    """Return [(gate, status, cell_count)] in the order the rows appear."""
    rows = []
    for line in record.splitlines():
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        name = cells[0].lower()
        if name in GATES:
            rows.append((name, cells[-1], len(cells)))
    return rows


def evidence_sections(text):
    """Split the evidence doc into {heading: body} on its level-2 headings."""
    sections, current, buf = {}, None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buf)
            current, buf = line[3:].strip(), []
        else:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf)
    return sections


def gate_passed(section, tokens):
    """True when the section shows a command block whose output carries the tokens.

    Requires at least one line starting with '$ ' (a command was actually run)
    and every token present in the fenced output, not in surrounding prose.
    """
    if not section or not tokens:
        return False, "no evidence section or no fixture"
    fenced = re.findall(r"```(.*?)```", section, re.S)
    if not fenced:
        return False, "no code block"
    blob = "\n".join(fenced)
    if not any(l.lstrip().startswith("$ ") for l in blob.splitlines()):
        return False, "no command line in the code block"
    if "hypothetical" in section.lower() or "no commands were run" in section.lower():
        return False, "section disclaims its own evidence"
    lacking = [t for t in tokens if t not in blob]
    if lacking:
        return False, f"output lacks {lacking}"
    return True, ""


def check(record_text, evidence_text):
    """Return a list of failure strings; empty means the ledger is sound."""
    problems = []
    lower = record_text.lower()

    rows = ledger_rows(record_text)
    names = [r[0] for r in rows]

    duplicates = {n for n in names if names.count(n) > 1}
    if duplicates:
        problems.append(f"gate rows duplicated: {sorted(duplicates)}")

    missing = [g for g in ORDER if g not in names]
    if missing:
        problems.append(f"gate rows missing: {missing}")

    if [n for n in names if n in GATES] != [g for g in ORDER if g in names]:
        problems.append(f"gate rows out of order: {names}")

    widths = {r[2] for r in rows}
    if len(widths) > 1:
        problems.append(f"gate rows have inconsistent column counts: {sorted(widths)}")

    sections = evidence_sections(evidence_text)

    for name, status, _ in rows:
        cell = status.strip().lower()
        # A cell reads like "Verified 2026-11-17" or "Partial — no delivery
        # channel". The leading word is the status; the rest is detail.
        lead = cell.split()[0] if cell.split() else ""
        if lead not in {"pending", "partial", "verified", "not"}:
            problems.append(
                f"{name!r} has status {status!r}; it must open with Pending, "
                f"Partial, Verified or Not verified")
            continue
        if lead != "verified":
            continue
        heading, tokens = GATES[name]
        ok, why = gate_passed(sections.get(heading), tokens)
        if not ok:
            problems.append(f"{name!r} reads Verified but evidence is insufficient: {why}")

    if "host-gate-evidence-2026-11-17" not in lower:
        problems.append("record does not link docs/host-gate-evidence-2026-11-17.md")

    if not any(r[1].strip().lower() in {"pending", "partial"} for r in rows):
        problems.append("no gate row is still Pending or Partial")

    if "not approved" not in lower:
        problems.append("record no longer says deployment is not approved")

    if not re.search(r"\b2026-11-17\b", evidence_text):
        problems.append("evidence is not dated 2026-11-17")

    env = sections.get("Environment", "").lower()
    if "peakybuildr" not in env:
        problems.append("evidence Environment block does not name peakybuildr")

    if "100.122.194.34" not in env:
        problems.append("evidence Environment block omits the host address")

    return problems


def main():
    problems = check(RECORD.read_text(), EVIDENCE.read_text())
    for p in problems:
        print("FAIL:", p)
    if problems:
        return 1
    print("gate ledger ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
