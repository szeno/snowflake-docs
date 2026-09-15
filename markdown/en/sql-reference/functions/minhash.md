Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Similarity Estimation) ,
    [Window functions](/sql-reference/functions-window-syntax) (Similarity Estimation)

# MINHASH

Returns a MinHash state containing an array of size `k` constructed by applying `k` number of different hash functions to the input rows and keeping the minimum of each hash function. This MinHash state can
then be input to the [APPROXIMATE\_SIMILARITY](/sql-reference/functions/approximate_similarity) function to estimate the similarity with one or more other MinHash states.

For more information about MinHash states, see [Estimating Similarity of Two or More Sets](/user-guide/querying-approximate-similarity).

See also:
:   [MINHASH\_COMBINE](/sql-reference/functions/minhash_combine)

## Syntax

**Aggregate function**

Copy code

```
MINHASH( <k> , [ DISTINCT ] expr+ )

MINHASH( <k> , * )
```

**Window function**

Copy code

```
MINHASH( <k> , [ DISTINCT ] expr+ ) OVER ( [ PARTITION BY <expr1> ] )

MINHASH( <k> , * ) OVER ( [ PARTITION BY <expr1> ] )
```

For details about the OVER clause, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Arguments

`k`
:   The number of hash functions to create. The larger the value, the better the approximation;
    however, this value has a linear impact on the computation time for estimating similarity
    using APPROXIMATE\_SIMILARITY. The suggested value is 100. The maximum value is 1024.

`expr`
:   One or more expressions (typically column names) that determine the values to hash.

`*`
:   Hash all columns in the input rows.

## Usage notes

- This function can be used as an [aggregate function](/sql-reference/functions-aggregation) or
  a [window function](/sql-reference/functions-window-syntax).
- DISTINCT can be included as an argument, but has no effect.

## Examples

Copy code

```
USE SCHEMA snowflake_sample_data.tpch_sf1;

SELECT MINHASH(5, *) FROM orders;

+----------------------+
| MINHASH(5, *)        |
|----------------------|
| {                    |
|   "state": [         |
|     78678383574307,  |
|     586952033158539, |
|     525995912623966, |
|     508991839383217, |
|     492677003405678  |
|   ],                 |
|   "type": "minhash", |
|   "version": 1       |
| }                    |
+----------------------+
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
