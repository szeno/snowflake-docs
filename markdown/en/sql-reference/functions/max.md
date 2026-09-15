Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General) , [Window functions](/sql-reference/functions-window)

# MAX

Returns the maximum value for the records within `expr`. NULL values are ignored unless all the records are NULL, in which case a NULL value is returned.

See also:
:   [COUNT](/sql-reference/functions/count) , [SUM](/sql-reference/functions/sum) , [MIN](/sql-reference/functions/min)

## Syntax

**Aggregate function**

Copy code

```
MAX( <expr> )
```

**Window function**

Copy code

```
MAX( <expr> ) [ OVER ( [ PARTITION BY <expr1> ] [ ORDER BY <expr2> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <window_frame> ] ] ) ]
```

For detailed `window_frame` syntax, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

# Returns

The data type of the returned value is the same as the data type of the input values.

## Usage Notes

- For compatibility with other systems, you can specify the DISTINCT keyword as an argument for the function,
  but it does not have any effect.
- If the function is called as a window function, the window can include an optional `window_frame`.
  The `window_frame` (either cumulative or sliding) specifies the subset of rows within the window for which
  the summed values are returned. If no `window_frame` is specified, the default is the following
  cumulative window frame (in accordance with the ANSI standard for window functions):

  > `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

  For more details about window frames, including syntax and examples, see [Usage notes for window frames](/sql-reference/functions-window-syntax#label-window-frames).

## Collation Details

- The comparisons follow the collation based on the input arguments’ collations and precedences.
- The collation of the result is the same as the collation of the input.

## Examples

The following examples demonstrate how to use the MAX function.

Create a table and data:

Copy code

```
CREATE OR REPLACE TABLE sample_table (k CHAR(4), d CHAR(4));

INSERT INTO sample_table VALUES
  ('1', '1'), ('1', '5'), ('1', '3'),
  ('2', '2'), ('2', NULL),
  ('3', NULL),
  (NULL, '7'), (NULL, '1');
```

Display the data:

Copy code

```
SELECT k, d
  FROM sample_table
  ORDER BY k, d;
```

```
+------+------+
| K    | D    |
|------+------|
| 1    | 1    |
| 1    | 3    |
| 1    | 5    |
| 2    | 2    |
| 2    | NULL |
| 3    | NULL |
| NULL | 1    |
| NULL | 7    |
+------+------+
```

Use the MAX function to retrieve the largest
value in the column named `d`:

Copy code

```
SELECT MAX(d)
  FROM sample_table;
```

```
+--------+
| MAX(D) |
|--------|
| 7      |
+--------+
```

Combine the GROUP BY clause with the MAX function
to retrieve the largest values in each group (where each
group is based on the value of column `k`):

Copy code

```
SELECT k, MAX(d)
  FROM sample_table
  GROUP BY k
  ORDER BY k;
```

```
+------+--------+
| K    | MAX(D) |
|------+--------|
| 1    | 5      |
| 2    | 2      |
| 3    | NULL   |
| NULL | 7      |
+------+--------+
```

Use a PARTITION BY clause to break the data into groups based on the
value of `k`. This is similar to, but not identical to, using
GROUP BY. In particular, GROUP BY produces one output
row per group, while PARTITION BY produces one output row per input
row.

Copy code

```
SELECT k, d, MAX(d) OVER (PARTITION BY k)
  FROM sample_table
  ORDER BY k, d;
```

```
+------+------+------------------------------+
| K    | D    | MAX(D) OVER (PARTITION BY K) |
|------+------+------------------------------|
| 1    | 1    | 5                            |
| 1    | 3    | 5                            |
| 1    | 5    | 5                            |
| 2    | 2    | 2                            |
| 2    | NULL | 2                            |
| 3    | NULL | NULL                         |
| NULL | 1    | 7                            |
| NULL | 7    | 7                            |
+------+------+------------------------------+
```

Use a windowing ORDER BY clause to create a sliding window two rows wide,
and output the highest value within that window. (Remember that ORDER BY in
the windowing clause is separate from ORDER BY at the statement level.)
This example uses a single partition, so there is no PARTITION BY clause
in the OVER() clause.

Copy code

```
SELECT k, d, MAX(d) OVER (ORDER BY k, d ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)
  FROM sample_table
  ORDER BY k, d;
```

```
+------+------+----------------------------------------------------------------------+
| K    | D    | MAX(D) OVER (ORDER BY K, D ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) |
|------+------+----------------------------------------------------------------------|
| 1    | 1    | 1                                                                    |
| 1    | 3    | 3                                                                    |
| 1    | 5    | 5                                                                    |
| 2    | 2    | 5                                                                    |
| 2    | NULL | 2                                                                    |
| 3    | NULL | NULL                                                                 |
| NULL | 1    | 1                                                                    |
| NULL | 7    | 7                                                                    |
+------+------+----------------------------------------------------------------------+
```
