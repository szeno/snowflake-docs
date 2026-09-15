# Use streams on dynamic tables

A [stream](/user-guide/streams) on a dynamic table captures row-level inserts, updates, and
deletes. Each read returns the net changes since the previous read. This lets you bridge a dynamic table pipeline into targets that
dynamic tables can’t reach on their own, such as stored procedures, external API calls, or
conditional logic in a task.

This example assumes you have an existing dynamic table named `dt_orders` that uses an incremental
refresh. See [Create a dynamic table](/user-guide/dynamic-tables/create) for setup guidance.

Important

Use the ON DYNAMIC TABLE syntax when creating the stream. ON TABLE doesn’t work with dynamic
tables and returns an error. See [Common error](#label-dynamic-tables-streams-common-error) for an
example.

Copy code

```
CREATE OR REPLACE STREAM dt_orders_stream ON DYNAMIC TABLE dt_orders;
```

## Supported stream types

Streams on dynamic tables support only the standard (delta) type. The standard stream captures
inserts, updates, and deletes as net changes since the stream was last read.

Copy code

```
CREATE STREAM ... ON DYNAMIC TABLE <name>
```

APPEND\_ONLY is not supported for streams on dynamic tables. If you need
insert-only semantics, consume the standard stream and filter on `METADATA$ACTION = 'INSERT'` in
your downstream task. Alternatively, [custom incremental dynamic tables](/user-guide/dynamic-tables/custom-incrementalization)
support append-only semantics natively through the `CHANGES(INFORMATION => APPEND_ONLY)` clause.

Note

The dynamic table must use an incremental refresh. Dynamic tables that use a full refresh don’t
support streams because each refresh replaces the entire table output, so there is no incremental
change history to track. If REFRESH\_MODE is set to AUTO, verify the resolved mode by running
`SHOW DYNAMIC TABLES` and checking the `refresh_mode` column before creating a stream.

## When to use this pattern

The primary use case is a hybrid pipeline where a dynamic table handles the declarative definition
and a triggered task handles imperative work the dynamic table can’t express:

**Dynamic table -> stream -> triggered task -> target**

Common scenarios:

- Writing to a non-dynamic-table target (regular table, external stage).
- Calling a stored procedure or external function with side effects.
- Running conditional logic (IF/ELSE, loops) on the change set.

Use SYSTEM$STREAM\_HAS\_DATA in the task’s WHEN clause so the task fires only when the stream has
unconsumed changes. The task runs after the dynamic table refreshes and produces new output. A
refresh that changes no rows doesn’t trigger the task.

Copy code

```
-- Create a triggered task that consumes the stream
CREATE OR REPLACE TASK load_completed_orders
  WAREHOUSE = transform_wh
  WHEN SYSTEM$STREAM_HAS_DATA('dt_orders_stream')
AS
  INSERT INTO completed_orders_archive
  SELECT order_id, customer_id, order_date, product_name, line_total
  FROM dt_orders_stream
  WHERE order_status = 'completed';
```

If multiple tasks consume the same dynamic table, create a separate stream for each. See [Introduction to streams](/user-guide/streams-intro) for details.

## Stream behavior after reinitialization

When a dynamic table [reinitializes](/user-guide/dynamic-tables/modify#label-dynamic-tables-evolving-reinitialization-triggers) (for example,
after a CREATE OR REPLACE on a base table, a masking policy change, or a change-tracking toggle),
the stream survives but its next read can return a much larger set of change rows than a normal
refresh produces. The stream remains attached and exposes all row-level differences between its last-read offset and the reinitialized output.

Warning

After reinitialization, rows that were previously updates will appear as DELETE + INSERT pairs with
METADATA$ISUPDATE set to FALSE. Downstream logic that relies on METADATA$ISUPDATE to distinguish
real deletes from updates can lose or duplicate data without an error. Use idempotent MERGE statements
rather than conditional INSERT/DELETE branching to handle this safely.

The following MERGE handles both normal changes and the DELETE + INSERT pairs that appear after
reinitialization. The three clauses cover deletes, updates, and inserts by matching on the primary
key:

Copy code

```
MERGE INTO completed_orders_archive t
USING (
    SELECT order_id, customer_id, order_date, product_name, line_total,
           METADATA$ACTION,
           METADATA$ISUPDATE
    FROM dt_orders_stream
    WHERE order_status = 'completed'
) s ON t.order_id = s.order_id
WHEN MATCHED
    AND s.METADATA$ACTION = 'DELETE'
    AND NOT s.METADATA$ISUPDATE THEN
    DELETE
WHEN MATCHED
    AND s.METADATA$ACTION = 'INSERT' THEN
    UPDATE SET t.customer_id  = s.customer_id,
               t.order_date   = s.order_date,
               t.product_name = s.product_name,
               t.line_total   = s.line_total
WHEN NOT MATCHED
    AND s.METADATA$ACTION = 'INSERT' THEN
    INSERT (order_id, customer_id, order_date, product_name, line_total)
    VALUES (s.order_id, s.customer_id, s.order_date, s.product_name, s.line_total);
```

After reinitialization, every surviving row appears as a DELETE + INSERT pair with
`METADATA$ISUPDATE = FALSE`. The MERGE processes each pair correctly: Clause 1 removes the old row,
Clause 3 re-inserts it. The net effect is the same data, with no duplicates or data loss. For normal
changes, Clause 2 handles updates in place.

Design your downstream task to handle these large change sets gracefully. Use idempotent inserts or
batch processing so that a post-reinitialization read doesn’t cause duplicate or missing data.

## Limitation: streams capture net changes, not full history

Don’t use a stream on a dynamic table as an audit log. If a row is inserted and then updated within a single
refresh cycle, the stream shows only the final state. If the stream is not read between two
refreshes, the changes from both refreshes collapse into a single net result.

If you need every state transition for compliance or auditing, write directly to an append-only
table from your ingestion layer instead. See [Introduction to streams](/user-guide/streams) for
more on how streams track changes.

## Verify the stream

After creating the stream, confirm it is attached and not stale:

Copy code

```
SHOW STREAMS LIKE 'dt_orders_stream';
```

```
+--------------------+---------------+---------------+--------------+-------+-------+
| name               | database_name | schema_name   | source_type  | mode  | stale |
|--------------------+---------------+---------------+--------------+-------+-------|
| DT_ORDERS_STREAM  | MY_DB         | PUBLIC        | Dynamic Table| DEFAULT| false |
+--------------------+---------------+---------------+--------------+-------+-------+
```

Output columns are truncated for readability. Check the `stale` column to confirm the stream is
active. If `stale` shows `true`, the stream has fallen behind the dynamic table’s change history
and must be recreated. To prevent staleness, make sure the stream is read regularly within the data
retention period. See [Introduction to streams](/user-guide/streams) for details on stream
staleness.

## Common error

Using ON TABLE instead of ON DYNAMIC TABLE returns an error:

Copy code

```
-- Incorrect: ON TABLE doesn't work with dynamic tables
CREATE OR REPLACE STREAM dt_orders_stream ON TABLE dt_orders;
```

```
002203 (42601): SQL compilation error:
Object found is of type 'DYNAMIC_TABLE', not specified type 'TABLE'.
```

To create a stream on a dynamic table, use the ON DYNAMIC TABLE syntax:

Copy code

```
-- Correct syntax
CREATE OR REPLACE STREAM dt_orders_stream ON DYNAMIC TABLE dt_orders;
```

## Required privileges

To create a stream on a dynamic table, your role needs:

- CREATE STREAM on the schema.
- SELECT on the dynamic table.

For the full list of access control requirements, see [CREATE STREAM](/sql-reference/sql/create-stream).

## What’s next

- To learn how dynamic table refreshes work, see [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes).
- To monitor refresh health for the upstream dynamic table, see
  [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring).
- To troubleshoot refresh failures that affect streams, see
  [Troubleshoot dynamic table refresh issues](/user-guide/dynamic-tables/troubleshoot-refreshes).
- For the full stream SQL reference, see [CREATE STREAM](/sql-reference/sql/create-stream).
