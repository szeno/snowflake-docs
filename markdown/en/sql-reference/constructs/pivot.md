Categories:
:   [Query syntax](/sql-reference/constructs)

# PIVOT

Rotates a table by turning the unique values from one column in the input expression into multiple columns and aggregating results
where required on any remaining column values. In a query, it is specified in the [FROM](/sql-reference/constructs/from) clause after
the table name or subquery.

PIVOT supports the following [built-in aggregate functions](/sql-reference/functions-aggregation):

- [AVG](/sql-reference/functions/avg)
- [COUNT](/sql-reference/functions/count)
- [MAX](/sql-reference/functions/max)
- [MIN](/sql-reference/functions/min)
- [SUM](/sql-reference/functions/sum)

PIVOT can be used to transform a narrow table (for example, `empid`, `month`, `sales`) into a wider table
(for example, `empid`, `jan_sales`, `feb_sales`, `mar_sales`).

See also:
:   [UNPIVOT](/sql-reference/constructs/unpivot)

## Syntax

Copy code

```
SELECT ...
FROM ...
   PIVOT ( <aggregate_function> ( <pivot_column> ) [ [ AS ] <alias> ]
            FOR <value_column> IN (
              <pivot_value_1> [ [ AS ] <alias> ] [ , <pivot_value_2> [ [ AS ] <alias> ] ... ]
              | ANY [ ORDER BY ... ]
              | <subquery>
            )
            [ DEFAULT ON NULL (<value>) ]
         )

[ ... ]
```

## Parameters

`aggregate_function`
:   The aggregate function for combining the grouped values from `pivot_column`.

`pivot_column [ [ AS ] alias ]`
:   The column from the source table or subquery that will be aggregated.

    The optional `[ AS ] alias` clause specifies the alias to use for the aggregate in the result of
    the PIVOT operation. An underscore and then the alias is appended to each pivot column name. For example,
    if the `alias` is `total`, then the pivot operation appends `_TOTAL` to the pivot column names.
    The AS keyword is optional.

`value_column`
:   The column from the source table or subquery that contains the values from which column names will be generated.

`pivot_value_N [ [ AS ] alias ]`
:   A list of values for the pivot column to pivot into headings in the query results.

    The optional `[ AS ] alias` clause specifies the alias to use for the value in the result of
    the PIVOT operation. The alias replaces the value.

`ANY [ ORDER BY ... ]`

> Pivot on all distinct values of the pivot column. To control the order of the pivot columns in the output,
> specify an [ORDER BY](/sql-reference/constructs/order-by) clause after the ANY keyword. If the pivot column contains NULLs,
> then NULL is also treated as a pivot value.

`subquery`
> Pivot on all values found in the subquery. The DISTINCT keyword is required if the subquery includes an
> ORDER BY clause. The subquery must be an uncorrelated subquery that returns a single column. Pivoting is
> performed on all distinct values returned by the subquery. For information about uncorrelated subqueries,
> see [Working with Subqueries](/user-guide/querying-subqueries).

`DEFAULT ON NULL` (`value`)
:   Replace all NULL values in the pivot result with the specified default value. The default value can be any scalar
    expression that does not depend on the pivot and aggregation column.

## Usage notes

- Snowflake supports *dynamic pivot*. A dynamic pivot query uses the ANY keyword or a subquery in the PIVOT
  subclause instead of specifying the pivot values explicitly.
- When dynamic pivot is used in a [view](/user-guide/views-introduction) definition, queries on the view
  might fail if the underlying data changes so that the pivot output columns are changed.
- Dynamic pivot isn’t supported in the body of a stored procedure or user-defined function (UDF).
- A pivot query that doesn’t use dynamic pivot can return output with duplicate columns. We recommend avoiding
  output with duplicate columns. A dynamic pivot query deduplicates duplicate columns.
- A pivot query that doesn’t use dynamic pivot might fail if it attempts to
  [CAST](/sql-reference/functions/cast) a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) column to a different
  data type. Dynamic pivot queries don’t have this limitation.
