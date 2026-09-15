# May 06, 2024 — Vector data type and vector similarity functions — *Preview*

With this release, we are pleased to announce the preview of VECTOR data type, Vector Similarity Functions,
and the Vector Embedding Function. These features enable important applications that require semantic
vector search and retrieval.

For more information, see [Vector Embeddings](/user-guide/snowflake-cortex/vector-embeddings).

## New SQL data type

The following data type was introduced in recent releases:

| Category | New data type | Description |
| --- | --- | --- |
| Vector | [VECTOR](/sql-reference/data-types-vector) | With the VECTOR data type, Snowflake encodes and processes vectors efficiently. This data type supports semantic vector search and retrieval applications, such as RAG-based applications, and common operations on vectors in vector-processing applications. |

Expand

Show lessSee more

## New SQL functions

The following functions were introduced in recent releases:

| Function Category | New Function | Description |
| --- | --- | --- |
| [Vector similarity function](/sql-reference/functions-vector) | [VECTOR\_INNER\_PRODUCT](/sql-reference/functions/vector_inner_product) | Returns the inner product of two vectors. The inner product (also known as the dot or scalar product) multiplies two vectors. |
| [Vector similarity function](/sql-reference/functions-vector) | [VECTOR\_L2\_DISTANCE](/sql-reference/functions/vector_l2_distance) | Measures the L2 distance between two vectors. |
| [Vector similarity function](/sql-reference/functions-vector) | [VECTOR\_COSINE\_SIMILARITY](/sql-reference/functions/vector_cosine_similarity) | Measures the cosine similarity between two vectors, which is the angular distance between the vectors in a multi-dimensional space. |
| [LLM Function](/user-guide/snowflake-cortex/aisql) | [EMBED\_TEXT\_768 (SNOWFLAKE.CORTEX)](/sql-reference/functions/embed_text-snowflake-cortex) | Creates a vector embedding for a given string of text in English. |

Expand

Show lessSee more
