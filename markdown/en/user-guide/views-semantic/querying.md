# Querying semantic views

To query a semantic view, you can use a standard [SELECT statement](/sql-reference/constructs). Within this statement, you
can use one of the following approaches:

- Specify the SEMANTIC\_VIEW clause in the FROM clause. For example:

  Copy code

  ```
  SELECT * FROM SEMANTIC_VIEW(
   tpch_analysis
   DIMENSIONS customer.customer_market_segment
   METRICS orders.order_average_value
    )
    ORDER BY customer_market_segment;
  ```

  For information, see [Specifying the SEMANTIC\_VIEW clause in the FROM clause](#label-semantic-views-querying-semantic-view-clause).
- Specify the name of the semantic view in the FROM clause. For example:

  Copy code

  ```
  SELECT customer_market_segment, AGG(order_average_value)
    FROM tpch_analysis
    GROUP BY customer_market_segment
    ORDER BY customer_market_segment;
  ```

  For information, see [Specifying the name of the semantic view in the FROM clause](#label-semantic-views-querying-standard-sql).

## Privileges required to query a semantic view

If you are using a role that does not own the semantic view, you must be granted the SELECT privilege on that semantic view to
query that semantic view.

Note

To query a semantic view, you don’t need the SELECT privilege on the tables used in the semantic view. You only need the
SELECT privilege on the semantic view itself.

This behavior is consistent with [the privileges required to query standard views](/user-guide/views-introduction#label-views-privileges).

For information about granting privileges on semantic views, see [Granting privileges on semantic views](/user-guide/views-semantic/sql#label-semantic-views-privileges).

## Specifying the SEMANTIC\_VIEW clause in the FROM clause

To query a semantic view, you can specify the [SEMANTIC\_VIEW clause](/sql-reference/constructs/semantic_view) in the FROM
clause.

The following example selects the `customer_market_segment` dimension and the `order_average_value` metric from the
`tpch_analysis` semantic view, [which you defined earlier](/user-guide/views-semantic/example):

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
    tpch_analysis
    DIMENSIONS customer.customer_market_segment
    METRICS orders.order_average_value
  )
  ORDER BY customer_market_segment;
```

```
+-------------------------+---------------------+
| CUSTOMER_MARKET_SEGMENT | ORDER_AVERAGE_VALUE |
+-------------------------+---------------------+
| AUTOMOBILE              |     142570.25947219 |
| FURNITURE               |     142563.63314267 |
| MACHINERY               |     142655.91550608 |
| HOUSEHOLD               |     141659.94753445 |
| BUILDING                |     142425.37987558 |
+-------------------------+---------------------+
```

Note that you can define an alias for a dimension or metric by specifying the alias after the dimension or metric name. You can
also specify the optional keyword AS before the alias. The following example runs the same query but uses the aliases `segment`
and `average` for the dimension and metric returned in the results.

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
    tpch_analysis
    DIMENSIONS customer.customer_market_segment AS segment
    METRICS orders.order_average_value average
  )
  ORDER BY segment;
```

```
+------------+-----------------+
| SEGMENT    |         AVERAGE |
|------------+-----------------|
| AUTOMOBILE | 142570.25947219 |
| BUILDING   | 142425.37987558 |
| FURNITURE  | 142563.63314267 |
| HOUSEHOLD  | 141659.94753445 |
| MACHINERY  | 142655.91550608 |
+------------+-----------------+
```

The following example selects the `customer_name` dimension and the `c_customer_order_count` fact from the
`tpch_analysis` semantic view:

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
    tpch_analysis
    DIMENSIONS customer.customer_name
    FACTS customer.c_customer_order_count
  )
  ORDER BY customer_name
  LIMIT 5;
```

```
+--------------------+------------------------+
| CUSTOMER_NAME      | C_CUSTOMER_ORDER_COUNT |
|--------------------+------------------------|
| Customer#000000001 |                      9 |
| Customer#000000002 |                     11 |
| Customer#000000003 |                      0 |
| Customer#000000004 |                     20 |
| Customer#000000005 |                     10 |
+--------------------+------------------------+
```

### Guidelines for specifying the SEMANTIC\_VIEW clause

When specifying the SEMANTIC\_VIEW clause, follow these guidelines:

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

To return all metrics or dimensions in a given logical table, use an asterisk as a wildcard, qualified by the name of the logical
table. For example, to return all metrics and dimensions defined in the `customer` logical table:

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
  tpch_analysis
  DIMENSIONS customer.*
  METRICS customer.*
);
```

```
+-----------------------+-------------------------+--------------------+----------------------+----------------------+----------------+----------------------+
| CUSTOMER_COUNTRY_CODE | CUSTOMER_MARKET_SEGMENT | CUSTOMER_NAME      | CUSTOMER_NATION_NAME | CUSTOMER_REGION_NAME | CUSTOMER_COUNT | CUSTOMER_ORDER_COUNT |
|-----------------------+-------------------------+--------------------+----------------------+----------------------+----------------+----------------------|
| 18                    | BUILDING                | Customer#000034857 | INDIA                | ASIA                 |              1 |                    0 |
| 14                    | AUTOMOBILE              | Customer#000145116 | EGYPT                | MIDDLE EAST          |              1 |                    0 |
...
```

### Examples of specifying the SEMANTIC\_VIEW clause

The following examples use the `tpch_analysis` view defined in [Example of using SQL to create a semantic view](/user-guide/views-semantic/example):

- [Retrieving a metric](#retrieving-a-metric)
- [Grouping metric data by a dimension](#grouping-metric-data-by-a-dimension)
- [Using the SEMANTIC\_VIEW subclause with other constructs](#using-the-semantic-view-subclause-with-other-constructs)
- [Specifying scalar expressions that use dimensions](#specifying-scalar-expressions-that-use-dimensions)
- [Specifying the WHERE clause](#specifying-the-where-clause)
- [Specifying facts in the WHERE clause](#specifying-facts-in-the-where-clause)

#### Retrieving a metric

The following statement retrieves the total count of customers by querying a metric:

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
    tpch_analysis
    METRICS customer.customer_count
  );
```

```
+----------------+
| CUSTOMER_COUNT |
+----------------+
|          15000 |
+----------------+
```

#### Grouping metric data by a dimension

The following statement groups metric data (`order_average_value`) by a dimension (`customer_market_segment`):

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
    tpch_analysis
    DIMENSIONS customer.customer_market_segment
    METRICS orders.order_average_value
  );
```

```
+-------------------------+---------------------+
| CUSTOMER_MARKET_SEGMENT | ORDER_AVERAGE_VALUE |
+-------------------------+---------------------+
| AUTOMOBILE              |     142570.25947219 |
| FURNITURE               |     142563.63314267 |
| MACHINERY               |     142655.91550608 |
| HOUSEHOLD               |     141659.94753445 |
| BUILDING                |     142425.37987558 |
+-------------------------+---------------------+
```

#### Using the SEMANTIC\_VIEW subclause with other constructs

The following example demonstrates how you can use dimensions and metrics in the SEMANTIC\_VIEW subclause with other SQL
constructs to filter, sort, and limit results:

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
    tpch_analysis
    DIMENSIONS customer.customer_name
    METRICS orders.average_line_items_per_order,
            orders.order_average_value
  )
  WHERE average_line_items_per_order > 4
  ORDER BY average_line_items_per_order DESC
  LIMIT 5;
```

```
+--------------------+------------------------------+---------------------+
| CUSTOMER_NAME      | AVERAGE_LINE_ITEMS_PER_ORDER | ORDER_AVERAGE_VALUE |
+--------------------+------------------------------+---------------------+
| Customer#000045678 |                         6.87 |           175432.21 |
| Customer#000067890 |                         6.42 |           182376.58 |
| Customer#000012345 |                         5.93 |           169847.42 |
| Customer#000034567 |                         5.76 |           178952.36 |
| Customer#000056789 |                         5.64 |           171248.75 |
+--------------------+------------------------------+---------------------+
```

#### Specifying scalar expressions that use dimensions

The following example uses a scalar expression that refers to a dimension in the DIMENSIONS clause:

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
    tpch_analysis
    DIMENSIONS DATE_PART('year', orders.order_date) AS year
  )
  ORDER BY year;
```

```
+------+
| YEAR |
|------|
| 1992 |
| 1993 |
| 1994 |
| 1995 |
| 1996 |
| 1997 |
| 1998 |
+------+
```

#### Specifying the WHERE clause

The following example specifies a WHERE clause that refers to a dimension in the DIMENSIONS clause:

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
    tpch_analysis
    DIMENSIONS orders.order_date
    METRICS orders.average_line_items_per_order,
            orders.order_average_value
    WHERE orders.order_date > '1995-01-01'
  )
  ORDER BY order_date ASC
  LIMIT 5;
```

```
+------------+------------------------------+---------------------+
| ORDER_DATE | AVERAGE_LINE_ITEMS_PER_ORDER | ORDER_AVERAGE_VALUE |
|------------+------------------------------+---------------------|
| 1995-01-02 |                     3.884547 |     151237.54900533 |
| 1995-01-03 |                     3.894819 |     145751.84384615 |
| 1995-01-04 |                     3.838863 |     145331.39167457 |
| 1995-01-05 |                     4.040689 |     150723.67353678 |
| 1995-01-06 |                     3.990755 |     152786.54109399 |
+------------+------------------------------+---------------------+
```

#### Specifying facts in the WHERE clause

The following example uses the `region.r_name` fact in a condition in the WHERE clause:

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
    tpch_analysis
    FACTS customer.c_customer_order_count
    WHERE orders.order_date < '2021-01-01' AND region.r_name = 'AMERICA'
  );
```

## Specifying the name of the semantic view in the FROM clause

You can specify the name of the semantic view in the FROM clause of a SELECT statement, as you would when querying a standard SQL
view:

Copy code

```
SELECT [ DISTINCT ]
    {
      [<qualifiers>.]<dimension_or_fact>                          |
      <scalar_expression_over_dimension_or_fact>                  |
      AGG( [<qualifiers>.]<metric> )                              |
      <aggregate_function>( [<qualifiers>.]<dimension_for_fact> )
    }
    [ , ... ]
  FROM <semantic_view> [ AS <alias> ]
  [ WHERE <expr_using_dimensions_or_facts> ]
  [ GROUP BY <expr_using_dimensions_or_facts> [ , ... ] ]
  [ HAVING <expr_using_metrics> ]
  [ ORDER BY ... ]
  [ LIMIT ... ]
```

Internally, this statement is rewritten as a SELECT statement that uses the
[SEMANTIC\_VIEW clause](#label-semantic-views-querying-semantic-view-clause):

- The expressions that you specify in the GROUP BY clause are rewritten into the DIMENSIONS clause in the SEMANTIC\_VIEW clause.

  In the SELECT statement, if you use an expression that is not in the GROUP BY clause (for example, a dimension
  expression in the SELECT list), the rewrite uses that expression in the FACTS clause in the SEMANTIC\_VIEW clause.
- When you refer to a metric that is defined in a semantic view, you must pass the metric to the AGG function.
- You can select ad-hoc metrics by passing a dimension or fact to any
  [aggregate function](/sql-reference/functions-aggregation).
- Any other calculated values that don’t fall into the first two categories are considered to be fact references.

The next sections explain these requirements in more detail:

- [Requirements for dimensions and metrics in a SELECT statement](#requirements-for-dimensions-and-metrics-in-a-select-statement)
- [Selecting metrics](#selecting-metrics)
- [Selecting dimensions](#selecting-dimensions)
- [Specifying the WHERE clause](#specifying-the-where-clause-1)
- [Specifying the HAVING clause](#specifying-the-having-clause)
- [Limitations with specifying the semantic view name in the FROM clause](#limitations-with-specifying-the-semantic-view-name-in-the-from-clause)

### Requirements for dimensions and metrics in a SELECT statement

When you specify the name of a semantic view in the `FROM` clause, you can reference dimensions, facts, and metrics
using their bare (unqualified) names or using dot-notation to qualify them with the entity (logical table) name.

**Bare names** work when a calculation name is unique across all entities in the semantic view, or when you reference
derived metrics and LOD metrics that are not bound to a specific entity:

Copy code

```
SELECT customer_market_segment, AGG(order_average_value)
  FROM tpch_analysis
  GROUP BY customer_market_segment;
```

**Dot-notation** (`entity.calculation`) is required when two or more entities define a calculation with the same
name. For example, suppose that a semantic view has two dimensions that share the unqualified name `name`:

Copy code

```
DIMENSIONS (
  nation.name AS nation.n_name,
  region.name AS region.r_name
);
```

Use dot-notation to specify which entity’s calculation you want:

Copy code

```
SELECT nation.name, region.name
  FROM duplicate_names
  GROUP BY nation.name, region.name;
```

If you use a bare name that is ambiguous, the query fails with an error:

Copy code

```
-- Fails: 'name' exists in both the nation and region entities
SELECT name FROM duplicate_names GROUP BY name;
```

```
SQL compilation error: Ambiguous column name 'NAME'.
```

You can also use dot-notation for unambiguous calculations. In that case, the entity qualifier is optional but
can improve readability.

### Selecting metrics

If you want to select a metric that is defined in a semantic view, you must pass the metric to the
[AGG](/sql-reference/functions/agg) function, which is a special aggregate function for metrics in semantic views.

For example:

Copy code

```
SELECT AGG(order_average_value) FROM tpch_analysis;
```

Note

The AGG function has no effect on the metric because the function evaluates one value of the metric.

In the SELECT list, you can specify an expression that uses a metric. For example:

Copy code

```
SELECT AGG(order_average_value) * 10 FROM tpch_analysis;
```

You can also define and select ad-hoc metrics by passing a dimension or fact to any
[aggregate function](/sql-reference/functions-aggregation). For example:

Copy code

```
SELECT COUNT(customer_market_segment) FROM tpch_analysis;
```

### Selecting dimensions

If the SELECT list includes dimensions, you must specify those dimensions in the GROUP BY clause. For example:

Copy code

```
SELECT customer_market_segment, customer_nation_name, AGG(order_average_value)
  FROM tpch_analysis
  GROUP BY customer_market_segment, customer_nation_name;
```

In the SELECT list and in the GROUP BY clause, you can specify a dimension or a scalar expression that uses a dimension or a fact.
For example:

Copy code

```
SELECT LOWER(customer_nation_name), AGG(order_average_value)
  FROM tpch_analysis
  GROUP BY customer_nation_name;
```

### Specifying the WHERE clause

In the WHERE clause, you can only use conditional expressions that refer to dimensions or facts. For example:

Copy code

```
SELECT customer_market_segment, AGG(order_average_value)
  FROM tpch_analysis
  WHERE customer_market_segment = 'BUILDING'
  GROUP BY customer_market_segment;
```

The dimensions must be reachable by every metric used in the query.

### Specifying the HAVING clause

In the HAVING clause, you can only specify metrics, and you must pass them to one of the aggregate functions listed in
[Selecting metrics](#label-semantic-views-query-standard-metrics). For example:

Copy code

```
SELECT customer_market_segment, AGG(order_average_value)
  FROM tpch_analysis
  GROUP BY customer_market_segment
  HAVING AGG(order_average_value) > 142500;
```

### Limitations with specifying the semantic view name in the FROM clause

You cannot specify the following in the SELECT statement:

- Extensions of the FROM clause, including:

  - PIVOT
  - UNPIVOT
  - MATCH\_RECOGNIZE
  - LATERAL
- Joins
- Window function calls
- QUALIFY
- Correlated subqueries (uncorrelated subqueries in WHERE and DIMENSIONS ad-hoc expressions are supported; see [Using subqueries in semantic view queries](#label-semantic-views-querying-subqueries))

## Choosing the dimensions that you can return for a given metric

When you specify a dimension and a metric to return, the base table for the dimension must be related to the base table for the
metric. In addition, the base table for the dimension must have an equal or lower level of granularity than the base table for
the metric.

For example, suppose that you query the `tpch_analysis` semantic view that you created in [Example of using SQL to create a semantic view](/user-guide/views-semantic/example), and you want to return
the `orders.order_date` dimension and the `customer.customer_order_count` metric:

Copy code

```
SELECT * FROM SEMANTIC_VIEW (
  tpch_analysis
  DIMENSIONS orders.order_date
  METRICS customer.customer_order_count
);
```

This query fails because the `orders` table for the `order_date` dimension has a higher level of granularity than the
`customer` table for the `customer_order_count` metric:

```
010234 (42601): SQL compilation error:
Invalid dimension specified: The dimension entity 'ORDERS' must be related to and
  have an equal or lower level of granularity compared to the base metric or dimension entity 'CUSTOMER'.
```

To list the dimensions that you can return with a specific metric, run the
[SHOW SEMANTIC DIMENSIONS FOR METRIC](/sql-reference/sql/show-semantic-dimensions-for-metric) command. For example:

Copy code

```
SHOW SEMANTIC DIMENSIONS IN tpch_analysis FOR METRIC customer_order_count;
```

```
+------------+-------------------------+-------------+----------+----------+---------+
| table_name | name                    | data_type   | required | synonyms | comment |
|------------+-------------------------+-------------+----------+----------+---------|
| CUSTOMER   | CUSTOMER_COUNTRY_CODE   | VARCHAR(15) | false    | NULL     | NULL    |
| CUSTOMER   | CUSTOMER_MARKET_SEGMENT | VARCHAR(10) | false    | NULL     | NULL    |
| CUSTOMER   | CUSTOMER_NAME           | VARCHAR(25) | false    | NULL     | NULL    |
| CUSTOMER   | CUSTOMER_NATION_NAME    | VARCHAR(25) | false    | NULL     | NULL    |
| CUSTOMER   | CUSTOMER_REGION_NAME    | VARCHAR(25) | false    | NULL     | NULL    |
| NATION     | NATION_NAME             | VARCHAR(25) | false    | NULL     | NULL    |
+------------+-------------------------+-------------+----------+----------+---------+
```

## Handling duplicate column names in the output

When a semantic view contains multiple calculations with the same name across different entities, you can
use dot-notation (`entity.calculation`) to disambiguate them in both the `SEMANTIC_VIEW` clause and the
standard SQL `FROM` clause.

### Using dot-notation in standard SQL

For example, suppose that you define the following semantic view with the dimensions `nation.name` and
`region.name`:

Copy code

```
CREATE OR REPLACE SEMANTIC VIEW duplicate_names

  TABLES (
    nation AS SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.NATION PRIMARY KEY (n_nationkey),
    region AS SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.REGION PRIMARY KEY (r_regionkey)
  )

  RELATIONSHIPS (
    nation (n_regionkey) REFERENCES region
  )

  DIMENSIONS (
    nation.name AS nation.n_name,
    region.name AS region.r_name
  );
```

Use dot-notation to select both dimensions:

Copy code

```
SELECT nation.name, region.name
  FROM duplicate_names
  GROUP BY nation.name, region.name;
```

```
+----------------+-------------+
| NAME           | NAME        |
+----------------+-------------+
| BRAZIL         | AMERICA     |
| MOROCCO        | AFRICA      |
| UNITED KINGDOM | EUROPE      |
| IRAN           | MIDDLE EAST |
| FRANCE         | EUROPE      |
| ...            | ...         |
+----------------+-------------+
```

To rename the output columns, use column aliases:

Copy code

```
SELECT nation.name AS nation_name, region.name AS region_name
  FROM duplicate_names
  GROUP BY nation.name, region.name;
```

```
+----------------+-------------+
| NATION_NAME    | REGION_NAME |
+----------------+-------------+
| BRAZIL         | AMERICA     |
| MOROCCO        | AFRICA      |
| UNITED KINGDOM | EUROPE      |
| IRAN           | MIDDLE EAST |
| FRANCE         | EUROPE      |
| ...            | ...         |
+----------------+-------------+
```

### SHOW COLUMNS behavior for ambiguous names

When a semantic view contains ambiguous calculation names, `SHOW COLUMNS` emits a separate row for
each calculation. For ambiguous names, the column name is reported using the `entity.calcName` convention
(for example, `orders.revenue`). This behavior ensures complete catalog visibility for both users and
downstream tools.

### BI tool compatibility

BI tools that rely on `SHOW COLUMNS` to discover available columns might automatically wrap dot-notation
column names in double quotes when generating queries (for example, `SELECT "orders.revenue" FROM sales_sv`).
Snowflake recognizes these quoted identifiers and resolves them to the correct entity and calculation,
so BI tool queries work without additional configuration.

## Defining and querying window function metrics

You can define metrics that call [window functions](/sql-reference/functions-window-syntax) and pass in aggregated values.
These metrics are called *window function metrics*.

The following examples illustrate the difference between a window function metric and a metric that passes a row-level
expression to a window function:

- The following metric is a window function metric:

  Copy code

  ```
  METRICS (
    table_1.metric_1 AS SUM(table_1.metric_3) OVER( ... )
  )
  ```

  In this example, the SUM window function takes another metric (`table_1.metric_3`) as an argument.

  The following metric is also a window function metric:

  Copy code

  ```
  METRICS (
    table_1.metric_2 AS SUM(
   SUM(table_1.column_1)
    ) OVER( ... )
  )
  ```

  In this example, the SUM window function takes a valid metric expression (`SUM(table_1.column_1)`) as an argument.
- The following metric is not a window function metric:

  Copy code

  ```
  METRICS (
    table_1.metric_1 AS SUM(
   SUM(table_1.column_1) OVER( ... )
    )
  )
  ```

  In this example, the SUM window function takes a column (`table_1.column_1`) as an argument, and the result of that window
  function call is passed to a separate SUM aggregate function call.

The following sections explain how to define and query window function metrics:

- [Defining window function metrics](#defining-window-function-metrics)
- [Querying window function metrics](#querying-window-function-metrics)

### Defining window function metrics

When specifying a window function call, use [this syntax](/sql-reference/sql/create-semantic-view#label-create-semantic-view-window-function-syntax), which is
described in [Parameters for window function metrics](/sql-reference/sql/create-semantic-view#label-create-semantic-view-window-function).

The following example creates a semantic view that includes the definitions of several window function metrics. The example uses
tables from the [TPC-DS](/user-guide/sample-data-tpcds) sample database. For information on accessing this database, see
[Add the TPC-DS data set to your account](/user-guide/sample-data-tpcds#label-sample-data-tpc-ds-adding).

Copy code

```
CREATE OR REPLACE SEMANTIC VIEW sv_window_function_example
  TABLES (
    store_sales AS SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.store_sales,
    date AS SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.date_dim PRIMARY KEY (d_date_sk)
  )
  RELATIONSHIPS (
    sales_to_date AS store_sales(ss_sold_date_sk) REFERENCES date(d_date_sk)
  )
  DIMENSIONS (
    date.date AS d_date,
    date.d_date_sk AS d_date_sk,
    date.year AS d_year
  )
  METRICS (
    store_sales.total_sales_quantity AS SUM(ss_quantity)
      WITH SYNONYMS = ('Total sales quantity'),

    store_sales.avg_7_days_sales_quantity AS AVG(total_sales_quantity)
      OVER (PARTITION BY EXCLUDING date.date, date.year ORDER BY date.date
        RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW)
      WITH SYNONYMS = ('Running 7-day average of total sales quantity'),

    store_sales.total_sales_quantity_30_days_ago AS LAG(total_sales_quantity, 30)
      OVER (PARTITION BY EXCLUDING date.date, date.year ORDER BY date.date)
      WITH SYNONYMS = ('Sales quantity 30 days ago'),

    store_sales.avg_7_days_sales_quantity_30_days_ago AS AVG(total_sales_quantity)
      OVER (PARTITION BY EXCLUDING date.date, date.year ORDER BY date.date
        RANGE BETWEEN INTERVAL '36 days' PRECEDING AND INTERVAL '30 days' PRECEDING)
      WITH SYNONYMS = ('Running 7-day average of total sales quantity 30 days ago')

  );
```

You can also use other metrics from the same logical table in the metric definition. For example:

Copy code

```
METRICS (
  orders.m3 AS SUM(m2) OVER (PARTITION BY m1 ORDER BY m2),
  orders.m4 AS ((SUM(m2) OVER (..)) / m1) + 1
)
```

Note

You can’t use window function metrics in row-level calculations (facts and dimensions) or in the definitions of other metrics.

### Querying window function metrics

When you query a semantic view and the query returns a window function metric, you must also return the dimensions specified in
PARTITION BY `dimension`, PARTITION BY EXCLUDING `dimension`, and ORDER BY `dimension` in the
[CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) statement for the semantic view.

For example, suppose that you specify the `date.date` and `date.year` dimensions in the PARTITION BY EXCLUDING and ORDER BY
clauses in the definition of the `store_sales.avg_7_days_sales_quantity` metric:

Copy code

```
CREATE OR REPLACE SEMANTIC VIEW sv_window_function_example
  ...
  DIMENSIONS (
    ...
    date.date AS d_date,
    ...
    date.year AS d_year
    ...
  )
  METRICS (
    ...
    store_sales.avg_7_days_sales_quantity AS AVG(total_sales_quantity)
      OVER (PARTITION BY EXCLUDING date.date, date.year ORDER BY date.date
        RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW)
      WITH SYNONYMS = ('Running 7-day average of total sales quantity'),
    ...
  );
```

If you return the `store_sales.avg_7_days_sales_quantity` metric in a query, you must also return the `date.date` and
`date.year` dimensions:

Copy code

```
SELECT * FROM SEMANTIC_VIEW (
  sv_window_function_example
  DIMENSIONS date.date, date.year
  METRICS store_sales.avg_7_days_sales_quantity
);
```

If you omit the `date.date` and `date.year` dimensions, an error occurs.

```
010260 (42601): SQL compilation error:
Invalid semantic view query: Dimension 'DATE.DATE' used in a
   window function metric must be requested in the query.
```

To determine which dimensions you must specify in the query, execute the
[SHOW SEMANTIC DIMENSIONS FOR METRIC](/sql-reference/sql/show-semantic-dimensions-for-metric) command. For example, to determine the dimensions that you must
specify when retrieving the `store_sales.avg_7_days_sales_quantity` metric, run this command:

Copy code

```
SHOW SEMANTIC DIMENSIONS IN sv_window_function_example FOR METRIC avg_7_days_sales_quantity;
```

In the output of the command, the `required` column contains `true` for the dimensions that you must specify in the query.

```
+------------+-----------+--------------+----------+----------+---------+
| table_name | name      | data_type    | required | synonyms | comment |
|------------+-----------+--------------+----------+----------+---------|
| DATE       | DATE      | DATE         | true     | NULL     | NULL    |
| DATE       | D_DATE_SK | NUMBER(38,0) | false    | NULL     | NULL    |
| DATE       | YEAR      | NUMBER(38,0) | true     | NULL     | NULL    |
+------------+-----------+--------------+----------+----------+---------+
```

The following additional examples query the window function metrics defined in
[Defining window function metrics](#label-semantic-views-querying-window-defining). Note that the DIMENSIONS clause includes the dimensions specified in the
PARTITION BY EXCLUDING and ORDER BY clauses of the metric definitions.

The following example returns the sales quantity 30 days ago:

Copy code

```
SELECT * FROM SEMANTIC_VIEW (
  sv_window_function_example
  DIMENSIONS date.date, date.year
  METRICS store_sales.total_sales_quantity_30_days_ago
);
```

The following example returns the running 7-day average of the total sales quantity 30 days ago:

Copy code

```
SELECT * FROM SEMANTIC_VIEW (
  sv_window_function_example
  DIMENSIONS date.date, date.year
  METRICS store_sales.avg_7_days_sales_quantity_30_days_ago
);
```

## Using subqueries in semantic view queries

You can use uncorrelated subqueries to filter or categorize semantic view results using values
computed by independent queries against any Snowflake object, including other semantic views.

The following table summarizes subquery support:

|  | WHERE clause | DIMENSIONS ad-hoc expressions |
| --- | --- | --- |
| **Uncorrelated** | Supported | Supported |
| **Correlated** | Not supported | Not supported |

Expand

Show lessSee more

Both the SEMANTIC\_VIEW clause and specifying the semantic view name in the FROM clause support subqueries.

### Subqueries in the WHERE clause

A subquery in the WHERE clause filters rows of the semantic view result before aggregation.
All standard Snowflake subquery operators are supported: `[NOT] IN`, `[NOT] EXISTS`,
`ALL`, `ANY`, and scalar subqueries in comparison contexts (`=`, `>`, `<`, and so on).

The following examples assume these base tables and semantic views:

Copy code

```
CREATE OR REPLACE TABLE t_orders(order_id INT, cust_id INT, amount NUMBER);
INSERT INTO t_orders VALUES (1, 101, 100), (2, 102, 200), (3, 103, 300), (4, 101, 120);

CREATE OR REPLACE TABLE t_customers(cust_id INT, region VARCHAR);
INSERT INTO t_customers VALUES (100, 'NORTH'), (100, 'SOUTH'), (101, 'EAST'), (102, 'WEST');

CREATE OR REPLACE SEMANTIC VIEW sv_orders
  TABLES (ord AS t_orders PRIMARY KEY (order_id))
  FACTS (ord.f_amount AS amount)
  DIMENSIONS (ord.d_cust_id AS cust_id, ord.d_ord_id AS order_id)
  METRICS (ord.m_total AS SUM(amount));

CREATE OR REPLACE SEMANTIC VIEW sv_customers
  TABLES (cust AS t_customers PRIMARY KEY (cust_id))
  FACTS (cust.f_cust_id AS cust_id)
  DIMENSIONS (cust.d_region AS region, cust.d_cust_id AS cust_id);
```

The following examples use the SEMANTIC\_VIEW clause:

Copy code

```
-- Filter to customers that appear in t_customers
SELECT * FROM SEMANTIC_VIEW(
  sv_orders
  DIMENSIONS ord.d_cust_id
  METRICS ord.m_total
  WHERE ord.d_cust_id IN (SELECT cust_id FROM t_customers));

-- Exclude customers from a specific region
SELECT * FROM SEMANTIC_VIEW(
  sv_orders
  DIMENSIONS ord.d_cust_id
  WHERE d_cust_id NOT IN (SELECT cust_id FROM t_customers WHERE region = 'WEST'));

-- Scalar subquery comparison
SELECT * FROM SEMANTIC_VIEW(
  sv_orders
  DIMENSIONS ord.d_cust_id
  WHERE d_cust_id = (SELECT MIN(cust_id) FROM t_customers));
```

When you specify the semantic view name in the FROM clause, the same subquery operators are supported in the WHERE clause:

Copy code

```
SELECT d_cust_id, AGG(m_total)
  FROM sv_orders
  WHERE d_cust_id IN (SELECT cust_id FROM t_customers)
  GROUP BY d_cust_id;
```

You can also use a subquery against another semantic view:

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
  sv_orders
  DIMENSIONS ord.d_cust_id
  METRICS ord.m_total
  WHERE ord.d_cust_id IN (
    SELECT * FROM SEMANTIC_VIEW(
      sv_customers
      DIMENSIONS cust.d_cust_id
      WHERE cust.d_region = 'EAST')));
```

### Subqueries in DIMENSIONS ad-hoc expressions

A subquery in a DIMENSIONS ad-hoc expression creates a computed dimension. The subquery
must appear as part of an expression that references at least one semantic view calculation.
A standalone subquery with no semantic view column reference is not valid.

Copy code

```
-- Group rows by whether cust_id appears in the subquery result (TRUE/FALSE)
SELECT * FROM SEMANTIC_VIEW(
  sv_orders
  DIMENSIONS ord.d_cust_id IN (SELECT cust_id FROM t_customers)
  METRICS ord.m_total);

-- CASE expression using a subquery
SELECT * FROM SEMANTIC_VIEW(
  sv_orders
  DIMENSIONS CASE WHEN d_cust_id IN (SELECT cust_id FROM t_customers)
               THEN d_cust_id ELSE -1 END
  METRICS m_total);

-- Scalar arithmetic with a scalar subquery
SELECT * FROM SEMANTIC_VIEW(
  sv_orders
  DIMENSIONS ord.d_cust_id + (SELECT MIN(cust_id) FROM t_customers)
  METRICS ord.m_total);
```

When you specify the semantic view name in the FROM clause, the subquery expression goes in the SELECT list and must be
included in GROUP BY. You can use an ordinal, alias, or the full expression:

Copy code

```
-- GROUP BY alias
SELECT d_cust_id IN (SELECT cust_id FROM t_customers) AS is_known_cust,
       AGG(m_total)
  FROM sv_orders
  GROUP BY is_known_cust;

-- GROUP BY ordinal
SELECT d_cust_id IN (SELECT cust_id FROM t_customers), AGG(m_total)
  FROM sv_orders
  GROUP BY 1;
```

### Subquery restrictions

- **Correlated subqueries are not supported.** Any reference from inside a subquery to a
  calculation in the outer semantic view query is rejected:

  Copy code

  ```
  -- Invalid: references d_cust_id from the outer query
  SELECT * FROM SEMANTIC_VIEW(
    sv_orders
    DIMENSIONS ord.d_cust_id
    METRICS ord.m_total
    WHERE ord.d_cust_id IN (
      SELECT cust_id FROM t_customers WHERE cust_id = d_cust_id));
  -- Error: Unsupported feature 'CORRELATED SUBQUERIES'.
  ```
- **Subqueries are not supported in FACTS or METRICS ad-hoc expressions:**

  Copy code

  ```
  -- Invalid: subquery in a FACTS expression
  SELECT * FROM SEMANTIC_VIEW(
    sv_orders
    FACTS f_amount * (SELECT MAX(amount) FROM t_orders));
  -- Error: Subqueries are not allowed in fact expressions

  -- Invalid: subquery in a METRICS expression
  SELECT * FROM SEMANTIC_VIEW(
    sv_orders
    METRICS m_total / (SELECT COUNT(*) FROM t_customers));
  -- Error: Subqueries are not allowed in metric expressions
  ```
- **A standalone subquery is not a valid DIMENSIONS expression.** The subquery must appear
  as part of an expression that references a semantic view calculation:

  Copy code

  ```
  -- Invalid: no semantic view calculation referenced
  SELECT * FROM SEMANTIC_VIEW(
    sv_orders
    DIMENSIONS (SELECT cust_id FROM t_customers)
    METRICS ord.m_total);
  -- Error: Invalid expression in dimension expression.
  --        Missing reference to a row-level expression.
  ```
- **If the subquery is itself a SEMANTIC\_VIEW() query, all standard semantic view rules
  apply to it**, including the restriction that aggregate functions are not allowed in the WHERE
  clause.

Note

Cortex Analyst does not generate semantic SQL queries that use subqueries. Subqueries are
available only in manually authored queries.
