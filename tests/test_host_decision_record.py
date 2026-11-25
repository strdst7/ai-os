"""Check the blocked host decision and its pending evidence gates."""

import re
from pathlib import Path


RECORD = Path(__file__).resolve().parents[1] / "docs/host-selection-and-evidence-plan.md"


def _decision_fields(text):
    return dict(re.findall(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$", text, re.M))


def test_host_decision_is_blocked_until_user_names_candidate_and_operator():
    text = RECORD.read_text()
    fields = _decision_fields(text)

    assert "Blocked: no eligible stateful API host candidate or operator named" in text
    assert "User" in fields["Decision owner"]
    assert all(word in fields["Reopen trigger"] for word in ("User", "both", "candidate", "operator"))
    for field in ("Candidate", "Operator", "Actual persistent mount", "Actual `AIOS_OBSERVATION_DB` path"):
        assert "Pending" in fields[field]
    assert "Docker/FastAPI `src.main:app`" in text
    assert "SQLite" in text and "one host and one replica" in text
    assert "Streamlit Community Cloud runs `app.py` with session-local history" in text
    assert "does not host the Docker/FastAPI service" in text
    assert "Keep the API private until target-host evidence" in text
    assert "separate security approval" in text
    assert "no deployment or production approval" in text


def test_five_gates_require_independent_target_host_evidence():
    text = RECORD.read_text()
    table = text.split("## Pending acceptance evidence", 1)[1].split("## Flagged unverified assumptions", 1)[0]
    rows = [list(map(str.strip, line.strip("|").split("|"))) for line in table.splitlines() if line.startswith("|")]
    assert rows[0] == ["Gate", "Owner", "Required evidence", "Evidence source", "Status"]
    gates = {row[0]: row for row in rows[2:]}
    assert set(gates) == {"Persistent volume", "Scheduled backup", "Restore drill", "Disk alerts", "Security review"}
    for row in gates.values():
        assert all("Pending" in row[i] for i in (1, 3, 4))

    required = {
        "Persistent volume": ("mount", "AIOS_OBSERVATION_DB", "ownership", "permissions", "restart", "recreation"),
        "Scheduled backup": ("frequency", "retention", "off-volume", "failure notification", "actual completed"),
        "Restore drill": ("real backup", "isolated", "history", "anomaly state", "UUID replay", "integrity_check"),
        "Disk alerts": ("capacity thresholds", "delivered alerts", "backup-write error", "without filling production storage"),
        "Security review": ("separate", "documented security review", "approval", "public API exposure"),
    }
    for name, terms in required.items():
        evidence = gates[name][2].casefold()
        assert all(term.casefold() in evidence for term in terms), name

    assert "CI results are background only, not target-host evidence or production approval" in text
    assert "No target-host checks ran" in text
    assert "docs/DEPLOYMENT.md" in text and "docs/operational-readiness-005c.md" in text
