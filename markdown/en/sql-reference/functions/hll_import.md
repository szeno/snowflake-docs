Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Cardinality Estimation) ,
    [Window functions](/sql-reference/functions-window-syntax) (Cardinality Estimation)

# HLL\_IMPORT

Converts input in OBJECT format to BINARY format.

The HyperLogLog states operated on by HLL\_ACCUMULATE, HLL\_COMBINE, and HLL\_ESTIMATE are in a proprietary binary format that may change in future versions of Snowflake. For long-term storage of HyperLogLog states, and for integration
with external tools, Snowflake supports using HLL\_IMPORT to convert states from an OBJECT format to BINARY, and vice versa.

See also:
:   [HLL](/sql-reference/functions/hll) , [HLL\_ACCUMULATE](/sql-reference/functions/hll_accumulate) , [HLL\_ESTIMATE](/sql-reference/functions/hll_estimate) , [HLL\_EXPORT](/sql-reference/functions/hll_export)

## Syntax

**Aggregate function**

Copy code

```
HLL_IMPORT( <obj> )
```

**Window function**

Copy code

```
HLL_IMPORT( <obj> ) OVER ( [ PARTITION BY <expr> ] )
```

For details about the OVER clause, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Arguments

`obj`
:   An expression that evaluates to a HyperLogLog state in OBJECT format.

## Usage notes

- This function can be used as an [aggregate function](/sql-reference/functions-aggregation) or
  a [window function](/sql-reference/functions-window-syntax).

## Examples

See examples for [HLL\_EXPORT](/sql-reference/functions/hll_export).
