Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Semi-structured Data) , [Window functions](/sql-reference/functions-window) (General) , [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_AGG

Returns the input values, pivoted into an array. If the input is empty, the function returns an empty array.

Aliases:
:   ARRAYAGG

## Syntax

**Aggregate function**

Copy code

```
ARRAY_AGG( [ DISTINCT ] <expr1> ) [ WITHIN GROUP ( <orderby_clause> ) ]
```

**Window function**

Copy code

```
ARRAY_AGG( [ DISTINCT ] <expr1> )
  [ WITHIN GROUP ( <orderby_clause> ) ]
  OVER ( [ PARTITION BY <expr2> ] [ ORDER BY <expr3> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] ] [ <window_frame> ] )
```

## Arguments

**Required:**

`expr1`
:   An expression (typically a column name) that determines the values to be put into the array.

`OVER()`
:   The OVER clause specifies that the function is being used as a window function.
    For details, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

**Optional:**

`DISTINCT`
:   Removes duplicate values from the array.

`WITHIN GROUP orderby_clause`
:   Clause that contains one or more expressions (typically column names) that determine the order of the values in each array.

    The WITHIN GROUP(ORDER BY) syntax supports the same parameters as the main ORDER BY clause in a SELECT statement.
    See [ORDER BY](/sql-reference/constructs/order-by).

`PARTITION BY expr2`
:   Window function clause that specifies an expression (typically a column name).
    This expression defines partitions that group the input rows before the function is applied.
    For details, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

`ORDER BY expr3` [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ *{window\_frame}* ]
:   Optional expression to order by within each partition, followed by an optional window frame. For detailed
    `window_frame` syntax, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

    When this function is used with a range-based frame, the ORDER BY clause supports only a single column.
    Row-based frames do not have this restriction.

LIMIT is not supported.

## Returns

Returns a value of type ARRAY.

The maximum amount of data that ARRAY\_AGG can return for a single call is 128 MB.

## Usage notes

- If you do not specify WITHIN GROUP(ORDER BY), the order of
  elements within each array is unpredictable. (An ORDER BY clause outside
  the WITHIN GROUP clause applies to the order of the output rows, not to
  the order of the array elements within a row.)
- If you specify a number for an expression in WITHIN GROUP(ORDER BY), this number is parsed as a numeric
  constant, not as the ordinal position of a column in the SELECT list. Therefore, do not specify
  numbers as WITHIN GROUP(ORDER BY) expressions.
- If you specify DISTINCT and WITHIN GROUP, both must refer to the same column. For example:

  Copy code

  ```
  SELECT ARRAY_AGG(DISTINCT O_ORDERKEY) WITHIN GROUP (ORDER BY O_ORDERKEY) ...;
  ```

  If you specify different columns for DISTINCT and WITHIN GROUP, an error occurs:

  Copy code

  ```
  SELECT ARRAY_AGG(DISTINCT O_ORDERKEY) WITHIN GROUP (ORDER BY O_ORDERSTATUS) ...;
  ```

  ```
  SQL compilation error: [ORDERS.O_ORDERSTATUS] is not a valid order by expression
  ```

  You must either specify the same column for DISTINCT and WITHIN GROUP or omit DISTINCT.
- DISTINCT and WITHIN GROUP are supported for window function calls only when there is no ORDER BY clause
  within the OVER clause. When an ORDER BY clause is used in the OVER clause, values in the output array
  follow the same default order (that is, the order equivalent to `WITHIN GROUP (ORDER BY expr3)`).
- NULL values are omitted from the output.

## Examples

The example queries below use the tables and data shown below:

Copy code

```
CREATE TABLE orders (
  o_orderkey INTEGER,
  o_clerk VARCHAR,
  o_totalprice NUMBER(12, 2),
  o_orderstatus CHAR(1)
);

INSERT INTO orders (o_orderkey, o_orderstatus, o_clerk, o_totalprice)
  VALUES
    ( 32123, 'O', 'Clerk#000000321',     321.23),
    ( 41445, 'F', 'Clerk#000000386', 1041445.00),
    ( 55937, 'O', 'Clerk#000000114', 1055937.00),
    ( 67781, 'F', 'Clerk#000000521', 1067781.00),
    ( 80550, 'O', 'Clerk#000000411', 1080550.00),
    ( 95808, 'F', 'Clerk#000000136', 1095808.00),
    (101700, 'O', 'Clerk#000000220', 1101700.00),
    (103136, 'F', 'Clerk#000000508', 1103136.00);
```

This example shows non-pivoted output from a query that does not use ARRAY\_AGG().
The contrast in output between this example and the following example
shows that ARRAY\_AGG() pivots the data.

Copy code

```
SELECT o_orderkey AS order_keys
  FROM orders
  WHERE o_totalprice > 450000
  ORDER BY o_orderkey;
```

```
+------------+
| ORDER_KEYS |
|------------|
|      41445 |
|      55937 |
|      67781 |
|      80550 |
|      95808 |
|     101700 |
|     103136 |
+------------+
```

This example shows how to use ARRAY\_AGG() to pivot a column of output
into an array in a single row:

Copy code

```
SELECT ARRAY_AGG(o_orderkey) WITHIN GROUP (ORDER BY o_orderkey ASC)
  FROM orders
  WHERE o_totalprice > 450000;
```

```
+--------------------------------------------------------------+
| ARRAY_AGG(O_ORDERKEY) WITHIN GROUP (ORDER BY O_ORDERKEY ASC) |
|--------------------------------------------------------------|
| [                                                            |
|   41445,                                                     |
|   55937,                                                     |
|   67781,                                                     |
|   80550,                                                     |
|   95808,                                                     |
|   101700,                                                    |
|   103136                                                     |
| ]                                                            |
+--------------------------------------------------------------+
```

This example shows the use of the DISTINCT keyword with ARRAY\_AGG().

Copy code

```
SELECT ARRAY_AGG(DISTINCT o_orderstatus) WITHIN GROUP (ORDER BY o_orderstatus ASC)
  FROM orders
  WHERE o_totalprice > 450000
  ORDER BY o_orderstatus ASC;
```

```
+-----------------------------------------------------------------------------+
| ARRAY_AGG(DISTINCT O_ORDERSTATUS) WITHIN GROUP (ORDER BY O_ORDERSTATUS ASC) |
|-----------------------------------------------------------------------------|
| [                                                                           |
|   "F",                                                                      |
|   "O"                                                                       |
| ]                                                                           |
+-----------------------------------------------------------------------------+
```

This example uses two separate ORDER BY clauses. One controls
the order within the output array inside each row, and the other controls
the order of the output rows:

Copy code

```
SELECT
    o_orderstatus,
    ARRAYAGG(o_clerk) WITHIN GROUP (ORDER BY o_totalprice DESC)
  FROM orders
  WHERE o_totalprice > 450000
  GROUP BY o_orderstatus
  ORDER BY o_orderstatus DESC;
```

```
+---------------+-------------------------------------------------------------+
| O_ORDERSTATUS | ARRAYAGG(O_CLERK) WITHIN GROUP (ORDER BY O_TOTALPRICE DESC) |
|---------------+-------------------------------------------------------------|
| O             | [                                                           |
|               |   "Clerk#000000220",                                        |
|               |   "Clerk#000000411",                                        |
|               |   "Clerk#000000114"                                         |
|               | ]                                                           |
| F             | [                                                           |
|               |   "Clerk#000000508",                                        |
|               |   "Clerk#000000136",                                        |
|               |   "Clerk#000000521",                                        |
|               |   "Clerk#000000386"                                         |
|               | ]                                                           |
+---------------+-------------------------------------------------------------+
```

The following example uses a different data set. The ARRAY\_AGG function is called as a window
function with a ROWS BETWEEN window frame. First, create the table and load it with 14 rows:

Copy code

```
CREATE OR REPLACE TABLE array_data AS (
WITH data AS (
  SELECT 1 a, [1,3,2,4,7,8,10] b
  UNION ALL
  SELECT 2, [1,3,2,4,7,8,10]
  )
SELECT 'Ord'||a o_orderkey, 'c'||value o_clerk, index
  FROM data, TABLE(FLATTEN(b))
);
```

Now run the following query. Note that only a partial result set is shown here.

Copy code

```
SELECT o_orderkey,
    ARRAY_AGG(o_clerk) OVER(PARTITION BY o_orderkey ORDER BY o_orderkey
      ROWS BETWEEN 3 PRECEDING AND CURRENT ROW) AS result
  FROM array_data;
```

```
+------------+---------+
| O_ORDERKEY | RESULT  |
|------------+---------|
| Ord1       | [       |
|            |   "c1"  |
|            | ]       |
| Ord1       | [       |
|            |   "c1", |
|            |   "c3"  |
|            | ]       |
| Ord1       | [       |
|            |   "c1", |
|            |   "c3", |
|            |   "c2"  |
|            | ]       |
| Ord1       | [       |
|            |   "c1", |
|            |   "c3", |
|            |   "c2", |
|            |   "c4"  |
|            | ]       |
| Ord1       | [       |
|            |   "c3", |
|            |   "c2", |
|            |   "c4", |
|            |   "c7"  |
|            | ]       |
| Ord1       | [       |
|            |   "c2", |
|            |   "c4", |
|            |   "c7", |
|            |   "c8"  |
|            | ]       |
| Ord1       | [       |
|            |   "c4", |
|            |   "c7", |
|            |   "c8", |
|            |   "c10" |
|            | ]       |
| Ord2       | [       |
|            |   "c1"  |
|            | ]       |
| Ord2       | [       |
|            |   "c1", |
|            |   "c3"  |
|            | ]       |
...
```
