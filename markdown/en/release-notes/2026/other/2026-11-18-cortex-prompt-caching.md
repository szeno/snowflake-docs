# Nov 18, 2026: Prompt caching for Cortex AI Functions

Prompt caching for [Snowflake Cortex AI Functions](/user-guide/snowflake-cortex/aisql) is now generally
available for [AI\_COMPLETE](/sql-reference/functions/ai_complete). Many AI workloads send the same leading
content with every request, such as a long system prompt, classification rules, a schema description, or a
set of few-shot examples, followed by a short piece of row-specific data. Without caching, that shared
content is reprocessed and billed in full on every row.

With prompt caching, Snowflake processes the shared prefix once and reuses it, so you pay a discounted cached
input rate for the repeated tokens. Discounts are up to 97.5% off the standard input rate, and long prompts
return faster. Prompt caching is automatic and requires no SQL change or manual enrollment.

For more information, see [Caching for Cortex AI Functions](/user-guide/snowflake-cortex/aisql-caching).
