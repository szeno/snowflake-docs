Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# EMBED\_TEXT\_1024 (SNOWFLAKE.CORTEX)

Notice

This page is provided for backward compatibility. For new use cases, start with
[AI\_EMBED](/sql-reference/functions/ai_embed), which is the canonical surface going forward.
This legacy function will be deprecated by the end of 2026.

Supported Regions for Feature

Available to all accounts in [selected regions](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability).

Creates a vector embedding of 1024 dimensions from text.

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.EMBED_TEXT_1024( <model>, <text> )
```

## Arguments

`model`
:   A string specifying the vector embedding model to be used to generate the embedding. This must be one of the following values.

    > - `snowflake-arctic-embed-l-v2.0`
    > - `snowflake-arctic-embed-l-v2.0-8k`
    > - `nv-embed-qa-4`
    > - `multilingual-e5-large`
    > - `voyage-multilingual-2`

    Supported models might have different [costs](/user-guide/snowflake-cortex/aisql-cost#label-cortex-llm-cost-considerations).

`text`
:   The text for which an embedding should be calculated.

## Returns

A vector embedding of type VECTOR.

## Access control requirements

You must use a role that has been granted the SNOWFLAKE.CORTEX\_USER database role *or* the SNOWFLAKE.CORTEX\_EMBED\_USER
database role to call this function. See [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) for more information on granting one of
these privileges.

You must also have the USAGE privilege on the SNOWFLAKE.CORTEX schema to call this function.

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features).
