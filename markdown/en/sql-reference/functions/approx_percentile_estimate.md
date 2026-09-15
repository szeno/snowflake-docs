Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Percentile Estimation) , [Window function syntax and usage](/sql-reference/functions-window-syntax)

# APPROX\_PERCENTILE\_ESTIMATE

Returns the desired approximated percentile value for the specified t-Digest state.

A t-Digest state produced by [APPROX\_PERCENTILE\_ACCUMULATE](/sql-reference/functions/approx_percentile_accumulate) and [APPROX\_PERCENTILE\_COMBINE](/sql-reference/functions/approx_percentile_combine) can be used to compute a percentile estimate using this function.

As such, APPROX\_PERCENTILE\_ESTIMATE(APPROX\_PERCENTILE\_ACCUMULATE(…)) is equivalent to APPROX\_PERCENTILE(…).

See also:
:   [APPROX\_PERCENTILE](/sql-reference/functions/approx_percentile) , [APPROX\_PERCENTILE\_ACCUMULATE](/sql-reference/functions/approx_percentile_accumulate) , [APPROX\_PERCENTILE\_COMBINE](/sql-reference/functions/approx_percentile_combine)

## Syntax

Copy code

```
APPROX_PERCENTILE_ESTIMATE( <state> , <percentile> )
```

## Arguments

`state`
:   An expression that contains state information generated
    by a call to [APPROX\_PERCENTILE\_ACCUMULATE](/sql-reference/functions/approx_percentile_accumulate) or
    [APPROX\_PERCENTILE\_COMBINE](/sql-reference/functions/approx_percentile_combine).

`percentile`
:   A constant real value greater than or equal to `0.0` and less than `1.0`.
    This indicates the percentile from 0 to 99.999… (e.g. the value 0.65 indicates the 65th percentile).

## Usage notes

- Decimal-float ([DECFLOAT](/sql-reference/data-types-numeric#label-data-type-decfloat)) values aren’t supported.

## Example

Consider a scenario where you need to approximate multiple percentile values from a given set of numbers. This can be done by creating the state and then using APPROX\_PERCENTILE\_ESTIMATE to calculate
all the percentiles:

1. First, store the state:

   Copy code

   ```
   CREATE OR REPLACE TABLE resultstate AS (
     SELECT APPROX_PERCENTILE_ACCUMULATE(c1) AS s
    FROM testtable
     );
   ```
2. Then, query the state for multiple percentiles:

   Copy code

   ```
   SELECT APPROX_PERCENTILE_ESTIMATE(s, 0.01),
    APPROX_PERCENTILE_ESTIMATE(s, 0.15),
    APPROX_PERCENTILE_ESTIMATE(s, 0.845)
     FROM testtable;
   ```

For a more extensive example, see the Examples section in
[APPROX\_PERCENTILE\_ACCUMULATE](/sql-reference/functions/approx_percentile_accumulate).
