Categories:
:   [Query syntax](/sql-reference/constructs)

# UNPIVOT

Rotates a table by transforming columns into rows. UNPIVOT is a relational operator that accepts
two columns (from a table or subquery), along with a list of columns, and generates a row for
each column specified in the list. In a query, it is specified in the [FROM](/sql-reference/constructs/from) clause after
the table name or subquery.

UNPIVOT is not exactly the reverse of PIVOT because it can’t undo aggregations made by PIVOT.

This operator can be used to transform a wide table (e.g. `empid`, `jan_sales`,
`feb_sales`, `mar_sales`) into a narrower table (e.g. `empid`, `month`,
`sales`).

See also:
:   [PIVOT](/sql-reference/constructs/pivot)

## Syntax

Copy code

```
SELECT ...
FROM ...
    UNPIVOT [ { INCLUDE | EXCLUDE } NULLS ]
      ( <value_column>
        FOR <name_column> IN (
          <col> [ [ AS ] <col_alias> ],
          ...
        )
      )

[ ... ]
```

## Parameters

`{ INCLUDE | EXCLUDE } NULLS`
:   Specifies whether to include or exclude rows with NULLs in the `name_column`:

    - `INCLUDE NULLS` includes rows with NULLs.
    - `EXCLUDE NULLS` excludes rows with NULLs.

    Default: `EXCLUDE NULLS`

`value_column`
:   The name to assign to the generated column that will be populated with the values from the columns in the column list.

`name_column`
:   The name to assign to the generated column that will be populated with the names of the columns in the column list.

