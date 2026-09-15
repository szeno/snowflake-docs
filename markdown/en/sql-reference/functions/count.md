Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General) , [Window functions](/sql-reference/functions-window)

# COUNT

Returns either the number of non-NULL records for the specified columns, or the total number of records.

See also:
:   [COUNT\_IF](/sql-reference/functions/count_if), [MAX](/sql-reference/functions/max), [MIN](/sql-reference/functions/min) , [SUM](/sql-reference/functions/sum)

## Syntax

**Aggregate function**

Copy code

```
COUNT( [ DISTINCT ] <expr1> [ , <expr2> ... ] )

COUNT(*)

COUNT(<alias>.*)
```

**Window function**

Copy code

```
COUNT( [ DISTINCT ] <expr1> [ , <expr2> ... ] ) OVER (
                                                     [ PARTITION BY <expr3> ]
                                                     [ ORDER BY <expr4> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <window_frame> ] ]
                                                     )
```

For detailed `window_frame` syntax, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Arguments

`expr1`
:   A column name, which can be a qualified name (for example, database.schema.table.column\_name).

`expr2`
:   You can include additional column name(s) if you wish. For example, you
    could count the number of distinct combinations of last name and first name.

`expr3`
:   The column to partition on, if you want the result to be split into multiple
    windows.

`expr4`
:   The column to order each window on. Note that this is separate from any
    ORDER BY clause to order the final result set.

`*`
:   Returns the total number of records.

    When you pass a wildcard to the function, you can qualify the wildcard with the name or alias for the table.
    For example, to pass in all of the columns from the table named `mytable`, specify the following:

    Copy code

    ```
    (mytable.*)
    ```

    You can also use the ILIKE and EXCLUDE keywords for filtering:

    - ILIKE filters for column names that match the specified pattern. Only one
      pattern is allowed. For example:

      Copy code

      ```
      (* ILIKE 'col1%')
      ```
    - EXCLUDE filters out column names that don’t match the specified column or columns. For example:

      Copy code

      ```
      (* EXCLUDE col1)

      (* EXCLUDE (col1, col2))
      ```

    Qualifiers are valid when you use these keywords. The following example uses the ILIKE keyword to
    filter for all of the columns that match the pattern `col1%` in the table `mytable`:

    Copy code

    ```
    (mytable.* ILIKE 'col1%')
    ```

    The ILIKE and EXCLUDE keywords can’t be combined in a single function call.

    If you specify an unqualified and unfiltered wildcard (`*`), the function returns the total number of records, including
    records with NULL values.

    If you specify a wildcard with the ILIKE or EXCLUDE keyword for filtering, the function excludes records with NULL values.

    For this function, the ILIKE and EXCLUDE keywords are valid only in a SELECT list or GROUP BY clause.

    For more information about the ILIKE and EXCLUDE keywords, see the “Parameters” section in [SELECT](/sql-reference/sql/select).

