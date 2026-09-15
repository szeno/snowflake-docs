# Apr 16, 2026: Primary key support in dynamic tables (*General availability*)

Snowflake can now use primary keys in dynamic tables to track row-level changes and enable incremental refresh downstream of full-refresh
dynamic tables. This release includes the following capabilities:

- **Base table-defined primary keys**: When a base table has a primary key with the `RELY` property, Snowflake uses it for change tracking
  in downstream dynamic tables. This is especially useful when the base table is periodically rewritten through INSERT OVERWRITE, which
  normally prevents change tracking across table versions.
- **Query-derived primary keys**: Snowflake automatically derives primary keys from the query definition of a dynamic table. Queries with
  GROUP BY clauses or QUALIFY ROW\_NUMBER() = 1 filters produce unique constraints that Snowflake relies on for change tracking.
- **Incremental refresh on full-refresh dynamic tables**: Dynamic tables in incremental refresh mode can now read from upstream dynamic
  tables that use full refresh mode, as long as the upstream table has a system-derived primary key. To use this capability, set
  `REFRESH_MODE = INCREMENTAL` explicitly on the downstream dynamic table.

To check whether a dynamic table has a derived primary key, run `SHOW UNIQUE KEYS IN <dt_name>`.

For more information, see [Optimize input data for dynamic tables](/user-guide/dynamic-tables/input-data-optimization). To try this feature with a
step-by-step example, see .
