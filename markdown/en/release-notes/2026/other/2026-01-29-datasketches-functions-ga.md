# Jan 29, 2026: Apache DataSketches functions (*General availability*)

The following Apache Datasketches functions are now generally available and are no longer in Preview:

| Function subcategory | New function | Description |
| --- | --- | --- |
| Cardinality estimation | [DATASKETCHES\_HLL](/sql-reference/functions/datasketches_hll) | Returns an approximation of the distinct cardinality of the input (that is, `DATASKETCHES_HLL(col1)` returns an approximation of `COUNT(DISTINCT col1)`). |
| Cardinality estimation | [DATASKETCHES\_HLL\_ACCUMULATE](/sql-reference/functions/datasketches_hll_accumulate) | Returns the sketch at the end of aggregation. |
| Cardinality estimation | [DATASKETCHES\_HLL\_COMBINE](/sql-reference/functions/datasketches_hll_combine) | Combines (merges) input sketches into a single output sketch. |
| Cardinality estimation | [DATASKETCHES\_HLL\_ESTIMATE](/sql-reference/functions/datasketches_hll_estimate) | Returns the cardinality estimate for the given sketch. |

Expand

Show lessSee more
