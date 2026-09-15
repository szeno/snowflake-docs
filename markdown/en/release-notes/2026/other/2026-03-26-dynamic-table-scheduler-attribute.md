# Mar 26, 2026: New SCHEDULER attribute for dynamic tables — *General availability*

You can now control whether a dynamic table is automatically refreshed by setting the optional `SCHEDULER` attribute to
`ENABLE` or `DISABLE` on [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table) or [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table).

When `SCHEDULER = DISABLE`, the dynamic table is excluded from automatic refresh and can only be refreshed manually with
`ALTER DYNAMIC TABLE ... REFRESH`. Manual refreshes do not cascade to upstream or downstream dynamic tables, which lets external
orchestrators (such as dbt) manage individual table refreshes without triggering the entire pipeline.

When `SCHEDULER = ENABLE`, the dynamic table is managed by Snowflake’s dynamic table scheduler using `TARGET_LAG`.

If the `SCHEDULER` attribute is not specified, the dynamic table behaves the same as existing dynamic tables: it is managed by the
scheduler using `TARGET_LAG`.

This feature is useful for external orchestrators, such as dbt, that manage refresh timing independently and need to refresh individual
dynamic tables without triggering the entire pipeline.

For more information, see [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table).
