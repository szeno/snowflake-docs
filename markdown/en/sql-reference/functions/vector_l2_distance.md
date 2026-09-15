Categories:
:   [Vector functions](/sql-reference/functions-vector)

# VECTOR\_L2\_DISTANCE

Computes the L2 distance between two [vectors](/user-guide/snowflake-cortex/vector-embeddings).

L2 distance, also known as the Euclidean distance, is a measure of the distance between two vectors in a vector space. The
distance is calculated by taking the square root of the sum of the squared differences of vector elements. The distance can be
a value of zero or higher. If the distance is zero, the vectors are identical. A larger distance indicates that the vectors are farther apart.

See also:
:   [VECTOR\_INNER\_PRODUCT](/sql-reference/functions/vector_inner_product) , [VECTOR\_COSINE\_SIMILARITY](/sql-reference/functions/vector_cosine_similarity) , [VECTOR\_L1\_DISTANCE](/sql-reference/functions/vector_l1_distance) , [Vector Embeddings](/user-guide/snowflake-cortex/vector-embeddings)

## Syntax

Copy code

```
VECTOR_L2_DISTANCE( <vector>, <vector> )
```

## Arguments

`vector`
:   The [VECTOR](/sql-reference/data-types-vector) value to calculate the distance from.

`vector`
:   The VECTOR value to calculate the distance to.

## Returns

Returns the distance between the two input vectors as a [FLOAT](/sql-reference/data-types-numeric#label-data-types-for-floating-point-numbers) value.

## Usage notes

- Vector functions are optimized in a way that can reduce floating point precision. This function’s results have a margin of error up to `1e-4`.

## Examples

This example uses the VECTOR\_L2\_DISTANCE function to determine which vectors in the table
are closest to each other between columns `a` and `b`:

Copy code

```
CREATE TABLE vectors (a VECTOR(FLOAT, 3), b VECTOR(FLOAT, 3));
INSERT INTO vectors SELECT [1.1,2.2,3]::VECTOR(FLOAT,3), [1,1,1]::VECTOR(FLOAT,3);
INSERT INTO vectors SELECT [1,2.2,3]::VECTOR(FLOAT,3), [4,6,8]::VECTOR(FLOAT,3);

-- Compute the pairwise inner product between columns a and b
SELECT VECTOR_L2_DISTANCE(a, b) FROM vectors;
```

```
+------+
| 2.3  |
|------|
| 6.95 |
+------+
```
