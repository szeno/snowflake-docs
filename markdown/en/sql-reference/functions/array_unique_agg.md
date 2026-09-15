Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Counting Distinct Values) ,
    [Window functions](/sql-reference/functions-window-syntax) (Semi-structured Data Aggregation)

# ARRAY\_UNIQUE\_AGG

Returns an [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) that contains all of the distinct values from the specified column.

See also:
:   [Using Arrays to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-arrays-for-distinct-counts)

## Syntax

**Aggregate function**

Copy code

```
ARRAY_UNIQUE_AGG( <column> )
```

**Window function**

Copy code

```
ARRAY_UNIQUE_AGG( <column> ) OVER ( [ PARTITION BY <expr> ] )
```

For details about the OVER clause, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Arguments

`column`
:   The column containing the values.

## Returns

The function returns an array containing the distinct values in the specified column. The values in the array are in no particular
order, and the order is not deterministic.

The function ignores NULL values in `column`. If `column` contains only NULL values or the table containing
`column` is empty, the function returns an empty array.

## Usage notes

- This function can be used as either of the following types of functions:

  - [aggregate function](/sql-reference/functions-aggregation)
  - [window function](/sql-reference/functions-window-syntax).
- When this function is called as a window function, it does not support explicit window frames.

- This function doesn’t support a [structured type](/sql-reference/data-types-structured) as an input argument.

## Examples

### Aggregation

See [Using Arrays to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-arrays-for-distinct-counts).
