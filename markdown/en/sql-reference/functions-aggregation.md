# Aggregate functions

Aggregate functions operate on values across rows to perform mathematical calculations such as sum, average, counting, minimum/maximum values, standard
deviation, and estimation, as well as some non-mathematical operations.

An aggregate function takes multiple rows (actually, zero, one, or more rows) as input and produces a single output.
In contrast, scalar functions take one row as input and produce one row (one value) as output.

An aggregate function always returns exactly one row, even when the input contains zero rows. Typically, if
the input contains zero rows, the output is NULL. However, an aggregate function could return `0`, an empty string, or
some other value when passed zero rows.

## List of functions (by sub-category)

| Function Name | Notes |
| --- | --- |
| **General Aggregation** |  |
| [ANY\_VALUE](/sql-reference/functions/any_value) |  |
| [AVG](/sql-reference/functions/avg) |  |
| [CORR](/sql-reference/functions/corr) |  |
| [COUNT](/sql-reference/functions/count) |  |
| [COUNT\_IF](/sql-reference/functions/count_if) |  |
| [COVAR\_POP](/sql-reference/functions/covar_pop) |  |
| [COVAR\_SAMP](/sql-reference/functions/covar_samp) |  |
| [LISTAGG](/sql-reference/functions/listagg) |  |
| [MAX](/sql-reference/functions/max) |  |
| [MAX\_BY](/sql-reference/functions/max_by) |  |
| [MEDIAN](/sql-reference/functions/median) |  |
| [MIN](/sql-reference/functions/min) |  |
| [MIN\_BY](/sql-reference/functions/min_by) |  |
| [MODE](/sql-reference/functions/mode) |  |
| [PERCENTILE\_CONT](/sql-reference/functions/percentile_cont) | Uses different syntax than the other aggregate functions. |
| [PERCENTILE\_DISC](/sql-reference/functions/percentile_disc) | Uses different syntax than the other aggregate functions. |
| [STDDEV, STDDEV\_SAMP](/sql-reference/functions/stddev) | STDDEV and STDDEV\_SAMP are aliases. |
| [STDDEV\_POP](/sql-reference/functions/stddev_pop) |  |
| [SUM](/sql-reference/functions/sum) |  |
| [VAR\_POP](/sql-reference/functions/var_pop) |  |
| [VAR\_SAMP](/sql-reference/functions/var_samp) |  |
| [VARIANCE\_POP](/sql-reference/functions/variance_pop) | Alias for [VAR\_POP](/sql-reference/functions/var_pop). |
| [VARIANCE , VARIANCE\_SAMP](/sql-reference/functions/variance) | Alias for [VAR\_SAMP](/sql-reference/functions/var_samp). |
| **Bitwise Aggregation** |  |
| [BITAND\_AGG](/sql-reference/functions/bitand_agg) |  |
| [BITOR\_AGG](/sql-reference/functions/bitor_agg) |  |
| [BITXOR\_AGG](/sql-reference/functions/bitxor_agg) |  |
| **Boolean Aggregation** |  |
| [BOOLAND\_AGG](/sql-reference/functions/booland_agg) |  |
| [BOOLOR\_AGG](/sql-reference/functions/boolor_agg) |  |
| [BOOLXOR\_AGG](/sql-reference/functions/boolxor_agg) |  |
| **Hash** |  |
| [HASH\_AGG](/sql-reference/functions/hash_agg) |  |
| **Semi-structured Data Aggregation** |  |
| [ARRAY\_AGG](/sql-reference/functions/array_agg) |  |
| [OBJECT\_AGG](/sql-reference/functions/object_agg) |  |
| **Linear Regression** |  |
| [REGR\_AVGX](/sql-reference/functions/regr_avgx) |  |
| [REGR\_AVGY](/sql-reference/functions/regr_avgy) |  |
| [REGR\_COUNT](/sql-reference/functions/regr_count) |  |
| [REGR\_INTERCEPT](/sql-reference/functions/regr_intercept) |  |
| [REGR\_R2](/sql-reference/functions/regr_r2) |  |
| [REGR\_SLOPE](/sql-reference/functions/regr_slope) |  |
| [REGR\_SXX](/sql-reference/functions/regr_sxx) |  |
| [REGR\_SXY](/sql-reference/functions/regr_sxy) |  |
| [REGR\_SYY](/sql-reference/functions/regr_syy) |  |
| **Statistics and Probability** |  |
| [KURTOSIS](/sql-reference/functions/kurtosis) |  |
| [SKEW](/sql-reference/functions/skew) |  |
| **Counting Distinct Values** |  |
| [ARRAY\_UNION\_AGG](/sql-reference/functions/array_union_agg) |  |
| [ARRAY\_UNIQUE\_AGG](/sql-reference/functions/array_unique_agg) |  |
| [BITMAP\_ABSOLUTE\_POSITION](/sql-reference/functions/bitmap_absolute_position) |  |
| [BITMAP\_AND](/sql-reference/functions/bitmap_and) |  |
| [BITMAP\_AND\_AGG](/sql-reference/functions/bitmap_and_agg) |  |
| [BITMAP\_BIT\_POSITION](/sql-reference/functions/bitmap_bit_position) |  |
| [BITMAP\_BUCKET\_NUMBER](/sql-reference/functions/bitmap_bucket_number) |  |
| [BITMAP\_COUNT](/sql-reference/functions/bitmap_count) |  |
| [BITMAP\_CONSTRUCT\_AGG](/sql-reference/functions/bitmap_construct_agg) |  |
| [BITMAP\_OR](/sql-reference/functions/bitmap_or) |  |
| [BITMAP\_OR\_AGG](/sql-reference/functions/bitmap_or_agg) |  |
| [BITMAP\_TO\_ARRAY](/sql-reference/functions/bitmap_to_array) |  |
| **Cardinality Estimation**   (**using** [HyperLogLog](/user-guide/querying-approximate-cardinality)) |  |
| [APPROX\_COUNT\_DISTINCT](/sql-reference/functions/approx_count_distinct) | Alias for [HLL](/sql-reference/functions/hll). |
| [DATASKETCHES\_HLL](/sql-reference/functions/datasketches_hll) |  |
| [DATASKETCHES\_HLL\_ACCUMULATE](/sql-reference/functions/datasketches_hll_accumulate) |  |
| [DATASKETCHES\_HLL\_COMBINE](/sql-reference/functions/datasketches_hll_combine) |  |
| [DATASKETCHES\_HLL\_ESTIMATE](/sql-reference/functions/datasketches_hll_estimate) | Not an aggregate function; uses scalar input from [DATASKETCHES\_HLL\_ACCUMULATE](/sql-reference/functions/datasketches_hll_accumulate) or [DATASKETCHES\_HLL\_COMBINE](/sql-reference/functions/datasketches_hll_combine). |
| [HLL](/sql-reference/functions/hll) |  |
| [HLL\_ACCUMULATE](/sql-reference/functions/hll_accumulate) |  |
| [HLL\_COMBINE](/sql-reference/functions/hll_combine) |  |
| [HLL\_ESTIMATE](/sql-reference/functions/hll_estimate) | Not an aggregate function; uses scalar input from [HLL\_ACCUMULATE](/sql-reference/functions/hll_accumulate) or [HLL\_COMBINE](/sql-reference/functions/hll_combine). |
| [HLL\_EXPORT](/sql-reference/functions/hll_export) |  |
| [HLL\_IMPORT](/sql-reference/functions/hll_import) |  |
| **Similarity Estimation**   (**using** [MinHash](/user-guide/querying-approximate-similarity)) |  |
| [APPROXIMATE\_JACCARD\_INDEX](/sql-reference/functions/approximate_jaccard_index) | Alias for [APPROXIMATE\_SIMILARITY](/sql-reference/functions/approximate_similarity). |
| [APPROXIMATE\_SIMILARITY](/sql-reference/functions/approximate_similarity) |  |
| [MINHASH](/sql-reference/functions/minhash) |  |
| [MINHASH\_COMBINE](/sql-reference/functions/minhash_combine) |  |
| **Frequency Estimation**   (**using** [Space-Saving](/user-guide/querying-approximate-frequent-values)) |  |
| [APPROX\_TOP\_K](/sql-reference/functions/approx_top_k) |  |
| [APPROX\_TOP\_K\_ACCUMULATE](/sql-reference/functions/approx_top_k_accumulate) |  |
| [APPROX\_TOP\_K\_COMBINE](/sql-reference/functions/approx_top_k_combine) |  |
| [APPROX\_TOP\_K\_ESTIMATE](/sql-reference/functions/approx_top_k_estimate) | Not an aggregate function; uses scalar input from [APPROX\_TOP\_K\_ACCUMULATE](/sql-reference/functions/approx_top_k_accumulate) or [APPROX\_TOP\_K\_COMBINE](/sql-reference/functions/approx_top_k_combine). |
| **Percentile Estimation**   (**using** [t-Digest](/user-guide/querying-approximate-percentile-values)) |  |
| [APPROX\_PERCENTILE](/sql-reference/functions/approx_percentile) |  |
| [APPROX\_PERCENTILE\_ACCUMULATE](/sql-reference/functions/approx_percentile_accumulate) |  |
| [APPROX\_PERCENTILE\_COMBINE](/sql-reference/functions/approx_percentile_combine) |  |
| [APPROX\_PERCENTILE\_ESTIMATE](/sql-reference/functions/approx_percentile_estimate) | Not an aggregate function; uses scalar input from [APPROX\_PERCENTILE\_ACCUMULATE](/sql-reference/functions/approx_percentile_accumulate) or [APPROX\_PERCENTILE\_COMBINE](/sql-reference/functions/approx_percentile_combine). |
| **Aggregation Utilities** |  |
| [GROUPING](/sql-reference/functions/grouping) | Not an aggregate function, but can be used in conjunction with aggregate functions to determine the level of aggregation for a row produced by a [GROUP BY](/sql-reference/constructs/group-by) query. |
| [GROUPING\_ID](/sql-reference/functions/grouping_id) | Alias for [GROUPING](/sql-reference/functions/grouping). |
| **AI Functions** |  |
| [AI\_AGG](/sql-reference/functions/ai_agg) |  |
| [AI\_SUMMARIZE\_AGG](/sql-reference/functions/ai_summarize_agg) |  |
| **Vector Aggregation** |  |
| [VECTOR\_AVG](/sql-reference/functions/vector_avg) |  |
| [VECTOR\_MAX](/sql-reference/functions/vector_max) |  |
| [VECTOR\_MIN](/sql-reference/functions/vector_min) |  |
| [VECTOR\_SUM](/sql-reference/functions/vector_sum) |  |
| **Semantic views** |  |
| [AGG](/sql-reference/functions/agg) |  |

