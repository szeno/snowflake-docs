Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Counting Distinct Values)

# BITMAP\_OR\_AGG

Returns a bitmap containing the results of a binary OR operation on the input bitmaps.

See also:
:   [Using Bitmaps to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-bitmaps-for-distinct-counts)

## Syntax

Copy code

```
BITMAP_OR_AGG( <bitmap> )
```

## Arguments

`bitmap`
:   A bitmap returned by the [BITMAP\_CONSTRUCT\_AGG](/sql-reference/functions/bitmap_construct_agg) or BITMAP\_OR\_AGG function.

## Returns

The function returns a bitmap containing the results of a binary OR operation on the input bitmaps.

## Examples

See [Using Bitmaps to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-bitmaps-for-distinct-counts).
