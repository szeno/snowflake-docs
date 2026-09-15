Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Cardinality Estimation) ,
    [Window functions](/sql-reference/functions-window-syntax) (Cardinality Estimation)

# HLL\_COMBINE

Combines (merges) input states into a single output state.

This allows scenarios where [HLL\_ACCUMULATE](/sql-reference/functions/hll_accumulate) is run over horizontal
partitions of the same table, producing an algorithm state for each table
partition. These states can later be combined using [HLL\_COMBINE](/sql-reference/functions/hll_combine),
producing the same output state as a single run of [HLL\_ACCUMULATE](/sql-reference/functions/hll_accumulate)
over the entire table.

See also:
:   [HLL](/sql-reference/functions/hll) , [HLL\_ACCUMULATE](/sql-reference/functions/hll_accumulate) , [HLL\_ESTIMATE](/sql-reference/functions/hll_estimate)

## Syntax

**Aggregate function**

Copy code

```
HLL_COMBINE( [ DISTINCT ] <state> )
```

**Window function**

Copy code

```
HLL_COMBINE( [ DISTINCT ] <state> ) OVER ( [ PARTITION BY <expr1> ] )
```

For details about the OVER clause, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Arguments

`state`
:   An expression that contains state information generated
    by a call to [HLL\_ACCUMULATE](/sql-reference/functions/hll_accumulate).

## Usage notes

- This function can be used as an [aggregate function](/sql-reference/functions-aggregation) or
  a [window function](/sql-reference/functions-window-syntax).
- DISTINCT is supported syntactically, but has no effect.
- The output of this function is not fully deterministic. Running this
  function on the same inputs might return different results at different
  times. The differences are typically small and are consistent with the fact
  that the HLL\_\* functions are approximation functions.

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
