# Using Arrays to Compute Distinct Values for Hierarchical Aggregations

If you are counting distinct values for hierarchical aggregations (e.g. multiple grouping sets, rollups, or cubes), you can
improve performance by producing [ARRAYs](/sql-reference/data-types-semistructured#label-data-type-array) that contain the distinct values and computing the number
of distinct values from these ARRAYs. Using this approach can be faster than using `COUNT(DISTINCT <expr>)`.

This topic explains how to use ARRAYs to count distinct values.

For other techniques for counting distinct values, see [Computing the Number of Distinct Values](/user-guide/querying-distinct-counts).

## Introduction

When computing the number of distinct values for hierarchical aggregations (e.g. multiple grouping sets, rollups, or cubes), you
can speed up the computation by calling functions that produce arrays containing the distinct values. You can then call
[ARRAY\_SIZE](/sql-reference/functions/array_size) to compute the count of those distinct values.

These aggregation functions that produce ARRAYs of distinct values can perform better than `COUNT(DISTINCT <expression>)` in
queries of the following forms:

- GROUP BY ROLLUP aggregate queries
- queries containing multiple grouping sets.

Unlike `COUNT(DISTINCT <expression>)` (which needs to be executed for each group), you can compose and reuse ARRAYs that
contain the distinct values. For hierarchical aggregations, you avoid repeatedly computing the distinct counts by producing these
ARRAYs once and reusing them in higher aggregation levels.

In addition, to improve performance further, you can produce these ARRAYs ahead of time (e.g. in a materialized view), rather
than during the query, and you can use these precomputed ARRAYs in your query.

## Creating an ARRAY Containing Distinct Values

To create an ARRAY that contains the distinct values in a column, call the [ARRAY\_UNIQUE\_AGG](/sql-reference/functions/array_unique_agg)
function in a SELECT statement.

`ARRAY_UNIQUE_AGG` is an aggregation function. Aggregation in this context means returning only one instance of a value that
appears in multiple rows. If multiple rows contain the value 3, `ARRAY_UNIQUE_AGG` just includes 3 once in the returned
ARRAY.

For example, create the following table containing a column of numeric values, and insert some values into that column.

Copy code

```
CREATE OR REPLACE TABLE array_unique_agg_test (a INTEGER);
INSERT INTO array_unique_agg_test VALUES (5), (2), (1), (2), (1);
```

Run the following command to produce an ARRAY that contains the distinct values in the column:

Copy code

```
SELECT ARRAY_UNIQUE_AGG(a) AS distinct_values FROM array_unique_agg_test;
```

Copy code

```
+-----------------+
| DISTINCT_VALUES |
|-----------------|
| [               |
|   5,            |
|   2,            |
|   1             |
| ]               |
+-----------------+
```

## Computing the Number of Distinct Values from the ARRAYs

To get the total count of the distinct values from the ARRAY, call [ARRAY\_SIZE](/sql-reference/functions/array_size), passing in the
ARRAY created by [ARRAY\_UNIQUE\_AGG](/sql-reference/functions/array_unique_agg).

For example:

Copy code

```
SELECT ARRAY_SIZE(ARRAY_UNIQUE_AGG(a)) AS number_of_distinct_values FROM array_unique_agg_test;
```

Copy code

```
+---------------------------+
| NUMBER_OF_DISTINCT_VALUES |
|---------------------------|
|                         3 |
+---------------------------+
```

## Using Arrays to Improve Query Performance

The following examples demonstrate how to use the aggregation functions that produce ARRAYs of distinct values as an alternative
to `COUNT(DISTINCT <expression>)`.

- [Example 1: Counting the Distinct Values in a Single Table](#label-array-unique-agg-functions-scalar-example)
- [Example 2: Using GROUP BY to Compute the Counts by Group](#label-array-unique-agg-functions-group-by-example)
- [Example 3: Using GROUP BY ROLLUP to Roll up Counts by Group](#label-array-unique-agg-functions-group-by-rollup-example)

### Example 1: Counting the Distinct Values in a Single Table

Suppose that you want to count the number of distinct values in `my_column`. The following table compares the SQL statements
for performing this task with `COUNT(DISTINCT expression)` and `ARRAY_UNIQUE_AGG(expression)`.

| Example With COUNT(DISTINCT <expression>) | Example With ARRAY\_UNIQUE\_AGG(<expression>) |
| --- | --- |
| Copy code  ``` SELECT   COUNT(DISTINCT my_column_1),   COUNT(DISTINCT my_column_2) FROM my_table; ``` | Copy code  ``` SELECT   ARRAY_SIZE(ARRAY_UNIQUE_AGG(my_column_1)),   ARRAY_SIZE(ARRAY_UNIQUE_AGG(my_column_2)) FROM my_table; ``` |

Expand

Show lessSee more

### Example 2: Using GROUP BY to Compute the Counts by Group

Suppose that you want to count the number of distinct values in `my_column` by `my_key_1` and `my_key_2`.
The following table compares the SQL statements for performing this task with `COUNT(DISTINCT expression)` and
`ARRAY_UNIQUE_AGG(expression)`.

| Example With COUNT(DISTINCT <expression>) | Example With ARRAY\_UNIQUE\_AGG(<expression>) |
| --- | --- |
| Copy code  ``` SELECT   COUNT(DISTINCT my_column_1),   COUNT(DISTINCT my_column_2) FROM my_table GROUP BY my_key_1, my_key_2; ``` | Copy code  ``` SELECT   ARRAY_SIZE(ARRAY_UNIQUE_AGG(my_column_1)),   ARRAY_SIZE(ARRAY_UNIQUE_AGG(my_column_2)) FROM my_table GROUP BY my_key_1, my_key_2; ``` |

Expand

Show lessSee more

### Example 3: Using GROUP BY ROLLUP to Roll up Counts by Group

`ARRAY_UNIQUE_AGG` works even more efficiently for `GROUP BY ROLLUP` aggregate queries. ARRAYs are composable (in
contrast to `COUNT(DISTINCT <expression>)`), which results in less computation work and lower execution times.

Suppose that you want to roll up the number of distinct values in `my_column` by `my_key_1` and `my_key_2`. The
following table compares the SQL statements for performing this task with `COUNT(DISTINCT expression)` and
`ARRAY_UNIQUE_AGG(expression)`.

| Example With COUNT(DISTINCT <expression>) | Example With ARRAY\_UNIQUE\_AGG(<expression>) |
| --- | --- |
| Copy code  ``` SELECT   COUNT(DISTINCT my_column) FROM my_table GROUP BY ROLLUP(my_key_1, my_key_2); ``` | Copy code  ``` SELECT   ARRAY_SIZE(ARRAY_UNIQUE_AGG(my_column)) FROM my_table GROUP BY ROLLUP(my_key_1, my_key_2); ``` |

Expand

Show lessSee more

## Precomputing the ARRAYs

To improve performance, you can precompute the ARRAYs of distinct values in a table or materialized view.

For example, suppose that your data warehouse contains a fact table with multiple dimensions. You can define a materialized view
that constructs the ARRAYs to perform a coarse-grained precomputation or pre-aggregation before computing the final aggregates or
cubes that require a `COUNT(DISTINCT <expression>)`.

To collect the distinct values from the ARRAYs in each row, call the [ARRAY\_UNION\_AGG](/sql-reference/functions/array_union_agg) function.

The following example creates a table containing the ARRAYs and uses this table to compute the number of distinct values,
aggregated by different dimensions.

The following statement creates a table named `precompute` that contains the ARRAYs:

Copy code

```
CREATE TABLE precompute AS
SELECT
  my_dimension_1,
  my_dimension_2,
  ARRAY_UNIQUE_AGG(my_column) arr
FROM my_table
GROUP BY 1, 2;
```

The following statement computes the aggregates for `my_dimension_1` and `my_dimension_2`:

Copy code

```
SELECT
  my_dimension_1,
  my_dimension_2,
  ARRAY_SIZE(arr)
FROM precompute
GROUP BY 1, 2;
```

The following statement computes the aggregate only for `my_dimension_1`:

Copy code

```
SELECT
  my_dimension_1,
  ARRAY_SIZE(ARRAY_UNION_AGG(arr))
FROM precompute
GROUP BY 1;
```

The following statement computes the aggregate only for `my_dimension_2`:

Copy code

```
SELECT
  my_dimension_2,
  ARRAY_SIZE(ARRAY_UNION_AGG(arr))
FROM precompute
GROUP BY 1;
```

## Limitations

In Snowflake, ARRAY data types are limited to 16 MiB, which means that ARRAY\_UNIQUE\_AGG or ARRAY\_UNION\_AGG will generate an error
if the physical size of the output ARRAY exceeds this size.

In these cases, consider using a [bitmap aggregation](/user-guide/querying-bitmaps-for-distinct-counts) instead. As an alternative, you
can apply a bucketization technique similar to the one used for bitmap aggregations but with a different bucketization function
than BITMAP\_BUCKET\_NUMBER.