Expand

Show lessSee more

## Introductory example

The following example illustrates the difference between an aggregate function ([AVG](/sql-reference/functions/avg)) and a scalar function ([COS](/sql-reference/functions/cos)). The scalar function returns one output row for each input
row, while the aggregate function returns one output row for multiple input rows:

Create a table and populate it with values:

Copy code

```
CREATE TABLE simple (x INTEGER, y INTEGER);
INSERT INTO simple (x, y) VALUES
    (10, 20),
    (20, 44),
    (30, 70);
```

Query the table:

Copy code

```
SELECT x, y
    FROM simple
    ORDER BY x,y;
```

```
+----+----+
|  X |  Y |
|----+----|
| 10 | 20 |
| 20 | 44 |
| 30 | 70 |
+----+----+
```

The scalar function returns one output row for each input row.

Copy code

```
SELECT COS(x)
    FROM simple
    ORDER BY x;
```

```
+---------------+
|        COS(X) |
|---------------|
| -0.8390715291 |
|  0.4080820618 |
|  0.1542514499 |
+---------------+
```

The aggregate function returns one output row for multiple input rows:

Copy code

```
SELECT SUM(x)
    FROM simple;
```

```
+--------+
| SUM(X) |
|--------|
|     60 |
+--------+
```

## Aggregate functions and NULL values

