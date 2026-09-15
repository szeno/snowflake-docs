Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# EXTRACT\_ANSWER (SNOWFLAKE.CORTEX)

Notice

This page is provided for backward compatibility. For new use cases, start with
[AI\_EXTRACT](/sql-reference/functions/ai_extract), which is the canonical surface going forward.
This legacy function will be deprecated by the end of 2026.

Extracts an answer to a given question from a text document. The document may be a plain-English document or a string
representation of a semi-structured (JSON) data object.

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.EXTRACT_ANSWER(
    <source_document>, <question>)
```

## Arguments

`source_document`
:   A string containing the plain-text or JSON document that contains the answer to the question.

`question`
:   A string containing the question to be answered.

## Returns

A string containing an answer to the given question.

## Access control requirements

Users must use a role that has been granted the [SNOWFLAKE.CORTEX\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user).
See [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) for more information on granting this privilege.

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features).
