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

## Prompt caching

Prompt caching reduces the input-token cost and latency of
[AI\_COMPLETE](/sql-reference/functions/ai_complete) by reusing a previously processed prompt prefix, such as
a large, consistent system prompt, instead of reprocessing it on every request.

When the rows in an AI\_COMPLETE query start with the same content, such as a system prompt, shared
instructions, few-shot examples, or static context, Snowflake caches that prefix and reuses it for the
remaining rows. Caching is managed by Snowflake, is on by default for supported models, and requires no
changes to your SQL. Snowflake serves the repeated prefix from cache on cache hits. Only the shared prefix is
cached. The variable portion of each prompt is always processed fresh. Savings scale with the share of input
tokens that are a reused prefix. Workloads that reuse a long system prompt across many rows see the largest
savings.

Tip

Put static content, such as instructions, schema, and examples, at the start of the prompt, and variable
content, such as the row’s data, at the end. Any change to the leading content produces a cache miss.

### Supported models

Prompt caching is not available for every AI\_COMPLETE model. Snowflake adds support for eligible models as more of
them launch. For the models that AI\_COMPLETE supports, see [Model availability](/user-guide/snowflake-cortex/model-availability).

### Pricing

- Cached input tokens are billed at the model’s Cached Input rate, listed in Table 6(a) of the
  [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
- Uncached input tokens are billed at the standard input rate.
- Output tokens are unaffected and billed at the standard output rate.

### Cache retention

Snowflake identifies the most common prompt prefix across the rows of a query and marks it for caching.
Cached prefixes are held by the model provider for a short time, typically about five minutes, and are
matched only on an exact prefix. Each cache hit resets this window. Cache hits are not guaranteed.

### Checking cached tokens

To check for cached tokens, query
[CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_ai_functions_usage_history):

Copy code

```
SELECT
  MODEL_NAME,
  SUM(CASE WHEN m.value:key:metric::string = 'cache_read_input'
           THEN m.value:value::number END) AS cached_input_tokens,
  SUM(CASE WHEN m.value:key:metric::string = 'input'
           THEN m.value:value::number END) AS input_tokens,
  SUM(CREDITS) AS credits
FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AI_FUNCTIONS_USAGE_HISTORY,
     LATERAL FLATTEN(input => METRICS) m
WHERE START_TIME >= DATEADD('day', -7, CURRENT_TIMESTAMP())
  AND FUNCTION_NAME = 'AI_COMPLETE'
GROUP BY MODEL_NAME;
```

Cached tokens are also returned in the AI\_COMPLETE response when `show_details` is TRUE, in the
`usage.prompt_cache_tokens` field. This field is present only when the call read tokens from the cache, so it
is absent when there is no cache hit. `usage.prompt_tokens` includes cached tokens.

### Considerations

- Prompt caching applies to AI\_COMPLETE text inputs only. Multi-modal inputs and other AI Functions are not
  yet supported.
- Not all prompts are eligible. Prompts must exceed a minimum cacheable length, which varies by model.
- Cache hits are best effort and are not guaranteed. For Anthropic models, Snowflake places a cache
  breakpoint only when enough rows in a batch share the same prefix, so single-row calls and small queries
  usually do not benefit.
- For Anthropic models, warehouse size can affect the cache hit rate. Larger warehouses split a query’s rows
  into more, smaller batches, so fewer rows share a prefix in each batch. If you see fewer cached tokens than
  expected, try a smaller warehouse, weighing the caching savings against query run time.
- Caching is automatic and cannot be turned off.

### Minimum cacheable prompt length

The shared prefix must be long enough to benefit from prefix caching. Snowflake follows the minimum cacheable
length set by each model provider, and those lengths can change. Shorter prefixes are processed at the standard
input rate.
