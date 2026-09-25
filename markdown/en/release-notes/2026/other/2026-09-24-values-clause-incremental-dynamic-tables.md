# Sep 24, 2026: VALUES clause is supported with dynamic table incremental refresh (*General availability*)

The [VALUES clause](/sql-reference/constructs/values) is now supported with dynamic table incremental refresh in INCREMENTAL,
AUTO, and ADAPTIVE refresh modes. You can use VALUES in the FROM clause to supply a constant set of rows, for example as
a small lookup table that you join to a base table.

For a complete list of supported queries and functions, see [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries).
