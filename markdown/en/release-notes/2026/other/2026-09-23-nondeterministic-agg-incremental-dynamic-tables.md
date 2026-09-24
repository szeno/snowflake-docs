# Sep 23, 2026: Non-deterministic aggregate functions are supported with dynamic table incremental refresh (*General availability*)

Non-deterministic aggregate functions such as [APPROX\_COUNT\_DISTINCT](/sql-reference/functions/approx_count_distinct), [APPROX\_PERCENTILE](/sql-reference/functions/approx_percentile), and [APPROX\_TOP\_K](/sql-reference/functions/approx_top_k) are now supported
with dynamic table incremental refresh in INCREMENTAL, AUTO, and ADAPTIVE refresh modes. For incremental
refresh, these functions are supported only in the SELECT clause. [ANY\_VALUE](/sql-reference/functions/any_value) remains unsupported.

You can use the non-deterministic aggregate functions as aggregates with GROUP BY or as window functions. They return
approximations, not exact results.

For a complete list of supported queries and functions, see [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries).
