# Computing the Number of Distinct Values

To compute the number of rows that have distinct values, you can use one of the following approaches:

- Call the SQL [COUNT](/sql-reference/functions/count) function with the `DISTINCT` keyword.
- If you just need an approximate count of distinct values, you can use the HyperLogLog functions
  (e.g. `APPROX_COUNT_DISTINCT`). For details, see [Estimating the Number of Distinct Values](/user-guide/querying-approximate-cardinality).
- If you are counting distinct values for hierarchical aggregations (e.g. multiple grouping sets, rollups, or cubes), you can
  improve performance by using one of the following approaches (rather than using `COUNT(DISTINCT <expr>)`):
  - [Use bitmaps to identify the number of distinct values](/user-guide/querying-bitmaps-for-distinct-counts).

    With this approach, you use the bitmap functions to produce bitmaps that identify the distinct integer values in a column.
    Because a bitmap can represent at most 32,768 distinct values, this approach requires “bucketizing” (using multiple bitmaps)
    if the number of distinct values exceeds 32,768.

    For details, see [Using Bitmaps to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-bitmaps-for-distinct-counts).
  - [Produce arrays that contain the distinct values](/user-guide/querying-arrays-for-distinct-counts).

    With this approach, you use the aggregate functions that produce arrays containing the unique values in a column. You can then
    call [ARRAY\_SIZE](/sql-reference/functions/array_size) to get the count of values.

    This approach works for values of any data type (e.g. [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant)) and does not require
    “bucketizing”, unless the size of the data in the ARRAY exceeds the maximum size of an ARRAY.

    For details, see [Using Arrays to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-arrays-for-distinct-counts).

**Next Topics:**

- [Estimating the Number of Distinct Values](/user-guide/querying-approximate-cardinality)
- [Using Bitmaps to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-bitmaps-for-distinct-counts)
- [Using Arrays to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-arrays-for-distinct-counts)
