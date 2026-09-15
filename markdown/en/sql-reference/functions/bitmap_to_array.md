Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Counting Distinct Values)

# BITMAP\_TO\_ARRAY

Returns an ARRAY containing the positions of all bits that are set in the input bitmap.

See also:
:   [Using Bitmaps to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-bitmaps-for-distinct-counts)

## Syntax

Copy code

```
BITMAP_TO_ARRAY( <bitmap> [, <bucket_number> ] )
```

## Arguments

`bitmap`
:   A bitmap returned by the [BITMAP\_CONSTRUCT\_AGG](/sql-reference/functions/bitmap_construct_agg), [BITMAP\_OR\_AGG](/sql-reference/functions/bitmap_or_agg), or other bitmap functions.

`bucket_number`
:   Optional. The bucket number (from [BITMAP\_BUCKET\_NUMBER](/sql-reference/functions/bitmap_bucket_number)). When specified, bit positions are converted to absolute positions using the given bucket number. Defaults to 1.

## Returns

An ARRAY of INTEGER values representing the positions of set bits.

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

SELECT user_id, bucket, bitmap_to_array(bmp, bucket)
FROM user_bitmaps
ORDER BY user_id;
```

```
+---------+--------+------------------------------+
| USER_ID | BUCKET | BITMAP_TO_ARRAY(BMP, BUCKET) |
+---------+--------+------------------------------+
| 1       | 1      | [ 1, 5, 100 ]                |
| 2       | 1      | [ 5, 100 ]                   |
| 2       | 2      | [ 50000 ]                    |
| 3       | 1      | [ 1, 2, 3, 5 ]               |
+---------+--------+------------------------------+
```
