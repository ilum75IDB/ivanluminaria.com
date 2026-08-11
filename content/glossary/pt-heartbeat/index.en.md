---
title: "pt-heartbeat"
description: "Percona Toolkit tool that measures MySQL replication lag by writing timestamps on the master and comparing them on the slave. More reliable than Seconds_Behind_Master."
translationKey: "glossary_pt_heartbeat"
aka: "Percona Toolkit Heartbeat"
articles:
  - "/posts/mysql/mysql-slave-lag-diagnosi-e-fix-con-parallel-replication"
---

`pt-heartbeat` is a Percona Toolkit utility designed to measure MySQL replication lag directly and reliably. Unlike the native `Seconds_Behind_Master` metric — which can return misleading values when replication errors occur or the connection drops — `pt-heartbeat` measures actual delay by tracking data written on the master and read on the slave.

## How it works

The tool runs in two distinct modes, typically as separate long-running processes:

```bash
# On the master: writes a timestamp to a dedicated table every N seconds
pt-heartbeat --host=master-host --user=repl --password=secret \
  --database=percona --update --interval=1

# On the slave: reads the table and calculates the delta against current time
pt-heartbeat --host=slave-host --user=repl --password=secret \
  --database=percona --monitor --master-server-id=1
```

The `heartbeat` table (created automatically on first run) holds a timestamp kept current by the `--update` process. The `--monitor` process on the slave reads that value and computes the difference against local time: the result is the actual lag in seconds, with centisecond precision.

## When to use it

`pt-heartbeat` is the go-to tool for production alerting when `Seconds_Behind_Master` falls short. Typical scenarios include:

- **Broken replication**: `Seconds_Behind_Master` returns `NULL`, while `pt-heartbeat` keeps reporting the growing lag.
- **Multi-source replication or filtered replicas**: the native calculation can be inaccurate; the timestamp written on the master is a ground truth.
- **Monitoring system integration**: the `--monitor` output is parseable by Nagios, Prometheus (via exporter), or any bash script.

The main limitation is the dependency on an active process on the master: if the `--update` process stops, the measured lag grows indefinitely even when replication itself is healthy.
