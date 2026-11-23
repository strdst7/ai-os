#!/usr/bin/env python3
"""Prove check_gate_ledger.py rejects claims without evidence.

Each tamper rebuilds a scratch copy of the two docs, applies one edit, and runs
the checker. The honest tree must pass; every tamper must fail.
"""

import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHECKER = REPO / "scripts" / "check_gate_ledger.py"
DOОC = REPO / "docs"


def build(root):
    root = Path(root)
    shutil.rmtree(root, ignore_errors=True)
    (root / "docs").mkdir(parents=True)
    shutil.copy(REPO / "scripts" / "check_gate_ledger.py", root / "check.py")
    for name in ("api-host-decision.md", "host-gate-evidence-2026-11-17.md"):
        shutil.copy(REPO / "docs" / name, root / "docs" / name)
    return root


def run(root):
    r = subprocess.run([sys.executable, str(Path(root) / "check.py")],
                       cwd=root, capture_output=True, text=True)
    return r.returncode


def edit(root, name, old, new):
    p = Path(root) / "docs" / name
    text = p.read_text()
    assert old in text, f"tamper target missing: {old[:50]!r}"
    p.write_text(text.replace(old, new))


def main():
    base = Path("/tmp/gate_tamper")
    results = []

    root = build(base / "honest")
    results.append(("honest tree", run(root), 0))

    root = build(base / "flip")
    edit(root, "api-host-decision.md", "| Partial", "| Verified 2026-11-17")
    results.append(("flip Disk monitoring to Verified", run(root), 1))

    root = build(base / "soup")
    edit(root, "api-host-decision.md", "| Partial", "| Verified 2026-11-17")
    edit(root, "host-gate-evidence-2026-11-17.md", "findmnt", "xxxx")
    results.append(("flip + break one proof token", run(root), 1))

    root = build(base / "gut")
    (root / "docs" / "host-gate-evidence-2026-11-17.md").write_text("placeholder\n")
    results.append(("evidence file gutted", run(root), 1))

    root = build(base / "unlink")
    edit(root, "api-host-decision.md", "host-gate-evidence-2026-11-17.md", "elsewhere.md")
    results.append(("evidence link rewritten", run(root), 1))

    root = build(base / "allver")
    for row in ("| Verified",):
        pass
    text = (root / "docs" / "api-host-decision.md").read_text()
    lines = []
    for line in text.splitlines():
        if line.startswith("| ") and line.split("|")[1].strip().lower() in (
                "host volume", "backup schedule", "restore drill",
                "disk monitoring", "security review"):
            cells = line.strip().strip("|").split("|")
            cells[-1] = " Verified 2026-11-17 "
            line = "|" + "|".join(cells) + "|"
        lines.append(line)
    (root / "docs" / "api-host-decision.md").write_text("\n".join(lines))
    results.append(("every gate flipped to Verified", run(root), 1))

    root = build(base / "secver")
    edit(root, "api-host-decision.md", "| Pending |", "| Verified 2026-11-17 |")
    results.append(("Security review flipped to Verified", run(root), 1))

    root = build(base / "nopending")
    text = (root / "docs" / "api-host-decision.md").read_text()
    text = text.replace("| Pending |", "| Verified 2026-11-17 |")
    text = text.replace("| Partial — no delivery channel |", "| Verified 2026-11-17 |")
    (root / "docs" / "api-host-decision.md").write_text(text)
    results.append(("no Pending row left", run(root), 1))

    root = build(base / "approved")
    edit(root, "api-host-decision.md", "not approved", "approved")
    results.append(("record stops saying not approved", run(root), 1))

    ok = True
    for label, got, want in results:
        good = (got == want)
        ok = ok and good
        flag = "ok  " if good else "BAD "
        print(f"{flag} {label}: exit {got} (want {want})")

    shutil.rmtree(base, ignore_errors=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
