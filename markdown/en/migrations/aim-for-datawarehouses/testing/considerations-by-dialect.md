# Considerations by source dialect

Testing executes each object on both sides — on the source (to capture a baseline) and on Snowflake (to validate). Both executions run in isolation so tests never leave a permanent change behind. How that isolation is achieved, and the privileges it requires, depends on the source dialect. This page documents the behavior as implemented today. For the overall flow, see [Testing stored procedures and UDFs](/migrations/aim-for-datawarehouses/testing/sprocs-and-udfs).

## Snowflake target-side isolation (all dialects)

Regardless of source, the Snowflake side of every test runs against a **per-run zero-copy clone** of the workload database (`CREATE DATABASE … CLONE`), which is dropped on teardown. This lets procedures that modify data (DML) run against real data without mutating it, and it also captures non-table state such as stages, sequences, and file formats.

Because of this, the Snowflake role running tests needs **`CREATE DATABASE ON ACCOUNT`**. The Snowflake AIM Agent for Data Warehouses probes for this privilege when you opt into testing and stops with the exact grant to apply if it’s missing.

Note

A backup-and-restore Snowflake isolation strategy (no `CREATE DATABASE` required) also exists and is used for BTEQ-script validation. Clone isolation is the default for procedure and UDF testing.

## Source-side isolation by dialect

The framework picks a source isolation strategy per dialect, and — for some dialects — per object, based on whether the procedure contains a `COMMIT`.

| Dialect | Read-only / no-COMMIT procedures | Procedures containing `COMMIT` (DML) |
| --- | --- | --- |
| **SQL Server** | Transaction rollback (default). Optional database **snapshot isolation**. | Backup-and-restore of affected tables + delta-undo. Requires snapshot isolation enabled on the source database. |
| **Amazon Redshift** | Transaction rollback. | Backup-and-restore of affected tables + delta-undo. |
| **Oracle** | `SAVEPOINT`-based transaction rollback. | **Not yet supported** — a `COMMIT` in the procedure body invalidates the savepoint. |
| **Teradata** | Backup-and-restore of affected tables + delta-undo (always — Teradata sub-transaction semantics prevent transaction rollback from working). | Backup-and-restore of affected tables + delta-undo (same path). |

Expand

Show lessSee more

Warning

**Oracle DML procedures.** Oracle procedures that issue `COMMIT` cannot be tested today; a backup-and-restore isolation provider is required first. Read-only Oracle procedures and functions test normally.

## Required privileges

### Snowflake side

The role used by your Snowflake connection needs, at minimum:

- `USAGE` on the shared `SNOWCONVERT_AI` database and `CREATE SCHEMA` on it (first run only, to provision `SNOWCONVERT_AI.TESTING`).
- `READ, WRITE` on the `@SNOWCONVERT_AI.TESTING.BASELINES` stage (baselines are stored in Snowflake).
- `USAGE` on the workload database, `SELECT` on its tables, and `USAGE` on its procedures and functions.
- **`CREATE DATABASE ON ACCOUNT`** for clone-based isolation.
- `USAGE, OPERATE` on the warehouse used to run validation.

The Snowflake AIM Agent for Data Warehouses surfaces the exact `GRANT` block if any check fails; apply it out-of-band and say “recheck” to re-probe.

### Source side

The source login must be able to (a) execute every procedure under test and (b) read every table those procedures touch. DML isolation adds a few dialect-specific requirements:

**SQL Server**

Copy code

```
GRANT EXECUTE ON SCHEMA::<SCHEMA> TO <LOGIN>;
GRANT SELECT  ON SCHEMA::<SCHEMA> TO <LOGIN>;
-- Snapshot isolation is used to capture DML deltas atomically:
ALTER DATABASE <DB> SET ALLOW_SNAPSHOT_ISOLATION ON;
ALTER DATABASE <DB> SET READ_COMMITTED_SNAPSHOT ON WITH NO_WAIT;
```

**Amazon Redshift**

Copy code

```
GRANT USAGE ON SCHEMA <schema> TO <user>;
GRANT SELECT ON ALL TABLES IN SCHEMA <schema> TO <user>;
GRANT EXECUTE ON ALL PROCEDURES IN SCHEMA <schema> TO <user>;
-- Transaction-based isolation needs nothing extra.
```

**Oracle**

Copy code

```
GRANT CONNECT, RESOURCE TO <USER>;
GRANT SELECT ON <SCHEMA>.<TABLE> TO <USER>;       -- per table
GRANT EXECUTE ON <SCHEMA>.<PROCEDURE> TO <USER>;  -- per proc / package
-- Or, less granular:
GRANT SELECT ANY TABLE, EXECUTE ANY PROCEDURE TO <USER>;
```

**Teradata**

Copy code

```
GRANT SELECT  ON <DATABASE> TO <USER>;
GRANT EXECUTE PROCEDURE ON <DATABASE> TO <USER>;
-- Backup/restore isolation creates short-lived database copies;
-- the user needs CREATE DATABASE on the parent database:
GRANT CREATE DATABASE ON <PARENT_DATABASE> TO <USER>;
```

## Related content

- [Testing overview](/migrations/aim-for-datawarehouses/testing/overview) — strategies and when to use each.
- [Testing stored procedures and UDFs](/migrations/aim-for-datawarehouses/testing/sprocs-and-udfs) — the capture/validate/fix-loop flow.
