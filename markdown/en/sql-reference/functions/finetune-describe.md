Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# FINETUNE (‘DESCRIBE’) (SNOWFLAKE.CORTEX)

Feature — Generally Available

Support for this feature is available to accounts in the following regions:

> - AWS US West 2 (Oregon)
> - AWS US East 1 (N. Virginia)
> - AWS Europe Central 1 (Frankfurt)
> - Azure East US 2 (Virginia)

Describes the properties of a fine-tuning job. If the job completes successfully, additional details about the job are returned, including
the final model name. Use this name when using the [COMPLETE (SNOWFLAKE.CORTEX)](/sql-reference/functions/complete-snowflake-cortex) function to make
an inference on your fine-tuned model.

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.FINETUNE(
  'DESCRIBE',
  '<finetune_job_id>'
)
```

## Parameters

`'DESCRIBE'`
:   Specifies that you want to get the properties of the provided fine-tuning job.

`finetune_job_id`
:   The ID of the fine-tuning job that was generated when you created the job.

## Output

| Column | Type | Description |
| --- | --- | --- |
| SNOWFLAKE.CORTEX.FINETUNE | [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) | An object containing the job status, progress and the tuning job ID. If the job status is `SUCCESS`, additional job information is returned.  `id`  Unique ID for the tuning job.  `status`  The status is one of the following:   - PENDING - IN\_PROGRESS - SUCCESS - ERROR - CANCELLED  `progress`  A number between zero and one that indicates the percentage of the job completed with 1.0 being 100%.  `error`  If the job has a status of `ERROR`, an object that contains the error message.  `base_model`  The name of the base model used for the fine-tuning job.  `created_on`  The timestamp of when the job was created.  `finished_on`  If the job has a status of `SUCCESS`, the timestamp of when the job finished.  `model`  If the job has a status of `SUCCESS`, the fine-tuned model name. Use this name when calling the [COMPLETE](/sql-reference/functions/complete-snowflake-cortex) function for inference.  `training_data`  The query used to retrieve the training data.  `trained_tokens`  If the job has a status of `SUCCESS`, the number of tokens used for training. This is calculated by the following formula:  Copy code  ``` trained tokens = number of input tokens  * number of epochs trained ```  `training_result`  If the job has a status of `SUCCESS`, the training result of the fine-tuning job.  `validation_data`  The query used to retrieve the validation data.  `options`  An [object](/sql-reference/data-types-semistructured#label-data-type-object) containing zero or more of options that affect the training hyperparameters. |

Expand

Show lessSee more

## Access control requirements

For access requirements, see [Access control requirements](/user-guide/snowflake-cortex/cortex-finetuning#label-cortex-finetune-privileges).

## Examples

Copy code

```
SELECT SNOWFLAKE.CORTEX.FINETUNE(
  'DESCRIBE',
  'ft_6556e15c-8f12-4d94-8cb0-87e6f2fd2299'
);
```

An example output for a successful job:

```
{
  "base_model":"mistral-7b",
  "created_on":1717004388348,
  "finished_on":1717004691577,
  "id":"ft_6556e15c-8f12-4d94-8cb0-87e6f2fd2299",
  "model":"mydb.myschema.my_tuned_model",
  "progress":1.0,
  "status":"SUCCESS",
  "training_data":"SELECT prompt, completion FROM train",
  "trained_tokens":2670734,
  "training_result":{"validation_loss":1.0138969421386719,"training_loss":0.6477728401547047},
  "validation_data":"SELECT prompt, completion FROM validation",
  "options":{"max_epochs":3}
}
```
