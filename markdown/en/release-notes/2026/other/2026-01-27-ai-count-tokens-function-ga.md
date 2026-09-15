# Jan 27, 2026: Estimate token usage with AI\_COUNT\_TOKENS (*General availability*)

AI\_COUNT\_TOKENS, a Cortex AI helper function that helps users estimate token consumption and understand how prompt
context impacts cost, is now generally available. AI\_COUNT\_TOKENS takes into account the function, the LLM model (if
applicable), and any additional inputs that affect token count, such as categories/labels for classification tasks.

In general, token usage increases as prompts become more descriptive and complex. Minimal prompts with limited context
consume fewer tokens, while deeper context, task descriptions, and examples increase token counts. With AI\_COUNT\_TOKENS,
users can evaluate how these tradeoffs affect token usage and therefore cost while developing their AI workloads.

This capability is especially useful for establishing best practices around:

- How much context to include in prompts
- When richer prompts meaningfully improve accuracy
- When examples are worth the additional token cost
- How best to standardize prompt design across teams and workloads

The supported functions include:

- [AI\_CLASSIFY](/sql-reference/functions/ai_classify)
- [AI\_COMPLETE](/sql-reference/functions/ai_complete)
- [AI\_EMBED](/sql-reference/functions/ai_embed)
- [AI\_SENTIMENT](/sql-reference/functions/ai_sentiment)
- [AI\_SIMILARITY](/sql-reference/functions/ai_similarity)
- [AI\_TRANSLATE](/sql-reference/functions/ai_translate)

For more information, see [AI\_COUNT\_TOKENS](/sql-reference/functions/ai_count_tokens).
