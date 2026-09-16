# Manage streams

This topic describes the administrative tasks associated with managing streams.

## Enabling change tracking on views and underlying tables

In order for users to query change data on a view, change tracking must be enabled on the view and underlying tables.

Only the object owner (that is, the role with the OWNERSHIP privilege) on a given view or underlying tables can enable change tracking.

The following options are available to enable change tracking:

1. Create a stream on the view using the view owner role. This action enables change tracking on the view.

   If the same role also owns the underlying tables, change tracking is also enabled on the tables. Otherwise, the table owner must explicitly
   enable change tracking on the tables. For these steps, see [Explicitly Enable Change Tracking on the Underlying Tables](#explicitly-enable-change-tracking-on-the-underlying-tables) (in this topic).
2. Explicitly enable change tracking on the view and tables. For instructions, see the remaining instructions in this section.

### Explicitly enable change tracking on views

Set the CHANGE\_TRACKING parameter when creating a view (using CREATE VIEW) or later (using ALTER VIEW).

Note that change tracking must also be explicitly enabled on the underlying tables for a view. For instructions, see [Explicitly Enable
Change Tracking on the Underlying Tables](#explicitly-enable-change-tracking-on-the-underlying-tables) (in this topic).

For example, create a secure view in the current schema that selects a subset of rows from a table:

> Copy code
>
> ```
> CREATE SECURE VIEW v CHANGE_TRACKING = TRUE AS SELECT col1, col2 FROM t;
> ```

For example, modify an existing view to enable change tracking:

> Copy code
>
> ```
> ALTER VIEW v2 SET CHANGE_TRACKING = TRUE;
> ```

### Explicitly enable change tracking on the underlying tables

Important

When either creating or altering a view to specify CHANGE\_TRACKING, the associated dependent database objects are automatically
updated to enable change tracking. During the operation, the underlying resources are locked, which can cause latency for DDL/DML operations.
For more information, refer to [Resource locking](/sql-reference/transactions#label-txn-locking).

If the user executing the statement has not specified a role with sufficient permissions (OWNERSHIP),
the statement will fail, underlying database objects will not be updated, and locks will be released.

Set the CHANGE\_TRACKING parameter when creating a table (using CREATE TABLE) or later (using ALTER TABLE).

For example, to create a table in the current schema:

Copy code

```
CREATE TABLE t (col1 STRING, col2 NUMBER) CHANGE_TRACKING = TRUE;
```

For example, to modify an existing table to enable change tracking:

Copy code

```
ALTER TABLE t1 SET CHANGE_TRACKING = TRUE;
```

Important

When either creating or altering a TABLE to specify CHANGE\_TRACKING, the table is locked for the duration of the operation
which can cause latency for DML operations. For more information, refer to [Resource locking](/sql-reference/transactions#label-txn-locking).

## Avoiding stream staleness

To prevent a stream from becoming stale, consume the stream records within a DML
statement during the table’s retention period and regularly consume its change data
before its STALE\_AFTER timestamp (that is, within the extended data retention period
for the source object). Additionally, calling
[SYSTEM$STREAM\_HAS\_DATA](/sql-reference/functions/system_stream_has_data) on the stream prevents it from
becoming stale, provided the stream is empty and the SYSTEM$STREAM\_HAS\_DATA function
returns `FALSE`.

Important

When `SYSTEM$STREAM_HAS_DATA` returns `TRUE` for a stream, you should consume the stream in a DML operation, even if
the result is a false positive. If you don’t consume the stream, `SYSTEM$STREAM_HAS_DATA`
returns `TRUE`, and any tasks that use this function in their WHEN clause won’t skip execution. This results
in unnecessary task runs and associated warehouse charges.

To consume the stream efficiently when the result is a false positive — for example, querying the stream with
`SELECT COUNT(*) FROM stream_name` returns no records — use a statement like the following example:

Copy code

```
CREATE TEMPORARY TABLE _unused_table AS SELECT * FROM my_stream WHERE 1=0;
```

This statement consumes the stream, because `CREATE TABLE AS SELECT` is a DML transaction. The `WHERE 1=0` clause
filters out all data, so nothing gets processed. This advances the stream offset, and `SYSTEM$STREAM_HAS_DATA` returns
`FALSE` until new changes occur.

For more information on data retention periods, see [Understanding & using Time Travel](/user-guide/data-time-travel).

To view the data retention period for a stream, execute the [DESCRIBE STREAM](/sql-reference/sql/desc-stream)
or [SHOW STREAMS](/sql-reference/sql/show-streams) command. The `stale_after` column timestamp indicates when
the stream is currently predicted to become stale (or when it became stale, if the timestamp is in
the past). This timestamp is calculated by adding the larger of the
[DATA\_RETENTION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-data-retention-time-in-days) or [MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-max-data-extension-time-in-days) parameter
setting to the current timestamp. Note that if the timestamp is in the past, the stream might already
be stale. The `stale` column also indicates whether the stream is expected to be stale, though the
stream might not actually be stale yet.

Consuming the change data for a stream moves the STALE\_AFTER timestamp forward.

For more information, see [Data retention period and staleness](/user-guide/streams-intro#label-streams-staleness).

## View and manage streams in Snowsight

To view and manage a stream in Snowsight, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Explorer**.
3. For a specific database and schema, select **Streams** and select the stream you want to manage.

When viewing the stream in Snowsight, you can do the following:

- In the **Details** section, review the table name to which the stream applies, the type of stream, and whether or not the stream is stale.
- Review the SQL statement used to create the stream.
- Manage privileges on the stream. See [Manage object privileges with Snowsight](/user-guide/security-access-control-configure#label-snowsight-manage-object-privileges).
