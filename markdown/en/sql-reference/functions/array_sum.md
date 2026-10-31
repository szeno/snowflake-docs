Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (General Aggregation) ,
    [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_SUM

Aggregates a column of [structured ARRAY](/sql-reference/data-types-structured) values by summing them element by
element. The value at each position in the result is the sum of the values at that position across all of the input
arrays.

Unlike [SUM](/sql-reference/functions/sum), which adds up scalar values, this function adds up arrays position by position
and returns an array. Unlike [VECTOR\_SUM](/sql-reference/functions/vector_sum), which operates on 32-bit
[VECTOR](/sql-reference/data-types-vector) values, this function operates on structured arrays of 64-bit floating-point
elements.

See also:
:   [SUM](/sql-reference/functions/sum) , [VECTOR\_SUM](/sql-reference/functions/vector_sum) , [ARRAY\_CONSTRUCT\_STRUCTURED](/sql-reference/functions/array_construct_structured)

## Syntax

Copy code

```
ARRAY_SUM( <array> )
```

## Arguments

`array`
:   A column of [structured ARRAY](/sql-reference/data-types-structured) values whose element type is floating-point:
    `ARRAY(FLOAT)`, `ARRAY(DOUBLE)`, or `ARRAY(REAL)`.

## Returns

Returns a structured `ARRAY` with the same element type as the input. Each element in the result is the sum of the
elements at the corresponding position across all of the input arrays.

The function returns `NULL` if the group contains no rows or if every value in the group is `NULL`.

## Usage notes

- All non-NULL arrays in a group must have the same length. If two arrays have different lengths, the function returns
  the following error:

  ```
  Input to ARRAY_SUM has mismatched lengths: expected <length> but got <length>
  ```
- A whole-row `NULL` is ignored, as it is with [SUM](/sql-reference/functions/sum). A row whose array value is `NULL` doesn’t
  contribute to the result.
- A `NULL` element contributes nothing to its position. If a position is `NULL` in every array in the group, the result is
  `NULL` at that position.
- The input must be a structured floating-point array. Untyped [ARRAY](/sql-reference/data-types-semistructured)
  values, and arrays with integer, `NUMBER`, or `DECFLOAT` elements, aren’t supported.
- Floating-point summation uses the same compensated accumulation as [SUM](/sql-reference/functions/sum), so results
  match scalar `SUM` over the same values. If the sum at a position exceeds the range of the element type, that position
  overflows to infinity.

## Examples

Store the values to add in an `ARRAY(DOUBLE)` column, then call `ARRAY_SUM` with that column. Use `GROUP BY` when you
want one result array for each group. For example, the following query sums the daily channel totals for each store:

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE daily_sales (
  store_id INTEGER,
  channel_sales ARRAY(DOUBLE)
);

INSERT INTO daily_sales
  SELECT 1, [12.50, 8.00, 4.25]::ARRAY(DOUBLE)
  UNION ALL SELECT 1, [10.00, 6.50, 5.75]::ARRAY(DOUBLE)
  UNION ALL SELECT 2, [7.00, 3.00, 2.00]::ARRAY(DOUBLE);

SELECT store_id, ARRAY_SUM(channel_sales) AS total_channel_sales
  FROM daily_sales
  GROUP BY store_id
  ORDER BY store_id;
```

```
+-------------------------------------+
| STORE_ID | TOTAL_CHANNEL_SALES      |
|----------+--------------------------|
| 1        | [                        |
|          |   2.250000000000000e+01, |
|          |   1.450000000000000e+01, |
|          |   1.000000000000000e+01  |
|          | ]                        |
| 2        | [                        |
|          |   7.000000000000000e+00, |
|          |   3.000000000000000e+00, |
|          |   2.000000000000000e+00  |
|          | ]                        |
+-------------------------------------+
```

A row whose array value is `NULL` is ignored:

Copy code

```
CREATE OR REPLACE TABLE array_sum_null_row (v ARRAY(DOUBLE));

INSERT INTO array_sum_null_row
  SELECT [1, 2, 3]::ARRAY(DOUBLE)
  UNION ALL SELECT NULL
  UNION ALL SELECT [4, 5, 6]::ARRAY(DOUBLE);

SELECT ARRAY_SUM(v) AS element_wise_sum FROM array_sum_null_row;
```

```
+--------------------------+
| ELEMENT_WISE_SUM         |
|--------------------------|
| [                        |
|   5.000000000000000e+00, |
|   7.000000000000000e+00, |
|   9.000000000000000e+00  |
| ]                        |
+--------------------------+
```

A `NULL` element contributes nothing to its position, while the other positions still accumulate. A position is `NULL` in
the result only when every input array has `NULL` at that position:

Copy code

```
CREATE OR REPLACE TABLE array_sum_null_element (v ARRAY(DOUBLE));

INSERT INTO array_sum_null_element
  SELECT [12.50, NULL, 4.25]::ARRAY(DOUBLE)
  UNION ALL SELECT [10.00, 6.50, NULL]::ARRAY(DOUBLE);

SELECT ARRAY_SUM(v) AS element_wise_sum FROM array_sum_null_element;
```

```
+--------------------------+
| ELEMENT_WISE_SUM         |
|--------------------------|
| [                        |
|   2.250000000000000e+01, |
|   6.500000000000000e+00, |
|   4.250000000000000e+00  |
| ]                        |
+--------------------------+
```

If the arrays in a group have different lengths, the function returns an error:

Copy code

```
CREATE OR REPLACE TABLE array_sum_mismatch (v ARRAY(DOUBLE));

INSERT INTO array_sum_mismatch
  SELECT [1, 2]::ARRAY(DOUBLE)
  UNION ALL SELECT [1, 2, 3]::ARRAY(DOUBLE);

SELECT ARRAY_SUM(v) FROM array_sum_mismatch;
```

```
Input to ARRAY_SUM has mismatched lengths: expected 2 but got 3
```
