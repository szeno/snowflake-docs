Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Counting Distinct Values)

# BITMAP\_BIT\_POSITION

Given a numeric value, returns the relative position for the bit that represents that value in a bitmap.

See also:
:   [Using Bitmaps to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-bitmaps-for-distinct-counts)

## Syntax

Copy code

```
BITMAP_BIT_POSITION( <numeric_expr> )
```

## Arguments

`numeric_expr`
:   This expression must evaluate to a data type that can be cast to NUMBER.

## Returns

The function returns the zero-based position of the bit for that value in a bitmap.

## Examples

See [Using Bitmaps to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-bitmaps-for-distinct-counts).
