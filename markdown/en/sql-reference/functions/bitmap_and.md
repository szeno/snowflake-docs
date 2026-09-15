Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Counting Distinct Values)

# BITMAP\_AND

Returns a bitmap that is the result of a bitwise AND operation on two input bitmaps.

See also:
:   [Using Bitmaps to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-bitmaps-for-distinct-counts)

## Syntax

Copy code

```
BITMAP_AND( <bitmap1> , <bitmap2> )
```

## Arguments

`bitmap1`
:   A bitmap returned by the [BITMAP\_CONSTRUCT\_AGG](/sql-reference/functions/bitmap_construct_agg), [BITMAP\_OR\_AGG](/sql-reference/functions/bitmap_or_agg), or other bitmap functions.

`bitmap2`
:   A bitmap returned by the [BITMAP\_CONSTRUCT\_AGG](/sql-reference/functions/bitmap_construct_agg), [BITMAP\_OR\_AGG](/sql-reference/functions/bitmap_or_agg), or other bitmap functions.

## Returns

A BINARY value representing a bitmap with only the bits set that are present in both input bitmaps.

## Examples

See [Using Bitmaps to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-bitmaps-for-distinct-counts).

Copy code

```
CREATE OR REPLACE TABLE events (user_id INT, value INT);
INSERT INTO events VALUES
  (1, 1), (1, 5), (1, 100),
  (2, 5), (2, 100), (2, 50000),
  (3, 1), (3, 2), (3, 3), (3, 5);

CREATE OR REPLACE TABLE user_bitmaps AS
  SELECT
    user_id,
    BITMAP_BUCKET_NUMBER(value) AS bucket,
    BITMAP_CONSTRUCT_AGG(BITMAP_BIT_POSITION(value)) AS bmp
  FROM events
  GROUP BY user_id, bucket;

SELECT bitmap_to_array(bitmap_and(a.bmp, b.bmp), a.bucket)
FROM user_bitmaps a
JOIN user_bitmaps b ON a.bucket = b.bucket
WHERE a.user_id = 1 AND b.user_id = 3;
```

```
+------------------------------------------------------+
| BITMAP_TO_ARRAY(BITMAP_AND(A.BMP, B.BMP), A.BUCKET)  |
+------------------------------------------------------+
| [ 1, 5 ]                                             |
+------------------------------------------------------+
```
