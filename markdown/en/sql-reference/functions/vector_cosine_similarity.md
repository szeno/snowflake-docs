Categories:
:   [Vector functions](/sql-reference/functions-vector)

# VECTOR\_COSINE\_SIMILARITY

Computes the cosine similarity between two [vectors](/user-guide/snowflake-cortex/vector-embeddings).

Cosine similarity is based on the angle between two vectors in a multi-dimensional space; the magnitude of the vectors is not
considered. The cosine similarity value is the inner product of the vectors divided by the product of their lengths. The cosine
similarity is always in the interval `[-1, 1]`. For example, identical vectors have a cosine similarity of `1`, two
orthogonal vectors have a similarity of `0`, and two opposite vectors have a similarity of `-1`.

See also:
:   [VECTOR\_INNER\_PRODUCT](/sql-reference/functions/vector_inner_product) , [VECTOR\_L1\_DISTANCE](/sql-reference/functions/vector_l1_distance) , [VECTOR\_L2\_DISTANCE](/sql-reference/functions/vector_l2_distance) , [Vector Embeddings](/user-guide/snowflake-cortex/vector-embeddings)

## Syntax

Copy code

```
VECTOR_COSINE_SIMILARITY( <vector>, <vector> )
```

## Arguments

`vector`
:   The [VECTOR](/sql-reference/data-types-vector) value to calculate the angle from.

`vector`
:   The VECTOR value to calculate the angle to.

## Returns

Returns a [FLOAT](/sql-reference/data-types-numeric#label-data-types-for-floating-point-numbers) value in the interval `[-1, 1]`, which indicates the
cosine similarity between the two input vectors.

## Usage notes

- Vector functions are optimized in a way that can reduce floating point precision. This function’s results have a margin of error up to `1e-4`.

## Examples

This example calls the VECTOR\_COSINE\_SIMILARITY function to find the vector closest to `[1,2,3]`.

Copy code

```
SELECT a, VECTOR_COSINE_SIMILARITY(a, [1,2,3]::VECTOR(FLOAT, 3)) AS similarity
  FROM vectors
  ORDER BY similarity DESC
  LIMIT 1;
```

```
+-------------------------+
| [1, 2.2, 3] | 0.9990... |
+-------------------------+
```
