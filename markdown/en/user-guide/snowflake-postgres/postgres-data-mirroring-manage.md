[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.
Currently, this feature is only available on Amazon Web Services (AWS) and Microsoft Azure.

# Manage and monitor mirrors

Use the procedures in the `snowflake.postgres` schema to alter, drop, inspect, and monitor mirrors after they’re created. These procedures take a mirror name but not an instance name;
mirror names are unique across all Postgres instances in the account, and the instance association is stored when the mirror is created.
To see all mirrors visible to the current role, or to find which instance a mirror belongs to, call `list_mirrors` without arguments:

Copy code

```
SELECT * FROM TABLE(SNOWFLAKE.POSTGRES.LIST_MIRRORS());
```

## Roles and permissions

Managing mirrors (create, alter, drop, inspect, monitor) requires the **`postgres_mirror_admin`**
application role on `snowflake.postgres`. `ACCOUNTADMIN` grants it to the role that manages
mirrors:

Copy code

```
GRANT APPLICATION ROLE snowflake.postgres_mirror_admin TO ROLE ACCOUNTADMIN;
```

The caller of every mirror management procedure must also own the source PostgreSQL instance.
The procedures verify this before doing any privileged work, so a user who holds
`postgres_mirror_admin` but doesn’t own the source instance can’t manage its mirrors.

For the role that governs reading mirrored data, see
[Query mirrored data](/user-guide/snowflake-postgres/postgres-data-mirroring-query#roles-and-permissions).

## Alter a mirror

Use `alter_mirror` to change the refresh interval, or to add or remove tables and schemas from
the mirror:

Copy code

```
CALL SNOWFLAKE.POSTGRES.ALTER_MIRROR(
    mirror_name      => 'orders_mirror',
    refresh_interval => '30 seconds',
    add_tables       => ['public.shipments'],
    remove_tables    => NULL,
    add_schemas      => NULL,
    remove_schemas   => NULL
);
```

Renaming a schema or table on PostgreSQL doesn’t require reconfiguring the mirror. The rename is
captured by the source extension and automatically applied to the target database.

## Drop a mirror

`drop_mirror` suspends the apply task and waits for any in-flight run to finish before removing the
mirror. It then removes all associated infrastructure: the CDC publication on the source Postgres
instance, the apply task, all mirrored target tables, the `<table>$changes` Iceberg change feeds,
and the `<MIRROR_NAME>_CATALOG_INTEGRATION` catalog integration that was auto-created when the
mirror was set up.

Copy code

```
CALL SNOWFLAKE.POSTGRES.DROP_MIRROR('orders_mirror');
```

The target database is left as an empty orphan. It can’t be reassigned to a new mirror (see
[Target database names can’t be reused](#target-database-names-cant-be-reused)). The target database
is owned by the `snowflake` application, so it can’t be dropped or modified directly. To drop it,
`ACCOUNTADMIN` can transfer ownership first:

Copy code

```
GRANT OWNERSHIP ON DATABASE POSTGRESMIRRORTOSNOWFLAKE TO ROLE ACCOUNTADMIN;
DROP DATABASE POSTGRESMIRRORTOSNOWFLAKE;
```

To drop the target database as part of `drop_mirror`, use `drop_target_database => TRUE`:

Copy code

```
CALL SNOWFLAKE.POSTGRES.DROP_MIRROR(mirror_name => 'orders_mirror', drop_target_database => TRUE);
```

Caution

Dropping the Snowflake target database while a mirror is still active orphans the mirror. The
apply task continues to run but fails on every attempt because its target no longer exists.
To recover, drop the orphaned mirror with `drop_mirror`, then create a new mirror with a fresh
`target_database` name.

### Drop is blocked by user-created Iceberg tables

If another role has created Iceberg tables in a different database that reference the mirror’s
`<MIRROR_NAME>_CATALOG_INTEGRATION`, `drop_mirror` fails:

Copy code

```
[4145] Catalog Integration <MIRROR_NAME>_CATALOG_INTEGRATION cannot be dropped because it has active table(s) using it. Some of those tables are not accessible by the current role.
```

The “not accessible by the current role” wording can be misleading: the blocking tables may be in a
database outside your current role’s privileges. To find them, run:

Copy code

```
SHOW ICEBERG TABLES IN ACCOUNT
  ->> SELECT "database_name", "schema_name", "name", "owner"
      FROM $1 WHERE "catalog_name" = '<MIRROR_NAME>_CATALOG_INTEGRATION';
```

Drop all tables that reference the catalog integration, then retry `drop_mirror`.

Tip

To keep teardown clean, query a mirror’s Iceberg change feed via a separate catalog integration
that you own rather than the mirror-managed `<MIRROR_NAME>_CATALOG_INTEGRATION`. That way, dropping
the mirror doesn’t affect your tables.

### Teardown order when dropping an instance

Each mirror’s `<MIRROR_NAME>_CATALOG_INTEGRATION` references the Postgres instance, so all mirrors must
be dropped before dropping the instance. Attempting to drop the instance first fails:

Copy code

```
Cannot drop Postgres instance <instance_name> because catalog integration(s) <MIRROR_NAME>_CATALOG_INTEGRATION still reference it.
```

Drop in this order:

Copy code

```
-- 1. Identify and drop any user-created Iceberg tables that reference the mirror's
--    catalog integration (see diagnostic query above)

-- 2. Drop each mirror (removes target tables, $changes feeds, and catalog integration)
CALL SNOWFLAKE.POSTGRES.DROP_MIRROR('<mirror_name>');

-- 3. Drop the Postgres instance
DROP POSTGRES INSTANCE "<instance_name>";

-- 4. Optional: drop the orphaned target database
DROP DATABASE <target_database>;
```

### Automatic cleanup of orphaned mirrors

If a Postgres instance is removed while mirrors still reference it, those mirrors are detected
and removed automatically. The target database is not removed automatically; drop it manually
when it’s no longer needed.

## Inspect mirrors

Use `describe_mirror` to check the configuration and runtime state of a specific mirror
(`error_message` contains the error from the most recent apply run, or NULL if the mirror is
healthy):

Copy code

```
CALL SNOWFLAKE.POSTGRES.DESCRIBE_MIRROR('orders_mirror');
```

Use `list_mirrors` to see mirrors on a specific Postgres instance, or call it without arguments
to list all mirrors visible to the current role:

Copy code

```
-- All mirrors on one instance:
CALL SNOWFLAKE.POSTGRES.LIST_MIRRORS('my_instance');

-- All mirrors in the account visible to the current role:
CALL SNOWFLAKE.POSTGRES.LIST_MIRRORS();
```

Use `list_mirrored_tables` to see the replication state of each table in a mirror:

Copy code

```
CALL SNOWFLAKE.POSTGRES.LIST_MIRRORED_TABLES('orders_mirror');
```

Each table has one of the following status indicators:

- **`SNAPSHOTTING`**: Snowflake is copying the current contents of the Postgres table into
  Snowflake for the first time.
- **`REPLICATING`**: The initial sync is complete and the mirror is continuously applying new
  changes from Postgres to Snowflake. This is the normal healthy state.

For full result column details, see [Mirror management procedures](/user-guide/snowflake-postgres/postgres-data-mirroring-reference#label-mirror-management-procedures).

## Monitor mirroring

The `describe_mirror` procedure surfaces a rolling window of recent apply runs in the
`recent_query_durations` column for a quick look at cadence and latency. Each apply run displays
a `state` of `SUCCEEDED`, `FAILED`, or `CANCELLED`.

For a full history, `ACCOUNTADMIN` can query Snowflake’s task history directly:

Copy code

```
SELECT name, state, scheduled_time, completed_time, error_code, error_message
FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.TASK_HISTORY(
    SCHEDULED_TIME_RANGE_START => DATEADD('hour', -24, CURRENT_TIMESTAMP()),
    RESULT_LIMIT => 100
))
WHERE name LIKE 'APPLY_MIRROR_%'
ORDER BY scheduled_time DESC;
```

The `query_admin_log` procedure exposes mirror-internal events with optional filters:

Copy code

```
CALL SNOWFLAKE.POSTGRES.QUERY_ADMIN_LOG(
    mirror_name       => 'orders_mirror',
    postgres_instance => 'my_instance',
    level             => 'ERROR',
    since_ts          => NULL,
    max_rows          => 500
);
```

If an apply task run fails, its error message is persisted on the mirror and surfaced by
`describe_mirror` and `list_mirrors`. The next successful run clears the error.

## Alert on mirror health

`describe_mirror` and `list_mirrors` support `TABLE(...)` syntax, so a
[Snowflake alert](https://docs.snowflake.com/en/user-guide/alerts) can watch them and notify you
when a mirror stops replicating. The same queries work from a Snowflake task or dashboard.

### Set up a mirror health alert

#### Grant the required privileges

The role that owns the alert must hold the `postgres_mirror_admin` application role and own the
source Postgres instance. The procedures only see mirrors on instances the caller owns:
`list_mirrors` silently returns nothing for other instances.

Copy code

```
USE ROLE ACCOUNTADMIN;
GRANT APPLICATION ROLE snowflake.postgres_mirror_admin TO ROLE mirror_ops;
GRANT EXECUTE ALERT ON ACCOUNT TO ROLE mirror_ops;
GRANT CREATE ALERT ON SCHEMA ops.public TO ROLE mirror_ops;
GRANT USAGE ON WAREHOUSE ops_wh TO ROLE mirror_ops;
```

#### Create a notification integration

Recipients must be verified email addresses of users in the account:

Copy code

```
CREATE NOTIFICATION INTEGRATION mirror_alert_email
  TYPE = EMAIL
  ENABLED = TRUE
  ALLOWED_RECIPIENTS = ('oncall@example.com');
GRANT USAGE ON INTEGRATION mirror_alert_email TO ROLE mirror_ops;
```

#### Create the alert

The condition fires when either of the following is true:

- `status = 'SUSPENDED'`: the apply task was suspended by `suspend_mirror` or auto-suspended
  after repeated failures.
- `error_message IS NOT NULL` and nothing has been processed for over an hour.
  Checking `last_operation_time` avoids firing for a transient error such as a lock timeout.

Copy code

```
USE ROLE mirror_ops;

CREATE OR REPLACE ALERT ops.public.mirror_health
  WAREHOUSE = ops_wh
  SCHEDULE = '10 MINUTE'
  IF (EXISTS (
      SELECT status, error_message, last_operation_time
      FROM TABLE(snowflake.postgres.describe_mirror('orders_mirror'))
      WHERE status = 'SUSPENDED'
         OR (error_message IS NOT NULL
             AND (last_operation_time IS NULL
                  OR last_operation_time < DATEADD('hour', -1, SYSDATE())))
  ))
  THEN CALL SYSTEM$SEND_EMAIL(
      'mirror_alert_email',
      'oncall@example.com',
      'Postgres mirror unhealthy',
      'Run: SELECT * FROM TABLE(snowflake.postgres.describe_mirror(''orders_mirror''));'
  );
```

#### Activate and verify the alert

Alerts are created suspended. Resume it, then run it once — conditions are validated at run time,
not at `CREATE ALERT`:

Copy code

```
ALTER ALERT ops.public.mirror_health RESUME;
EXECUTE ALERT ops.public.mirror_health;
```

Check what that run did:

Copy code

```
SELECT name, scheduled_time, state, action_state, error_message
FROM TABLE(INFORMATION_SCHEMA.ALERT_HISTORY(
    SCHEDULED_TIME_RANGE_START => DATEADD('hour', -24, CURRENT_TIMESTAMP())
))
ORDER BY scheduled_time DESC;
```

### Watch all mirrors

To watch every mirror instead of one, swap the `FROM` clause for
`TABLE(snowflake.postgres.list_mirrors())` and add `mirror_name` to the `SELECT`. Calling
`list_mirrors()` with no argument covers every mirror on every instance you own, including
mirrors created after the alert. The predicates are unchanged:

Copy code

```
SELECT mirror_name, status, error_message, last_operation_time
FROM TABLE(snowflake.postgres.list_mirrors())
WHERE status = 'SUSPENDED'
   OR (error_message IS NOT NULL
       AND (last_operation_time IS NULL
            OR last_operation_time < DATEADD('hour', -1, SYSDATE())))
```

Note

Don’t pass `NULL` to `list_mirrors` — an untyped `NULL` doesn’t resolve against the `STRING`
parameter and errors out.

### Tune the alert

- **Match the staleness threshold to `refresh_interval`.** Both procedures return
  `refresh_interval`, so you can derive the bound from it rather than hardcoding one value across
  mirrors with different cadences. A few multiples of the configured interval is a reasonable
  starting point.
- **Exclude mirrors you suspend deliberately**, to avoid being alerted by your own maintenance.
- **Don’t schedule the alert below `min(refresh_interval, 2 minutes)`.** That’s how often the
  apply task runs, so below that threshold the alert re-reads the same state on every evaluation.

### What the alert doesn’t check

- **A non-`ACTIVE` status isn’t treated as a failure.** A failing mirror usually stays `ACTIVE`
  while the apply task retries, so `status` alone isn’t a reliable failure signal. See
  [Mirror auto-suspend after repeated failures](#label-mirror-auto-suspend).
- **`STARTING` status.** A new mirror is legitimately `STARTING` until its first operation is
  applied, so a bare `STARTING` test fires on every `create_mirror`.
- **A missing apply task.** `status` is `NULL` when `describe_mirror` can’t find the mirror’s
  apply task, and `= 'SUSPENDED'` doesn’t match `NULL`. `create_mirror` always creates the task,
  so add `status IS NULL OR` to the `WHERE` clause only if you’ve seen one go missing.
- **An initial copy that never finished.** `STARTING` means the mirror has processed nothing yet,
  but neither procedure returns a creation timestamp. Record when the mirror first appeared and
  alert once it’s been `STARTING` longer than a full copy should take. `list_mirrored_tables`
  shows which table is holding up a slow initial copy.
- **A stall with no error.** If the source stops delivering changes, `status` stays `ACTIVE` and
  `error_message` stays `NULL`. Monitor `last_operation_time` and the lag figures in
  `postgres_status`. See [Monitor the source side](#label-alert-source-side).
- **`recent_query_durations` has a short window.** Its 20-slot history fills at the 2-minute
  task cadence, covering roughly 40 minutes. Count runs where `state LIKE 'FAILED%'` rather than
  looking for a streak — backoff-skipped runs are recorded as successes and break streaks up.

### Suppress repeat notifications

The alert fires on every evaluation where the condition matches, so a mirror broken for a day
sends 144 identical emails. To suppress repeats, record what you’ve already notified about and
exclude it from the condition.

Create a table to track notifications:

Copy code

```
CREATE TABLE ops.public.mirror_notified (
    mirror_name STRING, breach_kind STRING,
    first_seen  TIMESTAMP_NTZ, last_seen TIMESTAMP_NTZ
);
```

Add a `NOT EXISTS` check to the condition’s `WHERE` clause, keeping the existing predicates in
a group:

Copy code

```
AND NOT EXISTS (
    SELECT 1 FROM ops.public.mirror_notified n
    WHERE n.mirror_name = 'orders_mirror' AND n.breach_kind = 'UNHEALTHY'
)
```

On the `list_mirrors` variant, alias the procedure call and qualify both sides of the
comparison:

Copy code

```
AND NOT EXISTS (
    SELECT 1 FROM ops.public.mirror_notified n
    JOIN TABLE(snowflake.postgres.list_mirrors()) m ON n.mirror_name = m.mirror_name
    WHERE n.breach_kind = 'UNHEALTHY'
)
```

The action then has to both notify and record, so it becomes a procedure.
`GET_CONDITION_QUERY_UUID()` gives it access to the row the condition matched:

Copy code

```
CREATE OR REPLACE PROCEDURE ops.public.notify_mirror_breaches()
RETURNS STRING
LANGUAGE SQL
EXECUTE AS CALLER
AS
BEGIN
    LET condition_query STRING := SNOWFLAKE.ALERT.GET_CONDITION_QUERY_UUID();

    LET body STRING := (SELECT 'status: '          || status ||
                               ', last error: '     || COALESCE(error_message, 'none') ||
                               ', last processed: ' || COALESCE(last_operation_time::STRING, 'never')
                        FROM TABLE(RESULT_SCAN(:condition_query)));

    CALL SYSTEM$SEND_EMAIL('mirror_alert_email', 'oncall@example.com',
                           'Postgres mirror orders_mirror unhealthy', :body);

    INSERT INTO ops.public.mirror_notified
    VALUES ('orders_mirror', 'UNHEALTHY', SYSDATE(), SYSDATE());

    RETURN 'notified';
END;
```

Nothing clears those rows once a mirror recovers, so a second alert or a task has to remove
them. When writing the clearing logic:

- **Wait for more than one healthy observation before clearing.** A single evaluation that reads
  the mirror as healthy mid-recovery would clear the suppression state and allow the next
  evaluation to page for an outage that’s already being worked.
- **Anchor on `last_operation_time`, not a trailing window of task runs.** Whether the oldest
  run in a fixed lookback is older than some threshold depends on where the task’s schedule
  lands and flips between evaluations.

### Monitor the source side

The columns described on this page report the Snowflake side: the apply task and what it has
processed. A source-side problem shows up there only once it starves apply of work, which looks
the same as an idle source.

`describe_mirror` also returns `postgres_status`, read live from the source, so a condition can
test the source side without a session on the Postgres instance. `slot_lag_bytes` grows when the
CDC worker falls behind. It’s a subset of the `snowflake_cdc.publication_health` view, which has
the rest: worker PID, error detail, and per-table snapshot state.

For alert debugging, see [Troubleshoot mirrors](/user-guide/snowflake-postgres/postgres-data-mirroring-troubleshooting#label-alert-debug).

## Suspend and resume mirroring

You have two options when suspending a Postgres instance that has active mirrors: leave the mirror
running, or explicitly suspend it first. The two approaches have different effects on replication
continuity and the `$changes` feed.

### Suspend the instance without pausing the mirror

If you suspend the Postgres instance without calling `SUSPEND_MIRROR`, the apply task keeps
running and mirrored tables continue to show a status of `REPLICATING`. Once all buffered changes
that were already recorded in cloud storage are merged, no further data is applied until the instance
resumes. No action is needed on the mirror side.

When you resume the instance, mirroring picks up from where it left off. No re-snapshot is
performed, and the `$changes` feed retains the full incremental history of inserts, updates,
and deletes.

### Suspend the mirror before suspending the instance

To stop apply task activity entirely while the instance is suspended, call `SUSPEND_MIRROR`
before suspending:

Copy code

```
CALL SNOWFLAKE.POSTGRES.SUSPEND_MIRROR('orders_mirror');
```

After resuming the Postgres instance, restart the mirror:

Copy code

```
CALL SNOWFLAKE.POSTGRES.RESTART_MIRROR('orders_mirror');
```

Caution

`RESTART_MIRROR` performs a full re-snapshot of all mirrored tables. The `$changes` 7-day feed
is rebuilt from a fresh snapshot baseline: every row appears with `_CHANGE_TYPE = 'S'` (snapshot),
and incremental change history is lost. Change-feed consumers that rely on the `$changes` feed
lose continuity across a `RESTART_MIRROR` call.

By default, any queued-but-unapplied operations in the source-side metalog are preserved
(soft restart). Pass `truncate_feed => TRUE` to truncate the metalog first, discarding those
queued operations before rebuilding (hard restart). Use a hard restart only for recovery
scenarios where the apply state has diverged significantly from the source.

`$changes` continuity is not guaranteed in general. Schema changes on mirrored tables also
rebuild the feed.

### Mirror auto-suspend after repeated failures

Snowflake automatically suspends a mirror’s apply task if it has been failing continuously for
approximately 96 hours. The 96-hour window is designed to surface a silently failing mirror
before unapplied change records age out on the source side (which happens at 7 days), and covers
a Friday-to-Monday outage with time left for investigation.

When a mirror is auto-suspended, `describe_mirror` shows the mirror as suspended and includes the
error from the most recent failed apply run.

Once you’ve resolved the underlying problem, restart the mirror:

Copy code

```
-- Soft restart (default): re-snapshots all tables; preserves any queued operations in the source metalog
CALL SNOWFLAKE.POSTGRES.RESTART_MIRROR('orders_mirror');

-- Hard restart: re-snapshots all tables AND truncates the source-side metalog first.
-- Use when the apply state has diverged significantly from the source.
CALL SNOWFLAKE.POSTGRES.RESTART_MIRROR('orders_mirror', truncate_feed => TRUE);
```

## Troubleshooting

For solutions to common issues, see [Troubleshoot mirrors](/user-guide/snowflake-postgres/postgres-data-mirroring-troubleshooting).
