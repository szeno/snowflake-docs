Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# PROMPT

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The PROMPT function constructs a structured OBJECT containing a template string and a list of arguments. This object is
useful for dynamically formatting messages, constructing structured prompts, or storing formatted data for further
processing, such as by Cortex AI functions.

## Syntax

Copy code

```
SELECT PROMPT('<template_string>', <expr_1> [ , <expr_2>, ... ] )
    FROM <table>;
```

## Arguments

**Required:**

`template_string`
:   A string containing numbered placeholders like `{0}` where the number is at least 0 and less than the number of expressions specified.
    The first expression is substituted for `{0}`, the second for `{1}`, and so on.

`expr_1 [ , expr_2, ... ]`
:   Expressions whose values will eventually be substituted into the template string in place of the numbered
    placeholders. These can be column names or other expressions. Values can be of any type coercible to a string (for
    example, VARCHAR, NUMBER, etc.), or FILE.

## Returns

A SQL OBJECT with the following structure:

Copy code

```
{
  'template': '<template_string>',
  'args': ARRAY(<value_1>, <value_2>, ...)
}
```

The `args` array contains the value of the expressions specified in the PROMPT function call.

## Usage notes

- PROMPT does not perform any string formatting itself. It is intended to construct an object to be consumed by Cortex AI functions.
- It is an error to use a placeholder in the template string that does not have a corresponding expression, but it is not an error
  to provide expressions that are not used in the template string.

## Examples

### Basic usage

Copy code

```
SELECT PROMPT('Hello, {0}! Today is {1}.', 'Alice', 'Monday');
```

Output:

```
{
    'template': 'Hello, {0}! Today is {1}.',
    'args': ['Alice', 'Monday']
}
```

### Use with Cortex AI\_FILTER

Copy code

```
WITH reviews AS (
    SELECT 'Wow... Loved this place.' AS review, 5 AS rating
    UNION ALL
    SELECT 'Crust is not good.', 2 AS rating
)
SELECT * FROM reviews
WHERE AI_FILTER(PROMPT('The reviewer enjoyed the restaurant: {0}, Rating: {1}', review, rating));
```

### Use with Cortex COMPLETE and a FILE column

Copy code

```
AI_COMPLETE('claude-4-sonnet',
    PROMPT('Classify the input image {0} in no more than 2 words. Respond in JSON', img_file)) AS image_classification
FROM image_table;
```

See [AI\_COMPLETE (Prompt object)](/sql-reference/functions/ai_complete-prompt-object) for more examples.
