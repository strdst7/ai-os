"""Exercise real ENOSPC on an isolated 16 MiB Docker tmpfs volume.

Run only on an approved disposable host with adequate disk headroom.
"""

import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
from uuid import uuid4

import container_lifecycle as lifecycle


def inside(code):
    return subprocess.run(
        ["docker", "exec", lifecycle.NAME, "python", "-c", code],
        check=True, capture_output=True, text=True, timeout=30,
    ).stdout.strip()


def main():
    if os.environ.get("AIOS_RUN_ENOSPC_TEST") != "1":
        raise RuntimeError("Set AIOS_RUN_ENOSPC_TEST=1 only on an approved disposable Docker host")
    if shutil.disk_usage("/").free < 4 * 1024 ** 3:
        raise RuntimeError("At least 4 GiB free space is required before the Docker test")
    lifecycle.docker("info", "--format", "{{.ServerVersion}}")
    lifecycle.docker("volume", "create", "--driver", "local", "--opt", "type=tmpfs",
                     "--opt", "device=tmpfs", "--opt", "o=size=16m", lifecycle.VOLUME)
    try:
        url = lifecycle.start()
        critical = {**lifecycle.CRITICAL, "observation_id": str(uuid4())}
        lifecycle.request(url, "/agent/evaluate", critical)
        before = lifecycle.request(url, "/observability")
        assert before["anomaly"] is True
        mount = inside("""with open('/proc/self/mountinfo') as mounts:
    print(next(line.split(' - ', 1)[1].split()[0] for line in mounts if line.split()[4] == '/data'))
""")
        assert mount == "tmpfs", f"Refusing to fill non-tmpfs mount: {mount}"
        assert inside("""import os
stat = os.statvfs('/data')
print(stat.f_blocks * stat.f_frsize)
""") == str(16 * 1024 ** 2), "Refusing unexpected volume capacity"

        # Fill only the disposable tmpfs, never a host or production volume.
        filled = inside("""import errno, os
with open('/data/filler', 'wb', buffering=0) as out:
    try:
        while True:
            out.write(b'x' * 65536)
    except OSError as error:
        assert error.errno == errno.ENOSPC, error
print(os.statvfs('/data').f_bavail)
""")
        assert filled == "0", filled
        attempt = {**lifecycle.STABLE, "observation_id": str(uuid4())}
        request = json.dumps(attempt).encode()
        # urllib raises HTTPError for 500. A 200 response is an unsafe false success.
        try:
            with urllib.request.urlopen(urllib.request.Request(
                url + "/agent/evaluate", data=request,
                headers={"x-api-key": lifecycle.KEY, "Content-Type": "application/json"}), timeout=10) as response:
                raise AssertionError(f"Full-volume write reported success: HTTP {response.status}")
        except urllib.error.HTTPError as error:
            assert error.code >= 500, error.code
        assert lifecycle.request(url, "/observability") == before

        backup_result = inside("""import sqlite3
try:
    with sqlite3.connect('/data/observations.db') as source, sqlite3.connect('/data/backup.db') as backup:
        source.backup(backup)
except sqlite3.OperationalError as error:
    assert 'full' in str(error).lower() or 'open database' in str(error).lower(), error
    print('backup_failed')
else:
    raise AssertionError('Backup unexpectedly succeeded on full volume')
""")
        assert backup_result == "backup_failed"
        inside("import os; os.unlink('/data/filler')")
        assert inside("""import sqlite3
with sqlite3.connect('file:/data/observations.db?mode=rw', uri=True) as db:
    assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    print(db.execute('SELECT count(*) FROM observations').fetchone()[0])
""") == "1"
        assert lifecycle.request(url, "/observability") == before
        lifecycle.request(url, "/agent/evaluate", attempt)
        after = lifecycle.request(url, "/observability")
        assert len(after["history"]) == 2 and after["anomaly"] is True
        assert inside("""import sqlite3
with sqlite3.connect('/data/observations.db') as db:
    print(db.execute('PRAGMA integrity_check').fetchone()[0])
""") == "ok"
        assert inside("""import sqlite3
with sqlite3.connect('/data/observations.db') as source, sqlite3.connect('/data/backup.db') as backup:
    source.backup(backup)
    print(backup.execute('PRAGMA integrity_check').fetchone()[0])
""") == "ok"
        print("ENOSPC write and backup failed; API rejected write; integrity and recovery passed")
    finally:
        subprocess.run(["docker", "rm", "-f", lifecycle.NAME], capture_output=True)
        subprocess.run(["docker", "volume", "rm", lifecycle.VOLUME], capture_output=True)


if __name__ == "__main__":
    main()
