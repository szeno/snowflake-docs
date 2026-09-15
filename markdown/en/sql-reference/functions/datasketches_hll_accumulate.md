Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Cardinality Estimation) , [Window function syntax and usage](/sql-reference/functions-window-syntax)

# DATASKETCHES\_HLL\_ACCUMULATE

Returns the sketch at the end of aggregation.

This function is a version of the [HLL](/sql-reference/functions/hll) HyperLogLog function that can read binary sketches
in the format used by Apache DataSketches. For more information, see the
[Apache DataSketches documentation](https://datasketches.apache.org/docs/HLL/HllSketches.html).

[DATASKETCHES\_HLL](/sql-reference/functions/datasketches_hll) discards its intermediate state when the final cardinality estimate is returned.
In advanced use cases, such as incremental cardinality estimation during bulk loading, you might want to keep
the intermediate state. The intermediate state can later be combined (merged) with other intermediate states,
or can be exported to external tools.

In contrast to [DATASKETCHES\_HLL](/sql-reference/functions/datasketches_hll), DATASKETCHES\_HLL\_ACCUMULATE doesn’t return a cardinality estimate.
Instead, it skips the final estimation step and returns the algorithm state itself. For more information,
see [Estimating the Number of Distinct Values](/user-guide/querying-approximate-cardinality).

See also:
:   [DATASKETCHES\_HLL\_COMBINE](/sql-reference/functions/datasketches_hll_combine) , [DATASKETCHES\_HLL\_ESTIMATE](/sql-reference/functions/datasketches_hll_estimate)

## Syntax

Copy code

```
DATASKETCHES_HLL_ACCUMULATE( [ DISTINCT ] <expr> [ , <max_log_k> ] )
```

## Required arguments

`expr`
:   The expression for which you want to estimate cardinality (number of
    distinct values). This is typically a column name, but can be a more
    general expression.

## Optional arguments

`max_log_k`
:   The maximum value, in log2, of K for this union. Specify an INTEGER value between 4 and 21, inclusive.
    For more information, see the [Apache DataSketches documentation](https://datasketches.apache.org/docs/HLL/HllSketches.html).

    Default: 12

## Returns

The function returns a BINARY value that is compatible with the Apache Datasketches library.

## Usage notes

- DISTINCT is supported syntactically, but has no effect.
- The function supports arguments that are values of the following data types:

  - [String & binary data types](/sql-reference/data-types-text) (for example, VARCHAR and BINARY).

    For example, the following function calls are supported:

    Copy code

    ```
    SELECT DATASKETCHES_HLL_ACCUMULATE(1::TEXT);
    ```

    Copy code

    ```
    SELECT DATASKETCHES_HLL_ACCUMULATE(TO_BINARY(HEX_ENCODE(1), 'HEX'));
    ```
  - [Data types for floating-point numbers](/sql-reference/data-types-numeric#label-data-types-for-floating-point-numbers) (for example, FLOAT and DOUBLE)

    The DataSketches library casts these values to DOUBLE values.
  - [Data types for fixed-point numbers](/sql-reference/data-types-numeric#label-data-types-for-fixed-point-numbers) (for example, INTEGER and NUMERIC).

    The function only supports numeric types with a scale of 0. However, you can cast numeric values with a scale
    other than 0 to a data types for a floating-point number.

    The DataSketches library casts these values in the range of a 64-bit signed INTEGER to a 64-bit signed INTEGER value.

    The DataSketches library doesn’t directly cast INTEGER values exceeding the 64-bit signed INTEGER range (such as 128-bit
    integer values). However, Snowflake still supports these values by automatically converting them to DOUBLE values, which
    DataSketches supports. This behavior is identical to the behavior of the `datasketches-python` library.

  Values of other data types aren’t supported. For example, VARIANT and ARRAY values aren’t supported.

## Examples

Create a table and insert values:

Copy code

```
CREATE OR REPLACE TABLE datasketches_demo(v INT, g INT);

INSERT INTO datasketches_demo SELECT 1, 1;
INSERT INTO datasketches_demo SELECT 2, 1;
INSERT INTO datasketches_demo SELECT 2, 1;
INSERT INTO datasketches_demo SELECT 2, 1;
INSERT INTO datasketches_demo SELECT 1, 2;
INSERT INTO datasketches_demo SELECT 1, 2;
INSERT INTO datasketches_demo SELECT 4, 2;
INSERT INTO datasketches_demo SELECT 4, 2;
INSERT INTO datasketches_demo SELECT 5, 2;
```

Use the DATASKETCHES\_HLL\_ACCUMULATE function to create two binary sketches for the data in column `v`,
grouped by the values `1` and `2` in column `g`:

Copy code

```
SELECT g,
       DATASKETCHES_HLL_ACCUMULATE(v) AS accumulated_sketches
  FROM datasketches_demo
  GROUP BY g;
```

```
+---+------------------------------------------+
| G | ACCUMULATED_SKETCHES                     |
|---+------------------------------------------|
| 1 | 0201070C030802002BF2FB06862FF90D         |
| 2 | 0201070C030803002BF2FB0681BC5D067B65E608 |
+---+------------------------------------------+
```
