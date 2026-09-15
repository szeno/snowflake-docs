# Materializing dimensions and metrics in semantic views

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

To improve the query performance of a semantic view, you can materialize selected dimensions and metrics in the view,
similar to how you materialize data in a [materialized view](/user-guide/views-materialized).

When you query the semantic view, Snowflake reads from the materialized dimensions and metrics, rather than scanning the base table and
computing the information.

Note

Semantic view materializations benefit queries executed as Semantic SQL (via the
[SEMANTIC\_VIEW](/sql-reference/constructs/semantic_view) construct or standard SQL against a semantic view).
Queries from Cortex Analyst, Cortex Agents, and Snowflake CoWork that execute physical SQL directly against
the underlying tables do not benefit from semantic view materializations.

Note

If `MAX_STALENESS` is set too low and background refreshes can’t keep up, Snowflake automatically suspends the
materialization. To recover, either increase `MAX_STALENESS` or optimize the materialization definition (for example,
by using only incrementally maintainable metrics or adding an `IMMUTABLE WHERE` condition).

## Preparing a semantic view to support materialization

Before you can materialize the dimensions and metrics in a semantic view, you must

- [Set the MAX\_STALENESS property of the semantic view](#label-semantic-views-materializing-prereqs-staleness).
- [Verify that you are using a role that has been granted the privileges to materialize the dimensions and metrics](#label-semantic-views-materializing-prereqs-privileges).

### Setting the maximum staleness of the materialized dimensions and metrics

The MAX\_STALENESS property determines the maximum amount of time that the materialized dimensions and metrics
can be stale (out of date) before they are refreshed. For example, if you don’t want the materialized dimensions and
metrics to be out of date by more than 1 hour, set the MAX\_STALENESS property to ’1 hour’.

You can set this property when running the [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) command to create a new
semantic view:

Copy code

```
CREATE [ OR REPLACE ] SEMANTIC VIEW [ IF NOT EXISTS ] <name>
  ...
  [ AI_QUESTION_CATEGORIZATION '<instructions_for_question_categorization>' ]
  [ MAX_STALENESS = '<num> { seconds | minutes | hours | days }' ]
  [ COPY GRANTS ]
```

You can also set this property on an existing semantic view by running
[ALTER SEMANTIC VIEW … SET MAX\_STALENESS](/sql-reference/sql/alter-semantic-view):

Copy code

```
ALTER SEMANTIC VIEW <name> SET MAX_STALENESS = '<num> { seconds | minutes | hours | days }'
```

Note

The minimum allowed MAX\_STALENESS is 120 seconds.

The following example creates a semantic view with a maximum staleness of 1 hour:

Copy code

```
CREATE OR REPLACE SEMANTIC VIEW revenue_analysis
  TABLES (
    orders AS ORDERS PRIMARY KEY (o_orderkey),
    customers AS CUSTOMER PRIMARY KEY (c_custkey)
  )
  RELATIONSHIPS (
    orders_to_customers AS orders (o_custkey) REFERENCES customers
  )
  DIMENSIONS (
    customers.customer_name AS c_name,
    orders.order_date AS o_orderdate,
    orders.order_year AS YEAR(o_orderdate)
  )
  METRICS (
    orders.total_revenue AS SUM(o_totalprice),
    orders.avg_revenue AS AVG(o_totalprice),
    orders.order_count AS COUNT(o_orderkey)
  )
  MAX_STALENESS = '1 hour';
```

The MAX\_STALENESS property defines the maximum acceptable staleness for materialized data. The system uses this value to determine how
frequently materializations are refreshed. Queries are only rewritten to use a materialization when the materialization is not
older than the value of the MAX\_STALENESS property.

Note

You can’t unset MAX\_STALENESS while materializations exist on the semantic view. Drop all materializations first
if you need to remove the property.

### Granting the privileges to materialize the dimensions and metrics

To materialize the dimensions and metrics in a semantic view and manage those materializations, you must use a role that has been granted
the following privileges:

- the OWNERSHIP privilege on the semantic view
- the ADD SEMANTIC VIEW MATERIALIZATION privilege on the schema that contains the semantic view

To grant this privilege to a role, run the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command. For more information about granting
privileges, see [Access control privileges](/user-guide/security-access-control-privileges).

Note

The SHOW MATERIALIZATIONS command requires only the SELECT privilege on the semantic view.

## Materializing dimensions and metrics

To materialize dimensions and metrics in a semantic view, run ALTER SEMANTIC VIEW … ADD MATERIALIZATION:

Copy code

```
ALTER SEMANTIC VIEW <name> ADD MATERIALIZATION <materialization_name>
  WAREHOUSE = <warehouse_name>
  [ REFRESH_MODE = { AUTO | FULL | INCREMENTAL } ]
  [ IMMUTABLE WHERE ( <immutable_condition> ) ]
AS
  DIMENSIONS <dimension_name> [ , ... ]
  METRICS <metric_name> [ , ... ]
  [ WHERE ( <filter_condition> ) ];
```

where:

- `name`: Specifies the name of the semantic view.
- `materialization_name`: Specifies the name of the materialization to add.
- `WAREHOUSE = warehouse_name`: Specifies the warehouse to use when materializing the dimensions and metrics.
- `REFRESH_MODE = { AUTO | FULL | INCREMENTAL }`: Specifies how the materialization is refreshed.

  - `AUTO` (default): Snowflake automatically determines the best refresh strategy. For materializations that span multiple
    entities, AUTO typically resolves to FULL.
  - `FULL`: Forces a full recomputation of the materialization on every refresh.
  - `INCREMENTAL`: Forces incremental refresh, processing only the changed data. Use this to incrementalize queries that
    AUTO mode would otherwise process as full refreshes.
- `IMMUTABLE WHERE ( immutable_condition )`: Specifies a condition that identifies rows that don’t change.

  You specify this to
  [improve performance by limiting the scope of the refresh](#label-semantic-views-materializing-limit-refresh).

  Use unqualified column names (for example, `order_year` rather than `orders.order_year`). The condition is
  evaluated on the result of the semantic view query, which uses unqualified names.

  Important

  Snowflake strongly recommends specifying this clause to reduce the cost and time of materialization refreshes.
  For more information, see [Improving performance by incrementally refreshing materializations](#label-semantic-views-materializing-limit-refresh).
- `DIMENSIONS dimension_name [ , ... ]`: Specifies the dimensions to materialize.
- `METRICS metric_name [ , ... ]`: Specifies the metrics that you want to pre-aggregate.
- `WHERE ( filter_condition )`: Specifies a filter that limits which rows the materialization stores.
  This is different from `IMMUTABLE WHERE`: `WHERE` controls which rows are included in the materialization
  and determines when queries can be rewritten to use it. `IMMUTABLE WHERE` is a refresh optimization hint
  that identifies rows that don’t need to be recomputed.

  For more information, see [Materializing a filtered subset of data](#label-semantic-views-materializing-filter).

Note

You can’t use the following metric types in materializations:

- [Window function metrics](/user-guide/views-semantic/querying#label-semantic-views-querying-window)
- [Semi-additive metrics](/user-guide/views-semantic/sql#label-semantic-views-metrics-semi-additive)
- [Metrics that specify which relationships to use](/user-guide/views-semantic/sql#label-semantic-views-create-logical-tables-relations)

For example:

Copy code

```
ALTER SEMANTIC VIEW revenue_analysis ADD MATERIALIZATION revenue_by_customer
  WAREHOUSE = my_wh
  AS
    DIMENSIONS customers.customer_name
    METRICS orders.total_revenue;
```

To force incremental refresh for a multi-entity materialization:

Copy code

```
ALTER SEMANTIC VIEW revenue_analysis ADD MATERIALIZATION revenue_by_customer_year
  WAREHOUSE = my_wh
  REFRESH_MODE = INCREMENTAL
  AS
    DIMENSIONS customers.customer_name, orders.order_year
    METRICS orders.total_revenue;
```

You can add multiple materializations to a semantic view. Each materialization specifies a subset of dimensions and metrics to pre-aggregate.

You can also use this command to update the definition of an existing materialization. If you run ADD MATERIALIZATION with the same name:

- **Same definition**: The operation is a no-op.
- **Different definition**: The existing materialization is dropped and replaced with the new definition.

Snowflake automatically refreshes the materialization regularly to fulfill the desired `MAX_STALENESS`. If the refreshes take
too long and the materializations become more stale than the limit, they aren’t used for rewrites. In those cases, check the
refresh history and consider increasing the `MAX_STALENESS` on the semantic view:

Copy code

```
ALTER SEMANTIC VIEW revenue_analysis SET MAX_STALENESS = '2 hours';
```

## How materializations are used when processing a query

When you query a semantic view, Snowflake uses the materializations to fulfill the query. The planner selects the lowest-cost
materialization that covers the requested dimensions and metrics. The next sections explain how materializations are used when Snowflake
processes a query.

- [Reaggregation of additive metrics](#label-semantic-views-materializing-reaggregation)
- [How dimensions in a WHERE clause are handled](#label-semantic-views-materializing-where)
- [When materializations are not used](/user-guide/views-semantic/materializations#label-semantic-views-materializing-fallback)

### Reaggregation of additive metrics

When a materialization contains more dimensions than the query requests, Snowflake can reaggregate additive metrics. For
example, a materialization on `(customer_name, order_year)` with `SUM(total_revenue)` can serve a query requesting only
`customer_name` by summing across years.

If the metrics use the following functions, Snowflake can reaggregate the metrics:

- [SUM](/sql-reference/functions/sum)
- [COUNT](/sql-reference/functions/count)
- [MIN](/sql-reference/functions/min)
- [MAX](/sql-reference/functions/max)

Note

Metrics with an expression on top of the aggregation (for example, `2 * SUM(x) + COUNT(y)`) are not considered additive.

If metrics use the following functions, Snowflake can’t reaggregate the metrics:

- [COUNT(DISTINCT … )](/sql-reference/functions/count)
- [APPROX\_COUNT\_DISTINCT](/sql-reference/functions/approx_count_distinct)
- [MEDIAN](/sql-reference/functions/median)
- [PERCENTILE\_CONT](/sql-reference/functions/percentile_cont) and [PERCENTILE\_DISC](/sql-reference/functions/percentile_disc)
- [AVG](/sql-reference/functions/avg)
- Any `DISTINCT` aggregation
- Derived metrics referencing non-additive metrics

### How dimensions in a WHERE clause are handled

Dimensions used in a WHERE clause count as covered dimensions. For example, a materialization on
`(customer_name, order_year)` can be used when the following query is processed:

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
    revenue_analysis
    DIMENSIONS customers.customer_name
    METRICS orders.total_revenue
    WHERE orders.order_year = 2024
);
```

Expressions on dimensions in the WHERE clause (for example, `MOD(orders.order_year, 2) = 0`) are also supported, as long
as the underlying dimension is covered by the materialization. The same applies to expressions on top of additive metrics
and dimensions.

- No materialization covers the requested dimensions or metrics.
- The materialization exceeds the value of the MAX\_STALENESS property.
- A masking policy or row access policy exists on a column that is referenced by the materialization.
- Non-additive metrics require reaggregation.
- The materialization is in SUSPENDED state.
- The query’s WHERE clause is less restrictive than the materialization’s WHERE filter, or the query filters on
  a column that isn’t a materialized dimension. See [Materializing a filtered subset of data](#label-semantic-views-materializing-filter).

## Materializing a filtered subset of data

You can use a `WHERE` clause when adding a materialization to limit which rows are stored. This is useful for
materializing only the most recent or most frequently queried data (for example, orders from the last two years).

Copy code

```
ALTER SEMANTIC VIEW revenue_analysis ADD MATERIALIZATION recent_revenue
  WAREHOUSE = my_wh
AS
  DIMENSIONS orders.order_year, orders.category
  METRICS orders.total_revenue
  WHERE (order_year > 2020);
```

Snowflake rewrites a query to use this materialization when the query’s WHERE clause is **compatible** with the
materialization’s filter:

| Query WHERE clause | Rewrite? | Reason |
| --- | --- | --- |
| `WHERE order_year > 2020` | ✓ Yes | Identical to the materialization filter. |
| `WHERE order_year > 2022` | ✓ Yes | More restrictive than the filter, and `order_year` is a materialized dimension so Snowflake can apply the extra filter on top of the stored data. |
| `WHERE order_year > 2019` | ✗ No | Less restrictive — the materialization doesn’t contain rows from 2020 or earlier. |
| `WHERE order_year > 2020 AND category = 'X'` | ✗ No | `category` is not a materialized dimension, so the extra filter can’t be applied to the stored data. |

Expand

Show lessSee more

## Improving performance by incrementally refreshing materializations

If the semantic view contains non-additive metrics (for example, `COUNT(DISTINCT ... )`) or complex queries spanning multiple
entities, `REFRESH_MODE = INCREMENTAL` is not supported and Snowflake performs a full recomputation on every refresh.

You can still improve the performance of these full refreshes by specifying the IMMUTABLE WHERE clause.
The IMMUTABLE WHERE clause identifies rows that don’t change, which limits the scope of the full refresh.
Rows that satisfy the condition are treated as immutable, so Snowflake only recomputes the mutable portion.

For example, the following statement adds a materialization where all orders before January 1, 2020 are treated as immutable:

Copy code

```
ALTER SEMANTIC VIEW revenue_analysis ADD MATERIALIZATION historical_revenue
    WAREHOUSE = my_wh
    IMMUTABLE WHERE (order_date < '2020-01-01')
AS
    DIMENSIONS orders.order_date
    METRICS orders.total_revenue;
```

### Updating the immutable condition

You can update the IMMUTABLE WHERE condition of an existing materialization without recreating it. This is useful when you need to
move a watermark date forward as more data becomes historical.

To update the condition, run ADD MATERIALIZATION again with the same name and updated IMMUTABLE WHERE clause:

Copy code

```
ALTER SEMANTIC VIEW revenue_analysis ADD MATERIALIZATION historical_revenue
    WAREHOUSE = my_wh
    IMMUTABLE WHERE (order_date < '2024-01-01')
AS
    DIMENSIONS orders.order_date
    METRICS orders.total_revenue;
```

Note

- Enlarging the immutable region (moving the boundary forward in time) refreshes without full reinitialization.
- Shrinking the immutable region or dropping it entirely triggers a full reinitialization.
- To remove the IMMUTABLE WHERE clause entirely, re-issue the ADD MATERIALIZATION without it.

## Suspending and resuming materializations

You can manually suspend a materialization to stop its background refreshes and prevent it from being used for query rewrites.
To resume it later, use the RESUME command.

Materializations are also automatically suspended when:

- The semantic view is altered in a way that breaks the materialization definition (see
  [How DDL changes affect materializations](#label-semantic-views-materializing-coa)).
- A refresh fails or takes too long to complete within the `MAX_STALENESS` window. Check the
  [refresh history](#label-semantic-views-materializing-observability) to investigate.

Copy code

```
ALTER SEMANTIC VIEW <name> SUSPEND MATERIALIZATION <materialization_name>;
ALTER SEMANTIC VIEW <name> RESUME MATERIALIZATION <materialization_name>;
```

For example:

Copy code

```
ALTER SEMANTIC VIEW revenue_analysis SUSPEND MATERIALIZATION revenue_by_customer;

-- Later, resume it:
ALTER SEMANTIC VIEW revenue_analysis RESUME MATERIALIZATION revenue_by_customer;
```

Note

Materializations are also automatically suspended when the semantic view is altered in a way that
breaks the materialization definition. For more information, see
[Preserving materializations when altering a semantic view](#label-semantic-views-materializing-coa).

## How DDL changes affect materializations

The sections below explain how changes to the semantic view, its underlying objects, or the materialization
definition itself affect existing materializations.

### Changes to the semantic view

**CREATE OR REPLACE SEMANTIC VIEW** always drops all existing materializations immediately, regardless of what
changed. After replacing the view, recreate materializations with `ADD MATERIALIZATION`.

To preserve materializations across changes, use **CREATE OR ALTER SEMANTIC VIEW** instead. The effect depends
on what you change:

| Change | Effect on materialization | Still used for rewrite | Recovery |
| --- | --- | --- | --- |
| Add a metric, dimension, logical table, or relationship | None | ✅ | — |
| Change or delete a dimension, metric, logical table, or relationship **not used** by the materialization | None | ✅ | — |
| Change or delete a dimension, metric, logical table, or relationship **used** by the materialization | Suspended immediately | ❌ | Revert the SV definition and `RESUME`, or `DROP AND ADD MATERIALIZATION` |

Expand

Show lessSee more

For example, changing a metric’s aggregation function from `SUM` to `COUNT` suspends any materialization that
depends on that metric. Suspended materializations aren’t removed. If you revert the SV definition to the
previous state, you can resume the materialization:

Copy code

```
ALTER SEMANTIC VIEW revenue_analysis RESUME MATERIALIZATION revenue_by_customer;
```

If the definition is no longer compatible, drop and recreate the materialization instead:

Copy code

```
ALTER SEMANTIC VIEW revenue_analysis DROP MATERIALIZATION revenue_by_customer;

ALTER SEMANTIC VIEW revenue_analysis ADD MATERIALIZATION revenue_by_customer
  WAREHOUSE = my_wh
  ...;
```

### Changes to underlying objects

Changes to views or tables that the semantic view references can also affect materializations:

| Change | Effect on materialization | Still used for rewrite | Recovery |
| --- | --- | --- | --- |
| Change that affects the materialization (e.g., `CREATE OR REPLACE VIEW`, `ALTER TABLE DROP COLUMN`) | Next refresh becomes a full refresh; if the refresh fails, the materialization is suspended | ✅ (unless suspended) | If refreshes continue to fail, `DROP AND ADD MATERIALIZATION` |

Expand

Show lessSee more

Unlike semantic view changes, Snowflake does not immediately suspend the materialization when an underlying object
changes — it waits for the next scheduled refresh to detect and react to the change.

### Changes to the materialization definition

When you run `ADD MATERIALIZATION` for a materialization that already exists, the behavior depends on what changed:

| Change | Effect on materialization | Still used for rewrite |
| --- | --- | --- |
| Same definition as the existing materialization | No-op | ✅ |
| Different definition (e.g., added or dropped metric or dimension, changed `WHERE` clause) | Full refresh (reinitialize) with new definition | ✅ |
| `IMMUTABLE WHERE` condition made **stricter** (e.g., `year > 2020` → `year > 2021`) | None | ✅ |
| `IMMUTABLE WHERE` condition made **looser** (e.g., `year > 2021` → `year > 2020`) | Full refresh | ✅ |

Expand

Show lessSee more

## Refreshing a materialization manually

If you want to refresh the materialization of a set of dimensions and metrics, run ALTER SEMANTIC VIEW … REFRESH MATERIALIZATION:

Copy code

```
ALTER SEMANTIC VIEW <name> REFRESH MATERIALIZATION <materialization_name>;
```

Note

You must use a role that has been granted the [privileges to materialize the dimensions and metrics](#label-semantic-views-materializing-prereqs-privileges).

For example, the following statement refreshes the `revenue_by_customer` materialization for the `revenue_analysis` semantic view:

Copy code

```
ALTER SEMANTIC VIEW revenue_analysis REFRESH MATERIALIZATION revenue_by_customer;
```

When you run this command, the manual refresh uses the current warehouse of the session. Background refreshes occur automatically based on
the MAX\_STALENESS property using the warehouse specified when the materialization was created.

## Managing materializations declaratively with YAML

You can manage all materializations on a semantic view declaratively using
[SYSTEM$MANAGE\_SEMANTIC\_VIEW\_MATERIALIZATIONS\_FROM\_YAML](/sql-reference/stored-procedures/system_manage_semantic_view_materializations_from_yaml).
This stored procedure synchronizes the materializations on a semantic view with a YAML specification:

- Materializations in the YAML that don’t exist are created.
- Materializations that exist but have a changed definition are replaced.
- Materializations that already exist with the same definition are left unchanged (no-op).
- Materializations that exist on the semantic view but aren’t in the YAML are dropped.

For the full syntax, parameters, and examples, see
[SYSTEM$MANAGE\_SEMANTIC\_VIEW\_MATERIALIZATIONS\_FROM\_YAML](/sql-reference/stored-procedures/system_manage_semantic_view_materializations_from_yaml).

## Removing a materialization

To remove a materialization from a semantic view, run ALTER SEMANTIC VIEW … DROP MATERIALIZATION:

Copy code

```
ALTER SEMANTIC VIEW <name> DROP MATERIALIZATION <materialization_name>;
```

Note

You must use a role that has been granted the [privileges to materialize the dimensions and metrics](#label-semantic-views-materializing-prereqs-privileges).

For example, the following statement removes the `revenue_by_customer` materialization from the `revenue_analysis` semantic view:

Copy code

```
ALTER SEMANTIC VIEW revenue_analysis DROP MATERIALIZATION revenue_by_customer;
```

## Listing the materializations for a semantic view

To list the materializations for a semantic view, run the SHOW MATERIALIZATIONS command:

Copy code

```
SHOW MATERIALIZATIONS IN SEMANTIC VIEW <name>;
```

Note

You must use a role that has been granted the SELECT privilege on the semantic view.

For example, to list the materializations for the `revenue_analysis` semantic view:

Copy code

```
SHOW MATERIALIZATIONS IN SEMANTIC VIEW revenue_analysis;
```

The command returns tabular output in the following columns:

| Column | Description |
| --- | --- |
| `name` | Name of the materialization. |
| `state` | State of the materialization. The state can be one of the following:   - `ACTIVE`: The materialization is operational and eligible for query rewrite. - `SUSPENDED`: The materialization is suspended due to a refresh failure or a manual suspend. The `suspend_reason` field is populated with details. |
| `suspend_reason` | Reason why the materialization is suspended. |
| `stale_by` | Time when the materialization will be stale. |
| `warehouse` | Warehouse that is used to materialize the dimensions and metrics. |
| `dimensions` | Dimensions that are materialized. |
| `metrics` | Metrics that are materialized. |
| `immutable_where` | Condition that is used to identify immutable rows. |
| `refresh_mode` | The resolved refresh mode for the materialization (`FULL` or `INCREMENTAL`). When REFRESH\_MODE is set to AUTO, this column shows the mode that was automatically selected. |
| `refresh_mode_reason` | Explanation of why a particular refresh mode was chosen. Populated when AUTO selects FULL due to query complexity. |

Expand

Show lessSee more

## Monitoring materialization refreshes

You can monitor materialization refreshes using refresh history and event tables.

### Viewing refresh history

To view the history of refreshes for a materialization, call the SEMANTIC\_VIEW\_MATERIALIZATION\_REFRESH\_HISTORY table function in the
INFORMATION\_SCHEMA schema:

Copy code

```
SEMANTIC_VIEW_MATERIALIZATION_REFRESH_HISTORY(
    NAME => '<materialization_name>'
)
```

For example, to view the history of refreshes for the `revenue_by_customer` materialization:

Copy code

```
SELECT * FROM TABLE(INFORMATION_SCHEMA.SEMANTIC_VIEW_MATERIALIZATION_REFRESH_HISTORY(
    NAME => 'revenue_by_customer'
));
```

The function returns tabular output in the following columns:

| Column | Description |
| --- | --- |
| `name` | Name of the materialization. |
| `schema_name` | Name of the schema that contains the semantic view. |
| `database_name` | Name of the database that contains the semantic view. |
| `state` | State of the refresh. The state can be one of the following:   - `ACTIVE`: The materialization is operational and eligible for query rewrite. - `SUSPENDED`: The materialization is suspended due to a refresh failure. |
| `state_message` | Error or status message from the refresh. |
| `refresh_start_time` | Time when the refresh started. |
| `refresh_end_time` | Time when the refresh completed. |
| `warehouse` | Warehouse used for the refresh. |
| `refresh_action` | Action taken during the refresh (for example, `INITIALIZE`, `REINITIALIZE`, `REFRESH`, `NO_DATA`). |

Expand

Show lessSee more

### Setting up alerting with event tables

You can configure materializations to emit refresh events to an event table, allowing you to create alerts for failures
or suspension.

To enable event logging for a materialization:

Copy code

```
ALTER SEMANTIC VIEW <name> ALTER MATERIALIZATION <materialization_name>
  SET LOG_EVENT_LEVEL = 'INFO';
```

To disable event logging:

Copy code

```
ALTER SEMANTIC VIEW <name> ALTER MATERIALIZATION <materialization_name>
  UNSET LOG_EVENT_LEVEL;
```

Materialization refresh events appear in the event table with `snow.executable.type = 'SEMANTIC_VIEW_MATERIALIZATION'`.
You can query the event table and set up alerts based on refresh status, similar to
[dynamic table alerting](/user-guide/dynamic-tables/monitoring).

### How dimensions in a WHERE clause are handled

Dimensions used in a WHERE clause count as covered dimensions. For example, a materialization on
`(customer_name, order_year)` can be used when the following query is processed:

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
    revenue_analysis
    DIMENSIONS customers.customer_name
    METRICS orders.total_revenue
    WHERE orders.order_year = 2024
);
```

Expressions on dimensions in the WHERE clause (for example, `MOD(orders.order_year, 2) = 0`) are also supported, as long
as the underlying dimension is covered by the materialization.
