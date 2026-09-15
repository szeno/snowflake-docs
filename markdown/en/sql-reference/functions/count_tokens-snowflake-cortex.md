Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# COUNT\_TOKENS (SNOWFLAKE.CORTEX)

Notice

This page is provided for backward compatibility. For new use cases, start with
[AI\_COUNT\_TOKENS](/sql-reference/functions/ai_count_tokens), which is the canonical surface going forward.
This legacy function will be deprecated by the end of 2026.

Returns the number of tokens in a prompt for the large language model or the task-specific function specified in the argument. This
function does not support fine-tuned models.

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.COUNT_TOKENS( <model_name> , <input_text> )
```

## Arguments

**Required:**

`model_name`
:   Name of the model you want to base the token count on. See supported [models](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability).

`input_text`
:   Input text to count the tokens in.

## Returns

Returns an [INT , INTEGER , BIGINT , SMALLINT , TINYINT , BYTEINT](/sql-reference/data-types-numeric#label-data-type-integer) type that is the number of tokens in the input text based on the model or function specified.

## Usage notes

- If a function name is specified, the token count is based on the model used by the function.
- Use lowercase letters in function names.

Note

COUNT\_TOKENS does not account for the managed system prompt that is automatically added to the beginning of the input
text when using a Cortex [Cortex AI functions](/user-guide/snowflake-cortex/aisql#label-cortex-llm-ai-function). As a result, the value
returned by COUNT\_TOKENS is lower than the actual number of tokens processed by these functions.

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features).
