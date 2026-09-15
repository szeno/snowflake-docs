# Jan 22, 2026: AI\_AGG and AI\_SUMMARIZE\_AGG (*General availability*)

AI\_AGG and AI\_SUMMARIZE\_AGG, AI-powered aggregation functions that help you to analyze and summarize large volumes
of text data efficiently at scale, are now generally available.

Unlike row-by-row functions, such as AI\_COMPLETE, these functions are optimized for set-based aggregation, making them significantly more efficient for mass processing. Based on internal performance testing, AI\_AGG delivers up to twice the throughput compared to AI\_COMPLETE when aggregating large datasets.

- [AI\_AGG](/sql-reference/functions/ai_agg) reduces a column of text based on a natural language instruction, such as
  extracting common themes or issues across thousands of records.
- [AI\_SUMMARIZE\_AGG](/sql-reference/functions/ai_summarize_agg) produces an overall summary of a text column as a whole, such as
  summarizing customer feedback at the product or business level.

Suggested use cases for these AI aggregation functions include:

- Customer feedback and survey analysis: extract top themes, complaints, or praise.
- Support ticket and incident review: summarize frequent issues and outcomes.
- Topic discovery and modeling: automatically surface dominant topics or themes in text collections (e.g., product
  reviews, forum posts) using natural language prompts.
- Executive summaries: generate high-level narratives from large unstructured text sources.

Both functions support GROUP BY, enabling summarization and aggregation by product, region, time period, or customer
segment.

For more information, see [Cortex AI Functions](/user-guide/snowflake-cortex/aisql).
