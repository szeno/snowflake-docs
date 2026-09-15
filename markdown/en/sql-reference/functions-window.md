# Window functions

Window functions are analytic functions that you can use for various calculations such as running totals,
moving averages, and rankings.

For general syntax rules, see [Window function syntax and usage](/sql-reference/functions-window-syntax). For syntax specific to
individual functions, go to the links in the following table.

| Sub-category | Notes |
| --- | --- |
| **General window** |  |
| [ANY\_VALUE](/sql-reference/functions/any_value) |  |
| [AVG](/sql-reference/functions/avg) |  |
| [CONDITIONAL\_CHANGE\_EVENT](/sql-reference/functions/conditional_change_event) |  |
| [CONDITIONAL\_TRUE\_EVENT](/sql-reference/functions/conditional_true_event) |  |
| [CORR](/sql-reference/functions/corr) |  |
| [COUNT](/sql-reference/functions/count) |  |
| [COUNT\_IF](/sql-reference/functions/count_if) |  |
| [COVAR\_POP](/sql-reference/functions/covar_pop) |  |
| [COVAR\_SAMP](/sql-reference/functions/covar_samp) |  |
| [INTERPOLATE\_BFILL, INTERPOLATE\_FFILL, INTERPOLATE\_LINEAR](/sql-reference/functions/interpolate_bfill) |  |
| [LISTAGG](/sql-reference/functions/listagg) | Uses WITHIN GROUP syntax. |
| [MAX](/sql-reference/functions/max) |  |
| [MEDIAN](/sql-reference/functions/median) |  |
| [MIN](/sql-reference/functions/min) |  |
| [MODE](/sql-reference/functions/mode) |  |
| [PERCENTILE\_CONT](/sql-reference/functions/percentile_cont) | Uses WITHIN GROUP syntax. |
| [PERCENTILE\_DISC](/sql-reference/functions/percentile_disc) | Uses WITHIN GROUP syntax. |
| [RATIO\_TO\_REPORT](/sql-reference/functions/ratio_to_report) |  |
| [STDDEV, STDDEV\_SAMP](/sql-reference/functions/stddev) | STDDEV and STDDEV\_SAMP are aliases. |
| [STDDEV\_POP](/sql-reference/functions/stddev_pop) |  |
| [SUM](/sql-reference/functions/sum) |  |
| [VAR\_POP](/sql-reference/functions/var_pop) |  |
| [VAR\_SAMP](/sql-reference/functions/var_samp) |  |
| [VARIANCE\_POP](/sql-reference/functions/variance_pop) | Alias for [VAR\_POP](/sql-reference/functions/var_pop). |
| [VARIANCE , VARIANCE\_SAMP](/sql-reference/functions/variance) | Alias for [VAR\_SAMP](/sql-reference/functions/var_samp). |
| **Ranking** |  |
| [CUME\_DIST](/sql-reference/functions/cume_dist) |  |
| [DENSE\_RANK](/sql-reference/functions/dense_rank) |  |
| [FIRST\_VALUE](/sql-reference/functions/first_value) |  |
| [LAG](/sql-reference/functions/lag) |  |
| [LAST\_VALUE](/sql-reference/functions/last_value) |  |
| [LEAD](/sql-reference/functions/lead) |  |
| [NTH\_VALUE](/sql-reference/functions/nth_value) |  |
| [NTILE](/sql-reference/functions/ntile) |  |
| [PERCENT\_RANK](/sql-reference/functions/percent_rank) | Supports only RANGE BETWEEN window frames without explicit offsets. |
| [RANK](/sql-reference/functions/rank) |  |
| [ROW\_NUMBER](/sql-reference/functions/row_number) |  |
| **Bitwise aggregation** |  |
| [BITAND\_AGG](/sql-reference/functions/bitand_agg) |  |
| [BITOR\_AGG](/sql-reference/functions/bitor_agg) |  |
| [BITXOR\_AGG](/sql-reference/functions/bitxor_agg) |  |
| **Boolean aggregation** |  |
| [BOOLAND\_AGG](/sql-reference/functions/booland_agg) |  |
| [BOOLOR\_AGG](/sql-reference/functions/boolor_agg) |  |
| [BOOLXOR\_AGG](/sql-reference/functions/boolxor_agg) |  |
| **Hash** |  |
| [HASH\_AGG](/sql-reference/functions/hash_agg) |  |
| **Semi-structured data aggregation** |  |
| [ARRAY\_AGG](/sql-reference/functions/array_agg) |  |
| [OBJECT\_AGG](/sql-reference/functions/object_agg) |  |
| **Counting distinct values** |  |
| [ARRAY\_UNION\_AGG](/sql-reference/functions/array_union_agg) |  |
| [ARRAY\_UNIQUE\_AGG](/sql-reference/functions/array_unique_agg) |  |
| **Linear regression** |  |
| [REGR\_AVGX](/sql-reference/functions/regr_avgx) |  |
| [REGR\_AVGY](/sql-reference/functions/regr_avgy) |  |
| [REGR\_COUNT](/sql-reference/functions/regr_count) |  |
| [REGR\_INTERCEPT](/sql-reference/functions/regr_intercept) |  |
| [REGR\_R2](/sql-reference/functions/regr_r2) |  |
| [REGR\_SLOPE](/sql-reference/functions/regr_slope) |  |
| [REGR\_SXX](/sql-reference/functions/regr_sxx) |  |
| [REGR\_SXY](/sql-reference/functions/regr_sxy) |  |
| [REGR\_SYY](/sql-reference/functions/regr_syy) |  |
| **Statistics and probability** |  |
| [KURTOSIS](/sql-reference/functions/kurtosis) |  |
| **Cardinality estimation**   (**using** [HyperLogLog](/user-guide/querying-approximate-cardinality)) |  |
| [APPROX\_COUNT\_DISTINCT](/sql-reference/functions/approx_count_distinct) | Alias for [HLL](/sql-reference/functions/hll). |
| [HLL](/sql-reference/functions/hll) |  |
| [HLL\_ACCUMULATE](/sql-reference/functions/hll_accumulate) |  |
| [HLL\_COMBINE](/sql-reference/functions/hll_combine) |  |
| [HLL\_ESTIMATE](/sql-reference/functions/hll_estimate) | Not an aggregate function; uses scalar input from [HLL\_ACCUMULATE](/sql-reference/functions/hll_accumulate) or [HLL\_COMBINE](/sql-reference/functions/hll_combine). |
| [HLL\_EXPORT](/sql-reference/functions/hll_export) |  |
| [HLL\_IMPORT](/sql-reference/functions/hll_import) |  |
| **Similarity estimation**   (**using** [MinHash](/user-guide/querying-approximate-similarity)) |  |
| [APPROXIMATE\_JACCARD\_INDEX](/sql-reference/functions/approximate_jaccard_index) | Alias for [APPROXIMATE\_SIMILARITY](/sql-reference/functions/approximate_similarity). |
| [APPROXIMATE\_SIMILARITY](/sql-reference/functions/approximate_similarity) |  |
| [MINHASH](/sql-reference/functions/minhash) |  |
| [MINHASH\_COMBINE](/sql-reference/functions/minhash_combine) |  |
| **Frequency estimation**   (**using** [Space-Saving](/user-guide/querying-approximate-frequent-values)) |  |
| [APPROX\_TOP\_K](/sql-reference/functions/approx_top_k) |  |
| [APPROX\_TOP\_K\_ACCUMULATE](/sql-reference/functions/approx_top_k_accumulate) |  |
| [APPROX\_TOP\_K\_COMBINE](/sql-reference/functions/approx_top_k_combine) |  |
| [APPROX\_TOP\_K\_ESTIMATE](/sql-reference/functions/approx_top_k_estimate) | Not an aggregate function; uses scalar input from [APPROX\_TOP\_K\_ACCUMULATE](/sql-reference/functions/approx_top_k_accumulate) or [APPROX\_TOP\_K\_COMBINE](/sql-reference/functions/approx_top_k_combine). |
| **Percentile estimation**   (**using** [t-Digest](/user-guide/querying-approximate-percentile-values)) |  |
| [APPROX\_PERCENTILE](/sql-reference/functions/approx_percentile) |  |
| [APPROX\_PERCENTILE\_ACCUMULATE](/sql-reference/functions/approx_percentile_accumulate) |  |
| [APPROX\_PERCENTILE\_COMBINE](/sql-reference/functions/approx_percentile_combine) |  |
| [APPROX\_PERCENTILE\_ESTIMATE](/sql-reference/functions/approx_percentile_estimate) | Not an aggregate function; uses scalar input from [APPROX\_PERCENTILE\_ACCUMULATE](/sql-reference/functions/approx_percentile_accumulate) or [APPROX\_PERCENTILE\_COMBINE](/sql-reference/functions/approx_percentile_combine). |

Expand

Show lessSee more
