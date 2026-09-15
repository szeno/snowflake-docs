# Sep 23, 2025: AI\_FILTER Performance Optimization (*Preview*)

AI\_FILTER includes a performance optimization that delivers a 2-10x speedup and reduces token usage by up to 60% for suitable queries using AI functions in SELECT, WHERE, and JOIN … ON clauses.

This optimization is triggered automatically when the query engine detects a suitable pattern. Similar to other query optimizations, Snowflake doesn’t guarantee that this optimization will be applied for every query. The engine leverages adaptive routing and context-aware rewriting to execute more efficient AI operations where possible. This enhancement lets customers run filtering queries faster and at a lower cost, with minimal impact on quality. This results in significant value through both performance gains and savings.

This optimization offers the following key enhancements:

- **Accelerated Performance:** A 2 to 10x speedup on qualifying queries that use AI functions within SELECT, WHERE, and JOIN … ON clauses when optimization is available.
- **Significant Cost Savings:** A token consumption reduction of up to 60%, lowering the cost of running filtering queries and other AI operations with optimization.

For more information, see [AI\_FILTER](/sql-reference/functions/ai_filter).
