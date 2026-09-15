Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Cardinality Estimation) ,
    [Window functions](/sql-reference/functions-window-syntax) (Cardinality Estimation)

# HLL\_ESTIMATE

Returns the cardinality estimate for the given HyperLogLog state.

A HyperLogLog state produced by [HLL\_ACCUMULATE](/sql-reference/functions/hll_accumulate) and [HLL\_COMBINE](/sql-reference/functions/hll_combine) can be used to compute a cardinality estimate using the HLL\_ESTIMATE function.

Thus, HLL\_ESTIMATE(HLL\_ACCUMULATE(…)) is equivalent to HLL(…).

See also:
:   [HLL](/sql-reference/functions/hll) , [HLL\_ACCUMULATE](/sql-reference/functions/hll_accumulate) , [HLL\_COMBINE](/sql-reference/functions/hll_combine)

## Syntax

**Aggregate function**

Copy code

```
HLL_ESTIMATE( <state> )
```

**Window function**

Copy code

```
HLL_ESTIMATE( <state> ) OVER ( [ PARTITION BY <expr> ] )
```

For details about the OVER clause, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Arguments

`state`
:   An expression that contains state information generated
    by a call to [HLL\_ACCUMULATE](/sql-reference/functions/hll_accumulate) or [HLL\_COMBINE](/sql-reference/functions/hll_combine).

## Usage notes

- This function can be used as an [aggregate function](/sql-reference/functions-aggregation) or
  a [window function](/sql-reference/functions-window-syntax).

## Examples

This example shows how to use the three related functions
HLL\_ACCUMULATE, HLL\_ESTIMATE, and HLL\_COMBINE.

Create a simple table and data:

Copy code

```
CREATE OR REPLACE SEQUENCE seq92;
CREATE OR REPLACE TABLE sequence_demo (c1 INTEGER DEFAULT seq92.nextval, dummy SMALLINT);
INSERT INTO sequence_demo (dummy) VALUES (0);

INSERT INTO sequence_demo (dummy) SELECT dummy FROM sequence_demo;
INSERT INTO sequence_demo (dummy) SELECT dummy FROM sequence_demo;
INSERT INTO sequence_demo (dummy) SELECT dummy FROM sequence_demo;
```

Create a table that contains the “state” that represents the current
approximate cardinality information for the table named `sequence_demo`:

Copy code

```
CREATE OR REPLACE TABLE resultstate1 AS (
  SELECT HLL_ACCUMULATE(c1) AS rs1
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
  (SELECT HLL_ACCUMULATE(c1) AS rs1
     FROM test_table2);
```

Combine the “state” information for the two batches of rows:

Copy code

```
CREATE OR REPLACE TABLE combined_resultstate (c1) AS
  SELECT HLL_COMBINE(rs1) AS apc1
    FROM (
      SELECT rs1 FROM resultstate1
      UNION ALL
      SELECT rs1 FROM resultstate2
    );
```

Get the approximate cardinality of the combined set of rows:

Copy code

```
SELECT HLL_ESTIMATE(c1)
  FROM combined_resultstate;
```

```
+------------------+
| HLL_ESTIMATE(C1) |
|------------------|
|               12 |
+------------------+
```
