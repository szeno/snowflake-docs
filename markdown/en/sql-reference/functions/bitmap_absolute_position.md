Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Counting Distinct Values)

# BITMAP\_ABSOLUTE\_POSITION

Computes the absolute bit position from a bucket number and a relative bit position. This is the inverse of the [BITMAP\_BUCKET\_NUMBER](/sql-reference/functions/bitmap_bucket_number) and [BITMAP\_BIT\_POSITION](/sql-reference/functions/bitmap_bit_position) functions.

See also:
:   [Using Bitmaps to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-bitmaps-for-distinct-counts)

## Syntax

Copy code

```
BITMAP_ABSOLUTE_POSITION( <bucket_number> , <relative_position> )
```

## Arguments

`bucket_number`
:   The bucket number (returned by [BITMAP\_BUCKET\_NUMBER](/sql-reference/functions/bitmap_bucket_number)).

`relative_position`
:   The relative bit position within the bucket (returned by [BITMAP\_BIT\_POSITION](/sql-reference/functions/bitmap_bit_position)).

## Returns

An INTEGER representing the original absolute position (value).

## Examples

See [Using Bitmaps to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-bitmaps-for-distinct-counts).

Copy code

```
SELECT
  $1 pos,
  BITMAP_BUCKET_NUMBER(pos) bucket,
  BITMAP_BIT_POSITION(pos) bit_pos,
  BITMAP_ABSOLUTE_POSITION(bucket, bit_pos)
FROM VALUES (1), (123), (123456), (1234567);
```

```
+---------+--------+---------+-------------------------------------------+
| POS     | BUCKET | BIT_POS | BITMAP_ABSOLUTE_POSITION(BUCKET, BIT_POS) |
+---------+--------+---------+-------------------------------------------+
| 1       | 1      | 0       | 1                                         |
| 123     | 1      | 122     | 123                                       |
| 123456  | 4      | 25151   | 123456                                    |
| 1234567 | 38     | 22150   | 1234567                                   |
+---------+--------+---------+-------------------------------------------+
```
