Categories:
:   [Aggregate functions](/sql-reference/functions-aggregation) (Percentile Estimation) , [Window function syntax and usage](/sql-reference/functions-window-syntax)

# APPROX\_PERCENTILE\_COMBINE

Combines (merges) percentile input states into a single output state.

This allows scenarios where [APPROX\_PERCENTILE\_ACCUMULATE](/sql-reference/functions/approx_percentile_accumulate) is run over horizontal partitions of the same table, producing an algorithm state for each table partition. These states can later be
combined using [APPROX\_PERCENTILE\_COMBINE](/sql-reference/functions/approx_percentile_combine), producing the same output state as a single run of [APPROX\_PERCENTILE\_ACCUMULATE](/sql-reference/functions/approx_percentile_accumulate) over the entire table.

See also:
:   [APPROX\_PERCENTILE\_ACCUMULATE](/sql-reference/functions/approx_percentile_accumulate) , [APPROX\_PERCENTILE\_ESTIMATE](/sql-reference/functions/approx_percentile_estimate)

## Syntax

Copy code

```
APPROX_PERCENTILE_COMBINE( <state> )
```

## Arguments

`state`
:   An expression that contains state information generated
    by a call to [APPROX\_PERCENTILE\_ACCUMULATE](/sql-reference/functions/approx_percentile_accumulate).

## Usage notes

- Decimal-float ([DECFLOAT](/sql-reference/data-types-numeric#label-data-type-decfloat)) values aren’t supported.

## Example

Return an approximation for the median of numbers in the `testtable.c2`
column (0.5 means the 50th percentile):

> Copy code
>
> ```
> CREATE OR REPLACE TABLE mytesttable AS
>   SELECT APPROX_PERCENTILE_COMBINE(td) s FROM
>     (
>       (SELECT APPROX_PERCENTILE_ACCUMULATE(c2) td FROM testtable WHERE c2 <= 0)
>         UNION ALL
>       (SELECT APPROX_PERCENTILE_ACCUMULATE(c2) td FROM testtable WHERE c2 > 0 AND c2 <= 0.5)
>         UNION ALL
>       (SELECT APPROX_PERCENTILE_ACCUMULATE(C2) td FROM testtable WHERE c2 > 0.5)
>     );
>
> SELECT APPROX_PERCENTILE_ESTIMATE(s , 0.5) FROM mytesttable;
> ```

Return an approximate value for the 2nd percentile of numbers in `mytest.s1 union mytest2.s2`.

> Copy code
>
> ```
> CREATE OR REPLACE TABLE mytest AS (SELECT APPROX_PERCENTILE_ACCUMULATE(c2) s1 FROM testtable WHERE c2 < 0);
>
> CREATE OR REPLACE TABLE mytest2 AS (SELECT APPROX_PERCENTILE_ACCUMULATE(c2) s1 FROM testtable WHERE c2 >= 0);
>
> CREATE OR REPLACE TABLE combinedtable AS
>   SELECT APPROX_PERCENTILE_COMBINE(s) combinedstate FROM
>     (
>       (SELECT s1 s FROM mytest)
>         UNION ALL
>       (SELECT s1 s FROM mytest2)
>     );
>
> SELECT APPROX_PERCENTILE_ESTIMATE(combinedstate , 0.02) FROM combinedtable;
> ```

For a more extensive example, see the Examples section in
[APPROX\_PERCENTILE\_ACCUMULATE](/sql-reference/functions/approx_percentile_accumulate).
