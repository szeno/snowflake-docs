Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# AI\_CLASSIFY

Classifies text, images, or documents into categories that you specify.

## Region availability

The following table shows the regions where you can use the AI\_CLASSIFY function for each input type:

| Data type | AWS US West 2 (Oregon) | AWS US East 1 (N. Virginia) | AWS Europe Central 1 (Frankfurt) | AWS Europe West 1 (Ireland) | AWS AP Southeast 2 (Sydney) | AWS AP Northeast 1 (Tokyo) | Azure East US 2 (Virginia) | Azure West Europe (Netherlands) | AWS (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TEXT | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| IMAGE | ✔ | ✔ | ✔ |  |  |  |  |  | ✔ |
| DOCUMENT (Preview) |  |  |  |  |  |  |  |  | ✔ |

Expand

Show lessSee more

## Syntax

Copy code

```
AI_CLASSIFY( <input> , <list_of_categories> [, <config_object> ] [, <return_error_details> ] )
```

## Arguments

**Required:**

`input`
:   The string, image, document, or [prompt](/sql-reference/functions/prompt) object that you’re classifying.

    For text classification, the input string is case sensitive. Results may vary based on capitalization.

`list_of_categories`
:   An array of categories with at least two unique values. The number of categories is restricted only by the
    token window, but in practice, exceeding twenty categories might reduce classification accuracy.
    Categories are case sensitive.

    Categories can be simple strings or SQL objects of the same type.
    If you’re using objects, you can provide a description for one or more categories to improve classification accuracy.

    For each category, specify the following:

    - `label` (Required): The name of the category.
    - `description` (Optional): Describes the category in no more than 25 words.

    Note

    Descriptions count as input tokens, which affects the cost of the classification operation.
    For more information, see [Snowflake Cortex AI functions incur compute cost based on the number of tokens…](/user-guide/snowflake-cortex/aisql-cost#label-cortex-llm-cost-considerations).

**Optional:**

`config_object`
:   Configuration settings specified as key/value pairs. Supported keys:

    - `task_description`: An explanation of the classification task that is 50 words or fewer. This can help the model understand the context of the classification task and improve accuracy.
    - `output_mode`: Set to `'multi'` for multi-label classification. Defaults to `'single'` for single-label classification.
    - `examples`: A list of example objects for few-shot learning. Each example must include:
      - `input`: Example text to classify.
      - `labels`: List of correct categories for the input.
      - `explanation`: Explanation of why the input maps to those categories.
    - When the `input` is a document, `output_mode` must be `'single'` and `examples` is not supported.

`return_error_details`
:   A BOOLEAN flag that indicates whether to return error details in case of error. When set to TRUE, the function returns
    an OBJECT that contains the value and the error message, one of which is NULL depending on whether the function
    succeeded or failed. See [Error behavior](#error-behavior) for details.

## Returns

A serialized object. The object’s `labels` field is an array that specifies the list of categories to which the input belongs.

For single label classification, the `labels` array has exactly one element. For multi-label classification, the `labels` field can have multiple elements.

## Error behavior

By default, if AI\_CLASSIFY can’t process the input, the function returns NULL. If the query processes multiple rows,
rows with errors return NULL and don’t prevent the query from completing.

The return value on error depends on the `return_error_details`
argument. The following table shows the return value based on the `return_error_details` argument:

> | `return_error_details` | Return value | Description |
> | --- | --- | --- |
> | FALSE Not passed | NULL |  |
> | TRUE | OBJECT with `value` and `error` fields | `value`: An OBJECT containing the classification result, or NULL if an error occurred. `error`: A VARCHAR value that contains the error message if an error occurred, or NULL if the function succeeded. |
>
> Expand
>
> Show lessSee more

For more information about error handling for AI functions, see [Snowflake Cortex AI Function: Multirow error handling improvements](/release-notes/bcr-bundles/2026_02/bcr-2184).

## Access control requirements

Users must use a role that has the [SNOWFLAKE.CORTEX\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user).
For more information about this privilege, see [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges).

## Usage notes

For best results, follow these guidelines:

- Use plain text in English for the `input` and `list_of_categories`.
- Avoid trying to classify non-prose such as code snippets, logs, or non-English text.
- Avoid using code or formatting that is not open source (such as proprietary languages or formats) in the text. The
  underlying language model is not trained on proprietary formats.
- Don’t use abbreviations, special characters, or jargon in the category labels.
- Use descriptive categories. Avoid using category names such as “Xa4s3” or “category 1”.
- Use mutually exclusive categories.
- Providing a clear task description can improve accuracy when the relationship between the input and categories is unclear or complex.
- Adding label descriptions can improve accuracy, especially when labels are ambiguous or require specific selection
  criteria. Write descriptions that clearly highlight what distinguishes each label from the others.
- Each label, description, and example increases the number of input tokens for every AI\_CLASSIFY call, which affects cost.
- Examples can help to improve accuracy.

Note

AI\_CLASSIFY adds a prompt to your input to generate its response. This increases the token count beyond the text that you’ve provided.

### Documents

Supported file types: `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.html`, `.csv`, `.txt`. The following limits apply:

- Maximum 100 pages per document
- Maximum 200,000 tokens per document (~80 pages for an average document)
- Maximum file size: 22 MB
- Maximum image dimensions: 2000 × 2000 px
- Maximum 100 categories per call
- English only

## Examples

The following examples use the AI\_CLASSIFY function with only the required arguments.

### AI\_CLASSIFY: Text

The following example classifies the prompt into one of two categories, travel or cooking:

Copy code

```
SELECT AI_CLASSIFY('One day I will see the world', ['travel', 'cooking']);
```

The following is the output of the preceding command.

```
'{
  "labels": ["travel"]
 }';
```

The following example uses multi-label classification:

Copy code

```
SELECT AI_CLASSIFY(
  'One day I will see the world and learn to cook my favorite dishes',
  ['travel', 'cooking', 'reading', 'driving'],
  {'output_mode': 'multi'}
);
```

The following is the output of the preceding command.

```
'{
  "labels": ["travel", "cooking"]
 }';
```

The following example passes in a task description, label descriptions, and few-shot examples:

Copy code

```
SELECT AI_CLASSIFY(
  'One day I will see the world and learn to cook my favorite dishes',
  [
    {'label': 'travel', 'description': 'content related to traveling'},
    {'label': 'cooking'},
    {'label': 'reading'},
    {'label': 'driving'}
  ],
  {
    'task_description': 'Determine topics related to the given text',
    'output_mode': 'multi',
    'examples': [
      {
        'input': 'i love traveling with a good book',
        'labels': ['travel', 'reading'],
        'explanation': 'the text mentions traveling and a good book which relates to reading'
      }
    ]
  });
```

The following is the output of the preceding command.

```
'{
  "labels": ["travel", "cooking"]
}';
```

The following example creates a `text_classification_table` that contains a column for text and a column for possible
categories for that text. The AI\_CLASSIFY function is called on each row of the table to classify the string in the text
column.

Copy code

```
CREATE OR REPLACE TEMPORARY TABLE text_classification_table AS
SELECT 'France' AS input, ['North America', 'Europe', 'Asia'] AS classes
UNION ALL
SELECT 'Singapore', ['North America', 'Europe', 'Asia']
UNION ALL
SELECT 'one day I will see the world', ['travel', 'cooking', 'dancing']
UNION ALL
SELECT 'my lobster bisque is second to none', ['travel', 'cooking', 'dancing'];

SELECT input,
    classes,
    AI_CLASSIFY(input, classes):labels AS classification
FROM text_classification_table;
```

### AI\_CLASSIFY: Images

Using single file input:

Copy code

```
WITH food_pictures AS (
  SELECT
      TO_FILE(file_url) AS img
  FROM DIRECTORY(@file_stage)
)
SELECT
*,
AI_CLASSIFY(img, ['dessert', 'drink', 'main dish', 'side dish']):labels AS classification
FROM food_pictures;
```

Using a prompt object constructed by PROMPT():

Copy code

```
  WITH food_pictures AS (
  SELECT
      TO_FILE(file_url) AS img
  FROM DIRECTORY(@file_stage)
)
SELECT
*,
AI_CLASSIFY(PROMPT('Please help me classify the food within this image {0}', img),
  ['dessert', 'drink', 'main dish', 'side dish']):labels AS classification
FROM food_pictures;
```

### AI\_CLASSIFY: Documents

Copy code

```
WITH staged_docs AS (
  SELECT TO_FILE(file_url) AS doc FROM DIRECTORY(@my_doc_stage)
)
SELECT doc, AI_CLASSIFY(doc, ['invoice', 'contract', 'lab_report']):labels AS classification
FROM staged_docs;
```

The following is the output of the preceding command.

| DOC | CLASSIFICATION |
| --- | --- |
| @my\_doc\_stage/invoice\_001.pdf | [“invoice”] |
| @my\_doc\_stage/contract\_2026.pdf | [“contract”] |
| @my\_doc\_stage/blood\_panel\_report.pdf | [“lab\_report”] |

Expand

Show lessSee more

## Limitations

- Snowflake AI functions don’t work on FILE objects created from files in the following kinds of stages:
  - Internal stages with encryption mode `TYPE = 'SNOWFLAKE_FULL'`
  - External stages with any customer-side encrypted mode:

    - `TYPE = 'AWS_CSE'`
    - `TYPE = 'AZURE_CSE'`
  - User stage
  - Table stage
  - Stage with double-quoted names

Note

AI\_CLASSIFY is the updated version of [CLASSIFY\_TEXT](/sql-reference/functions/classify_text-snowflake-cortex).
For the latest functionality, use AI\_CLASSIFY.

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features) for legal notices.
