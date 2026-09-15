Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Counting Distinct Values)

# BITMAP\_CONSTRUCT\_AGG

Returns a bitmap with bits set for each distinct value in a group.

See also:
:   [Using Bitmaps to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-bitmaps-for-distinct-counts)

## Syntax

Copy code

```
BITMAP_CONSTRUCT_AGG( <relative_position> )
```

## Arguments

`relative_position`
:   The relative position of a bit for a value (returned by the [BITMAP\_BIT\_POSITION](/sql-reference/functions/bitmap_bit_position) function).

## Returns

The function returns a BINARY value that is a bitmap with bits set for each distinct value in a group.

## Examples

See [Using Bitmaps to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-bitmaps-for-distinct-counts).
