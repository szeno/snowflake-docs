Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Cardinality Estimation) , [Window function syntax and usage](/sql-reference/functions-window-syntax)

# DATASKETCHES\_HLL\_COMBINE

Combines (merges) input sketches into a single output sketch.

This function is a version of the [HLL](/sql-reference/functions/hll) HyperLogLog function that can read binary sketches
in the format used by Apache DataSketches. For more information, see the
[Apache DataSketches documentation](https://datasketches.apache.org/docs/HLL/HllSketches.html).

This function allows scenarios where the [DATASKETCHES\_HLL\_ACCUMULATE](/sql-reference/functions/datasketches_hll_accumulate) function is run over
horizontal partitions of the same table, producing an algorithm sketch for each table
partition. These sketches can later be combined using this function, producing the same output
sketch as a single run of [DATASKETCHES\_HLL\_ACCUMULATE](/sql-reference/functions/datasketches_hll_accumulate) over the entire table.

See also:
:   [DATASKETCHES\_HLL\_ACCUMULATE](/sql-reference/functions/datasketches_hll_accumulate)

## Syntax

Copy code

```
DATASKETCHES_HLL_COMBINE( [ DISTINCT ]  <state> [ , <max_log_k> ] )
```

## Required arguments

`state`
:   An expression that contains state information generated
    by a call to [DATASKETCHES\_HLL\_ACCUMULATE](/sql-reference/functions/datasketches_hll_accumulate).

## Optional arguments

`max_log_k`
:   The maximum value, in log2, of K for this union. Specify an INTEGER value between 4 and 21, inclusive.
    For more information, see the [Apache DataSketches documentation](https://datasketches.apache.org/docs/HLL/HllSketches.html).

    Default: 12

## Returns

The function returns a BINARY value that is compatible with the Apache Datasketches library.

## Usage notes

DISTINCT is supported syntactically, but has no effect.

## Examples

Create a table and insert values:

Copy code

```
CREATE OR REPLACE TABLE datasketches_demo(v INT, g INT);

INSERT INTO datasketches_demo SELECT 1, 1;
INSERT INTO datasketches_demo SELECT 2, 1;
INSERT INTO datasketches_demo SELECT 2, 1;
INSERT INTO datasketches_demo SELECT 2, 1;
INSERT INTO datasketches_demo SELECT 1, 2;
INSERT INTO datasketches_demo SELECT 1, 2;
INSERT INTO datasketches_demo SELECT 4, 2;
INSERT INTO datasketches_demo SELECT 4, 2;
INSERT INTO datasketches_demo SELECT 5, 2;
```

The following example performs the following actions:

1. The DATASKETCHES\_HLL\_ACCUMULATE function creates two binary sketches for the data in column `v`,
   grouped by the values `1` and `2` in column `g`.
2. The DATASKETCHES\_HLL\_COMBINE function combines these binary sketches.

Copy code

```
WITH
  accumulated AS (
    SELECT g,
           DATASKETCHES_HLL_ACCUMULATE(v) AS accumulated_sketches
      FROM datasketches_demo
      GROUP BY g)
SELECT DATASKETCHES_HLL_COMBINE(accumulated_sketches) AS combined_sketches
  FROM accumulated;
```

```
+--------------------------------------------------+
| COMBINED_SKETCHES                                |
|--------------------------------------------------|
| 0201070C030804002BF2FB06862FF90D81BC5D067B65E608 |
+--------------------------------------------------+
```

You can see values of the accumulated sketches in the example in [DATASKETCHES\_HLL\_ACCUMULATE](/sql-reference/functions/datasketches_hll_accumulate).
