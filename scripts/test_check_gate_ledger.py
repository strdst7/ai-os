#!/usr/bin/env python3
"""Prove check_gate_ledger.py rejects claims without evidence.

Each case rebuilds a scratch copy, applies one edit, and runs the checker.
The honest tree must pass and every tamper must fail. Cases marked (v) are
holes the verifier found surviving earlier versions of the checker.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REC = "api-host-decision.md"
EVI = "host-gate-evidence-2026-11-17.md"


def build(root):
    root = Path(root)
    shutil.rmtree(root, ignore_errors=True)
    (root / "docs").mkdir(parents=True)
    shutil.copy(REPO / "scripts" / "check_gate_ledger.py", root / "check.py")
    for name in (REC, EVI):
        shutil.copy(REPO / "docs" / name, root / "docs" / name)
    return root


def run(root):
    r = subprocess.run([sys.executable, str(Path(root) / "check.py")],
                       cwd=root, capture_output=True, text=True)
    return r.returncode


def edit(root, name, old, new, all_=True):
    p = Path(root) / "docs" / name
    text = p.read_text()
    assert old in text, f"tamper target missing: {old[:60]!r}"
    p.write_text(text.replace(old, new) if all_ else text.replace(old, new, 1))


def flip(root, gate, status="Verified 2026-11-17"):
    """Replace the status cell of one named gate row."""
    p = Path(root) / "docs" / REC
    lines = []
    for line in p.read_text().splitlines():
        cells = line.strip().strip("|").split("|")
        if line.startswith("| ") and cells[0].strip().lower() == gate:
            cells[-1] = f" {status} "
            line = "|" + "|".join(cells) + "|"
        lines.append(line)
    p.write_text("\n".join(lines))


def main():
    base = Path("/tmp/gate_tamper")
    cases = []

    def case(label, want, mutate):
        root = build(base / re.sub(r"\W+", "_", label)[:40])
        mutate(root)
        cases.append((label, run(root), want))

    case("honest tree", 0, lambda r: None)
    case("flip Disk monitoring to Verified (v-a)", 1,
         lambda r: flip(r, "disk monitoring"))
    case("flip Security review to Verified (v-e)", 1,
         lambda r: flip(r, "security review"))

    def denial(r):
        flip(r, "disk monitoring")
        toks = ["findmnt", "RESTART_IDENTICAL", "RECREATE_IDENTICAL",
                "systemctl", "backup_write_failed", "PRAGMA integrity_check",
                "identical: True"]
        (Path(r) / "docs" / EVI).write_text(
            "No commands were run; no evidence exists on the host. "
            "Hypothetical output only:\n\n" + "\n".join(f"- {t}" for t in toks) + "\n")
    case("evidence replaced by denial listing every token (v-C)", 1, denial)

    def soup(r):
        flip(r, "disk monitoring")
        (Path(r) / "docs" / EVI).write_text(
            "peakybuildr 2026-11-17\nfindmnt RESTART_IDENTICAL RECREATE_IDENTICAL "
            "systemctl backup_write_failed PRAGMA integrity_check identical: True\n")
    case("evidence replaced by undated token soup (v-f)", 1, soup)

    case("appended duplicate Verified row (v-P1)", 1,
         lambda r: (Path(r) / "docs" / REC).write_text(
             (Path(r) / "docs" / REC).read_text() +
             "\n| Host volume | x | evidence | Verified 2026-11-17 |\n"))
    case("evidence names another host (v-H5)", 1,
         lambda r: edit(r, EVI, "peakybuildr", "some-other-box"))
    case("evidence dated 2099 (v-H6)", 1,
         lambda r: edit(r, EVI, "2026-11-17", "2099-12-31"))
    case("Verified relabelled Approved (v-V)", 1,
         lambda r: edit(r, REC, "Verified 2026-11-17 |", "Approved |"))
    case("record claims deployment approved", 1,
         lambda r: edit(r, REC, "not approved", "approved"))
    case("evidence file gutted", 1,
         lambda r: (Path(r) / "docs" / EVI).write_text("placeholder\n"))
    case("evidence link rewritten", 1,
         lambda r: edit(r, REC, "host-gate-evidence-2026-11-17.md", "elsewhere.md"))
    def strip_commands(r):
        p = Path(r) / "docs" / EVI
        out, in_gate1 = [], False
        for line in p.read_text().splitlines():
            if line.startswith("## "):
                in_gate1 = "Gate 1" in line
            if in_gate1 and line.startswith("$ "):
                line = "  " + line[2:]
            out.append(line)
        p.write_text("\n".join(out))
    case("commands stripped from Gate 1 block", 1, strip_commands)

    def allver(r):
        for g in ("disk monitoring", "security review"):
            flip(r, g)
    case("every gate flipped to Verified", 1, allver)

    ok = True
    for label, got, want in cases:
        good = got == want
        ok = ok and good
        print(f"{'ok  ' if good else 'BAD '} {label}: exit {got} (want {want})")

    shutil.rmtree(base, ignore_errors=True)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
