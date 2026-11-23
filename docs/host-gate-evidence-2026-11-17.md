# Host gate evidence, 2026-11-17

Raw evidence for the three verified gates in [api-host-decision.md](api-host-decision.md).
Collected on `peakybuildr` against drill guest 158 `aios-drill`. The API image was built
from this repository's `Dockerfile`.

This file records what the commands returned. It is not a claim that the API is deployed.

## Environment

```
host        peakybuildr  100.122.194.34  pve-manager/9.2.11 (kernel 7.0.14-15-pve)
guest       158 aios-drill   LXC, Debian 13.6, unprivileged, 2 vCPU, 2 GB
rootfs      local-lvm:vm-158-disk-0, 8G
/data       /fourtera/aios-158-data  ->  /dev/mapper/fourtera-vm--158--data (ext4, rw)
volume      fourtera/vm-158-data  10.00g   (fourtera VG on the 3.6 TB sdb)
image       ai-os:local  built from Dockerfile, digest prefix e692d755696e
```

Guest config line that creates the mount:

```
mp0: /fourtera/aios-158-data,mp=/data
```

## Gate 1 — Host volume

Mount and ownership:

```
$ lvs fourtera/vm-158-data -o lv_name,vg_name,lv_size,lv_attr
  LV          VG       LSize  Attr
  vm-158-data fourtera 10.00g -wi-ao----

$ findmnt -T /fourtera/aios-158-data -o TARGET,SOURCE,FSTYPE,OPTIONS
/fourtera/aios-158-data /dev/mapper/fourtera-vm--158--data ext4 rw,relatime

$ pct exec 158 -- findmnt -T /data -o TARGET,SOURCE,FSTYPE,OPTIONS
/data  /dev/mapper/fourtera-vm--158--data ext4 rw,relatime

$ stat -c '%U:%G %a' /fourtera/aios-158-data      # host view
100000:100000 755
$ pct exec 158 -- stat -c 'guest: %U:%G %a %n' /data
guest: root:root 755 /data
$ pct exec 158 -- stat -c 'db:    %U:%G %a %n' /data/observations.db
db:    root:root 644 /data/observations.db
```

Restart, then recreate on the same volume. `history`, `current` and `anomaly` were
byte-identical before and after both operations, and `PRAGMA integrity_check` returned `ok`.

```
before restart:   {'current': {'observation_id': '37027938-…', 'ADSI': 1.0, …
after restart:    {'current': {'observation_id': '37027938-…', 'ADSI': 1.0, …
RESTART_IDENTICAL=yes
after recreate:   {'current': {'observation_id': '37027938-…', 'ADSI': 1.0, …
RECREATE_IDENTICAL=yes
live integrity: ok
```

The first attempt failed with `sqlite3.OperationalError: unable to open database file`
because `/data` was `nobody:nogroup 755`. Fixed with `chown 100000:100000` on the host
path; an unprivileged guest maps uid 100000 to root.

## Gate 2 — Backup schedule

```
$ systemctl list-timers aios-backup.timer
NEXT                         LEFT     LAST PASSED UNIT               ACTIVATES
Wed 2026-11-18 02:30:00 +08  5h 22min -    -      aios-backup.timer aios-backup.service

$ findmnt -T /srv/aios-backup -o SOURCE,FSTYPE -n
/dev/mapper/pve-root ext4          # different device from the fourtera LV holding /data
```

A run started through the unit, so the scheduled path is what executed:

```
2026-11-17T21:02:26+08:00 OK backup=/srv/aios-backup/observations-20261117T210226.db bytes=28672
```

Forced write failure against an unwritable destination:

```
exit=1
2026-11-17T21:06:52+08:00 ERROR backup_write_failed src=/fourtera/aios-158-data/observations.db dest=/srv/bkro/observations-20261117T210652.db
```

