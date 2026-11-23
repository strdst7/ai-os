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
# ponytail: refuses symlinks rather than resolving them; a repo-type check
# would catch a symlinked docs/ dir, but this is enough to stop a swap.

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
    """Split the evidence doc into ({heading: body}, duplicate_headings).

    A repeated heading is returned as a duplicate rather than overwriting the
    earlier one: last-wins would let an appended section replace real evidence.
    """
    sections, seen, current, buf = {}, [], None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                if current in sections:
                    seen.append(current)
                sections[current] = "\n".join(buf)
            current, buf = line[3:].strip(), []
        else:
            buf.append(line)
    if current is not None:
        if current in sections:
            seen.append(current)
        sections[current] = "\n".join(buf)
    return sections, seen


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

    sections, dupes = evidence_sections(evidence_text)
    if dupes:
        problems.append(f"evidence repeats headings, last would win: {sorted(set(dupes))}")

    status_line = next((l for l in record_text.splitlines()
                        if l.lower().lstrip("*_ ").startswith("status")), "")
    if "selected" not in status_line.lower():
        problems.append(
            f"record's Status line must still read Selected, found {status_line[:80]!r}")

    if not any(l.startswith("| ") and "status" in l.lower() for l in record_text.splitlines()) \
            and len(rows) < len(ORDER):
        problems.append("gate ledger table appears to be missing")

    env = sections.get("Environment", "").lower()
    guest = re.search(r"guest\s+(\d+)\s+([a-z0-9-]+)", env)
    if not guest:
        problems.append("Environment block does not name the guest and its id")
    else:
        gid, gname = guest.group(1), guest.group(2)
        if f"guest {gid}" not in lower or gname not in lower:
            problems.append(
                f"Environment guest {gid} {gname} is not the guest the record names")
        for heading in [GATES[n][0] for n in ORDER if n in sections]:
            body = sections[heading].lower()
            for other in re.findall(r"guest\s+(\d+)\s+([a-z0-9-]+)", body):
                if other != (gid, gname):
                    problems.append(
                        f"section {heading!r} cites guest {other[0]} {other[1]}, "
                        f"Environment says {gid} {gname}")

    for name, status, _ in rows:
        cell = status.strip().lower()
        # A cell reads like "Verified 2026-11-17" or "Partial — no delivery
        # channel". The leading word is the status; the rest is detail.
        lead = cell.split()[0] if cell.split() else ""
        if lead == "verified" and not re.search(r"\d{4}-\d{2}-\d{2}", cell):
            problems.append(f"{name!r} reads Verified with no evidence date")
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

    header = "\n".join(evidence_text.splitlines()[:6]).lower()
    if "2026-11-17" not in header:
        problems.append("evidence header is not dated 2026-11-17")
    if "2026-11-17" not in record_text:
        problems.append("record does not carry the 2026-11-17 evidence date")

    env = sections.get("Environment", "").lower()
    if "peakybuildr" not in env:
        problems.append("evidence Environment block does not name peakybuildr")

    if "100.122.194.34" not in env:
        problems.append("evidence Environment block omits the host address")

    return problems


def main():
    for path in (RECORD, EVIDENCE, Path("docs")):
        if path.is_symlink():
            print(f"FAIL: {path} is a symlink")
            return 1
    problems = check(RECORD.read_text(), EVIDENCE.read_text())
    for p in problems:
        print("FAIL:", p)
    if problems:
        return 1
    print("gate ledger ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
