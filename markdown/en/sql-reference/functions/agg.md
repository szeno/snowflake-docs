Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Semantic Views)

# AGG

Evaluates and returns the value of a metric in a [semantic view](/user-guide/views-semantic/overview) when you
[run a query](/user-guide/views-semantic/querying).

## Syntax

Copy code

```
AGG( <metric_in_semantic_view> )
```

## Arguments

`metric_in_semantic_view`
:   Name of a metric that is defined in the semantic view that you specify in the FROM clause of the query. You can use the bare
    (unqualified) metric name, or qualify it with the name of the logical table that defines it (for example,
    `orders.order_average_value`). You must qualify the name if more than one logical table in the semantic view defines a metric with the
    same name. For details, see [Requirements for dimensions and metrics in a SELECT statement](/user-guide/views-semantic/querying#label-semantic-views-query-standard-reqs).

## Returns

Returns the value of the specified metric.

## Examples

Return the value of the `order_average_value` metric for each customer market segment in the `tpch_analysis` semantic view:

Copy code

```
SELECT customer_market_segment, AGG(order_average_value)
  FROM tpch_analysis
  GROUP BY customer_market_segment;
```

For more examples, see [Selecting metrics](/user-guide/views-semantic/querying#label-semantic-views-query-standard-metrics).
