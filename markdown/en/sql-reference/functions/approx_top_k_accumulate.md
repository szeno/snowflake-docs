Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Frequency Estimation) , [Window function syntax and usage](/sql-reference/functions-window-syntax)

# APPROX\_TOP\_K\_ACCUMULATE

Returns the Space-Saving summary at the end of aggregation. (For more
information about the Space-Saving summary, see
[Estimating Frequent Values](/user-guide/querying-approximate-frequent-values).)

The function [APPROX\_TOP\_K](/sql-reference/functions/approx_top_k) discards its internal, intermediate state
when the final cardinality estimate is returned. However, in certain advanced
use cases, such as estimating incremental frequent values during bulk loading,
you might want to keep the intermediate state, in which case you would use
APPROX\_TOP\_K\_ACCUMULATE instead of [APPROX\_TOP\_K](/sql-reference/functions/approx_top_k).

In contrast to [APPROX\_TOP\_K](/sql-reference/functions/approx_top_k), APPROX\_TOP\_K\_ACCUMULATE does not return a frequency estimate of items. Instead,
it returns the algorithm state itself. The intermediate state can later be:

- Combined (that is, merged) with intermediate states from separate but related
  batches of data.
- Processed by other functions that operate directly on the intermediate state,
  for example, [APPROX\_TOP\_K\_ESTIMATE](/sql-reference/functions/approx_top_k_estimate). (For an example, see the
  Examples section below.)
- Exported to external tools.

See also:
:   [APPROX\_TOP\_K\_COMBINE](/sql-reference/functions/approx_top_k_combine), [APPROX\_TOP\_K\_ESTIMATE](/sql-reference/functions/approx_top_k_estimate)

## Syntax

Copy code

```
APPROX_TOP_K_ACCUMULATE( <expr> , <counters> )
```

## Arguments

`expr`
:   The expression (e.g. column name) for which you want to find the most common values.

`counters`
:   This is the maximum number of distinct values that can be tracked at a time during the estimation process.

    For example, if `counters` is set to 100000, then the algorithm tracks 100,000 distinct values, attempting to keep the
    100,000 most frequent values.

    The maximum number of `counters` is `100000` (100,000).

## Usage notes

- Decimal-float ([DECFLOAT](/sql-reference/data-types-numeric#label-data-type-decfloat)) values aren’t supported.

## Examples

This example shows how to use the three related functions
APPROX\_TOP\_K\_ACCUMULATE, APPROX\_TOP\_K\_ESTIMATE, and APPROX\_TOP\_K\_COMBINE.

Note

This example uses more counters than distinct data values in order to get
consistent results. In real-world applications, the number of distinct
values is usually larger than the number of counters, so approximations can vary.

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

Now create a second table and add data. (In a more realistic situation, the user could have
loaded more data into the first table and divided the data into non-overlapping sets based
on the time that the data was loaded.)

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
