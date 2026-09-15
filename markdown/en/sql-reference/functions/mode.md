Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General) , [Window functions](/sql-reference/functions-window)

# MODE

Returns the most frequent value for the values within `expr1`. NULL values are ignored. If all the values are
NULL, or there are 0 rows, then the function returns NULL.

## Syntax

**Aggregate function**

Copy code

```
MODE( <expr1> )
```

**Window function**

Copy code

```
MODE( <expr1> ) OVER ( [ PARTITION BY <expr2> ] )
```

## Arguments

`expr1`
:   This expression produces the values that are searched to find the most frequent value. The expression can be of any of the following data types:

    > - BINARY
    > - BOOLEAN
    > - DATE
    > - FLOAT
    > - INTEGER
    > - NUMBER
    > - TIMESTAMP (TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, TIMESTAMP\_TZ)
    > - VARCHAR
    > - VARIANT

    This function does not support the following data types:

    > - ARRAY
    > - GEOGRAPHY
    > - OBJECT

`expr2`
:   The optional expression on which to partition the data into groups. The output contains the most frequent
    value for each group/partition.

## Returns

The data type of the returned value is identical to the data type of the input expression.

## Usage notes

- If there is a tie for most frequent value (two or more values occur as frequently as each other, and
  more frequently than any other value), MODE returns one of those values.
- DISTINCT is not supported for this function.
- Even if NULL is the most frequent value, the function does not return NULL (unless all values are NULL).

- When this function is called as a window function, it does not support:
  - An ORDER BY clause within the OVER clause.
  - Explicit window frames.

## Examples

The following code demonstrates the use of the MODE function:

Create a table and data:

Copy code

```
CREATE OR REPLACE TABLE aggr (k INT, v DECIMAL(10,2));
```

Get the MODE value for column `v`. The function returns NULL because there are no rows.

Copy code

```
SELECT MODE(v)
  FROM aggr;
```

```
+---------+
| MODE(V) |
|---------|
|    NULL |
+---------+
```

Insert some rows:

Copy code

```
INSERT INTO aggr (k, v) VALUES
  (1, 10),
  (1, 10),
  (1, 10),
  (1, 10),
  (1, 20),
  (1, 21);
```

The MODE function returns the most frequent value `10`:

Copy code

```
SELECT MODE(v)
  FROM aggr;
```

```
+---------+
| MODE(V) |
|---------|
|   10.00 |
+---------+
```

Insert some more rows:

Copy code

```
INSERT INTO aggr (k, v) VALUES
  (2, 20),
  (2, 20),
  (2, 25),
  (2, 30);
```

Now there are two most frequent values. The MODE function selects the value `10`:

Copy code

```
SELECT MODE(v)
  FROM aggr;
```

```
+---------+
| MODE(V) |
|---------|
|   10.00 |
+---------+
```

Insert a row with a NULL value:

Copy code

```
INSERT INTO aggr (k, v) VALUES (3, NULL);
```

Get the MODE value for each group. Note that because group `k = 3` only contains NULL values, the returned
value for that group is NULL.

Copy code

```
SELECT k, MODE(v)
  FROM aggr
  GROUP BY k
  ORDER BY k;
```

```
+---+---------+
| K | MODE(V) |
|---+---------|
| 1 |   10.00 |
| 2 |   20.00 |
| 3 |    NULL |
+---+---------+
```

The MODE function can also be used as a basic window function with an OVER clause:

Copy code

```
SELECT k, v, MODE(v) OVER (PARTITION BY k)
  FROM aggr
  ORDER BY k, v;
```

```
+---+-------+-------------------------------+
| K |     V | MODE(V) OVER (PARTITION BY K) |
|---+-------+-------------------------------|
| 1 | 10.00 |                         10.00 |
| 1 | 10.00 |                         10.00 |
| 1 | 10.00 |                         10.00 |
| 1 | 10.00 |                         10.00 |
| 1 | 20.00 |                         10.00 |
| 1 | 21.00 |                         10.00 |
| 2 | 20.00 |                         20.00 |
| 2 | 20.00 |                         20.00 |
| 2 | 25.00 |                         20.00 |
| 2 | 30.00 |                         20.00 |
| 3 |  NULL |                          NULL |
+---+-------+-------------------------------+
```
