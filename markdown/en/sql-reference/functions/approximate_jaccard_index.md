Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Similarity Estimation) , [Window functions](/sql-reference/functions-window)

# APPROXIMATE\_JACCARD\_INDEX

Returns an estimation of the similarity (Jaccard index) of inputs based on their MinHash states. For more information about Jaccard indexes and the related
function [MINHASH](/sql-reference/functions/minhash), see [Estimating Similarity of Two or More Sets](/user-guide/querying-approximate-similarity).

Alias for [APPROXIMATE\_SIMILARITY](/sql-reference/functions/approximate_similarity)

## Syntax

Copy code

```
APPROXIMATE_JACCARD_INDEX( [ DISTINCT ] <expr> [ , ... ] )

APPROXIMATE_JACCARD_INDEX(*)
```

## Arguments

`expr`
:   The expression(s) should be one or more MinHash states returned by calls to
    the [MINHASH](/sql-reference/functions/minhash) function. In other words, the
    expressions must be `MinHash` state information, not the column or
    expression for which you want the approximate similarity. (The example below
    helps make this clear.)

    For more information about MinHash states, see
    [Estimating Similarity of Two or More Sets](/user-guide/querying-approximate-similarity).

## Returns

A floating point number between 0.0 and 1.0 (inclusive), where 1.0 indicates
that the sets are identical, and 0.0 indicates that the sets have no overlap.

## Usage notes

- `DISTINCT` can be included as an argument, but has no effect.
- The input MinHash states must have MinHash arrays of equal length.
- The array length of the input MinHash states is an indicator of the quality of approximation.

  The larger the value of `k` used in function [MINHASH](/sql-reference/functions/minhash), the better the approximation. However, this value has a linear impact on the computation time for estimating similarity.

## Examples

Copy code

```
USE SCHEMA snowflake_sample_data.tpch_sf1;

SELECT APPROXIMATE_JACCARD_INDEX(mh) FROM
    (
      (SELECT MINHASH(100, C5) mh FROM orders WHERE c2 <= 50000)
         UNION
      (SELECT MINHASH(100, C5) mh FROM orders WHERE C2 > 50000)
    );

+-------------------------------+
| APPROXIMATE_JACCARD_INDEX(MH) |
|-------------------------------|
|                          0.97 |
+-------------------------------+
```
