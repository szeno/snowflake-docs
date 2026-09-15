Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General) , [Window functions](/sql-reference/functions-window)

# COUNT\_IF

Returns the number of records that satisfy a condition or NULL if no records satisfy the condition.

See also:
:   [COUNT](/sql-reference/functions/count)

## Syntax

**Aggregate function**

Copy code

```
COUNT_IF( <condition> )
```

**Window function**

Copy code

```
COUNT_IF( <condition> )
    OVER ( [ PARTITION BY <expr1> ] [ ORDER BY <expr2> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <window_frame> ] ] )
```

For detailed `window_frame` syntax, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Arguments

`condition`
:   The condition is an expression that should evaluate to a BOOLEAN value (True, False, or NULL)

`expr1`
:   The column to partition on, if you want the result to be split into multiple
    windows.

`expr2`
:   The column to order each window on. Note that this is separate from the ORDER BY clause that sorts the final result set.

## Returns

If the function does not return NULL, the data type of the returned value is NUMBER.

## Usage notes

- When this function is called as a window function with an ORDER BY clause, you must specify a window frame. If
  you do not specify a window frame, the following default frame is used:

  `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

  For more information about window frames, including syntax, usage notes, and examples, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Examples

The examples in this section demonstrate how to use the `COUNT_IF` function.

The following statements set up a table for use in the examples:

Copy code

```
CREATE TABLE basic_example (i_col INTEGER, j_col INTEGER);

INSERT INTO basic_example VALUES
  (11, 101), (11, 102), (11, NULL), (12, 101), (NULL, 101), (NULL, 102);
```

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

The following example passes in `TRUE` for the condition, which returns the count of all rows in the table:

Copy code

```
SELECT COUNT_IF(TRUE)
  FROM basic_example;
```

```
+----------------+
| COUNT_IF(TRUE) |
|----------------|
|              6 |
+----------------+
```

The following example returns the number of rows where the value in `J_COL` is greater than the value in `I_COL`:

Copy code

```
SELECT COUNT_IF(j_col > i_col)
  FROM basic_example;
```

```
+-------------------------+
| COUNT_IF(J_COL > I_COL) |
|-------------------------|
|                       3 |
+-------------------------+
```

Note that in the example above, the count does not include rows with NULL values. As explained in
[Ternary logic](/sql-reference/ternary-logic), when any operand for a comparison operator is NULL, the result is NULL, which does not
satisfy the condition specified by `COUNT_IF`.

The following example returns the number of rows that do not contain any NULL values.

Copy code

```
SELECT COUNT_IF(i_col IS NOT NULL AND j_col IS NOT NULL)
  FROM basic_example;
```

```
+---------------------------------------------------+
| COUNT_IF(I_COL IS NOT NULL AND J_COL IS NOT NULL) |
|---------------------------------------------------|
|                                                 3 |
+---------------------------------------------------+
```
