Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Counting Distinct Values)

# BITMAP\_COUNT

Given a bitmap that represents the set of distinct values for a column, returns the number of distinct value.

See also:
:   [Using Bitmaps to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-bitmaps-for-distinct-counts)

## Syntax

Copy code

```
BITMAP_COUNT( <bitmap> )
```

## Arguments

`bitmap`
:   This expression must evaluate to a bitmap returned by the [BITMAP\_CONSTRUCT\_AGG](/sql-reference/functions/bitmap_construct_agg) or [BITMAP\_OR\_AGG](/sql-reference/functions/bitmap_or_agg) functions.

## Returns

The function returns the number of distinct values in a column, as represented by the bits set in the input bitmap.

## Examples

See [Using Bitmaps to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-bitmaps-for-distinct-counts).
