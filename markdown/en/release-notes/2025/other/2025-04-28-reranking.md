# Apr 28, 2025: Disable reranker in Cortex Search queries (*General availability*)

With this release, you can now disable reranking in any Cortex Search query. The Cortex Search reranker aims to elevate
results with higher relevance to the query. However, the reranking step can noticeably increase query latency. Disabling
reranking can improve search performance without penalty if you’ve found that reranking does not improve search quality for
your use case.

For more information, see [Reranking](/user-guide/snowflake-cortex/cortex-search/cortex-search-customize-scoring#label-cortex-search-reranking).
