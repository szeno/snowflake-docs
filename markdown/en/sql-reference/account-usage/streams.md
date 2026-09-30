Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# STREAMS view

This Account Usage view displays a row for each stream in the account.

See also:
:   [SHOW STREAMS](/sql-reference/sql/show-streams)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| STREAM\_ID | NUMBER | Internal, Snowflake-generated identifier for the stream. |
| STREAM\_NAME | VARCHAR | Name of the stream. |
| STREAM\_SCHEMA\_ID | NUMBER | Internal, Snowflake-generated identifier for the schema that contains the stream. |
| STREAM\_SCHEMA | VARCHAR | Name of the schema that contains the stream. |
| STREAM\_CATALOG\_ID | NUMBER | Internal, Snowflake-generated identifier for the database that contains the stream. |
| STREAM\_CATALOG | VARCHAR | Name of the database that contains the stream. |
| OWNER | VARCHAR | Name of the role that owns the stream. |
| COMMENT | VARCHAR | Comment for the stream. |
| TABLE\_NAME | VARCHAR | Fully qualified name of the stream’s source object (for example, a table or view). |
| SOURCE\_TYPE | VARCHAR | Type of the source object that the stream is defined on. Examples: `Table`, `View`, `External Table`, `Stage`. |
| BASE\_TABLES | VARCHAR | Underlying base table or tables whose changes the stream tracks. A stream on a view can list more than one base table. |
| TYPE | VARCHAR | Type of the stream. Currently, `DELTA` is the only value. |
| MODE | VARCHAR | Displays `APPEND_ONLY` if the stream is an append-only stream.   Displays `INSERT_ONLY` if the stream only returns information for inserted rows; currently applies to streams on external tables only.   Displays `DEFAULT` for a standard stream that tracks all DML changes (inserts, updates, and deletes). |
| STALE\_AFTER | TIMESTAMP\_LTZ | Timestamp when the stream became, or may become, stale if not consumed.     This value is calculated by adding the retention period for the source table (the larger of the [DATA\_RETENTION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-data-retention-time-in-days) and [MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-max-data-extension-time-in-days) parameter settings) to the last time the stream was read.     `STALE_AFTER` is NULL when Snowflake cannot calculate it, for example, when a base table was dropped or is inaccessible, or when the stream is a replicated stream that cannot be read (see `INVALID_REASON`). See the [Usage notes](#usage-notes) for accuracy considerations. |
| INVALID\_REASON | VARCHAR | Reason the stream cannot be queried successfully. Currently applies only to replicated streams that cannot be consumed or queried; otherwise, the value is `N/A`. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the stream was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the stream was last altered by a DDL operation. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the stream, or a schema or database that contains it, was dropped. NULL if the stream was not dropped. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 2 hours.
- The `STALE_AFTER` timestamp can appear to have passed before a stream actually becomes stale. Some time can elapse between when a stream is permitted to become stale and when the underlying data is dropped. During this grace period, `STALE_AFTER` is in the past, but reading from the stream might still succeed. Treat a stream as safe to drop only when `STALE_AFTER` is comfortably in the past (for example, more than a day ago), rather than acting as soon as the timestamp appears to have passed.
- Because the view is refreshed periodically, `STALE_AFTER` can lag slightly behind the current stream metadata.
- When the stream’s source object or a base table cannot be resolved (for example, because it was dropped), the view shows a placeholder instead of the name. `TABLE_NAME` shows `No privilege or table dropped`, and `BASE_TABLES` reports unresolvable tables as a count in the form `N inaccessible table(s)`. When some base tables resolve and others do not, `BASE_TABLES` lists the resolvable names followed by the inaccessible count.
- This view does not fully support streams whose base tables are shared from another account. The shared tables are reported as `No privilege or table dropped` for `TABLE_NAME`, inaccessible for `BASE_TABLES`, and `STALE_AFTER` is NULL.

## Examples

List the active streams in your account:

> Copy code
>
> ```
> SELECT stream_catalog, stream_schema, stream_name, source_type, mode, created
> FROM snowflake.account_usage.streams
> WHERE deleted IS NULL
> ORDER BY stream_catalog, stream_schema, stream_name;
> ```

List streams that appear stale and are candidates to review or drop. This query returns only streams whose `STALE_AFTER` is more than a day in the past. Streams with a NULL `STALE_AFTER` are excluded and need separate review (see the [Usage notes](#usage-notes) for why `STALE_AFTER` can be NULL):

> Copy code
>
> ```
> SELECT stream_catalog, stream_schema, stream_name, table_name, stale_after
> FROM snowflake.account_usage.streams
> WHERE deleted IS NULL
>   AND stale_after < DATEADD('day', -1, CURRENT_TIMESTAMP())
> ORDER BY stale_after;
> ```
