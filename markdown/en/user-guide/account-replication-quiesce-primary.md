# Quiesce a primary failover group

You can put a primary failover group into read-only mode as part of a planned
disaster recovery (DR) drill or account migration. Read-only mode prevents new writes to the
objects in the failover group on the source account, ensuring that no data changes occur on the
primary while you coordinate a final replication refresh and failover.

Note

Be sure to review the [Constraints when a primary failover group is in read-only mode](#label-quiesce-primary-fg-constraints) section before using this feature.

## Understanding the need for read-only mode

For planned DR drills and account migrations, you need to ensure zero data loss during failover.
The standard workflow is the following:

- Stop all writes to the source (primary) account.
- Perform a final replication refresh from source to target.
- Promote the target failover group to primary.

Without a first-class mechanism to stop writes to a primary failover group, you typically resort
to error-prone workarounds such as disabling users, revoking privileges, killing running jobs,
and suspending tasks and pipes individually. These workarounds are difficult to coordinate, risk
missing in-flight transactions, and provide no clear observability signal that the source has
been quiesced.

Read-only mode for primary failover groups addresses these problems with a single, atomic
operation that does the following:

- Prevents new DDL and DML writes to objects in the failover group.
- Suppresses background workloads (tasks, pipes, alerts, streams) on the primary.
- Is fully reversible without requiring a failover.
- Is visible to both the source and target accounts using
  [SHOW FAILOVER GROUPS](/sql-reference/sql/show-failover-groups), so the DR operator on the
  target can confirm the source is quiesced before triggering the final refresh and promote.

## Workflow when using read-only mode

The following steps represent the typical sequence of events for a planned DR drill or account
migration that uses read-only mode:

1. The DR admin runs `ALTER FAILOVER GROUP <name> SET READ_ONLY = TRUE` on the source (primary)
   account to quiesce writes.
2. The DR admin terminates any in-flight queries that target objects in the failover group.
   Setting read-only mode doesn’t proactively cancel running queries; uncommitted writes fail
   at commit time, but long-running writers can keep consuming compute until the DR admin
   cancels them. See [Step 2: Terminate in-flight queries against the failover group](#label-quiesce-terminate-queries).
3. On the target account, the DR admin runs `ALTER FAILOVER GROUP <name> REFRESH` to perform a
   final refresh from the read-only primary.
4. On the target account, the DR admin promotes the target. The source becomes a standard
   read-only secondary; the `read_only` flag on the original primary is cleared because the
   failover group is no longer the primary.
5. Application traffic is redirected to the new primary (using Client Redirect or DNS or
   application configuration).

If the drill is being performed without failing over the failover group, the DR admin runs
`ALTER FAILOVER GROUP <name> UNSET READ_ONLY` on the source to restore the primary to
read-write mode. Tasks, pipes, alerts, and other objects that change state resume automatically.

## Prerequisites for read-only mode

- The failover group must be a *primary* failover group on the account where the command is executed.
- The user must have OWNERSHIP or the FAILOVER privilege on the failover group (the same
  privileges required for `ALTER FAILOVER GROUP ... PRIMARY`).

## Configuring read-only mode

This section walks through the end-to-end DR drill flow: setting read-only mode on the source,
quiescing in-flight work, and refreshing and promoting the failover group on the target. To
restore a primary to read-write mode without performing a failover, run
`ALTER FAILOVER GROUP <name> UNSET READ_ONLY` on the source account.

### Access control requirements

Refer to the [Replication privileges](/user-guide/account-replication-considerations#label-replication-privileges)
topic to see the roles required to perform replication and failover operations.

### Step 1: Set the primary failover group to read-only

On the source (primary) account, run the following command:

Copy code

```
ALTER FAILOVER GROUP myfg SET READ_ONLY = TRUE;
```

After this command succeeds:

- New DDL and DML statements that target objects in the failover group fail.
- Tasks, pipes, and alerts whose database is in the failover group are not scheduled. Any
  existing tasks or alerts that are already scheduled to run are still triggered, but fail to
  execute because of the read-only state.
- Read operations (SELECT, SHOW, DESCRIBE) on objects in the failover group continue to work
  normally.

### Step 2: Terminate in-flight queries against the failover group

Setting read-only mode doesn’t proactively cancel queries that are already running. Uncommitted
writes fail at commit time. Cancel any in-flight queries that target objects in the failover
group:

Copy code

```
-- Cancel all queries related to your database(s) in your failover group
SHOW DATABASES IN FAILOVER GROUP myfg;

SELECT SYSTEM$CANCEL_QUERY(q.query_id)
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY()) q
WHERE q.execution_status = 'RUNNING'
  AND q.database_name IN (SELECT "name" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())));
-- Note: both statements must be executed in the same session
```

### Step 3: Refresh the failover group on the target account

On the target account, perform a final refresh from the read-only primary so the target has
the most up-to-date data before promotion:

Copy code

```
ALTER FAILOVER GROUP myfg REFRESH;
```

### Step 4: Promote the failover group on the target account

On the target account, promote the target to make it the new primary. Choose one of the
following options based on the type of drill:

- **Read-only failover (drill only)**: Promote only the connection object so that client
  traffic is redirected to the target account, but the failover group on the target remains a
  secondary. Use this option to validate client redirection without committing to a full
  failover.

  Copy code

  ```
  ALTER CONNECTION myconn PRIMARY;
  ```
- **Read-write failover (full failover)**: Promote both the connection object and the failover
  group so that the target becomes the new primary for both client traffic and data writes.

  Copy code

  ```
  ALTER CONNECTION myconn PRIMARY;
  ALTER FAILOVER GROUP myfg PRIMARY;
  ```

After the failover group is promoted on the target, the source becomes a standard secondary
and the `read_only` flag on the original primary is cleared. You don’t need to run
`ALTER FAILOVER GROUP ... UNSET READ_ONLY` on the source.

## Behavior

### Write blocking

When a primary failover group is in read-only mode, all DDL and DML operations that target
objects within the failover group are blocked. Enforcement matches the behavior on a secondary
(non-primary) replica:

- New statements fail at compile time as an early rejection.
- In-flight transactions that began before the read-only flag was set continue executing, but
  fail at commit time. Any changes made by such a transaction aren’t visible outside the
  session in which the transaction ran.

### Background workloads

Background workloads on the primary are suppressed in the same way they are on a secondary
replica.

- **User tasks**: Tasks aren’t scheduled for execution while the failover group is read-only.
  Task scheduling resumes automatically when read-only is unset.
- **Pipes (Snowpipe)**: Pipes become read-only. Ingest queue processing skips them. Pipe
  activation resumes automatically when read-only is unset.
- **Alerts**: Alerts aren’t scheduled for execution while the failover group is read-only.
  Alert scheduling resumes automatically when read-only is unset.
- **Streams**: Stream state advancement is skipped. DML that targets a stream inside the
  failover group fails with the read-only error. Reading from a stream (without consuming it)
  continues to work.

### Read operations

All read operations (SELECT, SHOW, DESCRIBE, and so on) continue to work normally on a
read-only primary. Read-only mode only blocks write operations.

### Failover while in read-only mode

When `ALTER FAILOVER GROUP <name> PRIMARY` is executed on the target account while the source
is in read-only mode:

- The target becomes the new primary and is read-write.
- The source transitions from read-only primary to a standard secondary replica. The
  `read_only` flag is cleared because the failover group is no longer primary.

No special handling is needed beyond the existing failover steps, because the source was
already blocking writes before the failover.

### Reversibility

UNSET READ\_ONLY restores the primary failover group to full read-write mode. Background
workloads resume. New transactions can write normally. In-flight read transactions are
unaffected.

## Observability

[SHOW FAILOVER GROUPS](/sql-reference/sql/show-failover-groups) and
[SHOW REPLICATION GROUPS](/sql-reference/sql/show-replication-groups) include a `read_only`
column:

| Column | Type | Description |
| --- | --- | --- |
| `read_only` | BOOLEAN | `TRUE` when the primary failover group is in read-only mode. `FALSE` when the primary failover group is in read-write mode. |

Expand

Show lessSee more

The column is visible from both the source and target accounts. Use it to verify that the
source has been quiesced before triggering a final refresh and promote.

## Constraints when a primary failover group is in read-only mode

The following operations are blocked while a primary failover group is in read-only mode:

- Modifying the membership of the failover group with
  `ALTER FAILOVER GROUP ... ADD <database|share>` or
  `ALTER FAILOVER GROUP ... REMOVE <database|share>`. Unset read-only mode before changing
  membership.
- Any DDL or DML that targets objects within the failover group, including tables, schemas,
  views, streams, tasks, pipes, alerts, and stages.

The following operations are allowed while a primary failover group is in read-only mode:

- `ALTER FAILOVER GROUP ... RENAME TO`. Renaming the failover group is metadata-only DDL on
  the failover group itself.
- `ALTER FAILOVER GROUP ... SET REPLICATION_SCHEDULE`. Changing the replication schedule is
  metadata-only DDL on the failover group itself.
- `ALTER FAILOVER GROUP ... PRIMARY` on the target account. The failover proceeds normally;
  the source transitions to a standard secondary.
- `ALTER FAILOVER GROUP ... REFRESH` on the target account. The final refresh reads from the
  read-only primary.
- All read operations on objects in the failover group.

## Known limitations

The following limitations apply:

- **In-flight transactions aren’t proactively canceled**: Transactions that begin before
  `SET READ_ONLY = TRUE` continue to execute but are rejected at commit time. Snowflake
  doesn’t actively kill running queries when read-only mode is set. Customers who require an
  immediate cut-off can use
  [SYSTEM$ABORT\_SESSION](/sql-reference/functions/system_abort_session) or
  [SYSTEM$ABORT\_TRANSACTION](/sql-reference/functions/system_abort_transaction) to terminate
  long-running writers manually.
- **Dynamic table refreshes aren’t suppressed automatically**: Setting the primary failover
  group to read-only doesn’t stop dynamic table refreshes from being attempted. Snowflake
  retries each refresh up to five times; all attempts fail because of the read-only state,
  after which the dynamic table’s refresh schedule is suspended. Unsetting read-only mode
  doesn’t automatically resume dynamic table refreshes; you must resume them manually.

## Examples

### Planned DR drill or migration

The following example mirrors the end-to-end flow described in
[Configuring read-only mode](#label-quiesce-configuring).

Copy code

```
-- Step 1: On source account (X) - set the primary failover group to read-only
ALTER FAILOVER GROUP myfg SET READ_ONLY = TRUE;

-- Step 2: On source account (X) - terminate in-flight queries against the failover group
SHOW DATABASES IN FAILOVER GROUP myfg;

SELECT SYSTEM$CANCEL_QUERY(q.query_id)
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY()) q
WHERE q.execution_status = 'RUNNING'
  AND q.database_name IN (SELECT "name" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())));

-- Step 3: On target account (Y) - refresh the failover group
ALTER FAILOVER GROUP myfg REFRESH;

-- Step 4: On target account (Y) - promote the target to primary
-- For read-only failover (drill only): promote only the connection object
ALTER CONNECTION myconn PRIMARY;

-- For read-write failover (full failover): promote both the connection object and the failover group
ALTER CONNECTION myconn PRIMARY;
ALTER FAILOVER GROUP myfg PRIMARY;
```
