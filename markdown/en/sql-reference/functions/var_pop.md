Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General) , [Window function syntax and usage](/sql-reference/functions-window-syntax) (General)

# VAR\_POP

Returns the population variance of non-NULL records in a group. If all records inside a group are NULL, a NULL is returned.

Aliases:
:   [VARIANCE\_POP](/sql-reference/functions/variance_pop)

## Syntax

**Aggregate function**

Copy code

```
VAR_POP( [ DISTINCT ] <expr1> )
```

**Window function**

Copy code

```
VAR_POP( [ DISTINCT ] <expr1> ) OVER (
                                     [ PARTITION BY <expr2> ]
                                     [ ORDER BY <expr3> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <window_frame> ] ]
                                     )
```

For detailed `window_frame` syntax, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Arguments

`expr1`
:   The `expr1` should evaluate to one of the numeric data types.

`expr2`
:   This is the optional expression to partition by.

`expr3`
:   This is the optional expression to order by within each partition.

## Returns

The data type of the returned value is `NUMBER(<precision>, <scale>)`. The scale depends upon the values being processed.

## Usage notes

- When passed a VARCHAR expression, this function implicitly casts the input to floating point values. If the cast
  cannot be performed, an error is returned.
- When this function is called as a window function with an OVER clause that contains an ORDER BY clause:
  - A window frame is required. If no window frame is specified explicitly, the following implied window frame is used:

    `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

    For more information about window frames, including syntax, usage notes, and examples, see [Window function syntax and usage](/sql-reference/functions-window-syntax).
  - The DISTINCT keyword cannot be used.

## Examples

This example shows how to use the VAR\_POP function:

Create and fill a table:

Copy code

```
CREATE TABLE aggr (k INT, v DECIMAL(10,2), v2 DECIMAL(10, 2));

INSERT INTO aggr VALUES
  (1, 10, NULL),
  (2, 10, 11),
  (2, 20, 22),
  (2, 25, NULL),
  (2, 30, 35);
```

Query the table:

Copy code

```
SELECT k, VAR_POP(v), VAR_POP(v2)
  FROM aggr
  GROUP BY k
  ORDER BY k;
```

```
+---+---------------+---------------+
| K |    VAR_POP(V) |   VAR_POP(V2) |
|---+---------------+---------------|
| 1 |  0.0000000000 |          NULL |
| 2 | 54.6875000000 | 96.2222222222 |
+---+---------------+---------------+
```
