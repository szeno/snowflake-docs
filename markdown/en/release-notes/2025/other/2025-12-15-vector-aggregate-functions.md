# Dec 15, 2025: Vector aggregate functions

Snowflake now has vector aggregate functions that enable element-wise mathematical operations across multiple [VECTOR](/sql-reference/data-types-vector) values. These functions perform aggregation operations on columns of vectors, computing element-wise results across all vectors in a group.

Vector aggregate functions are essential for machine learning and data science workflows that require statistical operations on vector embeddings, such as computing centroids, finding ranges, or calculating averages across vector datasets. These functions ignore NULL in aggregation, preserve data types where possible, and are optimized for handling vector data.

The newly offered vector aggregation functions are:

- [VECTOR\_SUM](/sql-reference/functions/vector_sum) – Compute the element-wise sum of vectors, preserving type.
- [VECTOR\_MIN](/sql-reference/functions/vector_min) – Compute the element-wise minimum of vectors, preserving type.
- [VECTOR\_MAX](/sql-reference/functions/vector_max) – Compute the element-wise maximum of vectors, preserving type.
- [VECTOR\_AVG](/sql-reference/functions/vector_avg) – Compute the element-wise average of vectors, returning a vector containing [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) elements.

For more information, see [Vector functions](/sql-reference/functions-vector).
