# Estimating Frequent Values

Snowflake uses the Space-Saving algorithm, a space and time efficient way of estimating approximate frequent values in data sets.

## Overview

Snowflake provides an implementation of the Space-Saving algorithm presented in [Efficient Computation of Frequent and Top-k Elements in Data Streams](https://www.cs.ucsb.edu/research/tech-reports/2005-23) by Metwally, Agrawal and Abbadi. It is implemented through the [APPROX\_TOP\_K](/sql-reference/functions/approx_top_k) family of functions.

Additionally, the [APPROX\_TOP\_K\_COMBINE](/sql-reference/functions/approx_top_k_combine) function utilizes the [parallel Space-Saving algorithm](https://arxiv.org/abs/1401.0702) outlined by Cafaro, Pulimeno and Tempesta.

The percentage of error for the algorithm depends heavily on how skewed the data is, and the number of counters used in the algorithm. As data becomes more skewed, or more counters are used, the output
will be more accurate.

## SQL Functions

The following [Aggregate functions](/sql-reference/functions-aggregation) are provided for using Space-Saving to estimate frequent values:

- [APPROX\_TOP\_K](/sql-reference/functions/approx_top_k): Returns an approximation of frequent values in the input.
- [APPROX\_TOP\_K\_ACCUMULATE](/sql-reference/functions/approx_top_k_accumulate): Skips the final estimation step and returns the Space-Saving state at the end of an aggregation.
- [APPROX\_TOP\_K\_COMBINE](/sql-reference/functions/approx_top_k_combine): Combines (that is, merges) input states into a single output state.
- [APPROX\_TOP\_K\_ESTIMATE](/sql-reference/functions/approx_top_k_estimate): Computes a cardinality estimate of a Space-Saving state produced by APPROX\_TOP\_K\_ACCUMULATE and APPROX\_TOP\_K\_COMBINE.

## Implementation Details

Each counter in our implementation tracks an item and its frequency. Notably, our implementation does not track the epsilon values of counters, as they are only useful for giving guarantees about the
output of the algorithm, they are not used for the algorithm itself.

The maximum number of counters is set to 100 thousand. In this case, there are 100 thousand counters stored in memory, but only a fraction of these are stored in an exported state.

The maximum number of `k` is 100 thousand. This value is automatically reduced if all the values cannot fit in the output.

In most cases, the runtime of our implementation does not depend on the number of counters. Our implementation ensures the number of counters does not have a noticeable effect on the runtime of the
algorithm.

Each counter in each aggregation state uses a constant amount of memory overhead of around 100 bytes. Thus, if an aggregation uses `c` counters and there are `g` aggregation groups, the
aggregation will use `c * g * 100B` of memory, plus memory to store the values. If this memory exceeds the total memory budget, memory is spilled to disk. This is far less memory than the
exact version would use, especially when there is a large number of unique values.
