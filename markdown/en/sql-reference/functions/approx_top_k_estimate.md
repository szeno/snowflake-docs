Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Frequency Estimation) , [Window function syntax and usage](/sql-reference/functions-window-syntax)

# APPROX\_TOP\_K\_ESTIMATE

Returns the approximate most frequent values and their estimated frequency for the given Space-Saving state. (For more information about the Space-Saving
summary, see [Estimating Frequent Values](/user-guide/querying-approximate-frequent-values).)

A Space-Saving state produced by [APPROX\_TOP\_K\_ACCUMULATE](/sql-reference/functions/approx_top_k_accumulate) and [APPROX\_TOP\_K\_COMBINE](/sql-reference/functions/approx_top_k_combine) can be used to compute a cardinality estimate using the APPROX\_TOP\_K\_ESTIMATE function.

Thus, APPROX\_TOP\_K\_ESTIMATE(APPROX\_TOP\_K\_ACCUMULATE(…)) is equivalent to APPROX\_TOP\_K(…).

See also:
:   [APPROX\_TOP\_K](/sql-reference/functions/approx_top_k) , [APPROX\_TOP\_K\_ACCUMULATE](/sql-reference/functions/approx_top_k_accumulate) , [APPROX\_TOP\_K\_COMBINE](/sql-reference/functions/approx_top_k_combine)

## Syntax

Copy code

```
APPROX_TOP_K_ESTIMATE( <state> [ , <k> ] )
```

## Arguments

`state`
:   An expression that contains state information generated
    by a call to [APPROX\_TOP\_K\_ACCUMULATE](/sql-reference/functions/approx_top_k_accumulate) or
    [APPROX\_TOP\_K\_COMBINE](/sql-reference/functions/approx_top_k_combine).

`k`
:   The number of values whose counts you want approximated.
    For example, if you want to see the top 10 most common values, then
    set `k` to 10.

    If `k` is omitted, the default is `1`.

    The maximum value is `100000` (100,000), and is automatically reduced if
    items cannot fit in the output.

## Returns

Returns a value of type ARRAY.

## Usage notes

- Decimal-float ([DECFLOAT](/sql-reference/data-types-numeric#label-data-type-decfloat)) values aren’t supported.

## Examples

This example shows how to use the three related functions
APPROX\_TOP\_K\_ACCUMULATE, APPROX\_TOP\_K\_ESTIMATE, and APPROX\_TOP\_K\_COMBINE.

Note

This example uses more counters than distinct data values in order to get
consistent results. In real-world applications, the number of distinct values
is usually larger than the number of counters, so the approximations can vary.

This example generates one table with 8 rows that have values 1 - 8, and a
second table with 8 rows that have values 5 - 12. Thus the most frequent
values in the union of the two tables are the values 5-8, each of which has a
count of 2.

Create a simple table and data:

Copy code

```
CREATE OR REPLACE SEQUENCE seq91;
CREATE OR REPLACE TABLE sequence_demo (c1 INTEGER DEFAULT seq91.NEXTVAL, dummy SMALLINT);
INSERT INTO sequence_demo (dummy) VALUES (0);

INSERT INTO sequence_demo (dummy) SELECT dummy FROM sequence_demo;
INSERT INTO sequence_demo (dummy) SELECT dummy FROM sequence_demo;
INSERT INTO sequence_demo (dummy) SELECT dummy FROM sequence_demo;
```

Create a table that contains the “state” that represents the current
approximate Top K information for the table named `sequence_demo`:

Copy code

```
CREATE OR REPLACE TABLE resultstate1 AS (
  SELECT APPROX_TOP_K_ACCUMULATE(c1, 50) AS rs1
    FROM sequence_demo);
```

Now create a second table and add data. (In a more realistic situation,
the user could have loaded more data into the first table and divided the
data into non-overlapping sets based on the time that the data was loaded.)

Copy code

```
CREATE OR REPLACE TABLE test_table2 (c1 INTEGER);
INSERT INTO test_table2 (c1) SELECT c1 + 4 FROM sequence_demo;
```

Get the “state” information for just the new data.

Copy code

```
CREATE OR REPLACE TABLE resultstate2 AS
  (SELECT APPROX_TOP_K_ACCUMULATE(c1, 50) AS rs1
     FROM test_table2);
```

Combine the “state” information for the two batches of rows:

Copy code

```
CREATE OR REPLACE TABLE combined_resultstate (c1) AS
  SELECT APPROX_TOP_K_COMBINE(rs1) AS apc1
    FROM (
      SELECT rs1 FROM resultstate1
      UNION ALL
      SELECT rs1 FROM resultstate2
    );
```

Get the approximate Top K value of the combined set of rows:

Copy code

```
SELECT APPROX_TOP_K_ESTIMATE(c1, 4)
  FROM combined_resultstate;
```

```
+------------------------------+
| APPROX_TOP_K_ESTIMATE(C1, 4) |
|------------------------------|
| [                            |
|   [                          |
|     5,                       |
|     2                        |
|   ],                         |
|   [                          |
|     6,                       |
|     2                        |
|   ],                         |
|   [                          |
|     7,                       |
|     2                        |
|   ],                         |
|   [                          |
|     8,                       |
|     2                        |
|   ]                          |
| ]                            |
+------------------------------+
```
