Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# AI\_SIMILARITY

Computes a similarity score based on the vector cosine similarity value of the inputs’ embedding vectors. Currently supports both text and image similarity computation.

## Syntax

Applying AI\_SIMILARITY to string or image inputs:

Copy code

```
AI_SIMILARITY( <input1>, <input2> )
```

Specifying the config object:

Copy code

```
AI_SIMILARITY( <input1>, <input2>, <config_object> )
```

## Arguments

**Required:**

If you’re specifying input strings:

`input1`, `input2`
:   The strings with the text that you’re comparing and using to compute the similarity score.

If you’re specifying input images:

`input1`, `input2`
:   [FILE data type](/user-guide/unstructured-intro#label-unstructured-data-file-data-type) referencing the images to be compared.

Note

AI\_SIMILARITY does not support computing the similarity between text and image inputs.

**Optional:**

`config_object`
:   An [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) containing key-value pairs used to configure the model.

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `model` | [STRING](/sql-reference/data-types-text#label-character-datatypes) | For STRING input, default to *‘snowflake-arctic-embed-l-v2.0’*. For IMAGE input, default to *‘voyage-multimodal-3’* | The embedding model used for embedding. Supported values are:   - `'snowflake-arctic-embed-l-v2.0'` - `'nv-embed-qa-4'` - `'multilingual-e5-large'` - `'voyage-multilingual-2'` - `'snowflake-arctic-embed-m-v1.5'` - `'snowflake-arctic-embed-m'` - `'e5-base-v2'` - `'voyage-multimodal-3'` (IMAGE) |

Expand

Show lessSee more

## Returns

Returns a float value of range -1 to 1 that represents the similarity score computed using vector similarity between two embedding vectors for the inputs.

## Access control requirements

Users must use a role that has been granted the [SNOWFLAKE.CORTEX\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user).
See [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) for more information on this privilege.

## Examples

### AI\_SIMILARITY: Text

In this example, the function is computing a similarity score between the two statement inputs *‘I like this dish’* and *‘This dish is very good’*.

Copy code

```
SELECT AI_SIMILARITY('I like this dish', 'This dish is very good');
```

We can also compute similarity on text columns.

Copy code

```
SELECT
    review
FROM restaurant_reviews
ORDER BY AI_SIMILARITY(review, 'I love the food here!');
```

### AI\_SIMILARITY: Images

In this example, the function computes a similarity score between the two images, `cat.jpg` and `2cats.jpg`, stored in a Snowflake stage `@file_stage`.

Copy code

```
SELECT AI_SIMILARITY(TO_FILE('@file_stage', 'cat.jpg'), TO_FILE('@file_stage', '2cats.jpg'));
```

We can also compute similarity among the images using Snowflake Directory Table for the stage containing the images.

Copy code

```
SELECT
    to_file('@file_stage', relative_path)
FROM directory(@file_stage)
WHERE AI_SIMILARITY(f, to_file(@file_stage, 'cat.jpg')) >= 0.5;
```

## Limitations

- Snowflake AI functions don’t work on FILEs created from stage files from the following stage types:
  - Internal stages with encryption mode `TYPE = 'SNOWFLAKE_FULL'`
  - External stages with any customer-side encrypted mode:

    - `TYPE = 'AWS_CSE'`
    - `TYPE = 'AZURE_CSE'`
  - User stage, table stage
  - Stage with double-quoted names

## Billing

*AI\_SIMILARITY* is currently billed under the *AI\_EMBED* line item in SNOWFLAKE.ACCOUNT\_USAGE.CORTEX\_FUNCTIONS\_USAGE\_HISTORY view.

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features) for legal notices.
