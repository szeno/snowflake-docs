# Snowflake Postgres logging

All Postgres servers on Snowflake Postgres instances log locally to syslog. The log data is collected
from there and sent to your account’s active
[event table](/developer-guide/logging-tracing/event-table-setting-up). In addition to logs,
Snowflake Postgres automatically collects instance-level metrics (CPU, memory, disk, network, and
Postgres-specific counters). For details, see [Snowflake Postgres metrics](/user-guide/snowflake-postgres/postgres-metrics).

## Retrieving Postgres log data

To view the Postgres logs for a given instance, query the event table for the TIMESTAMP field and the MESSAGE portion of the VALUE field of
the records with `record_type = 'LOG'` using the initial portion of the instance’s hostname, aka the instance ID (or `cluster_id`).
For example, this will pull the last 10 minutes of log entries for instance with id `oyrpb2cwtvbu5al5vtbyrsnkgy`:

Copy code

```
SELECT TIMESTAMP, VALUE:MESSAGE as log_line
FROM SNOWFLAKE.TELEMETRY.EVENTS
WHERE resource_attributes['snowflake.o11y.logtype'] = 'postgres-otelcol-vm-agent'
  AND resource_attributes['instance.id'] = 'oyrpb2cwtvbu5al5vtbyrsnkgy'
  AND record_type = 'LOG'
  AND TIMESTAMP > CURRENT_TIMESTAMP() - INTERVAL '10 MINUTES'
LIMIT 100;
```

Note

The above query uses the account default event table, SNOWFLAKE.TELEMETRY.EVENTS. If you have set up a custom event table, you should
adjust the query appropriately.

Each row of the output will contain a single log-line entry that was logged by the Postgres server on the given Snowflake Postgres instance
with the timestamp when it was originally logged. Note that it can take up to a few minutes between the time Postgres makes a log entry
and it is available in the event table.

## Understanding Postgres log-line interleaving

Note that Postgres uses multi-line logging and since multiple Postgres server processes will be making log entries
concurrently, full log entries from different Postgres server processes will often be interleaved. For example, let’s consider these log line
entries:

**Postgres log lines example**

| timestamp | log\_line |
| --- | --- |
| 2025-12-09 23:16:38.760 | “[14-1] [1592908][client backend][27/2][0] [user=snowflake\_admin,db=postgres,app=psql] [34.214.158.144] ERROR: canceling statement due to user request” |
| 2025-12-09 23:16:38.760 | “[10-1] [1593992][not initialized][][0] [user=[unknown],db=[unknown],app=[unknown]] [34.214.158.144] LOG: connection received: host=34.214.158.144 port=46114” |
| 2025-12-09 23:16:38.760 | “[14-2] [1592908][client backend][27/2][0] [user=snowflake\_admin,db=postgres,app=psql] [34.214.158.144] STATEMENT: select pg\_sleep(10);” |
| 2025-12-09 23:16:43.007 | “[15-1] [1592908][client backend][27/3][0] [user=snowflake\_admin,db=postgres,app=psql] [34.214.158.144] LOG: AUDIT: SESSION,2,1,MISC,SHOW,,,show log\_min\_duration\_statement,<not logged>” |

Expand

Show lessSee more

In each log line entry:

- The first bracketed values are the command number for the session that ran the command and the log line for that command separated by a hyphen.
  For example, [1-1] and [1-2] would be two log lines from the first command run in a session.
- The second bracketed value is the process ID (pid) for the session that logged the line. Postgres uses a process-based (vs. thread-based) concurrency
  model so each session is run on its own server process.

In this example, you can see that:

- Command 14 was run by the session with pid `1592908` as the cancellation of a `select pg_sleep(10);` query.
- Logging of command 14 by pid `1592908` added two log lines, [14-1] and [14-2].
- A single log line from the 10th command run by the session with pid `1593992` ended up between the two lines from command 14 on
  pid `1592908`.
- The next command run by the session with pid `1592908` was a `show log_min_duration_statement` query and required only one log line,
  [15-1].

Tip

The Postgres log line format is determined by its [log\_line\_prefix](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-LINE-PREFIX)
server setting, which defaults to ‘[%p][%b][%v][%x] %q[user=%u,db=%d,app=%a] [%h]’ on Snowflake Postgres instances.
