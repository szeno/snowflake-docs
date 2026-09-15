Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Cardinality Estimation) , [Window functions](/sql-reference/functions-window)

# DATASKETCHES\_HLL

Returns an approximation of the distinct cardinality of the input (that is, `DATASKETCHES_HLL(col1)`
returns an approximation of `COUNT(DISTINCT col1)`).

This function is a version of the [HLL](/sql-reference/functions/hll) HyperLogLog function that can read binary sketches
in the format used by Apache DataSketches. For more information, see the
[Apache DataSketches documentation](https://datasketches.apache.org/docs/HLL/HllSketches.html).

See also:
:   [DATASKETCHES\_HLL\_ACCUMULATE](/sql-reference/functions/datasketches_hll_accumulate) , [DATASKETCHES\_HLL\_COMBINE](/sql-reference/functions/datasketches_hll_combine) , [DATASKETCHES\_HLL\_ESTIMATE](/sql-reference/functions/datasketches_hll_estimate)

## Syntax

**Aggregate function**

Copy code

```
DATASKETCHES_HLL( [ DISTINCT ] <expr1> [ , <max_log_k> ] )
```

**Window function**

Copy code

```
DATASKETCHES_HLL( [ DISTINCT ] <expr1> [ , <max_log_k> ] )
  OVER ( [ PARTITION BY <expr2> ] )
```

## Required arguments

`expr1`
:   The expression for which you want to know the number of distinct values.

## Optional arguments

`max_log_k`
:   The maximum value, in log2, of K to initialize the datasketches HLL object. Specify an INTEGER value between 4 and 21, inclusive.
    For more information, see the [Apache DataSketches documentation](https://datasketches.apache.org/docs/HLL/HllSketches.html).

    Default: 12

`expr2`
:   The optional expression used to group rows into partitions.

## Returns

The function returns a value of type DOUBLE.

If the input is empty, the output is `0.0`.

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
- For information about NULL values and aggregate functions, see [Aggregate functions and NULL values](/sql-reference/functions-aggregation#label-aggregate-functions-and-null-values).
- When this function is called as a window function, it doesn’t support:

  - An ORDER BY clause within the OVER clause.
  - Explicit window frames.

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

The following examples use the data in the table.

### Return the estimated cardinality of grouped data in a column

Use the DATASKETCHES\_HLL function to approximate the distinct cardinality of the data in column `v`
grouped by the values in column `g`.

Copy code

```
SELECT g,
       DATASKETCHES_HLL(v),
       COUNT(DISTINCT v)
  FROM datasketches_demo GROUP BY g;
```

```
+---+---------------------+-------------------+
| G | DATASKETCHES_HLL(V) | COUNT(DISTINCT V) |
|---+---------------------+-------------------|
| 1 |         2.000000005 |                 2 |
| 2 |         3.000000015 |                 3 |
+---+---------------------+-------------------+
```

The output shows that for value `1` in column `g`, there are about two distinct values in column `v`
(that is, `1` and `2`). For value `2` in column `g`, there are about three distinct values in column `v`
(that is, `1`, `4`, and `5`). The `COUNT(DISTINCT v))` call returns exact number of distinct
values instead of an estimate.

If you use the [DATASKETCHES\_HLL\_ACCUMULATE](/sql-reference/functions/datasketches_hll_accumulate) function to create binary sketches from the grouped data,
the [DATASKETCHES\_HLL\_ESTIMATE](/sql-reference/functions/datasketches_hll_estimate) function returns the same results for the accumulated sketches. For an
example, see [Return the cardinality estimate for accumulated binary sketches](/sql-reference/functions/datasketches_hll_estimate#label-function-data-sketches-hll-estimate-accumulate).

### Return the estimated cardinality of all data in a column

Use the DATASKETCHES\_HLL function to approximate the distinct cardinality of all of the data in column `v`.

Copy code

```
SELECT DATASKETCHES_HLL(v),
       COUNT(DISTINCT v)
  FROM datasketches_demo;
```

```
+---------------------+-------------------+
| DATASKETCHES_HLL(V) | COUNT(DISTINCT V) |
|---------------------+-------------------|
|          4.00000003 |                 4 |
+---------------------+-------------------+
```

The output shows that there are about four distinct values in column `v` (that is, `1`, `2`, `4`, and `5`).
The `COUNT(DISTINCT v))` call returns exact number of distinct values instead of an estimate.

If you use the [DATASKETCHES\_HLL\_ACCUMULATE](/sql-reference/functions/datasketches_hll_accumulate) function to create binary sketches from the grouped data, and
then use the [DATASKETCHES\_HLL\_COMBINE](/sql-reference/functions/datasketches_hll_combine) function to combine the sketches into one unified sketch,
the [DATASKETCHES\_HLL\_ESTIMATE](/sql-reference/functions/datasketches_hll_estimate) function returns the same results for the unified sketch. For an
example, see [Return the cardinality estimate for combined binary sketches](/sql-reference/functions/datasketches_hll_estimate#label-function-data-sketches-hll-estimate-combine).