`alias.*`
:   Returns the number of records that don’t contain any NULL values. For an example, see [Examples](#examples).

## Returns

Returns a value of type NUMBER.

## Usage notes

- This function treats [JSON null](/user-guide/semistructured-considerations#label-variant-null) (VARIANT NULL) as SQL NULL.
- For more information about NULL values and aggregate functions, see
  [Aggregate functions and NULL values](/sql-reference/functions-aggregation#label-aggregate-functions-and-null-values).
- When this function is called as an aggregate function:

  - If the `DISTINCT` keyword is used, it applies to all columns. For example,
    `DISTINCT col1, col2, col3` means to return the number of different
    combinations of columns `col1`, `col2`, and `col3`. For example, assume the data is:

    Copy code

    ```
    1, 1, 1
    1, 1, 1
    1, 1, 1
    1, 1, 2
    ```

    In this case, the function returns `2`, because that’s the number of distinct combinations of values in the three columns.
- When this function is called as a window function with an OVER clause that contains an ORDER BY clause:

  - A window frame is required. If no window frame is specified explicitly, the following implied window frame is used:

    `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

    For more information about window frames, including syntax, usage notes, and examples, see [Window function syntax and usage](/sql-reference/functions-window-syntax).
- `DISTINCT` can be used with an `OVER` clause that includes **ORDER BY** when the distinct set applies to **a single column**; for example,
  `COUNT(DISTINCT <expr>) OVER ( ... ORDER BY <orderexpr> [ ... ] )`. A distinct count that references **multiple** column expressions, such as
  `COUNT(DISTINCT <expr1>, <expr2>, ... )` in a window, is not valid when the `OVER` clause also contains **ORDER BY**.
- To return the number of rows that match a condition, use [COUNT\_IF](/sql-reference/functions/count_if).
- When possible, use the COUNT function on tables and views without a [row access policy](/user-guide/security-row-intro#label-security-row-intro-considerations).
  The query with this function is faster and more accurate on tables or views without a row access policy. The reasons for the performance
  difference include:

  - Snowflake maintains statistics on tables and views, and this optimization allows simple queries to run faster.
  - When a row access policy is set on a table or view and the COUNT function is used in a query, Snowflake must scan each row and
    determine whether the user is allowed to view the row.

## Examples

The following examples use the COUNT function on data with NULL values.

Create a table and insert values:

Copy code

```
CREATE TABLE basic_example (i_col INTEGER, j_col INTEGER);

INSERT INTO basic_example VALUES
  (11, 101), (11, 102), (11, NULL), (12, 101), (NULL, 101), (NULL, 102);
```

Query the table:

Copy code

```
SELECT *
  FROM basic_example
  ORDER BY i_col;
```

```
+-------+-------+
| I_COL | J_COL |
|-------+-------|
|    11 |   101 |
|    11 |   102 |
|    11 |  NULL |
|    12 |   101 |
|  NULL |   101 |
|  NULL |   102 |
+-------+-------+
```

Copy code

```
SELECT COUNT(*) AS "All",
    COUNT(* ILIKE 'i_c%') AS "ILIKE",
    COUNT(* EXCLUDE i_col) AS "EXCLUDE",
    COUNT(i_col) AS "i_col",
    COUNT(DISTINCT i_col) AS "DISTINCT i_col",
    COUNT(j_col) AS "j_col",
    COUNT(DISTINCT j_col) AS "DISTINCT j_col"
  FROM basic_example;
```

```
+-----+-------+---------+-------+----------------+-------+----------------+
| All | ILIKE | EXCLUDE | i_col | DISTINCT i_col | j_col | DISTINCT j_col |
|-----+-------+---------+-------+----------------+-------+----------------|
|   6 |     4 |       5 |     4 |              2 |     5 |              2 |
+-----+-------+---------+-------+----------------+-------+----------------+
```

The `All` column in this output shows that when an unqualified and unfiltered wildcard is specified
for COUNT, the function returns the total number of rows in the table, including rows with NULL values. The other
columns in the output show that when a column or a wildcard with filtering is specified, the function excludes
rows with NULL values.

The next query uses the COUNT function with the GROUP BY clause:

Copy code

```
SELECT i_col, COUNT(*), COUNT(j_col)
  FROM basic_example
  GROUP BY i_col
  ORDER BY i_col;
```

```
+-------+----------+--------------+
| I_COL | COUNT(*) | COUNT(J_COL) |
|-------+----------+--------------|
|    11 |        3 |            2 |
|    12 |        1 |            1 |
|  NULL |        2 |            2 |
+-------+----------+--------------+
```

The following example shows that `COUNT(alias.*)` returns the number of rows that don’t contain any NULL values.
The `basic_example` table has a total of six rows, but three rows have at least one NULL value, and the other three rows
have no NULL values.

Copy code

```
SELECT COUNT(n.*) FROM basic_example AS n;
```

```
+------------+
| COUNT(N.*) |
|------------|
|          3 |
+------------+
```

The following example shows that [JSON null](/user-guide/semistructured-considerations#label-variant-null) (VARIANT NULL) is treated as SQL NULL by
the COUNT function.

Create the table and insert data that contains both SQL NULL and JSON null values:

Copy code

```
CREATE OR REPLACE TABLE count_example_with_variant_column (
  i_col INTEGER,
  j_col INTEGER,
  v VARIANT);
```

Copy code

```
BEGIN WORK;

INSERT INTO count_example_with_variant_column (i_col, j_col, v)
  VALUES (NULL, 10, NULL);
INSERT INTO count_example_with_variant_column (i_col, j_col, v)
  SELECT 1, 11, PARSE_JSON('{"Title": null}');
INSERT INTO count_example_with_variant_column (i_col, j_col, v)
  SELECT 2, 12, PARSE_JSON('{"Title": "O"}');
INSERT INTO count_example_with_variant_column (i_col, j_col, v)
  SELECT 3, 12, PARSE_JSON('{"Title": "I"}');

COMMIT WORK;
```

In this SQL code, note the following:

- The first INSERT INTO statement inserts a SQL NULL for both a VARIANT column and a non-VARIANT column.
- The second INSERT INTO statement inserts a JSON null (VARIANT NULL).
- The last two INSERT INTO statements insert non-NULL VARIANT values.

Show the data:

Copy code

```
SELECT i_col, j_col, v, v:Title
  FROM count_example_with_variant_column
  ORDER BY i_col;
```

```
+-------+-------+-----------------+---------+
| I_COL | J_COL | V               | V:TITLE |
|-------+-------+-----------------+---------|
|     1 |    11 | {               | null    |
|       |       |   "Title": null |         |
|       |       | }               |         |
|     2 |    12 | {               | "O"     |
|       |       |   "Title": "O"  |         |
|       |       | }               |         |
|     3 |    12 | {               | "I"     |
|       |       |   "Title": "I"  |         |
|       |       | }               |         |
|  NULL |    10 | NULL            | NULL    |
+-------+-------+-----------------+---------+
```

Show that the COUNT function treats both the NULL and the JSON null (VARIANT NULL) values
as NULLs. There are four rows in the table. One has a SQL NULL and the other has a
JSON null. Both those rows are excluded from the count, so the count is `2`.

Copy code

```
SELECT COUNT(v:Title)
  FROM count_example_with_variant_column;
```

```
+----------------+
| COUNT(V:TITLE) |
|----------------|
|              2 |
+----------------+
```

Calculate the number of unique customers over time using COUNT(DISTINCT …) with the OVER clause:

Copy code

```
CREATE OR REPLACE TABLE customer_product_sales_fct (
    sale_date DATE,
    sale_id INTEGER,
    customer_id STRING,
    product_id STRING,
    quantity INTEGER,
    sales_amount NUMBER(10,2)
);

INSERT INTO customer_product_sales_fct VALUES
    ('2026-01-01', 1, 'C001', 'P100', 1, 19.99),
    ('2026-01-02', 2, 'C002', 'P100', 2, 39.98),
    ('2026-01-03', 3, 'C001', 'P100', 1, 19.99),
    ('2026-01-04', 4, 'C003', 'P100', 1, 19.99),
    ('2026-01-05', 5, 'C002', 'P200', 1, 9.99),
    ('2026-01-06', 6, 'C004', 'P100', 3, 59.97),
    ('2026-01-07', 7, 'C003', 'P100', 1, 19.99),
    ('2026-01-08', 8, 'C005', 'P100', 2, 39.98),
    ('2026-01-09', 9, 'C001', 'P200', 1, 9.99),
    ('2026-01-10', 10, 'C006', 'P100', 1, 19.99);

SELECT
    product_id,
    customer_id,
    sale_date,
    sale_id,
    COUNT(DISTINCT customer_id) OVER (
        PARTITION BY product_id
        ORDER BY sale_date
    ) AS distinct_customers_to_date
FROM customer_product_sales_fct
WHERE product_id = 'P100'
ORDER BY sale_date, sale_id;
```

```
+------------+-------------+------------+---------+----------------------------+
| PRODUCT_ID | CUSTOMER_ID | SALE_DATE  | SALE_ID | DISTINCT_CUSTOMERS_TO_DATE |
+------------+-------------+------------+---------+----------------------------+
| P100       | C001        | 2026-01-01 | 1       | 1                          |
| P100       | C002        | 2026-01-02 | 2       | 2                          |
| P100       | C001        | 2026-01-03 | 3       | 2                          |
| P100       | C003        | 2026-01-04 | 4       | 3                          |
| P100       | C004        | 2026-01-06 | 6       | 4                          |
| P100       | C003        | 2026-01-07 | 7       | 4                          |
| P100       | C005        | 2026-01-08 | 8       | 5                          |
| P100       | C006        | 2026-01-10 | 10      | 6                          |
+------------+-------------+------------+---------+----------------------------+
```
