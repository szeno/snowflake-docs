# Custom incrementalization

When standard refresh modes (INCREMENTAL, FULL) can’t express your transformation, custom
incrementalization lets you write MERGE or INSERT logic that Snowflake executes on each refresh.
You define exactly how changes reach the dynamic table: Snowflake handles scheduling, retries,
and transactional guarantees.

## When to use custom incrementalization

Consider custom incrementalization when SELECT-based dynamic tables can’t express the transformation
you need.

| Aspect | SELECT-based dynamic tables | Custom incremental dynamic tables |
| --- | --- | --- |
| Logic type | Declarative SELECT | Imperative MERGE or INSERT |
| Incremental strategy | Auto-inferred by Snowflake | User-defined |
| Semantics | Delayed-view equivalence | User-defined (no system guarantee) |
| Best for | Transformations expressible as SELECT | CDC with deletes, stream-static joins, audit trails |
| Migration from streams and tasks | Requires rewrite to SELECT | Accepts single-statement MERGE or INSERT patterns |

Expand

Show lessSee more

Scenarios suited to custom incrementalization:

1. **Query not expressible as SELECT:** Stream-static joins, time-range deduplication logic, or
   conditional branching that a single SELECT can’t capture.
2. **Explicit control over update and delete semantics:** Soft-deletes, conditional updates,
   or merge logic where you need to decide per-row whether to update, delete, or skip.
