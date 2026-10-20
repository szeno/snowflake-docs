# Bring-your-own model for AI\_COMPLETE

Preview Feature — Open

Available to all accounts where Snowpark Container Services model inference is supported, with no additional edition restrictions.

Generates a response (completion) using a model that you deploy as a Snowpark Container Services (SPCS) model inference service, instead of a Snowflake-hosted Cortex model. The prompt can be a text string, a text string with a single [FILE object](/sql-reference/functions/to_file), or a prompt object that contains text and FILE objects. FILE objects can contain images or text documents.

To use this feature, set the `model` argument to the name of an SPCS model inference service that hosts a text generation model or a vision-language (image-text-to-text) model.

## Prerequisites

Before you can use this feature, log a text generation or vision-language model from Hugging Face using [Hugging Face pipeline](/developer-guide/snowflake-ml/model-registry/built-in-models/hugging-face), then deploy it as an SPCS model inference service using the [Snowsight UI](/developer-guide/snowflake-ml/model-registry/snowsight-ui#deploy-user-models) or the [Python API](/developer-guide/snowflake-ml/inference/real-time-inference-rest-api#deploy-a-model-for-online-inference). For more examples on creating SPCS inference services, see [Example workflows](/developer-guide/snowflake-ml/inference/real-time-inference-examples).

To process files, store them on an internal stage with server-side encryption enabled. To process all files on a stage in a single query, also enable a [directory table](/user-guide/data-load-dirtables) on the stage:

Copy code

```
CREATE OR REPLACE STAGE my_files
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
```

## Syntax

The function accepts the same arguments as [AI\_COMPLETE (Single string)](/sql-reference/functions/ai_complete-single-string), [AI\_COMPLETE (Single image)](/sql-reference/functions/ai_complete-single-file), and [AI\_COMPLETE (Prompt object)](/sql-reference/functions/ai_complete-prompt-object). The only change is that the `model` argument is the name of an SPCS service instead of the name of a Cortex model.

The function can be used with either positional or named argument syntax.

Using AI\_COMPLETE with a single string input:

Copy code

```
AI_COMPLETE(
    <model>, <prompt> [ , <model_parameters>, <response_format>, <show_details> ] )
```

Using AI\_COMPLETE with a single file input:

Copy code

```
AI_COMPLETE(
    <model>, <predicate>, <file> [ , <model_parameters> ] )
```

Using AI\_COMPLETE with a prompt object:

Copy code

```
AI_COMPLETE(
    <model>, <prompt> [ , <model_parameters>, <response_format>, <show_details> ] )
```

## Arguments

`model`
:   A string specifying the name of an SPCS model inference service that hosts a text generation or vision-language model from [Hugging Face](/developer-guide/snowflake-ml/model-registry/built-in-models/hugging-face).

    To process images, the service must host a vision-language model that accepts image input, such as a Qwen3-VL model.

`prompt`
:   A string prompt, or a prompt object created with the [PROMPT](/sql-reference/functions/prompt) function. The prompt object’s template can contain numbered placeholders (`{0}`, `{1}`, and so on) that correspond to text strings or FILE objects created with [TO\_FILE](/sql-reference/functions/to_file).

`predicate`
:   For the single file input, a string prompt. When you use named argument syntax, the argument name is `predicate`, not `prompt`.

`file`
:   For the single file input, a FILE object created with [TO\_FILE](/sql-reference/functions/to_file), or a column of type FILE.

`model_parameters`
:   An [object](/sql-reference/data-types-semistructured#label-data-type-object) containing zero or more options that affect the model’s hyperparameters, such as `temperature`, `top_p`, and `max_tokens`. For descriptions of these options, see [Arguments](/sql-reference/functions/ai_complete-single-string#arguments).

    The `guardrails` option isn’t supported.

`response_format`
:   The format that the response should follow, specified as a JSON schema or a SQL type literal. For more information, see [Arguments](/sql-reference/functions/ai_complete-single-string#arguments).

`show_details`
:   A boolean flag that indicates whether to return a serialized JSON object containing the response and information about it. For more information, see [Arguments](/sql-reference/functions/ai_complete-single-string#arguments).

## Returns

By default, returns a string containing the model’s response.

When the `response_format` argument is specified, returns an object that follows the provided format. When the `show_details` argument is set to TRUE, returns a JSON object containing the response and inference metadata. For full details on each return shape, see [Returns](/sql-reference/functions/ai_complete-single-string#returns).

## Error behavior

The function follows the same error behavior as the [AI\_COMPLETE](/sql-reference/functions/ai_complete) function. For the return values for the `return_error_details` argument, see [Error behavior](/sql-reference/functions/ai_complete#error-behavior).

Specifying the `guardrails` option in the `model_parameters` argument causes the entire query to fail with an error, regardless of the `return_error_details` setting.

## Examples

The examples in this section set a SQL variable to the name of the SPCS service:

Copy code

```
SET service_name = '<db>.<schema>.<service>';
```

To confirm that the service exists, describe it:

Copy code

```
DESC SERVICE IDENTIFIER($service_name);
```

The responses shown in these examples were generated by a Qwen3-VL-8B model. Responses vary by model and between runs.

### Single response

To generate a single response:

Copy code

```
SELECT AI_COMPLETE($service_name, 'Say hello in five words.');
```

### Responses from a table column

The following example generates a response for each row in the `prompts` table, using the `q` column as input:

Copy code

```
CREATE OR REPLACE TABLE prompts (id INT, q VARCHAR);
INSERT INTO prompts VALUES
  (1, 'Translate "good morning" to French.'),
  (2, 'What is 2+2?'),
  (3, 'Summarize: Snowflake is a cloud data platform.');

SELECT
  id,
  q,
  AI_COMPLETE($service_name, q) AS reply
FROM prompts
ORDER BY id;
```

### Controlling model parameters

The following example specifies the `model_parameters` used to provide a response:

Copy code

```
SELECT AI_COMPLETE(
  model            => $service_name,
  prompt           => 'Write a haiku about Snowflake.',
  model_parameters => {
    'temperature': 0.7,
    'top_p':       0.9,
    'max_tokens':  64
  }
) AS haiku;
```

### Using a prompt template

The following example uses a prompt object with text arguments:

Copy code

```
SELECT AI_COMPLETE(
  $service_name,
  PROMPT('Translate {0} into {1}.', 'hello world', 'French')
) AS translation;
```

### Visual question answering with a single image

The following example passes one image with a text prompt, using the single file input:

Copy code

```
SELECT AI_COMPLETE(
  $service_name,
  'Describe this image in one sentence.',
  TO_FILE('@my_files', 'landscape.jpg')
) AS description;
```

Response:

```
The image depicts a serene landscape featuring a dense forest of tall trees in the foreground, a vast expanse of
deep blue water in the middle ground, and distant mountain ranges under a clear sky in the background.
```

With named argument syntax, the prompt argument is named `predicate`:

Copy code

```
SELECT AI_COMPLETE(
  model     => $service_name,
  predicate => 'Describe this image in one sentence.',
  file      => TO_FILE('@my_files', 'cityscape.jpg')
) AS description;
```

### Entity extraction from an image

The following example extracts the objects in an image and returns the results in JSON format:

Copy code

```
SELECT AI_COMPLETE(
  $service_name,
  PROMPT('Identify the setting and list up to 5 visible objects. Respond in JSON with keys ''setting'' and ''objects'': {0}',
         TO_FILE('@my_files', 'cityscape.jpg')),
  {'max_tokens': 256}
) AS objects;
```

Response:

```
{
  "setting": "a bustling city street at night, likely Times Square in New York City",
  "objects": [
    "illuminated billboards",
    "streetlights",
    "pedestrians",
    "skyscrapers",
    "traffic lights"
  ]
}
```

### Passing multiple images

To pass more than one file in the same prompt, use multiple numbered placeholders in the prompt template:

Copy code

```
SELECT AI_COMPLETE(
  $service_name,
  PROMPT(
    'Compare these two images. List 3 key differences. Image A: {0} Image B: {1}',
    TO_FILE('@my_files', 'landscape.jpg'),
    TO_FILE('@my_files', 'cityscape.jpg')
  ),
  {'max_tokens': 256}
) AS differences;
```

### Combining text and file arguments

A prompt object can combine text strings and FILE objects:

Copy code

```
SELECT AI_COMPLETE(
  $service_name,
  PROMPT('Describe this image in {0}: {1}',
         'exactly five words',
         TO_FILE('@my_files', 'landscape.jpg')),
  {'max_tokens': 256}
) AS description;
```

Response:

```
Forest meets tranquil blue sea.
```

### Extracting information from a text document

The following example lists the statistics in a text file:

Copy code

```
SELECT AI_COMPLETE(
  $service_name,
  PROMPT('List the key statistics mentioned in this text as bullet points: {0}',
         TO_FILE('@my_files', 'sample_article.txt')),
  {'max_tokens': 256}
) AS statistics;
```

Response:

```
- 95% accuracy in tumor detection
- 30% reduction in diagnostic time
- $150 billion projected market by 2030
```

You can ask questions about CSV, JSON, and HTML files the same way:

Copy code

```
SELECT AI_COMPLETE(
  $service_name,
  PROMPT('Analyze this inventory data. Which items are low or out of stock? {0}',
         TO_FILE('@my_files', 'inventory_data.json')),
  {'max_tokens': 256}
) AS inventory_analysis;
```

### Batch processing files from a directory or table

The following example classifies every file on a stage by retrieving the file paths from the stage’s directory table. PDF files aren’t supported, so the query excludes them:

Copy code

```
SELECT
  RELATIVE_PATH,
  AI_COMPLETE(
    $service_name,
    PROMPT('What type of content is this file? Respond in 5 words or less: {0}',
           TO_FILE('@my_files', RELATIVE_PATH)),
    {'max_tokens': 32}
  ) AS classification
FROM DIRECTORY(@my_files)
WHERE NOT ENDSWITH(LOWER(RELATIVE_PATH), '.pdf')
ORDER BY RELATIVE_PATH;
```

Response:

```
+---------------------+------------------------------------------+
| RELATIVE_PATH       | CLASSIFICATION                           |
|---------------------+------------------------------------------|
| cityscape.jpg       | Urban nightlife photography.             |
| cityscape.webp      | Urban night scene photograph.            |
| inventory_data.json | Inventory report data JSON.              |
| landscape.jpg       | Natural landscape photograph.            |
| landscape.png       | Natural landscape photograph.            |
| product_page.html   | HTML product specification page.         |
| sales_data.csv      | Financial report data for products.      |
| sample_article.txt  | Educational content on AI in healthcare. |
| test_pattern.gif    | Solid color background image.            |
+---------------------+------------------------------------------+
```

If you have a table with a column of type FILE, you can pass the column in the single file input or in a prompt object:

Copy code

```
CREATE OR REPLACE TABLE my_docs AS
  SELECT RELATIVE_PATH AS path, TO_FILE('@my_files', RELATIVE_PATH) AS file_col
  FROM DIRECTORY(@my_files)
  WHERE NOT ENDSWITH(LOWER(RELATIVE_PATH), '.pdf');

SELECT
  path,
  AI_COMPLETE($service_name, 'Describe this file in one sentence.', file_col) AS description
FROM my_docs
ORDER BY path;

SELECT
  path,
  AI_COMPLETE(
    $service_name,
    PROMPT('Describe this file in one sentence: {0}', file_col),
    {'max_tokens': 256}
  ) AS description
FROM my_docs
ORDER BY path;
```

### Joining with a table

The following example builds a prompt from the columns of each row in the `customers` table:

Copy code

```
CREATE OR REPLACE TABLE customers (id INT, name VARCHAR, city VARCHAR);
INSERT INTO customers VALUES
  (1, 'Alice', 'Paris'),
  (2, 'Bob',   'Tokyo'),
  (3, 'Carol', 'Lima');

SELECT
  c.id,
  c.name,
  c.city,
  AI_COMPLETE(
    $service_name,
    'Suggest a one-line dinner recommendation for ' || c.name ||
    ' visiting ' || c.city || '.'
  ) AS suggestion
FROM customers c
ORDER BY c.id;
```

## Usage notes for processing images

- To process images, the SPCS service must host a vision-language model. A text-only model can’t interpret image content.
- Supported image formats:

  - `.jpg`
  - `.png`
  - `.gif`
  - `.webp`
- To process multiple images, specify a prompt object that contains a numbered placeholder for each image. Use the [TO\_FILE](/sql-reference/functions/to_file) function to specify the image files.
- The stage containing the images must have server-side encryption enabled. Client-side encrypted stages are not supported.
- Stage names are case-insensitive; paths are case-sensitive.

## Usage notes for processing documents

- Supported document formats:

  - `.txt`
  - `.csv`
  - `.json`
  - `.html`
- PDF files are not supported. When you process all files on a stage, exclude PDF files, as shown in [Batch processing files from a directory or table](#processing-all-files-on-a-stage).
- The stage containing the documents must have server-side encryption enabled. Client-side encrypted stages are not supported.
- Stage names are case-insensitive; paths are case-sensitive.

## Limitations

The `guardrails` option ([Cortex Guard](/sql-reference/functions/ai_complete-single-string#label-cortex-llm-complete-cortex-guard)) in the `model_parameters` argument isn’t supported. A query that specifies `guardrails` fails with an error.

## Access control requirements

The user must have the USAGE privilege on the SPCS service and on its inference function. To process staged files, the user must also have the READ privilege on the stage that contains the files.

## Legal notices

Refer to [Snowflake Cortex AI Functions (including LLM functions)](/user-guide/snowflake-cortex/aisql#legal-notices).
