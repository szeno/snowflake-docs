# June 17, 2024 — New LLM helper functions - TRY\_COMPLETE and COUNT\_TOKENS

With this release, we are pleased to announce the availability of two Cortex LLM helper functions, TRY\_COMPLETE and COUNT\_TOKENS.
These functions are purpose-built and managed functions that help to reduce cases of query failures when the number of input tokens
exceed a model limit.

For more information, see [Snowflake Cortex AI Functions (including LLM functions)](/user-guide/snowflake-cortex/aisql).

## New SQL function

The following functions are now generally available with this release:

| Function Category | New Function | Description |
| --- | --- | --- |
| [LLM Function](/user-guide/snowflake-cortex/aisql) | [TRY\_COMPLETE (SNOWFLAKE.CORTEX)](/sql-reference/functions/try_complete-snowflake-cortex) | Tries to run the COMPLETE function but returns NULL instead of an error code if unable to run. |
| [LLM Function](/user-guide/snowflake-cortex/aisql) | [COUNT\_TOKENS (SNOWFLAKE.CORTEX)](/sql-reference/functions/count_tokens-snowflake-cortex) | Counts the tokens in a given input text based on the model or function specified. |

Expand

Show lessSee more