Retention is 7 files, pruned oldest-first. Backup uses `sqlite3 .backup`, not `cp`,
so it is consistent against a live database.

A `chmod 500` test did **not** work as a failure simulation, because root ignores
directory permissions. The immutable-destination run above is the real error-path test.

## Gate 3 — Restore drill

```
$ sqlite3 /srv/aios-backup/observations-20261117T210226.db ".backup '/srv/aios-restore-isolated/observations.db'"
$ sqlite3 /srv/aios-restore-isolated/observations.db 'PRAGMA integrity_check'
ok
```

The restored copy was attached to a second container on port 18001, separate from the
live one on 18000:

```
restored anomaly: False history: 9
history identical: True
current identical: True
anomaly identical: True
PASS
live source untouched: rows 9 integrity ok
```

UUID replay: the restored database carried the same observation UUIDs as the live
database without re-running any write, and each stored row replays identically
because `monitoring_service.evaluate` returns the stored report for a known
`observation_id` when the telemetry fingerprint matches.

The first restore attempt failed with `attempt to write a readonly database`: the copy
was `root:root 644`. A restored database must be owned by uid 100000 before the
container may open it read-write.

## Gate 4 — Disk monitoring (partial)

```
$ df --output=pcent /fourtera | tail -1
21%
$ /usr/local/bin/aios-disk-alert.sh
2026-11-17T20:56:40+08:00 ok disk_use=21% threshold=80%
$ # threshold forced below measured capacity
2026-11-17T20:56:40+08:00 ALERT disk_use=21% threshold=1% volume=fourtera FORCED-PROOF
```

The threshold and the backup-write error path are proven. **No delivery channel exists**,
so an alert writes to a local log and reaches nobody. The gate is `Partial` for that reason.

## What this evidence does not cover

- No guest is sized or appointed for the API. Guest 158 is a drill guest.
- No alert reaches a person.
- No independent security review exists.
- The image was built and run; it is not deployed, and nothing listens beyond loopback.

## Reproduce

```bash
# on peakybuildr
pct exec 158 -- docker run -d --name aios-gate -p 127.0.0.1:18000:8000 \
  -v /data:/data -e AIOS_API_KEY=<32+ char key> \
  -e AIOS_OBSERVATION_DB=/data/observations.db ai-os:local
systemctl start aios-backup.service && tail -1 /srv/aios-alerts/backup.log
```

## Drill footprint left on the host

The drill needed root on `peakybuildr`. These changes remain and need an operator decision
to keep or remove. They were not created by an automated pipeline and are not part of the API.

| Item | Status |
| --- | --- |
| Guest 158 `aios-drill` and LV `fourtera/vm-158-data` (10 GB) | Keep until the gate record is reviewed; remove with `pct destroy 158` and `lvremove fourtera/vm-158-data` |
| Containers `aios-gate` (18000) and `aios-restore` (18001) in guest 158 | Leftover from the drill; remove with `pct exec 158 -- docker rm -f aios-gate aios-restore` |
| `/srv/aios-backup` (5 backup files) and `/srv/aios-alerts` (alert and backup logs) | Evidence; keep |
| `/srv/aios-restore-isolated` | Isolated restore copy; safe to remove |
| `/srv/bkro` | Temporary unwritable-destination probe; remove if present |
| `/usr/local/bin/aios-backup.sh`, `/usr/local/bin/aios-disk-alert.sh`, `aios-backup.timer`/`.service` | Drill monitoring only; not the API's alerting |
| `chown 100000:100000` on `/fourtera/aios-158-data` | Required for an unprivileged guest to write `/data`; keep |

No production storage was filled. The forced threshold and the immutable-directory probe
ran against the drill volume and a throwaway directory only. Guest 157 and its Collabora
container were never touched.

An earlier cleanup attempt was blocked before it ran, and a later attempt could not reach
the host because Tailscale SSH required interactive re-authentication. The rows above are
therefore stated as present, not as removed.
