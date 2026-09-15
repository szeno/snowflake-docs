Categories:
:   [Vector functions](/sql-reference/functions-vector)

# VECTOR\_L1\_DISTANCE

Computes the L1 distance between two [vectors](/user-guide/snowflake-cortex/vector-embeddings).

L1 distance, also known as the Taxicab or Manhattan distance, is a measure of
the distance between two points in a vector space. The distance is calculated by
taking the sum of the absolute value of the differences of vector elements. The
result is a value of zero or higher. If the distance is zero, the vectors
are identical. The larger the distance, the farther apart the vectors are.

See also:
:   [VECTOR\_INNER\_PRODUCT](/sql-reference/functions/vector_inner_product) , [VECTOR\_L2\_DISTANCE](/sql-reference/functions/vector_l2_distance) , [VECTOR\_COSINE\_SIMILARITY](/sql-reference/functions/vector_cosine_similarity) , [Vector Embeddings](/user-guide/snowflake-cortex/vector-embeddings)

## Syntax

Copy code

```
VECTOR_L1_DISTANCE( <vector>, <vector> )
```

## Arguments

`vector`
:   The [VECTOR](/sql-reference/data-types-vector) value to calculate the distance from.

`vector`
:   The VECTOR value to calculate the distance to.

## Returns

Returns the L1 distance between the two input vectors as a [FLOAT](/sql-reference/data-types-numeric#label-data-types-for-floating-point-numbers) value.

## Usage notes

- Vector functions are optimized in a way that can reduce floating point precision. This function’s results have a margin of error up to `1e-4`.

## Examples

This example uses the VECTOR\_L1\_DISTANCE function to determine which vectors in
the table are closest to each other between columns `a` and `b`:

Copy code

```
CREATE TABLE vectors (a VECTOR(FLOAT, 3), b VECTOR(FLOAT, 3));
INSERT INTO vectors SELECT [1.1,2.2,3]::VECTOR(FLOAT,3), [1,1,1]::VECTOR(FLOAT,3);
INSERT INTO vectors SELECT [1,2.2,3]::VECTOR(FLOAT,3), [4,6,8]::VECTOR(FLOAT,3);

SELECT VECTOR_L1_DISTANCE(a, b) FROM vectors;
```

```
+--------------+
| 3.300000191  |
|--------------|
| 11.800000191 |
+--------------+
```
