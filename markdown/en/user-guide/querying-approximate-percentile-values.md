# Estimating Percentile Values

Snowflake uses an improved version of the t-Digest algorithm, a space and time efficient way of estimating approximate percentile
values in data sets.

## Overview

Snowflake provides an improved version of an implementation of the
[t-Digest algorithm papers](https://github.com/tdunning/t-digest/tree/master/docs/t-digest-paper) by Dunning and Ertl.
It has been implemented through the
[APPROX\_PERCENTILE](/sql-reference/functions/approx_percentile) family of functions.

As documented, the algorithm has a constant relative error. Note that the algorithm has substantial empirical support, but no rigorous proof of any accuracy guarantees.

## SQL Functions

The following [Aggregate functions](/sql-reference/functions-aggregation) are provided for using t-Digest to approximate percentile values:

- [APPROX\_PERCENTILE](/sql-reference/functions/approx_percentile): Returns an approximation of the desired percentile value.
- [APPROX\_PERCENTILE\_ACCUMULATE](/sql-reference/functions/approx_percentile_accumulate): Skips the final estimation step and, instead, returns the intermediate t-Digest state at the end of an aggregation.
- [APPROX\_PERCENTILE\_COMBINE](/sql-reference/functions/approx_percentile_combine): Combines (i.e. merges) multiple input states into a single output state.
- [APPROX\_PERCENTILE\_ESTIMATE](/sql-reference/functions/approx_percentile_estimate): Computes a percentile estimate of a t-Digest state produced by APPROX\_PERCENTILE\_ACCUMULATE or APPROX\_PERCENTILE\_COMBINE.

## Implementation Details

- The estimation uses a constant amount of space regardless of the size of the input.
- The t-Digest state is independent from the percentile value. This enables calculating the t-Digest state once, and then querying the state for multiple percentile values.
