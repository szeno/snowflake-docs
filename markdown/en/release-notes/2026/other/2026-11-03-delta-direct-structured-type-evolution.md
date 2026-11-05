# Nov 3, 2026: Delta Direct: Structured type evolution (*General availability*)

With this release, Delta Direct tables reconcile changes to the structure of `OBJECT`, `ARRAY`, and `MAP` columns during refresh.
Previously, a change to a structured column in the source Delta table, such as adding a subfield, caused the refresh to fail with
error `091989`, and the only workaround was to drop and recreate the table.

Snowflake now supports adding, renaming, and dropping subfields at any nesting depth, and widening supported scalar types inside
structured columns.

For more information, see [Schema changes](/user-guide/tables-iceberg-delta-direct#label-tables-iceberg-delta-direct-schema-changes).