3. **User-defined output semantics:** Audit trails, accumulators, or point-in-time snapshots.
4. **State reuse and memoization:** Accumulate intermediate results across refreshes to avoid
   re-scanning historical data. For example, maintain a running top-K leaderboard by combining
   previous results with new changes. See
   [Top-K leaderboard](/user-guide/dynamic-tables/design-patterns#label-dynamic-tables-patterns-top-k).
5. **Migrating from streams and tasks:** Single-statement MERGE or INSERT patterns port
   directly into `REFRESH USING`. You gain managed scheduling and monitoring without
   rewriting to SELECT. Pipelines that use stored procedures or multi-statement
   transactions require restructuring into a single supported DML statement.

## Syntax

Copy code

```
CREATE [ OR REPLACE ] DYNAMIC TABLE <name> (
  <col_name> <col_type> [ , ... ]
)
  TARGET_LAG = { '<time_spec>' | DOWNSTREAM }
  WAREHOUSE = <warehouse_name>
  [ REFRESH_MODE = { AUTO | CUSTOM_INCREMENTAL } ]
  [ INITIALIZE = ON_SCHEDULE ]
  [ BACKFILL FROM <table_name> ]
  [ START AT ({ STREAM => '<stream_name>' | TIMESTAMP => <timestamp> | STATEMENT => <query_id> | OFFSET => -<seconds> }) ]
  REFRESH USING ( <dml_statement> )
```

Key requirements:

- An explicit column list is required. Snowflake can’t infer the schema from DML.
- `REFRESH_MODE = AUTO` resolves to `CUSTOM_INCREMENTAL` when `REFRESH USING` is present.
- Only one DML statement is allowed per `REFRESH USING` block (no multi-statement transactions).

### MERGE INTO SELF

Use `MERGE INTO SELF` when you need to update or delete existing rows in addition to inserting
new ones. `SELF` refers to the dynamic table being created, and you can alias it.

Copy code

```
REFRESH USING (
  MERGE INTO SELF [AS <target_alias>]
  USING (
    SELECT ...
    FROM <source> CHANGES( [INFORMATION => { DEFAULT | APPEND_ONLY }] ) [AS <alias>]
    [ JOIN <table> ON ... ]
    [ WHERE ... ]
    [ QUALIFY ... ]
  ) AS <source_alias>
  ON <join_condition>
  [ WHEN MATCHED [ AND ... ] THEN { UPDATE SET ... | DELETE } ] [...]
  [ WHEN NOT MATCHED [ AND ... ] THEN INSERT (...) VALUES (...) ]
)
```

You can read `SELF` in the `USING` subquery to join incoming changes with current contents of
the dynamic table. You can’t reference the dynamic table by its object name inside
`REFRESH USING`.

### INSERT INTO SELF

Use `INSERT INTO SELF` for append-only patterns where you don’t need to modify existing rows.

Copy code

```
REFRESH USING (
  INSERT INTO SELF
  SELECT ...
  FROM <source> CHANGES( [ INFORMATION => { DEFAULT | APPEND_ONLY } ] ) [AS <alias>]
  [ JOIN <table> ON ... ]
  [ WHERE ... ]
)
```

`INSERT INTO SELF` only appends rows. Use `MERGE` when you need to update or delete existing rows.

### The CHANGES clause

The `CHANGES` clause replaces stream semantics. Snowflake automatically binds the change interval
to refresh boundaries, so you don’t specify time bounds (`AT`, `BEFORE`, `END`).

Constraints:

- You can’t use `CHANGES` on `SELF` (Snowflake returns an error).
- Base tables must have [change tracking enabled](/user-guide/streams-intro). Creating a custom incremental dynamic table attempts to enable change tracking on the base tables.
- You can’t specify time bounds: the interval is managed automatically by Snowflake.

`INFORMATION` modes control which change types are visible:

If `INFORMATION` isn’t specified, the `DEFAULT` mode is used (for example, `CHANGES()`).

- `DEFAULT`: Inserts, updates, and deletes.
- `APPEND_ONLY`: Inserts only.

Metadata columns available in the change set:

| Column | Description |
| --- | --- |
| METADATA$ACTION | `'INSERT'` or `'DELETE'` (updates appear as a DELETE + INSERT pair) |
| METADATA$ISUPDATE | `TRUE` if the row is part of an UPDATE operation |

Expand

Show lessSee more

Use `SELECT * EXCLUDE (METADATA$ACTION, METADATA$ISUPDATE)` to strip metadata columns before
insertion.

### The SELF keyword

`SELF` has two roles inside `REFRESH USING`:

- **Write target:** `MERGE INTO SELF` or `INSERT INTO SELF`.
- **Read source:** `FROM SELF AS cur` in the `USING` subquery reads the current contents of the
  dynamic table.

You can’t reference the dynamic table by its object name inside `REFRESH USING`. Use `SELF`
exclusively. `CHANGES()` on `SELF` is not allowed.

### BACKFILL FROM and START AT

These clauses control how the dynamic table is initially populated and where subsequent refreshes
begin reading changes.

Without `BACKFILL FROM`, the initial refresh runs your `REFRESH USING` statement against the full
change history of the source. Because `CHANGES()` treats all existing rows as INSERTs on the initial
run, the initial refresh effectively replays every row in the source through your MERGE or INSERT
logic. For large base tables, this can be expensive and slow.

`BACKFILL FROM` provides a faster alternative: Snowflake populates the dynamic table by cloning from
an existing table without executing the `REFRESH USING`
logic. Subsequent refreshes then process only new changes that arrive after the backfill.

| Configuration | Initial population | Subsequent refresh start |
| --- | --- | --- |
| Neither (default) | Initial refresh processes all existing source rows as INSERTs through REFRESH USING | From creation time |
| `BACKFILL FROM <table>` | Cloned from the backfill table (bypasses REFRESH USING) | From creation time |
| `BACKFILL FROM` + `START AT` | Cloned from the backfill table (bypasses REFRESH USING) | From the START AT point |

Expand

Show lessSee more

`START AT` accepts four options:

- `TIMESTAMP => <timestamp>`: A specific point in time.
- `STATEMENT => <query_id>`: The point after a specific query completed.
- `STREAM => <stream_name>`: The current offset of an existing stream.
- `OFFSET => -<seconds>`: A negative offset in seconds from the current time.

`BACKFILL FROM` and `START AT` can only be set at creation time. You can’t add or change them via
`ALTER DYNAMIC TABLE` or `CREATE OR ALTER DYNAMIC TABLE`.

## Examples

### Append-only enrichment with stream-static join (INSERT INTO)

This example enriches new click events with page metadata. The `clicks` table is append-only,
and `pages` is a static dimension table.

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_enriched_clicks (
  click_id INT,
  user_id INT,
  page_title STRING,
  section STRING,
  click_ts TIMESTAMP
)
  TARGET_LAG = '1 minute'
  WAREHOUSE = transform_wh
  REFRESH USING (
    INSERT INTO SELF
    SELECT c.click_id, c.user_id, p.page_title, p.section, c.click_ts
    FROM clicks CHANGES(INFORMATION => APPEND_ONLY) AS c
    LEFT OUTER JOIN pages AS p ON c.page_id = p.page_id
  );
```

Only new clicks since the last refresh are processed. The LEFT OUTER JOIN enriches each click
with its page title and section without re-scanning historical data. For a full CDC variant
that handles updates and deletes using MERGE, see
[Stream-static join with full CDC](/user-guide/dynamic-tables/design-patterns#label-dynamic-tables-patterns-stream-static-join).

### Audit deletes log (INSERT INTO)

This example captures standalone deletes from a `users` table into an audit log, filtering out
the DELETE half of updates.

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_deletions_log (
  id INT,
  name STRING,
  email STRING
)
  TARGET_LAG = '1 minute'
  WAREHOUSE = transform_wh
  INITIALIZE = ON_SCHEDULE
  REFRESH USING (
    INSERT INTO SELF
    SELECT * EXCLUDE (METADATA$ISUPDATE, METADATA$ACTION)
    FROM users CHANGES(INFORMATION => DEFAULT)
    WHERE NOT METADATA$ISUPDATE AND METADATA$ACTION = 'DELETE'
  );
```

The `DEFAULT` information mode exposes all change types (inserts, updates, deletes). The WHERE
clause keeps only standalone deletes by excluding rows where `METADATA$ISUPDATE` is TRUE.
`EXCLUDE` strips the metadata columns before insertion.

### Incremental aggregation on append-only changes

This example maintains a running total of player scores. Each refresh sums only the new rows
and adds them to existing totals.

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE dt_player_scores (
  player_id INT,
  total_score INT
)
  TARGET_LAG = '1 minute'
  WAREHOUSE = transform_wh
  REFRESH USING (
    MERGE INTO SELF AS tgt
    USING (
      SELECT player_id, SUM(score) AS batch_score
      FROM match_results CHANGES(INFORMATION => APPEND_ONLY)
      GROUP BY player_id
    ) AS src
    ON tgt.player_id = src.player_id
    WHEN MATCHED THEN
      UPDATE SET tgt.total_score = tgt.total_score + src.batch_score
    WHEN NOT MATCHED THEN
      INSERT (player_id, total_score) VALUES (src.player_id, src.batch_score)
  );
```

Existing players get their score updated by adding the batch total. New players are inserted
with their first batch score. This avoids re-scanning the entire `match_results` history on
every refresh.

Because this example uses `APPEND_ONLY` mode, only inserts are processed.
Deletes and updates in the source are ignored.
If you need to handle deletes, use `DEFAULT` mode instead.

## Usage notes

- Each refresh executes as a single autocommit transaction. If the REFRESH USING statement fails, the entire refresh rolls back.
- If data retention expires on a base table queried through `CHANGES()` before the next refresh, the refresh fails. Set retention periods on those tables to exceed your longest expected refresh gap.
- Custom incremental dynamic tables don’t automatically derive primary keys. To enable downstream dynamic tables or streams to consume changes efficiently, [add a RELY primary key constraint manually](/user-guide/dynamic-tables/input-data-optimization).
- MERGE operations are subject to standard [nondeterminism rules](/sql-reference/sql/merge#label-merge-example-deterministic-nondeterministic). If multiple source rows match the same target row, the result is nondeterministic. Add deduplication (such as `ROW_NUMBER()` with `QUALIFY`) to guarantee deterministic results.
- Objects outside a `CHANGES()` clause (such as dimension tables in JOINs) are read at their state at the refresh snapshot time, not incrementally.
- The `CHANGES(INFORMATION => APPEND_ONLY)` clause gives custom incremental dynamic tables native append-only semantics. Dynamic tables that use a SELECT-based definition don’t support this directly.

### RELY primary key and CHANGES() behavior

With `CHANGES(INFORMATION => DEFAULT)`, how Snowflake identifies rows in `CHANGES()` output depends on whether the base table has a RELY primary key:

| Base table configuration | Row identity | Effect on CHANGES() |
| --- | --- | --- |
| No RELY primary key | Internal row tracking | A DELETE then INSERT of the same values appear as two separate change rows |
| With RELY primary key | Primary key value | A DELETE then INSERT of the same key value cancel out (net zero change) |

Expand

Show lessSee more

If delete-then-insert of the same row should be invisible to your merge logic (for example, arising from INSERT OVERWRITE), add `RELY` to the primary key constraint so that Snowflake can compact these pairs before they reach `CHANGES()`.

`CHANGES(INFORMATION => APPEND_ONLY)` in a custom incremental dynamic table never uses primary keys for row identity.

## Limitations

- No dbt or DCM integration. Use `CREATE OR ALTER` to update custom incremental dynamic table definitions.
- Only `CREATE OR ALTER` can modify the `REFRESH USING` definition and properties (such as [`TARGET_LAG`](/user-guide/dynamic-tables/target-lag)).
- Upstream schema changes cause the next refresh to fail with a compile error. If the upstream object was altered (not replaced or dropped), use `CREATE OR ALTER` with an updated `REFRESH USING` definition to recover. The next refresh continues from the last successful refresh. If the upstream used `CREATE OR REPLACE`, change tracking is broken and you must recreate the downstream with `CREATE OR REPLACE`.
- [Frozen regions (`FROZEN WHERE`)](/user-guide/dynamic-tables/frozen-regions) and `INSERT ONLY INPUTS` can’t be combined with `REFRESH USING`.
- Cloning: if a custom incremental dynamic table’s base tables are swapped after it has refreshed, the cloned table doesn’t refresh. Refresh the clone source first (manually if needed), then clone.
- Replication has the following limitations:
  - Custom incremental dynamic tables and their base tables in different failover groups aren’t supported.
  - Replication of custom incremental dynamic tables with Apache Iceberg™ base tables, or of custom incremental dynamic tables that are themselves dynamic Iceberg tables, isn’t supported.
  - If a custom incremental dynamic table’s base tables are swapped or recreated, the replica is usable only after up to two replication refresh cycles.

### Supported data types

Custom incremental dynamic tables support all [Snowflake SQL data types](/sql-reference/intro-summary-data-types)
in the column list and in `REFRESH USING` DML, except:

- [Structured data types](/sql-reference/data-types-structured) (structured OBJECT, structured ARRAY, and MAP).
  Semi-structured types (VARIANT, OBJECT, ARRAY without a defined schema) are fully supported.
- `INTERVAL` types.
- Geospatial types in the `MERGE` `ON` clause. `GEOGRAPHY` and `GEOMETRY` are supported as projected
  columns, but you can’t use them in `MERGE INTO SELF ... ON`: direct equality
  (for example, `tgt.geo_col = source.geo_col`) and geospatial functions such as `ST_EQUALS` aren’t
  supported in `REFRESH USING`. Use a non-geospatial join key (for example, a primary key column) instead.

### User-defined functions

Custom incremental dynamic tables support scalar UDFs in `REFRESH USING`, subject to the following constraints:

- A SQL UDF whose body contains a subquery isn’t supported.
- For the query in the `CHANGES()` clause, any non-SQL scalar UDF (Python, Java, JavaScript, or Scala) must be marked [`IMMUTABLE`](/sql-reference/sql/create-function#label-create-function-volatile-immutable).
- Table functions (UDTFs) aren’t supported in `REFRESH USING`.

Only mark a function `IMMUTABLE` if it always returns the same output for the same input. Snowflake doesn’t validate this, and incorrect use can produce wrong results.

Replacing an `IMMUTABLE` UDF that the dynamic table or an upstream view depends on can break subsequent refreshes. Recreate the dynamic table after replacing the UDF.

### Iceberg base tables and CHANGES()

The following table summarizes `CHANGES()` support when the base table is an Iceberg table.

| When this applies | `CHANGES(INFORMATION => DEFAULT)` | `CHANGES(INFORMATION => APPEND_ONLY)` |
| --- | --- | --- |
| Snowflake-managed Iceberg V2 base table | Supported. If external engines wrote to the table since the last refresh: supported; unchanged rows appear as delete+insert pairs ([copy-on-write](/user-guide/tables-iceberg-manage#label-iceberg-merge-on-read-behavior)). | Supported. If external engines wrote to the table since the last refresh: unsupported (refresh will fail). |
| Snowflake-managed Iceberg V3 base table | Supported. | Supported. If external engines wrote to the table since the last refresh: unsupported (refresh will fail). |
| Iceberg V2 base table with an external catalog | Supported only with `RELY` on the source primary key. | Unsupported. |
| Iceberg V3 base table with an external catalog | Supported. | Unsupported. |

Expand

Show lessSee more

For the same external-engine write behavior on streams over Snowflake-managed Iceberg tables, see [Streams limitations](/user-guide/streams-intro#label-stream-limitations).

## What’s next

- [Design patterns](/user-guide/dynamic-tables/design-patterns): More examples including full
  CDC MERGE and SELF-read patterns.
- [Migrate from streams and tasks](/user-guide/dynamic-tables/migrate-streams-tasks): Move
  existing stream-task pipelines to dynamic tables.
- [Streams and change tracking](/user-guide/streams-intro): How change tracking works in
  Snowflake.
- [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table): Full SQL reference.
