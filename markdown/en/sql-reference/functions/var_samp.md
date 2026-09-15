Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General) , [Window function syntax and usage](/sql-reference/functions-window-syntax) (General)

# VAR\_SAMP

Returns the sample variance of non-NULL records in a group. If all records inside a group are NULL, a NULL is returned.

Aliases:
:   [VARIANCE , VARIANCE\_SAMP](/sql-reference/functions/variance)

## Syntax

**Aggregate function**

Copy code

```
VAR_SAMP( [DISTINCT] <expr1> )
```

**Window function**

Copy code

```
VAR_SAMP( <expr1> ) OVER (
                         [ PARTITION BY <expr2> ]
                         [ ORDER BY <expr3> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ <window_frame> ] ]
                         )
```

For detailed `window_frame` syntax, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Arguments

`expr1`
:   The `expr1` should evaluate to one of the numeric data types.

`expr2`
:   This is the expression to partition by.

`expr3`
:   This is the expression to order by within each partition.

## Returns

The data type of the returned value is `NUMBER(<precision>, <scale>)`. The scale depends upon the values being processed.

## Usage notes

- For single-record inputs, VAR\_SAMP, VARIANCE, and VARIANCE\_SAMP all return NULL. This is different from the Oracle behavior,
  where VAR\_SAMP returns NULL for a single record and VARIANCE returns 0.
- When passed a VARCHAR expression, this function implicitly casts the input to floating point values. If the cast
  cannot be performed, an error is returned.
- When this function is called as a window function:
  - The syntax allows the DISTINCT keyword, but it is ignored.
  - If you do not specify a window frame, the following implied window frame is used:

    `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

    For more information about window frames, including syntax, usage notes, and examples, see
    [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Examples

This example shows how to use the VAR\_SAMP function:

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
SELECT k, VAR_SAMP(v), VAR_SAMP(v2)
  FROM aggr
  GROUP BY k
  ORDER BY k;
```

```
+---+---------------+----------------+
| K |   VAR_SAMP(V) |   VAR_SAMP(V2) |
|---+---------------+----------------|
| 1 |          NULL |           NULL |
| 2 | 72.9166666667 | 144.3333333333 |
+---+---------------+----------------+
```
