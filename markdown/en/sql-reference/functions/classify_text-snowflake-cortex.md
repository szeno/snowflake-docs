Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# CLASSIFY\_TEXT (SNOWFLAKE.CORTEX)

Supported Regions for Feature

Available to all accounts in [selected regions](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability).

Notice

This page is provided for backward compatibility. For new use cases, start with
[AI\_CLASSIFY](/sql-reference/functions/ai_classify), which is the canonical surface going forward.
This legacy function will be deprecated by the end of 2026.

Classifies free-form text into categories that you provide.

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.CLASSIFY_TEXT( <input> , <list_of_categories>, [ <options> ] )
```

## Arguments

**Required:**

`input`
:   String to classify. The input string is case sensitive. You may get different results for the same string that uses different
    capitalization.

`list_of_categories`
:   Array that represents the categories. Must contain at least two and at most 100 unique categories. Categories are case
    sensitive.

    Categories may be simple strings or SQL objects; all categories must be the same type. Using objects, you can
    provide a description and examples of each category, providing context that can help improve classification accuracy.
    It is not required to provide descriptions or examples for each category; you are free to provide a description,
    examples, both, or neither for each category.

    - `label`: The name of the category. This key is required.
    - `description`: A description of the category. Descriptions should be no longer than about 25 words (1-2 sentences) long.
      This key is optional.
    - `examples`: An array of examples that are representative of the category. Typically no more than five examples are needed,
      but there is a limit of 20 examples per category. The number of examples does not need to be the same for every category.
      This key is optional.

    Note

    Descriptions and examples count as input tokens, which increases the cost of the classification operation. Read
    more in [Snowflake Cortex AI functions incur compute cost based on the number of tokens…](/user-guide/snowflake-cortex/aisql-cost#label-cortex-llm-cost-considerations).

**Optional:**

`options`
:   An object that contains optional configuration (as key/value pairs) for the classification operation. Currently, the
    only available key is:

    - `task_description`: A string containing a short explanation of the text classification task. Task descriptions should
      be no more than about 50 words (3-4 sentences) long.

## Returns

An OBJECT value (VARIANT). The object’s `label` field is a string specifying the category to which the input prompt belongs.

## Access control requirements

Users must use a role that has been granted the [SNOWFLAKE.CORTEX\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user).
See [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) for more information on this privilege.

## Usage notes

For optimal performance, follow these guidelines:

- Use plain English text for input and categories.
- Limit the amount of text that is not plain English in the input text. For example, try to limit content such as code snippets or logs
  in the text input.
- Text shouldn’t contain code or formats that are not open source (company specific languages, proprietary formats, etc.). The function
  won’t return an error, but the results may not be what you expect.
- Don’t use abbreviations, special characters, or jargon in the category labels.
- Categories should be descriptive. For example using a category such as `Xa4s3` or `category 1` won’t produce good results.
- Categories should be mutually exclusive.
- Adding a clear task description can improve accuracy when the relationship between the input text and categories is
  ambiguous or nuanced.
- Adding label descriptions can improve accuracy in cases where the descriptions are ambiguous or when specific logic
  should be followed when selecting a particular label. When writing descriptions, focus on key aspects that distinguish
  a particular label from the others.
- Each label, description, and example counts as input tokens for each record processed by a CLASSIFY\_TEXT function call.
  Costs are incurred accordingly.
- Examples can help to improve accuracy.
