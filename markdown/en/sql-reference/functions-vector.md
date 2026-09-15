# Vector functions

Snowflake provides both similarity and element-wise aggregation functions for the [VECTOR](/sql-reference/data-types-vector) data type. These functions allow for finding vectors nearest to a source vector, used for semantic search and fine-tuning generative responses from LLMs and generative AI.

Similarity functions operate on two VECTOR arguments of equal element type and dimension, computing the specified metric. Snowflake provides the following vector similarity functions:

> - [VECTOR\_INNER\_PRODUCT](/sql-reference/functions/vector_inner_product)
> - [VECTOR\_L1\_DISTANCE](/sql-reference/functions/vector_l1_distance)
> - [VECTOR\_L2\_DISTANCE](/sql-reference/functions/vector_l2_distance)
> - [VECTOR\_COSINE\_SIMILARITY](/sql-reference/functions/vector_cosine_similarity)

Vector manipulation functions take an existing vector and return a new vector with different properties, such as truncation or normalization. Snowflake provides the following vector manipulation functions:

> - [VECTOR\_TRUNCATE](/sql-reference/functions/vector_truncate)
> - [VECTOR\_NORMALIZE](/sql-reference/functions/vector_normalize)

Vector aggregate functions operate on columns of VECTOR values to perform element-wise mathematical operations such as sum, average, minimum, and maximum across all vectors in a group. Snowflake provides the following vector aggregation functions:

> - [VECTOR\_SUM](/sql-reference/functions/vector_sum)
> - [VECTOR\_MIN](/sql-reference/functions/vector_min)
> - [VECTOR\_MAX](/sql-reference/functions/vector_max)
> - [VECTOR\_AVG](/sql-reference/functions/vector_avg)

Note

Vector functions on Snowflake are optimized in a way that can reduce floating point precision. These functions have a margin of error up to `1e-4`.

## List of functions

| Function Name | Notes |
| --- | --- |
| [VECTOR\_INNER\_PRODUCT](/sql-reference/functions/vector_inner_product) |  |
| [VECTOR\_L1\_DISTANCE](/sql-reference/functions/vector_l1_distance) |  |
| [VECTOR\_L2\_DISTANCE](/sql-reference/functions/vector_l2_distance) |  |
| [VECTOR\_COSINE\_SIMILARITY](/sql-reference/functions/vector_cosine_similarity) | Not supported in Snowpark API. |
| [VECTOR\_TRUNCATE](/sql-reference/functions/vector_truncate) |  |
| [VECTOR\_NORMALIZE](/sql-reference/functions/vector_normalize) |  |
| [VECTOR\_SUM](/sql-reference/functions/vector_sum) |  |
| [VECTOR\_MIN](/sql-reference/functions/vector_min) |  |
| [VECTOR\_MAX](/sql-reference/functions/vector_max) |  |
| [VECTOR\_AVG](/sql-reference/functions/vector_avg) |  |

Expand

Show lessSee more
