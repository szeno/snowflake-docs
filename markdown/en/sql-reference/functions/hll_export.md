Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Cardinality Estimation) ,
    [Window functions](/sql-reference/functions-window-syntax) (Cardinality Estimation)

# HLL\_EXPORT

Converts input in BINARY format to OBJECT format.

The HyperLogLog states operated on by HLL\_ACCUMULATE, HLL\_COMBINE, and HLL\_ESTIMATE are in a proprietary binary format that may change in future versions of Snowflake. For long-term storage of HyperLogLog states, and for integration
with external tools, Snowflake supports converting states from the BINARY format to an OBJECT (which can be printed and exported as JSON), and vice versa.

See also:
:   [HLL](/sql-reference/functions/hll) , [HLL\_ACCUMULATE](/sql-reference/functions/hll_accumulate) , [HLL\_ESTIMATE](/sql-reference/functions/hll_estimate) , [HLL\_IMPORT](/sql-reference/functions/hll_import)

## Syntax

**Aggregate function**

Copy code

```
HLL_EXPORT( <binary_expr> )
```

**Window function**

Copy code

```
HLL_EXPORT( <binary_expr> ) OVER ( [ PARTITION BY <expr> ] )
```

For details about the OVER clause, see [Window function syntax and usage](/sql-reference/functions-window-syntax).

## Arguments

`binary_expr`
:   An expression that evaluates to a HyperLogLog state in BINARY format.

## Usage notes

- This function can be used as an [aggregate function](/sql-reference/functions-aggregation) or
  a [window function](/sql-reference/functions-window-syntax).

## Examples

Copy code

```
SELECT HLL(o_orderdate), HLL_ESTIMATE(HLL_IMPORT(HLL_EXPORT(HLL_ACCUMULATE(o_orderdate))))
FROM orders;

------------------+-------------------------------------------------------------------+
 HLL(O_ORDERDATE) | HLL_ESTIMATE(HLL_IMPORT(HLL_EXPORT(HLL_ACCUMULATE(O_ORDERDATE)))) |
------------------+-------------------------------------------------------------------+
 2398             | 2398                                                              |
------------------+-------------------------------------------------------------------+
```
