# Fine-tuning `arctic-extract` models

Feature — Generally Available

Support for this feature is available to accounts in the following regions:

> - AWS US West 2 (Oregon)
> - AWS US East 1 (N. Virginia)
> - AWS Europe Central 1 (Frankfurt)
> - Azure East US 2 (Virginia)

You can fine-tune `arctic-extract` models using the [Snowflake Cortex Fine-tuning](/user-guide/snowflake-cortex/cortex-finetuning)
function and [Snowflake Datasets](/developer-guide/snowflake-ml/dataset). The fine-tuned model can then be used for inference with the
[AI\_EXTRACT](/sql-reference/functions/ai_extract) function.

## Syntax

For specific syntax, usage notes, and examples, see:

- [FINETUNE (‘CREATE’) (SNOWFLAKE.CORTEX)](#label-arctic-extract-finetune-create)
- [FINETUNE (‘DESCRIBE’) (SNOWFLAKE.CORTEX)](#label-arctic-extract-finetune-describe)
- [FINETUNE (‘SHOW’) (SNOWFLAKE.CORTEX)](/sql-reference/functions/finetune-show)
- [FINETUNE (‘CANCEL’) (SNOWFLAKE.CORTEX)](/sql-reference/functions/finetune-cancel)

### FINETUNE (‘CREATE’) (SNOWFLAKE.CORTEX)

Creates a fine-tuning job.

#### Syntax

Copy code

```
SNOWFLAKE.CORTEX.FINETUNE(
  'CREATE',
  '@<database>.<schema>.<model_name>',
  'arctic-extract',
  '<training_dataset>'
  [
    , '<validation_dataset>'
    [, '<options>' ]
  ]
)
```

#### Required parameters

`'CREATE'`
:   Specifies that you want to create a fine-tuning job.

`'training_dataset'`
:   Dataset object to use for training. For more information, see [Dataset requirements](#label-arctic-extract-finetune-dataset-requirements).

#### Optional parameters

`'validation_dataset'`
:   Dataset object to use for validation. For more information, see [Dataset requirements](#label-arctic-extract-finetune-dataset-requirements).

`'options'`
:   Optional. A string representation of a JSON object that sets training hyperparameters for the job. You can specify `max_epochs` with an integer from 2 through 10 (inclusive) to control how many epochs the job runs. If you omit `options`, the number of epochs is determined automatically by the system.

    For the JSON format of the `options` argument, see [FINETUNE (‘CREATE’) (SNOWFLAKE.CORTEX)](/sql-reference/functions/finetune-create).

#### Access control requirements

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE or OWNERSHIP | DATABASE | The database that the Dataset object is stored in. |
| USAGE or OWNERSHIP | SCHEMA | The schema that the Dataset object is stored in. |
| READ or OWNERSHIP | STAGE | The internal or external named stage that stores the document files. For more information, see [Snowflake Cortex AI Functions (including LLM functions)](/user-guide/snowflake-cortex/aisql). |
| USAGE or OWNERSHIP | SCHEMA | The schema that the fine-tuned model is stored in. |
| CREATE MODEL | SCHEMA | The schema that the fine-tuned model is stored in. |

Expand

Show lessSee more

Additionally, to use the FINETUNE function, the ACCOUNTADMIN role must grant the SNOWFLAKE.CORTEX\_USER database
role to the user who will call the function. See [LLM Functions required privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges)
topic for details.

#### Example

Copy code

```
  SELECT SNOWFLAKE.CORTEX.FINETUNE(
  'CREATE',
  '@database.schema.model_name',
  'arctic-extract',
  'snow://dataset/training_ds/versions/2',
  'snow://dataset/validation_ds/versions/4'
);
```

The following example adds the `options` argument to set `max_epochs`:

Copy code

```
  SELECT SNOWFLAKE.CORTEX.FINETUNE(
  'CREATE',
  '@database.schema.model_name',
  'arctic-extract',
  'snow://dataset/training_ds/versions/2',
  'snow://dataset/validation_ds/versions/4',
  '{"max_epochs": 3}'
);
```

### FINETUNE (‘DESCRIBE’) (SNOWFLAKE.CORTEX)

Describes the properties of a fine-tuning job.

For syntax and parameters, see [FINETUNE (‘DESCRIBE’) (SNOWFLAKE.CORTEX)](/sql-reference/functions/finetune-describe).

An example output for a successful job when fine-tuning `arctic-extract` model:

```
{
  "base_model":"arctic-extract",
  "created_on":1717004388348,
  "finished_on":1717004691577,
  "id":"ft_6556e15c-8f12-4d94-8cb0-87e6f2fd2299",
  "model":"mydb.myschema.my_tuned_model",
  "progress":1.0,
  "status":"SUCCESS",
  "training_data":"snow://dataset/training_ds/versions/2",
  "trained_tokens":2670734,
  "training_result":{"validation_loss":1.0138969421386719,"training_loss":0.6477728401547047},
  "validation_data":"snow://dataset/validation_ds/versions/4",
}
```

## Dataset requirements

The [Dataset](/developer-guide/snowflake-ml/dataset) used for training and validation must contain the following columns:

File:
:   A string containing the file path to the document for extraction. The path can reference a file on an internal stage or a named external stage (for example, Amazon S3, Google Cloud Storage, or Microsoft Azure). For example: `@db.schema.stage/file.pdf`

Prompt:
:   A JSON value that specifies key and question pairs for extraction in one of the formats supported by the `responseFormat` argument of
    the [AI\_EXTRACT](/sql-reference/functions/ai_extract) function.

    For more information, see [AI\_EXTRACT](/sql-reference/functions/ai_extract).

Response:
:   A JSON object containing key and response pairs.

Note

Column names are case-insensitive and can be in any order in the Dataset; however, all required columns
(`File`, `Prompt`, and `Response`) must be present for the Dataset to be valid. Additional columns in the Dataset are ignored.

When preparing the Dataset, note the following:

- The schema of the fine-tuned model is the unique set of all questions in the Dataset.
- The answers in the `Response` column should match the questions in the `Prompt` column by matching keys in the `Prompt` and `Response` columns.
- You don’t have to specify the same set of questions for every document.
- To improve model accuracy, add a prompt and response row for each question, even if the model’s default response is correct. This action confirms that the default answer is accurate.

For more information about Datasets, see [Snowflake Datasets](/developer-guide/snowflake-ml/dataset).

### Example Dataset

| File | Prompt | Response |
| --- | --- | --- |
| `file1.pdf` | `{"date": "What is the date?", "total": "What is the total amount?"}` | `{"date": "2024-06-30", "total": "82.50"}` |
| `file2.pdf` | `[["invoice_number", "What is the invoice number?"], ["vendor", "What is the vendor name?"]]` | `{"invoice_number": "543433434", "vendor": "Example Corp"}` |
| `file3.pdf` | ``` {   "schema":   {     "type": "object",     "properties": {       "deductions": {         "description": "Deductions",         "type": "object",         "properties": {           "deductions_name": {             "type": "array"           },           "current": {             "type": "array"           }         }       }     }   } } ``` | ``` {   "deductions": {     "deductions_name": [       "Federal Tax",       "Wyoming State Tax",       "SDI",       "Soc Sec / OASDI",       "Health Insurance Tax",       "None"     ],     "current": [       "82.50",       "64.08",       "None",       "13.32",       "91.74",       "21.46"     ]   } } ``` |

Expand

Show lessSee more

Note

When you create the Dataset, set the response to `None` if the document does not contain an answer to the question.

## Usage notes

- Snowflake recommends using at least 20 documents for fine-tuning.
- In the training Dataset, at most 100 unique questions are supported for entity extraction, and at most 10 unique questions are supported for table extraction.
- Training and validation documents can reside on an internal stage or a named external stage. For access requirements and setup when you use cloud storage, see [Snowflake Cortex AI Functions (including LLM functions)](/user-guide/snowflake-cortex/aisql).
- Client-side encrypted stages are not supported. For more information, see [AI\_EXTRACT](/sql-reference/functions/ai_extract).
- Fine-tuning `arctic-extract` models is currently incompatible with custom [network policies](/user-guide/network-policies).
- Supported file formats for documents are:

  - PDF
  - PNG
  - JPG, JPEG
  - TIFF, TIF
- The maximum number of pages per document is:

  - 64 pages for AWS US West 2 (Oregon) and AWS Europe Central 1 (Frankfurt)
  - 125 pages for AWS US East 1 (N. Virginia) and Azure East US 2 (Virginia)
- The maximum number of unique document files in the Dataset is 1,000. You can reference the same document file multiple times.
- A limit exists on how many questions and documents can be in a fine-tuning job. Number of questions multiplied by total number
  of pages in all document files in the Dataset must be equal or less than 50,000.

  For example, some valid combinations are:

  | Number of questions | Number of pages | Number of document file references [[1]](#footnote-1) |
  | --- | --- | --- |
  | 10 | 1 | 5,000 |
  | 100 | 1 | 500 |
  | 10 | 10 | 500 |
  | 25 | 10 | 200 |

  Expand

  Show lessSee more

[1]
The total number of document file references (including repeats). The maximum number of unique document files in the Dataset is 1,000. However, you can reference the same file multiple times.

## Create a fine-tuning job

To create a fine-tuning job, you must create a Dataset object that contains the training data. The following example shows how to
create a Dataset object and use the Dataset to create a fine-tuning job for an `arctic-extract` model.

1. Create the table which will contain the training data:

   Copy code

   ```
   CREATE OR REPLACE TABLE my_data_table (f FILE, p VARCHAR, r VARCHAR);
   ```
2. Populate the table with the training data:

   Copy code

   ```
   INSERT INTO my_data_table (f, p, r)
   SELECT TO_FILE('@db.schema.stage', '1.pdf'), '{"net": "What is the net value?"}', '{"net": "3,762.56"}';
   ```
3. Create the Dataset object:

   Copy code

   ```
   CREATE OR REPLACE DATASET my_dataset;
   ```
4. Create a new version of the Dataset that adds the training data, using the [FL\_GET\_STAGE](/sql-reference/functions/fl_get_stage) and
   the [FL\_GET\_RELATIVE\_PATH](/sql-reference/functions/fl_get_relative_path) functions to get the file paths:

   Copy code

   ```
   ALTER DATASET my_dataset
   ADD VERSION 'v1' FROM (
     SELECT FL_GET_STAGE(f) || '/' || FL_GET_RELATIVE_PATH(f) AS "file",
       p AS "prompt",
       r AS "response"
     FROM my_data_table
   );
   ```
5. Create a fine-tuning job:

   Copy code

   ```
   SELECT SNOWFLAKE.CORTEX.FINETUNE(
     'CREATE',
     'my_tuned_model',
     'arctic-extract',
     'snow://dataset/db.schema.my_dataset/versions/v1'
   );
   ```

## Use your fine-tuned `arctic-extract` model for inference

To use the fine-tuned `arctic-extract` model for inference, ensure you have the following privileges on the model object:

- OWNERSHIP
- USAGE
- READ

To use the fine-tuned `arctic-extract` model for inference with the [AI\_EXTRACT](/sql-reference/functions/ai_extract) function,
specify the model using the `model` parameter as shown in the following example:

Copy code

```
SELECT AI_EXTRACT(
  model => 'db.schema.my_tuned_model',
  file => TO_FILE('@db.schema.files','document.pdf')
);
```

You can overwrite questions used for fine-tuning by using the `responseFormat` parameter as shown in the following example:

Copy code

```
SELECT AI_EXTRACT(
  model => 'db.schema.my_tuned_model',
  file => TO_FILE('@db.schema.files','document.pdf'),
  responseFormat => [['name', 'What is the first name of the employee?'], ['city', 'Where does the employee live?']]
);
```

For more information, see [AI\_EXTRACT](/sql-reference/functions/ai_extract).

Tip

You can copy your fine-tuned `arctic-extract` model between databases and/or schemas within an account or between accounts.
For more information, see [Copy arctic-extract models between databases, schemas, and accounts](/user-guide/snowflake-cortex/copy-arctic-extract-models).