- Currently, the PIVOT semantic doesn’t allow multiple aggregations, but you can achieve similar results by using
  PIVOT with the [UNION operator](/sql-reference/operators-query#label-query-operators-union). For an example, see
  [Dynamic pivot with multiple aggregations using UNION](#label-pivot-example-multiple-aggregations).

## Examples

The PIVOT examples use the following `quarterly_sales` table:

Copy code

```
CREATE OR REPLACE TABLE quarterly_sales(
  empid INT,
  amount INT,
  quarter TEXT)
  AS SELECT * FROM VALUES
    (1, 10000, '2023_Q1'),
    (1, 400, '2023_Q1'),
    (2, 4500, '2023_Q1'),
    (2, 35000, '2023_Q1'),
    (1, 5000, '2023_Q2'),
    (1, 3000, '2023_Q2'),
    (2, 200, '2023_Q2'),
    (2, 90500, '2023_Q2'),
    (1, 6000, '2023_Q3'),
    (1, 5000, '2023_Q3'),
    (2, 2500, '2023_Q3'),
    (2, 9500, '2023_Q3'),
    (3, 2700, '2023_Q3'),
    (1, 8000, '2023_Q4'),
    (1, 10000, '2023_Q4'),
    (2, 800, '2023_Q4'),
    (2, 4500, '2023_Q4'),
    (3, 2700, '2023_Q4'),
    (3, 16000, '2023_Q4'),
    (3, 10200, '2023_Q4');
```

The following examples use PIVOT:

- [Dynamic pivot on all distinct column values automatically](#label-pivot-example-dynamic)
- [Dynamic pivot on column values using a subquery](#label-pivot-example-subquery)
- [Dynamic pivot with multiple aggregations using UNION](#label-pivot-example-multiple-aggregations)
- [Dynamic pivot with a join query](#label-pivot-example-join)
- [Pivot on a specified list of column values for the pivot column](#label-pivot-example-column-list)
- [Pivot with a default value for NULL values](#label-pivot-example-default-on-nulls)
- [Pivot examples that involve multiple columns](#label-pivot-example-multiple-columns)

### Dynamic pivot on all distinct column values automatically

Given the table `quarterly_sales`, pivot on the `amount` column using the ANY keyword to sum the
total sales per employee for all of the distinct quarters, and specify ORDER BY so that the pivot columns
are in order:

Copy code

```
SELECT *
  FROM quarterly_sales
    PIVOT(SUM(amount) FOR quarter IN (ANY ORDER BY quarter))
  ORDER BY empid;
```

```
+-------+-----------+-----------+-----------+-----------+
| EMPID | '2023_Q1' | '2023_Q2' | '2023_Q3' | '2023_Q4' |
|-------+-----------+-----------+-----------+-----------|
|     1 |     10400 |      8000 |     11000 |     18000 |
|     2 |     39500 |     90700 |     12000 |      5300 |
|     3 |      NULL |      NULL |      2700 |     28900 |
+-------+-----------+-----------+-----------+-----------+
```

The following example is the same as the previous example, but it appends the alias `_TOTAL` to
each pivot column name:

Copy code

```
SELECT *
  FROM quarterly_sales
    PIVOT(SUM(amount) AS total FOR quarter IN (ANY ORDER BY quarter))
  ORDER BY empid;
```

```
+-------+-----------------+-----------------+-----------------+-----------------+
| EMPID | '2023_Q1_TOTAL' | '2023_Q2_TOTAL' | '2023_Q3_TOTAL' | '2023_Q4_TOTAL' |
|-------+-----------------+-----------------+-----------------+-----------------|
|     1 |           10400 |            8000 |           11000 |           18000 |
|     2 |           39500 |           90700 |           12000 |            5300 |
|     3 |            NULL |            NULL |            2700 |           28900 |
+-------+-----------------+-----------------+-----------------+-----------------+
```

### Dynamic pivot on column values using a subquery

Assume that in addition to the `quarterly_sales` table, an `ad_campaign_types_by_quarter`
table tracks the types of advertisements run during particular quarters. This table has the following
structure and data:

Copy code

```
CREATE OR REPLACE TABLE ad_campaign_types_by_quarter(
  quarter VARCHAR,
  television BOOLEAN,
  radio BOOLEAN,
  print BOOLEAN)
  AS SELECT * FROM VALUES
    ('2023_Q1', TRUE, FALSE, FALSE),
    ('2023_Q2', FALSE, TRUE, TRUE),
    ('2023_Q3', FALSE, TRUE, FALSE),
    ('2023_Q4', TRUE, FALSE, TRUE);
```

You can use a subquery in a pivot query to determine the sum of the sales in the quarters that had
specific ad campaigns. For example, the following pivot query returns data only for quarters with
television ad campaigns:

Copy code

```
SELECT *
  FROM quarterly_sales
    PIVOT(SUM(amount) FOR quarter IN (
      SELECT DISTINCT quarter
        FROM ad_campaign_types_by_quarter
        WHERE television = TRUE
        ORDER BY quarter))
  ORDER BY empid;
```

```
+-------+-----------+-----------+
| EMPID | '2023_Q1' | '2023_Q4' |
|-------+-----------+-----------|
|     1 |     10400 |     18000 |
|     2 |     39500 |      5300 |
|     3 |      NULL |     28900 |
+-------+-----------+-----------+
```

### Dynamic pivot with multiple aggregations using UNION

You can use the [UNION operator](/sql-reference/operators-query#label-query-operators-union) to show multiple aggregations in
a single result set. This example uses dynamic pivot and the UNION operator to show the following
information for each employee in each quarter:

- The average amount of a sale, using the [AVG](/sql-reference/functions/avg) function.
- The sale with the highest value, using the [MAX](/sql-reference/functions/max) function.
- The sale with the lowest value, using the [MIN](/sql-reference/functions/min) function.
- The number of sales, using the [COUNT](/sql-reference/functions/count) function.
- The total amount for all sales, using the [SUM](/sql-reference/functions/sum) function.

Run the query:

Copy code

```
SELECT 'Average sale amount' AS aggregate, *
  FROM quarterly_sales
    PIVOT(AVG(amount) FOR quarter IN (ANY ORDER BY quarter))
UNION
SELECT 'Highest value sale' AS aggregate, *
  FROM quarterly_sales
    PIVOT(MAX(amount) FOR quarter IN (ANY ORDER BY quarter))
UNION
SELECT 'Lowest value sale' AS aggregate, *
  FROM quarterly_sales
    PIVOT(MIN(amount) FOR quarter IN (ANY ORDER BY quarter))
UNION
SELECT 'Number of sales' AS aggregate, *
  FROM quarterly_sales
    PIVOT(COUNT(amount) FOR quarter IN (ANY ORDER BY quarter))
UNION
SELECT 'Total amount' AS aggregate, *
  FROM quarterly_sales
    PIVOT(SUM(amount) FOR quarter IN (ANY ORDER BY quarter))
ORDER BY aggregate, empid;
```

```
+---------------------+-------+--------------+--------------+--------------+--------------+
| AGGREGATE           | EMPID |    '2023_Q1' |    '2023_Q2' |    '2023_Q3' |    '2023_Q4' |
|---------------------+-------+--------------+--------------+--------------+--------------|
| Average sale amount |     1 |  5200.000000 |  4000.000000 |  5500.000000 |  9000.000000 |
| Average sale amount |     2 | 19750.000000 | 45350.000000 |  6000.000000 |  2650.000000 |
| Average sale amount |     3 |         NULL |         NULL |  2700.000000 |  9633.333333 |
| Highest value sale  |     1 | 10000.000000 |  5000.000000 |  6000.000000 | 10000.000000 |
| Highest value sale  |     2 | 35000.000000 | 90500.000000 |  9500.000000 |  4500.000000 |
| Highest value sale  |     3 |         NULL |         NULL |  2700.000000 | 16000.000000 |
| Lowest value sale   |     1 |   400.000000 |  3000.000000 |  5000.000000 |  8000.000000 |
| Lowest value sale   |     2 |  4500.000000 |   200.000000 |  2500.000000 |   800.000000 |
| Lowest value sale   |     3 |         NULL |         NULL |  2700.000000 |  2700.000000 |
| Number of sales     |     1 |     2.000000 |     2.000000 |     2.000000 |     2.000000 |
| Number of sales     |     2 |     2.000000 |     2.000000 |     2.000000 |     2.000000 |
| Number of sales     |     3 |     0.000000 |     0.000000 |     1.000000 |     3.000000 |
| Total amount        |     1 | 10400.000000 |  8000.000000 | 11000.000000 | 18000.000000 |
| Total amount        |     2 | 39500.000000 | 90700.000000 | 12000.000000 |  5300.000000 |
| Total amount        |     3 |         NULL |         NULL |  2700.000000 | 28900.000000 |
+---------------------+-------+--------------+--------------+--------------+--------------+
```

### Dynamic pivot with a join query

To pivot in a query with a join, you can use a [common table expression (CTE)](/user-guide/queries-cte)
for the pivot query.

For example, assume a simple table maps employees to managers:

Copy code

```
CREATE OR REPLACE TABLE emp_manager(
    empid INT,
    managerid INT)
  AS SELECT * FROM VALUES
    (1, 7),
    (2, 8),
    (3, 9);

SELECT * from emp_manager;
```

```
+-------+-----------+
| EMPID | MANAGERID |
|-------+-----------|
|     1 |         7 |
|     2 |         8 |
|     3 |         9 |
+-------+-----------+
```

Run a query that joins the `emp_manager` table and the `quarterly_sales` table and pivots on the
`amount` column in the `quarterly_sales` table:

Copy code

```
WITH
  src AS
  (
    SELECT *
      FROM quarterly_sales
        PIVOT(SUM(amount) FOR quarter IN (ANY ORDER BY quarter))
  )
SELECT em.managerid, src.*
  FROM emp_manager em
  JOIN src ON em.empid = src.empid
  ORDER BY empid;
```

```
+-----------+-------+-----------+-----------+-----------+-----------+
| MANAGERID | EMPID | '2023_Q1' | '2023_Q2' | '2023_Q3' | '2023_Q4' |
|-----------+-------+-----------+-----------+-----------+-----------|
|         7 |     1 |     10400 |      8000 |     11000 |     18000 |
|         8 |     2 |     39500 |     90700 |     12000 |      5300 |
|         9 |     3 |      NULL |      NULL |      2700 |     28900 |
+-----------+-------+-----------+-----------+-----------+-----------+
```

### Pivot on a specified list of column values for the pivot column

Given the table `quarterly_sales`, pivot on the `amount` column to sum the
total sales per employee for the specified quarters:

Copy code

```
SELECT *
  FROM quarterly_sales
    PIVOT(SUM(amount) FOR quarter IN (
      '2023_Q1',
      '2023_Q2',
      '2023_Q3'))
  ORDER BY empid;
```

```
+-------+-----------+-----------+-----------+
| EMPID | '2023_Q1' | '2023_Q2' | '2023_Q3' |
|-------+-----------+-----------+-----------|
|     1 |     10400 |      8000 |     11000 |
|     2 |     39500 |     90700 |     12000 |
|     3 |      NULL |      NULL |      2700 |
+-------+-----------+-----------+-----------+
```

You can pivot on all of the quarters in the `amount` column by running the following
query:

Copy code

```
SELECT *
  FROM quarterly_sales
    PIVOT(SUM(amount) FOR quarter IN (
      '2023_Q1',
      '2023_Q2',
      '2023_Q3',
      '2023_Q4'))
  ORDER BY empid;
```

```
+-------+-----------+-----------+-----------+-----------+
| EMPID | '2023_Q1' | '2023_Q2' | '2023_Q3' | '2023_Q4' |
|-------+-----------+-----------+-----------+-----------|
|     1 |     10400 |      8000 |     11000 |     18000 |
|     2 |     39500 |     90700 |     12000 |      5300 |
|     3 |      NULL |      NULL |      2700 |     28900 |
+-------+-----------+-----------+-----------+-----------+
```

You can modify the column names in the output with the AS clause. For example, to shorten the column names and
show them without quotes, run the following query:

Copy code

```
SELECT *
  FROM quarterly_sales
    PIVOT(SUM(amount) FOR quarter IN (
      '2023_Q1' AS q1,
      '2023_Q2' AS q2,
      '2023_Q3' AS q3,
      '2023_Q4' AS q4))
  ORDER BY empid;
```

```
+-------+-------+-------+-------+-------+
| EMPID |    Q1 |    Q2 |    Q3 |    Q4 |
|-------+-------+-------+-------+-------|
|     1 | 10400 |  8000 | 11000 | 18000 |
|     2 | 39500 | 90700 | 12000 |  5300 |
|     3 |  NULL |  NULL |  2700 | 28900 |
+-------+-------+-------+-------+-------+
```

### Pivot with a default value for NULL values

If the query returns NULL values, you can replace them with a default value by using DEFAULT ON NULL.
For example, you can use dynamic pivot and replace the NULL values with a default value of `0` by
running the following query:

Copy code

```
SELECT *
  FROM quarterly_sales
    PIVOT(SUM(amount) FOR quarter IN (ANY ORDER BY quarter)
      DEFAULT ON NULL (0))
  ORDER BY empid;
```

```
+-------+-----------+-----------+-----------+-----------+
| EMPID | '2023_Q1' | '2023_Q2' | '2023_Q3' | '2023_Q4' |
|-------+-----------+-----------+-----------+-----------|
|     1 |     10400 |      8000 |     11000 |     18000 |
|     2 |     39500 |     90700 |     12000 |      5300 |
|     3 |         0 |         0 |      2700 |     28900 |
+-------+-----------+-----------+-----------+-----------+
```

You can also use DEFAULT ON NULL with a specified list of columns:

Copy code

```
SELECT *
  FROM quarterly_sales
    PIVOT(SUM(amount)
      FOR quarter IN (
        '2023_Q1',
        '2023_Q2')
      DEFAULT ON NULL (0))
  ORDER BY empid;
```

```
+-------+-----------+-----------+
| EMPID | '2023_Q1' | '2023_Q2' |
|-------+-----------+-----------|
|     1 |     10400 |      8000 |
|     2 |     39500 |     90700 |
|     3 |         0 |         0 |
+-------+-----------+-----------+
```

### Pivot examples that involve multiple columns

Pivot queries can work with multiple columns. Before running these examples, add a column to the `quarterly_sales`
table and populate the column with random values.

First, add a column that tracks the discount applied to each sale to the `quarterly_sales` table:

Copy code

```
ALTER TABLE quarterly_sales ADD COLUMN discount_percent INT DEFAULT 0;
```

Populate the new column with random values between `0` and `5`, which specify the discount
percentage for each sale:

Copy code

```
UPDATE quarterly_sales SET discount_percent = UNIFORM(0, 5, RANDOM());
```

Query the table to show the new column with the random values added:

Copy code

```
SELECT * FROM quarterly_sales;
```

```
+-------+--------+---------+------------------+
| EMPID | AMOUNT | QUARTER | DISCOUNT_PERCENT |
|-------+--------+---------+------------------|
|     1 |  10000 | 2023_Q1 |                0 |
|     1 |    400 | 2023_Q1 |                1 |
|     2 |   4500 | 2023_Q1 |                4 |
|     2 |  35000 | 2023_Q1 |                2 |
|     1 |   5000 | 2023_Q2 |                2 |
|     1 |   3000 | 2023_Q2 |                1 |
|     2 |    200 | 2023_Q2 |                2 |
|     2 |  90500 | 2023_Q2 |                1 |
|     1 |   6000 | 2023_Q3 |                1 |
|     1 |   5000 | 2023_Q3 |                3 |
|     2 |   2500 | 2023_Q3 |                1 |
|     2 |   9500 | 2023_Q3 |                3 |
|     3 |   2700 | 2023_Q3 |                1 |
|     1 |   8000 | 2023_Q4 |                1 |
|     1 |  10000 | 2023_Q4 |                4 |
|     2 |    800 | 2023_Q4 |                3 |
|     2 |   4500 | 2023_Q4 |                5 |
|     3 |   2700 | 2023_Q4 |                3 |
|     3 |  16000 | 2023_Q4 |                0 |
|     3 |  10200 | 2023_Q4 |                1 |
+-------+--------+---------+------------------+
```

Now that the new column is added and populated, run the following examples:

- [Exclude columns from a pivot query with a CTE](#label-pivot-example-multiple-columns-exclude)
- [Run a multidimensional pivot query](#label-pivot-example-multiple-columns-multidimensional)

#### Exclude columns from a pivot query with a CTE

You can use a [common table expression (CTE)](/user-guide/queries-cte) to exclude columns
from a pivot query.

The following example uses a CTE to exclude the `discount_percent` column from a pivot query:

Copy code

```
WITH
  sales_without_discount AS
    (SELECT * EXCLUDE(discount_percent) FROM quarterly_sales)
SELECT *
  FROM sales_without_discount
    PIVOT(SUM(amount) FOR quarter IN (ANY ORDER BY quarter))
  ORDER BY empid;
```

```
+-------+-----------+-----------+-----------+-----------+
| EMPID | '2023_Q1' | '2023_Q2' | '2023_Q3' | '2023_Q4' |
|-------+-----------+-----------+-----------+-----------|
|     1 |     10400 |      8000 |     11000 |     18000 |
|     2 |     39500 |     90700 |     12000 |      5300 |
|     3 |      NULL |      NULL |      2700 |     28900 |
+-------+-----------+-----------+-----------+-----------+
```

You can use a CTE to exclude the `amount` column and show the average discount that
each employee gave in each quarter:

Copy code

```
WITH
  sales_without_amount AS
    (SELECT * EXCLUDE(amount) FROM quarterly_sales)
SELECT *
  FROM sales_without_amount
    PIVOT(AVG(discount_percent) FOR quarter IN (ANY ORDER BY quarter))
  ORDER BY empid;
```

```
+-------+-----------+-----------+-----------+-----------+
| EMPID | '2023_Q1' | '2023_Q2' | '2023_Q3' | '2023_Q4' |
|-------+-----------+-----------+-----------+-----------|
|     1 |  0.500000 |  1.500000 |  2.000000 |  2.500000 |
|     2 |  3.000000 |  1.500000 |  2.000000 |  4.000000 |
|     3 |      NULL |      NULL |  1.000000 |  1.333333 |
+-------+-----------+-----------+-----------+-----------+
```

#### Run a multidimensional pivot query

A multidimensional pivot query pivots on more than one column. This example pivots on the `amount`
column and the `discount_percentage` column. The query returns the sum of all sales by all employees
each quarter and the maximum discount percentage for all sales each quarter.

In the query, the SELECT list uses `$col_position` parameters to run [SUM](/sql-reference/functions/sum)
and [MAX](/sql-reference/functions/max) functions on the returned columns in order, and to name the returned
columns. A subquery in the FROM clause supplies the data for the pivot operations. Because the output shows sales
results for all employees, the subquery doesn’t include the `empid` column.

Copy code

```
SELECT SUM($1) AS q1_sales_total,
       SUM($2) AS q2_sales_total,
       SUM($3) AS q3_sales_total,
       SUM($4) AS q4_sales_total,
       MAX($5) AS q1_maximum_discount,
       MAX($6) AS q2_maximum_discount,
       MAX($7) AS q3_maximum_discount,
       MAX($8) AS q4_maximum_discount
  FROM
    (SELECT amount,
            quarter AS quarter_amount,
            quarter AS quarter_discount,
            discount_percent
      FROM quarterly_sales)
  PIVOT (
    SUM(amount)
    FOR quarter_amount IN (
      '2023_Q1',
      '2023_Q2',
      '2023_Q3',
      '2023_Q4'))
  PIVOT (
    MAX(discount_percent)
    FOR quarter_discount IN (
      '2023_Q1',
      '2023_Q2',
      '2023_Q3',
      '2023_Q4'));
```

```
+----------------+----------------+----------------+----------------+---------------------+---------------------+---------------------+---------------------+
| Q1_SALES_TOTAL | Q2_SALES_TOTAL | Q3_SALES_TOTAL | Q4_SALES_TOTAL | Q1_MAXIMUM_DISCOUNT | Q2_MAXIMUM_DISCOUNT | Q3_MAXIMUM_DISCOUNT | Q4_MAXIMUM_DISCOUNT |
|----------------+----------------+----------------+----------------+---------------------+---------------------+---------------------+---------------------|
|          49900 |          98700 |          25700 |          52200 |                   4 |                   2 |                   3 |                   5 |
+----------------+----------------+----------------+----------------+---------------------+---------------------+---------------------+---------------------+
```
