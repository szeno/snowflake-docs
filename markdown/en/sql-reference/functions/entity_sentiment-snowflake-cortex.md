Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# ENTITY\_SENTIMENT (SNOWFLAKE.CORTEX)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Notice

This page is provided for backward compatibility. For new use cases, start with
[AI\_SENTIMENT](/sql-reference/functions/ai_sentiment), which is the canonical surface going forward.
This legacy function will be deprecated by the end of 2026.

Returns sentiment scores for English-language text, including overall sentiment and specific sentiment for specified entities.

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.ENTITY_SENTIMENT(<text> [, <entities> ])
```

## Arguments

`text`
:   A string containing the text for which sentiment scores should be calculated.

`entities`
:   An array containing up to ten entities or aspects for which sentiment scores should be calculated. Each entity is a
    string. For example, if scoring sentiment from a restaurant review, the `entities` array might be `['cost', 'quality', 'waiting time']`. Entities may be a maximum of 30 characters long.

    This argument is optional. If you do not provide it, the function will return only the overall sentiment.

## Returns

An OBJECT containing a `categories` field. `categories` is an ARRAY of category records. Each category includes these fields:

- `name`: The name of the category.
- `sentiment`: The sentiment of the category: positive, negative, neutral, mixed, or unknown, as a string.

Additionally, an `overall` category contains the overall sentiment of the text.

## Access control requirements

Users must use a role that has been granted the [SNOWFLAKE.CORTEX\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user).
See [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) for more information on this privilege.

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features).
