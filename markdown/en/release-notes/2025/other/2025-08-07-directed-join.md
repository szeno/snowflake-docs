# Aug 07, 2025: Enforced join order with directed joins (*Preview*)

When you run join queries, you can now enforce the join order of the tables using the `DIRECTED` keyword.
When you run a query with a directed join, the first, or left, table is scanned before the second, or right, table.
For example, `o1 INNER DIRECTED JOIN o2` scans the `o1` table before the `o2` table.

Directed joins are useful in the following situations:

> - You are migrating workloads into Snowflake that have join order directives.
> - You want to improve performance by scanning join tables in a specific order.

For more information, see [JOIN](/sql-reference/constructs/join).
