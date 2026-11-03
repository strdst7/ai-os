"""Run on a Docker host to check the single-replica volume contract."""

import json
import secrets
import subprocess
import time
import urllib.error
import urllib.request
from uuid import uuid4


IMAGE = "ai-os-lifecycle:ci"
NAME = f"ai-os-{uuid4().hex[:12]}"
VOLUME = f"ai-os-{uuid4().hex[:12]}"
KEY = secrets.token_urlsafe(32)
CRITICAL = {"kpi_error": 1.0, "retrieval_score": 0.0,
            "latency_dev": 1.0, "embedding_shift": 1.0}
STABLE = {"kpi_error": 0.0, "retrieval_score": 1.0,
          "latency_dev": 0.0, "embedding_shift": 0.0}


def docker(*args):
    return subprocess.run(["docker", *args], check=True, capture_output=True, text=True).stdout.strip()


def start(path="/data/observations.db"):
    docker("run", "-d", "--name", NAME, "-p", "127.0.0.1::8000", "-v", f"{VOLUME}:/data",
           "-e", f"AIOS_API_KEY={KEY}", "-e", f"AIOS_OBSERVATION_DB={path}", IMAGE)
    port = docker("port", NAME, "8000/tcp").rsplit(":", 1)[1]
    url = f"http://127.0.0.1:{port}"
    for _ in range(100):
        if docker("inspect", "-f", "{{.State.Running}}", NAME) == "false":
            raise RuntimeError("Container stopped before health became ready")
        try:
            request(url, "/health")
            return url
        except (urllib.error.URLError, ConnectionError):
            time.sleep(0.2)
    raise RuntimeError("Container health did not become ready")


def request(url, path, payload=None):
    body = None if payload is None else json.dumps(payload).encode()
    headers = {"x-api-key": KEY}
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url + path, data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=5) as response:
        return json.load(response)


def sql(command):
    script = (
        "import sqlite3; "
        "a=sqlite3.connect('file:/data/observations.db?mode=rw', uri=True); "
        + command
    )
    return docker("run", "--rm", "-v", f"{VOLUME}:/data", "--entrypoint", "python", IMAGE,
                  "-c", script)


def main():
    docker("info", "--format", "{{.ServerVersion}}")
    docker("volume", "create", VOLUME)
    try:
        # A container without an explicit database must stop instead of using memory.
        docker("run", "-d", "--name", NAME, "-e", f"AIOS_API_KEY={KEY}", IMAGE)
        for _ in range(100):
            if docker("inspect", "-f", "{{.State.Running}}", NAME) == "false":
                break
            time.sleep(0.2)
        else:
            raise RuntimeError("Container without database path did not stop")
        assert docker("inspect", "-f", "{{.State.ExitCode}}", NAME) != "0"
        docker("rm", NAME)

        docker("run", "-d", "--name", NAME, "-e", f"AIOS_API_KEY={KEY}",
               "-e", "AIOS_OBSERVATION_DB=relative.db", IMAGE)
        for _ in range(100):
            if docker("inspect", "-f", "{{.State.Running}}", NAME) == "false":
                break
            time.sleep(0.2)
        else:
            raise RuntimeError("Container with relative path did not stop")
        assert docker("inspect", "-f", "{{.State.ExitCode}}", NAME) != "0"
        docker("rm", NAME)

        url = start()
        critical = {**CRITICAL, "observation_id": str(uuid4())}
        first = request(url, "/agent/evaluate", critical)
        before = request(url, "/observability")
        assert before["anomaly"] is True and len(before["history"]) == 1
        assert request(url, "/agent/evaluate", critical) == first
        docker("restart", NAME)
        port = docker("port", NAME, "8000/tcp").rsplit(":", 1)[1]
        url = f"http://127.0.0.1:{port}"
        for _ in range(100):
            try:
                restored_state = request(url, "/observability")
            except (urllib.error.URLError, ConnectionError):
                time.sleep(0.2)
                continue
            assert restored_state == before
            break
        else:
            raise RuntimeError("Container restart did not restore observability")
        docker("stop", NAME)
        docker("rm", NAME)
        url = start()
        assert request(url, "/observability") == before
        # The online SQLite backup API creates a consistent copy of the mounted file.
        assert sql("b=sqlite3.connect('/data/backup.db'); a.backup(b); print(b.execute('PRAGMA integrity_check').fetchone()[0])") == "ok"
        assert sql("print(a.execute('PRAGMA integrity_check').fetchone()[0])") == "ok"
        assert sql("print(a.execute('SELECT count(*) FROM observations').fetchone()[0])") == "1"
        request(url, "/agent/evaluate", {**STABLE, "observation_id": str(uuid4())})
        assert request(url, "/observability")["anomaly"] is True
        docker("stop", NAME)
        docker("rm", NAME)
        url = start("/data/backup.db")
        assert request(url, "/observability") == before
        request(url, "/agent/evaluate", {**STABLE, "observation_id": str(uuid4())})
        assert request(url, "/observability")["anomaly"] is True
        request(url, "/agent/evaluate", {**STABLE, "observation_id": str(uuid4())})
        assert request(url, "/observability")["anomaly"] is False
        print("Container restart, recreation, backup, restore, integrity, and path check passed")
    finally:
        subprocess.run(["docker", "rm", "-f", NAME], capture_output=True)
        subprocess.run(["docker", "volume", "rm", VOLUME], capture_output=True)


if __name__ == "__main__":
    main()
