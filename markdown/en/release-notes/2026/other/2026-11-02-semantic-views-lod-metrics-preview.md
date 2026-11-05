# Nov 02, 2026: Level of detail (LOD) expressions in semantic views (*Preview*)

Level of detail (LOD) expressions are now in preview for semantic views. An LOD expression calculates a value at a grain
that’s different from the query grain. You can use LOD expressions to:

- Fix a calculation to an exact set of dimensions, no matter what the query groups by (`FIXED DIMENSIONS`).
- Add dimensions to the query grain for one calculation (`INCLUDE DIMENSIONS`).
- Remove dimensions from the query grain for one calculation (`EXCLUDE DIMENSIONS`).

For example, the following metric shows each customer’s average revenue within each region:

Copy code

```
avg_customer_rev_by_region AS AVG(
  SUM(orders.order_amount) INCLUDE DIMENSIONS (customers.customer_id)
)
```

You can define LOD expressions in the `FACTS`, `DIMENSIONS`, and `METRICS` clauses of [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view),
or in the model-level `facts`, `dimensions`, and `metrics` keys of the [YAML specification](/user-guide/views-semantic/semantic-view-yaml-spec).

LOD metrics work in SQL queries against semantic views. Cortex Analyst and Cortex Agents don’t use LOD metrics yet.
Semantic Studio in Snowsight also supports LOD metrics.

For more information, see [Defining level of detail (LOD) metrics](/user-guide/views-semantic/sql#label-semantic-views-lod).