`column_list`
:   The names of the columns in the source table or subquery that will be rotated into a single pivot column.
    The column names will populate `name_column`, and the column values will populate `value_column`.

    The `column_list` can only contain literal column names, not a subquery.

    The columns in `column_list` must have exactly the same data type, with the following exceptions:

    - The [data types for text strings](/sql-reference/data-types-text#label-character-datatypes) can be different lengths.
    - If the columns contain text strings, different columns can use different data types for text. For example,
      the list can include a VARCHAR column and a CHAR column.

`[ AS ] col_alias`
:   Specifies the column alias to use in the result of the UNPIVOT operation instead of the original column names.
    You can’t use different aliases for the same column name. However, you can’t use the same alias for multiple
    column names. The AS keyword is optional.

## Usage notes

- You can’t use a [LATERAL join](/sql-reference/constructs/join-lateral) to directly reference the
  result set of an UNPIVOT operation. Attempting to do so returns an error. As a workaround, materialize the UNPIVOT
  result into a temporary table first, then reference that table in the LATERAL join. To create and load the
  `monthly_sales` table that is selected from in this example, see the [examples section](#label-unpivot-examples).

  The following query doesn’t work because LATERAL can’t reference an UNPIVOT result set directly:

  Copy code

  ```
  SELECT *
    FROM monthly_sales
   UNPIVOT (sales FOR month IN (jan, feb, mar, apr)) unpvt
   JOIN LATERAL (SELECT unpvt.sales AS sales_value) jl;
  ```

  The following CREATE TEMPORARY TABLE statement creates a temporary table to materialize the UNPIVOT result.
  The query that follows that statement references the temporary table in the LATERAL join:

  Copy code

  ```
  CREATE OR REPLACE TEMPORARY TABLE unpivot_result AS
    SELECT *
   FROM monthly_sales
     UNPIVOT (sales FOR month IN (jan, feb, mar, apr));

  SELECT *
    FROM unpivot_result
   JOIN LATERAL (SELECT unpivot_result.sales AS sales_value) jl;
  ```

## Examples

Create a table, `monthly_sales`, with the following structure and data:

Copy code

```
CREATE OR REPLACE TABLE monthly_sales(
  empid INT,
  dept TEXT,
  jan INT,
  feb INT,
  mar INT,
  apr INT);

INSERT INTO monthly_sales VALUES
  (1, 'electronics', 100, 200, 300, 100),
  (2, 'clothes', 100, 300, 150, 200),
  (3, 'cars', 200, 400, 100, 50),
  (4, 'appliances', 100, NULL, 100, 50);

SELECT * FROM monthly_sales;
```

```
+-------+-------------+-----+------+------+-----+
| EMPID | DEPT        | JAN | FEB  | MAR  | APR |
|-------+-------------+-----+------+------+-----|
|     1 | electronics | 100 | 200  | 300  | 100 |
|     2 | clothes     | 100 | 300  | 150  | 200 |
|     3 | cars        | 200 | 400  | 100  |  50 |
|     4 | appliances  | 100 | NULL | 100  |  50 |
+-------+-------------+-----+------+------+-----+
```

Unpivot the individual month columns to return a single `sales` value by `month` for each employee.

Copy code

```
SELECT *
  FROM monthly_sales
    UNPIVOT (sales FOR month IN (jan, feb, mar, apr))
  ORDER BY empid;
```

```
+-------+-------------+-------+-------+
| EMPID | DEPT        | MONTH | SALES |
|-------+-------------+-------+-------|
|     1 | electronics | JAN   |   100 |
|     1 | electronics | FEB   |   200 |
|     1 | electronics | MAR   |   300 |
|     1 | electronics | APR   |   100 |
|     2 | clothes     | JAN   |   100 |
|     2 | clothes     | FEB   |   300 |
|     2 | clothes     | MAR   |   150 |
|     2 | clothes     | APR   |   200 |
|     3 | cars        | JAN   |   200 |
|     3 | cars        | FEB   |   400 |
|     3 | cars        | MAR   |   100 |
|     3 | cars        | APR   |    50 |
|     4 | appliances  | JAN   |   100 |
|     4 | appliances  | MAR   |   100 |
|     4 | appliances  | APR   |    50 |
+-------+-------------+-------+-------+
```

The following example is the same as the previous example, but it uses aliases for the column names:

Copy code

```
SELECT *
  FROM monthly_sales
    UNPIVOT (sales FOR month IN (
      jan AS january,
      feb AS february,
      mar AS march,
      apr AS april)
    )
  ORDER BY empid;
```

```
+-------+-------------+----------+-------+
| EMPID | DEPT        | MONTH    | SALES |
|-------+-------------+----------+-------|
|     1 | electronics | JANUARY  |   100 |
|     1 | electronics | FEBRUARY |   200 |
|     1 | electronics | MARCH    |   300 |
|     1 | electronics | APRIL    |   100 |
|     2 | clothes     | JANUARY  |   100 |
|     2 | clothes     | FEBRUARY |   300 |
|     2 | clothes     | MARCH    |   150 |
|     2 | clothes     | APRIL    |   200 |
|     3 | cars        | JANUARY  |   200 |
|     3 | cars        | FEBRUARY |   400 |
|     3 | cars        | MARCH    |   100 |
|     3 | cars        | APRIL    |    50 |
|     4 | appliances  | JANUARY  |   100 |
|     4 | appliances  | MARCH    |   100 |
|     4 | appliances  | APRIL    |    50 |
+-------+-------------+----------+-------+
```

The previous SELECT statements exclude NULLs by default. So, they don’t include a row for appliances in February
in the results. To include NULLs in the results, run the following SQL statement:

Copy code

```
SELECT *
  FROM monthly_sales
    UNPIVOT INCLUDE NULLS (sales FOR month IN (jan, feb, mar, apr))
  ORDER BY empid;
```

```
+-------+-------------+-------+-------+
| EMPID | DEPT        | MONTH | SALES |
|-------+-------------+-------+-------|
|     1 | electronics | JAN   |   100 |
|     1 | electronics | FEB   |   200 |
|     1 | electronics | MAR   |   300 |
|     1 | electronics | APR   |   100 |
|     2 | clothes     | JAN   |   100 |
|     2 | clothes     | FEB   |   300 |
|     2 | clothes     | MAR   |   150 |
|     2 | clothes     | APR   |   200 |
|     3 | cars        | JAN   |   200 |
|     3 | cars        | FEB   |   400 |
|     3 | cars        | MAR   |   100 |
|     3 | cars        | APR   |    50 |
|     4 | appliances  | JAN   |   100 |
|     4 | appliances  | FEB   |  NULL |
|     4 | appliances  | MAR   |   100 |
|     4 | appliances  | APR   |    50 |
+-------+-------------+-------+-------+
```

This output includes a row for appliances in February.

Instead of selecting all columns with `*`, you can include specific columns in the SELECT list and reference
the UNPIVOT `value_column` and `name_column`. The following example is similar to the previous
example, but it specifies the `value_column` `sales` and the `name_column` `month` in the
SELECT list. The query excludes the `empid` column:

Copy code

```
SELECT dept, month, sales
  FROM monthly_sales
    UNPIVOT INCLUDE NULLS (sales FOR month IN (jan, feb, mar, apr))
  ORDER BY dept;
```

```
+-------------+-------+-------+
| DEPT        | MONTH | SALES |
|-------------+-------+-------|
| appliances  | JAN   |   100 |
| appliances  | FEB   |  NULL |
| appliances  | MAR   |   100 |
| appliances  | APR   |    50 |
| cars        | JAN   |   200 |
| cars        | FEB   |   400 |
| cars        | MAR   |   100 |
| cars        | APR   |    50 |
| clothes     | JAN   |   100 |
| clothes     | FEB   |   300 |
| clothes     | MAR   |   150 |
| clothes     | APR   |   200 |
| electronics | JAN   |   100 |
| electronics | FEB   |   200 |
| electronics | MAR   |   300 |
| electronics | APR   |   100 |
+-------------+-------+-------+
```