Some aggregate functions ignore NULL values. For example, [AVG](/sql-reference/functions/avg) calculates the average of values `1`, `5`, and `NULL` to be `3`,
based on the following formula:

> `(1 + 5) / 2 = 3`

In both the numerator and the denominator, only the two non-NULL values are used.

If all of the values passed to the aggregate function are NULL, then the aggregate function returns NULL.

Some aggregate functions can be passed more than one column. For example:

Copy code

```
SELECT COUNT(col1, col2) FROM table1;
```

In these instances, the aggregate function ignores a row if any individual column is NULL.

For example, in the following query, [COUNT](/sql-reference/functions/count) returns `1`, not `4`, because three of the four rows contain at least one NULL
value in the selected columns:

Create a table and populate it with values:

Copy code

```
CREATE OR REPLACE TABLE test_null_aggregate_functions (x INT, y INT);
INSERT INTO test_null_aggregate_functions (x, y) VALUES
  (1, 2),         -- No NULLs.
  (3, NULL),      -- One but not all columns are NULL.
  (NULL, 6),      -- One but not all columns are NULL.
  (NULL, NULL);   -- All columns are NULL.
```

Query the table:

Copy code

```
SELECT COUNT(x, y) FROM test_null_aggregate_functions;
```

```
+-------------+
| COUNT(X, Y) |
|-------------|
|           1 |
+-------------+
```

If [SUM](/sql-reference/functions/sum) is called with an expression that references two or more columns, and if one or more of those columns
is NULL, then the expression evaluates to NULL, and the row is ignored:

Copy code

```
SELECT SUM(x + y) FROM test_null_aggregate_functions;
```

```
+------------+
| SUM(X + Y) |
|------------|
|          3 |
+------------+
```

This behavior differs from the behavior of [GROUP BY](/sql-reference/constructs/group-by), which does not discard rows when some columns are NULL:

Copy code

```
SELECT x AS X_COL, y AS Y_COL
  FROM test_null_aggregate_functions
  GROUP BY x, y;
```

```
+-------+-------+
| X_COL | Y_COL |
|-------+-------|
|     1 |     2 |
|     3 |  NULL |
|  NULL |     6 |
|  NULL |  NULL |
+-------+-------+
```
