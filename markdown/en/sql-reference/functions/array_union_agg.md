Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Counting Distinct Values) ,
    [Window functions](/sql-reference/functions-window-syntax) (Semi-structured Data Aggregation)

# ARRAY\_UNION\_AGG

Returns an [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) that contains the union of the distinct values from the input arrays in a column.
You can use this to aggregate distinct values in arrays produced by [ARRAY\_UNIQUE\_AGG](/sql-reference/functions/array_unique_agg).

See also:
:   [ARRAY\_UNIQUE\_AGG](/sql-reference/functions/array_unique_agg) , [Using Arrays to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-arrays-for-distinct-counts)

## Syntax

**Aggregate function**

Copy code

```
ARRAY_UNION_AGG( <column> )
```

**Window function**

Copy code

```
ARRAY_UNION_AGG( <column> ) OVER ( [ PARTITION BY <expr> ] )
```

For details about the OVER clause, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Arguments

`column`
:   The column containing the arrays with the distinct values (the arrays produced by [ARRAY\_UNIQUE\_AGG](/sql-reference/functions/array_unique_agg)).

## Returns

The function returns an array containing the distinct values from the arrays in `column`. The values in the array are in
no particular order, and the order is not deterministic.

Note that this function uses [multiset semantics](https://en.wikipedia.org/wiki/Multiset), which means that the maximum number
of occurrences of an individual value in a single input array determines the number of occurrences of that value in the output
array. See [Examples](#examples).

The function ignores NULL values in `column` and in the arrays in `column`. If `column` contains only
NULL values or the table containing `column` is empty, the function returns an empty array.

## Usage notes

- This function can be used as either of the following types of functions:

  - [aggregate function](/sql-reference/functions-aggregation)
  - [window function](/sql-reference/functions-window-syntax).
- When this function is called as a window function, it does not support explicit window frames.
- When you pass a [structured array](/sql-reference/data-types-structured) to the function, the function returns a structured
  array of the same type.

## Examples

### Aggregation: Union of arrays

The following example illustrates how the function returns the union of distinct values from two arrays:

Copy code

```
CREATE TABLE union_test(a array);

INSERT INTO union_test
    SELECT PARSE_JSON('[ 1, 1, 2]')
    UNION ALL
    SELECT PARSE_JSON('[ 1, 2, 3]');

SELECT ARRAY_UNION_AGG(a) FROM union_test;
+-------------------------+
| ARRAY_UNION_AGG(A)      |
+-------------------------+
| [ 1, 1, 2, 3]           |
+-------------------------+
```

The operation uses [multiset](https://en.wikipedia.org/wiki/Multiset) semantics. The value `1` appears twice in the output
because it appears twice in one of the input arrays.

See [Using Arrays to Compute Distinct Values for Hierarchical Aggregations](/user-guide/querying-arrays-for-distinct-counts).
