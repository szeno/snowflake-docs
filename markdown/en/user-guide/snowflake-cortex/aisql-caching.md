# Caching for Cortex AI Functions

## Response caching

[Snowflake Cortex AI Functions](/user-guide/snowflake-cortex/aisql) automatically caches and reuses the
results of [AI\_COMPLETE](/sql-reference/functions/ai_complete) calls to reduce cost and speed up query
execution. Snowflake stores the encrypted response of each AI\_COMPLETE call within a query. When the query
makes an identical call more than once, Snowflake can return the stored result instead of running inference
again. Cache hits are not billed, so you see lower token and credit consumption for the query.

Response caching is applied automatically and requires no configuration. Caching is best effort, and cache
hits are not guaranteed. We have active optimization efforts in place to improve caching performance.

The following apply to response caching today:

- Caching is available for AI\_COMPLETE for text only.
- Caching applies within a single query, with a 24-hour time to live (TTL). Most queries do not reach this
  time limit.
- For a call to be eligible, the row content must match a previous call in the same query exactly, including
  the model, prompt, and any model options.
- Calls are not cached when the row uses non-deterministic model settings (for example, a non-zero
  `temperature` or `top_p`), when the input is a file, or when the call returns a non-deterministic value.

No action is required to benefit from response caching. Writing set-based queries that let Snowflake process
rows together gives Snowflake the most opportunity to reuse identical results.
