Categories:
:   [Vector functions](/sql-reference/functions-vector)

# VECTOR\_INNER\_PRODUCT

Computes the inner product of two [vectors](/user-guide/snowflake-cortex/vector-embeddings).

The inner product (also known as the dot or scalar product) multiplies two vectors. The result represents the combined direction
of the two vectors. Similar vectors result in larger inner products than dissimilar ones.

See also:
:   [VECTOR\_COSINE\_SIMILARITY](/sql-reference/functions/vector_cosine_similarity) , [VECTOR\_L1\_DISTANCE](/sql-reference/functions/vector_l1_distance) , [VECTOR\_L2\_DISTANCE](/sql-reference/functions/vector_l2_distance) , [Vector Embeddings](/user-guide/snowflake-cortex/vector-embeddings)

## Syntax

Copy code

```
VECTOR_INNER_PRODUCT( <vector>, <vector> )
```

## Arguments

`vector`
:   First [VECTOR](/sql-reference/data-types-vector) value.

`vector`
:   Second VECTOR value.

## Returns

Returns a REAL that is the inner product of the two vectors given as inputs.

## Usage notes

- Vector functions are optimized in a way that can reduce floating point precision. This function’s results have a margin of error up to `1e-4`.

## Examples

This example uses the VECTOR\_INNER\_PRODUCT function to determine which vectors in the table
are closest to each other between columns `a` and `b`:

Copy code

```
CREATE TABLE vectors (a VECTOR(FLOAT, 3), b VECTOR(FLOAT, 3));
INSERT INTO vectors SELECT [1.1,2.2,3]::VECTOR(FLOAT,3), [1,1,1]::VECTOR(FLOAT,3);
INSERT INTO vectors SELECT [1,2.2,3]::VECTOR(FLOAT,3), [4,6,8]::VECTOR(FLOAT,3);

-- Compute the pairwise inner product between columns a and b
SELECT VECTOR_INNER_PRODUCT(a, b) FROM vectors;
```

```
+------+
| 6.3  |
|------|
| 41.2 |
+------+
```
