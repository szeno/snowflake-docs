Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Similarity Estimation) , [Window function syntax and usage](/sql-reference/functions-window-syntax)

# APPROXIMATE\_SIMILARITY

Returns an estimation of the similarity (Jaccard index) of inputs based on their MinHash states. For more information about MinHash states, see [Estimating Similarity of Two or More Sets](/user-guide/querying-approximate-similarity).

Aliases:
:   [APPROXIMATE\_JACCARD\_INDEX](/sql-reference/functions/approximate_jaccard_index)

See also:
:   [MINHASH](/sql-reference/functions/minhash) , [MINHASH\_COMBINE](/sql-reference/functions/minhash_combine)

## Syntax

Copy code

```
APPROXIMATE_SIMILARITY( [ DISTINCT ] <expr> [ , ... ] )

APPROXIMATE_SIMILARITY(*)
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

SELECT APPROXIMATE_SIMILARITY(mh) FROM
    (
      (SELECT MINHASH(100, C5) mh FROM orders WHERE c2 <= 50000)
         UNION
      (SELECT MINHASH(100, C5) mh FROM orders WHERE C2 > 50000)
    );

+----------------------------+
| APPROXIMATE_SIMILARITY(MH) |
|----------------------------|
|                       0.97 |
+----------------------------+
```

Here is a more extensive example, showing the three related functions
MINHASH, MINHASH\_COMBINE and APPROXIMATE\_SIMILARITY. This
example creates 3 tables (`ta`, `tb`, and `tc`), two of which (`ta` and `tb`) are
similar, and two of which (`ta` and `tc`) are completely dissimilar.

Create and populate tables with values:

Copy code

```
CREATE TABLE ta (i INTEGER);
CREATE TABLE tb (i INTEGER);
CREATE TABLE tc (i INTEGER);

INSERT INTO ta (i) VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (10);
INSERT INTO tb (i) VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (11);
INSERT INTO tc (i) VALUES (-1), (-20), (-300), (-4000);
```

Calculate minhash info for the initial set of data:

Copy code

```
CREATE TABLE minhash_a_1 (mh) AS SELECT MINHASH(100, i) FROM ta;
CREATE TABLE minhash_b (mh) AS SELECT MINHASH(100, i) FROM tb;
CREATE TABLE minhash_c (mh) AS SELECT MINHASH(100, i) FROM tc;
```

Add more data to one of the tables:

Copy code

```
INSERT INTO ta (i) VALUES (12);
```

Demonstrate the MINHASH\_COMBINE function:

Copy code

```
CREATE TABLE minhash_a_2 (mh) AS SELECT MINHASH(100, i) FROM ta WHERE i > 10;

CREATE TABLE minhash_a (mh) AS
  SELECT MINHASH_COMBINE(mh)
    FROM (
      (SELECT mh FROM minhash_a_1)
      UNION ALL
      (SELECT mh FROM minhash_a_2)
    );
```

This query shows the approximate similarity of the two similar tables
(`ta` and `tb`):

Copy code

```
SELECT APPROXIMATE_SIMILARITY(mh)
  FROM (
    (SELECT mh FROM minhash_a)
    UNION ALL
    (SELECT mh FROM minhash_b)
  );
```

```
+-----------------------------+
| APPROXIMATE_SIMILARITY (MH) |
|-----------------------------|
|                        0.75 |
+-----------------------------+
```

This query shows the approximate similarity of the two very different tables
(`ta` and `tc`):

Copy code

```
SELECT APPROXIMATE_SIMILARITY(mh)
  FROM (
    (SELECT mh FROM minhash_a)
    UNION ALL
    (SELECT mh FROM minhash_c)
  );
```

```
+-----------------------------+
| APPROXIMATE_SIMILARITY (MH) |
|-----------------------------|
|                           0 |
+-----------------------------+
```
