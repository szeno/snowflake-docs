Categories:
:   [Query syntax](/sql-reference/constructs)

# SEMANTIC\_VIEW

Specifies the [semantic view](/user-guide/views-semantic/overview) to [query](/user-guide/views-semantic/querying).
You specify SEMANTIC\_VIEW(…) in a [FROM](/sql-reference/constructs/from) clause in a [SELECT](/sql-reference/sql/select) statement.

Note

You can’t query [private facts or metrics](/user-guide/views-semantic/sql#label-semantic-views-private) or use them in the WHERE condition.

See also:
:   [FROM](/sql-reference/constructs/from), [Querying semantic views](/user-guide/views-semantic/querying)

## Syntax

Copy code

```
SEMANTIC_VIEW(
  [<namespace>.]<semantic_view_name>
  [
    {
      METRICS <metric_expr> [ [ AS ] <alias> ] [ , ... ] |
      FACTS <fact_expr>  [ , ... ]
    }
  ]
  [ DIMENSIONS <dimension_expr>  [ [ AS ] <alias> ] [ , ... ] ]
  [ WHERE <predicate> ]
)
```

## Parameters

`[namespace.]semantic_view_name`
:   Specifies the identifier for the semantic view to query.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`METRICS metric_expr [ [ AS ] alias ] [ , ... ]`
:   Specifies the metrics that you want to return in the results. You can also specify an expression that includes:

    - Scalar expressions that refer to metrics in the semantic view.
    - Aggregations of dimensions or facts in the semantic view.

    Note

    - You can’t specify [private metrics](/user-guide/views-semantic/sql#label-semantic-views-private).

    For the names of the metrics:

    - You can qualify the name of the metric (for example, `my_logical_table.my_metric`).

      Using the unqualified name works only if there are no other identifiers with the same unqualified name in the semantic view.
      For example, if a metric and a dimension use the same unqualified name, you must qualify the name of the metric in the query.
    - To specify all metrics in a logical table, use an asterisk as a wildcard, qualified by the logical table name (for example,
      `my_logical_table.*`).

      You can’t specify an asterisk without qualifying it with a table name.

    You can specify an alias for a metric after the name of the metric. You can use the optional AS keyword before the alias.

    Specify the metrics in the order in which they should appear in the results.

`FACTS fact_expr [ , ... ]`
:   Specifies the facts that you want to return in the results. You can also specify scalar expressions that refer to facts or
    dimensions in the semantic view. If you specify a scalar expression, the dimensions and facts in that expression must belong to
    the same logical table.

    Note

    You can’t specify [private facts](/user-guide/views-semantic/sql#label-semantic-views-private).

    Unlike dimensions specified in the DIMENSIONS clause, the query does not group the facts specified in the FACTS clause.
    Different rows can include the same value for a fact.

    Specify the facts in the order in which they should appear in the results.

`DIMENSIONS dimension_expr [ [ AS ] alias ] [ , ... ]`
:   Specifies the dimensions that you want to return in the results. You can also specify scalar expressions that refer to
    dimensions or facts in the semantic view. If you specify a scalar expression, the dimensions and facts in that expression must
    belong to the same logical table.

    The query groups the results by the dimensions that you specify here. For example, if a logical table includes five distinct
    values for a dimension, specifying that dimension in the DIMENSIONS clause returns five rows.

    For the names of the dimensions:

    - You can qualify the name of the dimension (for example, `my_logical_table.my_dimension`). Using the unqualified name works
      only if there are no other identifiers with the same unqualified name in the semantic view. For example, if a metric and a
      dimension use the same unqualified name, you must qualify the name of the dimension in the query.
    - To specify all dimensions in a logical table, use an asterisk as a wildcard, qualified by the logical table name (for example,
      `my_logical_table.*`).

      You can’t specify an asterisk without qualifying it with a table name.

    You can specify an alias for a dimension after the expression for the dimension. You can use the optional AS keyword before the
    alias.

    If you specify a scalar expression, you can’t refer to dimensions in other semantic views or metrics.

    Specify the dimensions in the order in which they should appear in the results.

    Note

    If you are returning a window function metric, you must also return the dimensions that are specified in
    PARTITION BY `dimension`, PARTITION BY EXCLUDING `dimension`, and ORDER BY `dimension` clauses
    in the [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) statement for that semantic view.

    See [Defining and querying window function metrics](/user-guide/views-semantic/querying#label-semantic-views-querying-window).

`WHERE predicate`
:   A boolean expression. The expression can include [logical operators](/sql-reference/operators-logical),
    [built-in functions](/sql-reference-functions), and
    [user-defined functions (UDFs)](/developer-guide/udf/udf-overview).

    In the condition, you can only refer to dimensions, facts, and expressions that use dimensions and facts.

    If you specify facts from different entities, the RELATIONSHIPS clause in the semantic view definition must define a
    relationship between these entities.

    This filter condition is applied before the metrics are computed.

## Usage notes

- In the SEMANTIC\_VIEW clause, you must specify at least one of the following clauses:

  - METRICS
  - DIMENSIONS
  - FACTS

  You cannot omit all of these clauses from the SEMANTIC\_VIEW clause.
- When specifying a combination of these clauses, note the following:

  - You cannot specify FACTS and METRICS in the same SEMANTIC\_VIEW clause.
  - Although you can specify both FACTS and DIMENSIONS in a query, you should do so only if the dimensions can uniquely determine
    the facts.

    The query groups the results by dimensions. if the facts do not depend on the dimensions, the results can be
    non-deterministic.
  - If you specify both FACTS and DIMENSIONS, all facts and dimensions used in the query (including those specified in the WHERE
    clause) must be defined in the same logical table.
  - If you specify a dimension and a metric, the logical table for the dimension must be related to the logical table for the
    metric.

    In addition, the logical table for the dimension must have an equal or lower level of granularity than the logical table for
    the metric.

    To determine which dimensions meet this criteria, you can run the
    [SHOW SEMANTIC DIMENSIONS FOR METRIC](/sql-reference/sql/show-semantic-dimensions-for-metric) command.

    For details, see [Choosing the dimensions that you can return for a given metric](/user-guide/views-semantic/querying#label-semantic-views-query-dimensions-metrics).
- In the DIMENSIONS clause, you can specify an expression that refers to a fact. Similarly, in the FACTS clause, you can specify
  an expression that refers to a dimension. For example:

  Copy code

  ```
  -- Dimension expression that refers to a fact
  DIMENSIONS my_table.my_fact

  -- Fact expression that refers to a dimension
  FACTS my_table.my_dimension
  ```

  One of the main differences between using DIMENSIONS and FACTS is that the query groups the results by the dimensions and
  expressions specified in the DIMENSIONS clause.
- In the METRICS clause, you can specify an expression that includes:

  - A scalar expression referring to metrics.
  - An aggregation of dimensions or facts.
- Specify the METRICS, DIMENSIONS, and FACTS clauses in the order in which you want them to appear in the results.

  If you want the dimensions to appear first in the results, specify DIMENSIONS before METRICS. Otherwise, specify METRICS first.

  For example, suppose that you specify the METRICS clause first:

  Copy code

  ```
  SELECT * FROM SEMANTIC_VIEW(
   tpch_analysis
   METRICS customer.customer_order_count
   DIMENSIONS customer.customer_name
    )
    ORDER BY customer_name
    LIMIT 5;
  ```

  In the output, the first column is the metric column (`customer_order_count`) and the second column is the dimension column
  (`customer_name`):

  ```
  +----------------------+--------------------+
  | CUSTOMER_ORDER_COUNT | CUSTOMER_NAME      |
  |----------------------+--------------------|
  |                    6 | Customer#000000001 |
  |                    7 | Customer#000000002 |
  |                    0 | Customer#000000003 |
  |                   20 | Customer#000000004 |
  |                    4 | Customer#000000005 |
  +----------------------+--------------------+
  ```

  If you instead specify the DIMENSIONS clause first:

  Copy code

  ```
  SELECT * FROM SEMANTIC_VIEW(
   tpch_analysis
   DIMENSIONS customer.customer_name
   METRICS customer.customer_order_count
    )
    ORDER BY customer_name
    LIMIT 5;
  ```

  In the output, the first column is the dimension column (`customer_name`) and the second column is the metric column
  (`customer_order_count`):

  ```
  +--------------------+----------------------+
  | CUSTOMER_NAME      | CUSTOMER_ORDER_COUNT |
  |--------------------+----------------------|
  | Customer#000000001 |                    6 |
  | Customer#000000002 |                    7 |
  | Customer#000000003 |                    0 |
  | Customer#000000004 |                   20 |
  | Customer#000000005 |                    4 |
  +--------------------+----------------------+
  ```
- You can use the relation defined by a SEMANTIC\_VIEW clause in other SQL constructs, including
  [JOIN](/sql-reference/constructs/join), [PIVOT](/sql-reference/constructs/pivot), [UNPIVOT](/sql-reference/constructs/unpivot),
  [GROUP BY](/sql-reference/constructs/group-by), and [common table expressions (CTEs)](/user-guide/queries-cte).
- The output column headers use the unqualified names of the metrics and dimensions.

  If you have multiple metrics and dimensions with the same names, use a table alias to assign different names to the column
  headers. See [Handling duplicate column names in the output](/user-guide/views-semantic/querying#label-semantic-views-duplicate-columns).

## Examples

See [Querying semantic views](/user-guide/views-semantic/querying).
