Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Frequency Estimation) , [Window functions](/sql-reference/functions-window)

# APPROX\_TOP\_K

Uses Space-Saving to return an approximation of the most frequent values in the input, along with their approximate frequencies.

The output is a JSON array of arrays. In the inner arrays, the first entry is a value in the input, and the second entry corresponds to its estimated frequency in the input. The outer array contains
`k` items, sorted by descending frequency.

For more information about APPROX\_TOP\_K, see [Estimating Frequent Values](/user-guide/querying-approximate-frequent-values).

See also:
:   [APPROX\_TOP\_K\_ACCUMULATE](/sql-reference/functions/approx_top_k_accumulate) , [APPROX\_TOP\_K\_COMBINE](/sql-reference/functions/approx_top_k_combine), [APPROX\_TOP\_K\_ESTIMATE](/sql-reference/functions/approx_top_k_estimate)

## Syntax

**Aggregate function**

Copy code

```
APPROX_TOP_K( <expr> [ , <k> [ , <counters> ] ] )
```

**Window function**

Copy code

```
APPROX_TOP_K( <expr> [ , <k> [ , <counters> ] ] ) OVER ( [ PARTITION BY <expr4> ] )
```

## Arguments

- `expr`: The expression (e.g. column name) for which you want to find
  the most common values.
- `k`: The number of values whose counts you want approximated.
  For example, if you want to see the top 10 most common values, then
  set `k` to 10.

  If `k` is omitted, the default is `1`.

  The maximum value is `100000` (100,000), and is automatically reduced if
  items cannot fit in the output.
- `counters`: This is the maximum number of distinct values that
  can be tracked at a time during the estimation process. For example, if
  `counters` is set to 100000, then the algorithm tracks 100,000
  distinct values, attempting to keep the 100,000 most frequent values.

  The maximum number of `counters` is `100000` (100,000).

`expr4`
:   This is the optional expression used to group rows into partitions.

## Usage notes

- The approximation is more accurate if the number of `counters` is
  large, so in most cases `counters` should be considerably bigger
  than `k`.
  (Each counter uses only a small amount of memory, so increasing the number
  of counters is not expensive in terms of memory.)

- When this function is called as a window function, it does not support:
  - An ORDER BY clause within the OVER clause.
  - Explicit window frames.

- Decimal-float ([DECFLOAT](/sql-reference/data-types-numeric#label-data-type-decfloat)) values aren’t supported.

## Examples

Copy code

```
SELECT APPROX_TOP_K(C4) FROM lineitem;
```

```
+--------------------+
| APPROX_TOP_K(C4,3) |
+--------------------+
| [                  |
|   [                |
|     1,             |
|     124923         |
|   ],               |
|   [                |
|     2,             |
|     107093         |
|   ],               |
|   [                |
|     3,             |
|    89315           |
|   ]                |
| ]                  |
+--------------------+
```

Copy code

```
WITH states AS (
  SELECT approx_top_k(C4, 3, 5) AS state
  FROM lineitem)
SELECT value[0]::INT AS value, value[1]::INT AS frequency
  FROM states, LATERAL FLATTEN(state);
```

```
+-------+-----------+
| VALUE | FREQUENCY |
+-------+-----------+
|     1 |    124923 |
|     2 |    107093 |
|     3 |     89438 |
+-------+-----------+
```
