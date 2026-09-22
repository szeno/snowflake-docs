# Fine-tuning (Snowflake Cortex)

Feature — Generally Available

Support for this feature is available to accounts in the following regions:

> - AWS US West 2 (Oregon)
> - AWS US East 1 (N. Virginia)
> - AWS Europe Central 1 (Frankfurt)
> - Azure East US 2 (Virginia)

Support for inference of fine-tuned models is available to accounts in regions that support the COMPLETE function for the base model.
For details, see [Regional availability](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability).

The Snowflake Cortex Fine-tuning function offers a way to customize large language models for your specific task.
This topic describes how the feature works and how to get started with creating your own fine-tuned model.

## Overview

Cortex Fine-tuning allows users to leverage parameter-efficient fine-tuning (PEFT) to create customized
adaptors for use with pre-trained models on more specialized tasks. If you don’t want
the high cost of training a large model from scratch but need better latency and results than you’re
getting from prompt engineering or even retrieval augmented generation (RAG) methods, fine-tuning
an existing large model is an option. Fine-tuning allows you to use examples to adjust the behavior
of the model and improve the model’s knowledge of domain-specific tasks.

Cortex Fine-tuning is a fully managed service that lets you fine-tune popular LLMs using your data, all within Snowflake.

Cortex Fine-tuning features are provided as a Snowflake Cortex function, [FINETUNE](/sql-reference/functions/finetune-snowflake-cortex),
with the following arguments:

- [CREATE](/sql-reference/functions/finetune-create#label-cortex-finetuning-create): Creates a fine-tuning job with the given training data.
- [SHOW](/sql-reference/functions/finetune-show#label-cortex-finetuning-show): Lists all the fine-tuning jobs in the current account.
- [DESCRIBE](/sql-reference/functions/finetune-describe#label-cortex-finetuning-describe): Describes the progress and status of a particular fine-tuning job.
- [CANCEL](/sql-reference/functions/finetune-cancel#label-cortex-finetuning-cancel): Cancels a given fine-tuning job.

## Cost considerations

The Snowflake Cortex Fine-tuning function incurs compute cost based on the number of tokens used in training. In addition,
running the [AI\_COMPLETE](/sql-reference/functions/ai_complete) function on a fine-tuned model incurs compute costs based on the number of tokens
processed. Refer to the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) for each
cost in credits per million tokens.

A token is the smallest unit of text processed by the Snowflake Cortex Fine-tuning function, approximately equal to four
characters of text. The equivalence of raw input or output text to tokens can vary by model.

- For the COMPLETE function, which generates new text in the response, both input and output tokens are counted.
- Fine-tuning trained tokens are calculated as follows:

  Copy code

  ```
  Fine-tuning trained tokens = number of input tokens * number of epochs trained
  ```

  Use the [FINETUNE (‘DESCRIBE’) (SNOWFLAKE.CORTEX)](/sql-reference/functions/finetune-describe) to see the number of trained tokens for your fine-tuning job.
- In addition to tuning and inference charges, standard [storage](/user-guide/cost-understanding-data-storage) and
  [warehouse](/user-guide/cost-understanding-compute) costs apply for storing the customized adaptors and running SQL commands.

### Track credit consumption for Fine-tuning training

To view the credit and token consumption for fine-tuning training jobs, use the [CORTEX\_FINE\_TUNING\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_fine_tuning_usage_history):

Copy code

```
SELECT *
  FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_FINE_TUNING_USAGE_HISTORY;
```

## Other considerations

- Fine-tuning jobs are often long running and are not attached to a worksheet session.
- The number of rows in the training/validation dataset is limited by the base model and the number of training epochs. The following table shows the limits for 3 epochs:

  Copy code

  ```
  Effective row count limit = 1 epoch limit for base model / number of epochs trained
  ```

  | Model | 1 epoch | 3 epochs (default) |
  | --- | --- | --- |
  | `llama3.1-8b` | 150k | 50k |

  Expand

  Show lessSee more

## Access control requirements

To run a fine-tuning job, the role that creates the fine-tuning job needs the following privileges:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | DATABASE | The database that the training (and validation) data are queried from. |
| CREATE MODEL or OWNERSHIP | SCHEMA | The schema that the model is saved to. |

Expand

Show lessSee more

The following SQL is an example of granting the CREATE MODEL privilege to a role, `my_role`, on `my_schema`.

Copy code

```
GRANT CREATE MODEL ON SCHEMA my_schema TO ROLE my_role;
```

Additionally, to use the FINETUNE function,
the ACCOUNTADMIN role must grant the SNOWFLAKE.CORTEX\_USER database role to the user who will call the function.
See [LLM Functions required privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) topic for details.

To give other roles access to use the fine-tuned model, you must grant usage on the model. For details, see
[Model privileges](/user-guide/security-access-control-privileges#label-security-access-control-model-privileges).

## Models available to fine-tune

You have the following base models that you can fine-tune. Models available for fine-tuning may be added or removed in the future:

| Name | Description |
| --- | --- |
| `llama3.1-8b` | A large language model from Meta that is ideal for tasks that require low to moderate reasoning. It’s a light-weight, ultra-fast model with a context window of 24K. |

Expand

Show lessSee more

## How to fine-tune a model

The overall workflow for tuning a model is as follows:

1. [Prepare the training data](#label-cortex-finetuning-data-prep).
2. [Start the fine-tuning job with the required parameters](#label-cortex-finetuning-start-job).
3. [Monitor training job](#label-cortex-finetuning-monitor).

Once training is complete, you can use the model name provided by Cortex Fine-tuning to run inference on your model.

### Prepare the fine-tuning data

The fine-tuning data must come from a Snowflake table or view and the query result must contain columns named `prompt` and `completion`.
If your table or view does not contain columns with the required names, use a column alias in your query to name them. This query is given
as a parameter to the FINETUNE function. You will get an error if the results do not contain `prompt` and `completion` column names.

Note

All columns other than the prompt and completion columns will be ignored by the FINETUNE function. Snowflake recommends using a
query that selects only the columns you need.

The following code calls the FINETUNE function and uses the `SELECT ... AS` syntax to set two of the columns in the query result
to `prompt` and `completion`.

Copy code

```
SELECT SNOWFLAKE.CORTEX.FINETUNE(
  'CREATE',
  'my_tuned_model',
  'llama3.1-8b',
  'SELECT a AS prompt, d AS completion FROM train',
  'SELECT a AS prompt, d AS completion FROM validation'
);
```

Note

To get responses that follow a schema you define, use structured outputs to generate fine-tuning data.
For more information about structured outputs, see [AI\_COMPLETE (Structured outputs)](/sql-reference/functions/ai_complete-structured-outputs).

A prompt is an input to the LLM and completion is the response from the LLM. Your training data should include prompt and completion pairs
that show how you want the model to respond to particular prompts.

The following are additional recommendations and requirements regarding your training data for getting
optimal performance from fine-tuning.

- Start with a few hundred examples. Starting with too many examples may increase tuning time drastically with
  minimal improvement in performance.
- For each example, you must use only a portion of the allotted context window for the base model you are tuning. Context window is
  defined in terms of tokens. A token is the smallest unit of text processed by Snowflake Cortex functions, approximately equal to
  four characters of text. Prompt and completion pairs that exceed this limit will be truncated, which may negatively impact
  the quality of the trained model.
- The portion of the context window allotted for `prompt` and `completion` for each base model is defined in the following table:

  > | Model | Context Window | Input Context (prompt) | Output Context (completion) |
  > | --- | --- | --- | --- |
  > | llama3.1-8b | 24k | 20k | 4k |
  >
  > Expand
  >
  > Show lessSee more

### Start the fine-tuning job

You can start a fine-tuning job by
calling the [SNOWFLAKE.CORTEX.FINETUNE function and passing in ‘CREATE’ as the first argument](/sql-reference/functions/finetune-create#label-cortex-finetuning-create)
or using Snowsight.

#### Use SQL

This example uses the `llama3.1-8b` model as the base model to create a job with a model output name of `my_tuned_model` and training
and validation data querying from the `my_training_data` and `my_validation_data` tables respectively.

Copy code

```
USE DATABASE mydb;
USE SCHEMA myschema;

SELECT SNOWFLAKE.CORTEX.FINETUNE(
  'CREATE',
  'my_tuned_model',
  'llama3.1-8b',
  'SELECT prompt, completion FROM my_training_data',
  'SELECT prompt, completion FROM my_validation_data'
);
```

You can use absolute paths for each of the database objects such as the model or data if you want to use different database and schema for each. The following example shows creating a fine-tuning job with data from `mydb2.myschema2` database and schema and saving the fine-tuned model to the `mydb.myschema` database and schema.

Copy code

```
SELECT SNOWFLAKE.CORTEX.FINETUNE(
  'CREATE',
  'mydb.myschema.my_tuned_model',
  'llama3.1-8b',
  'SELECT prompt, completion FROM mydb2.myschema2.my_training_data',
  'SELECT prompt, completion FROM mydb2.myschema2.my_validation_data'
);
```

The [SNOWFLAKE.CORTEX.FINETUNE function with ‘CREATE’ as the first argument](/sql-reference/functions/finetune-create#label-cortex-finetuning-create)
returns a fine-tuned model ID as the output. Use this ID to get status or job progress using the
[SNOWFLAKE.CORTEX.FINETUNE function with ‘DESCRIBE’ as the first argument](/sql-reference/functions/finetune-describe#label-cortex-finetuning-describe).

#### Use Snowsight

Follow these steps to create a fine-tuning job in the Snowsight:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Choose a role that is granted the SNOWFLAKE.CORTEX\_USER database role.
3. In the navigation menu, select **AI & ML** » **AI Studio**.
4. Select **Fine-tune** from the **Create Custom LLM** box.
5. Select a base model using the drop-down menu.
6. Select the role under which the fine-tuning job will execute and the warehouse where it will run. The role must be granted
   the SNOWFLAKE.CORTEX\_USER database role.
7. Select a database in which to store the fine-tuned model.
8. Enter a name for your fine-tuned model, then select **Let’s go**.
9. Select the table or view that contains your training data, then select **Next**. The training data can come from any database or
   schema that the role has access to.
10. Select the column that contains the prompts in your training data, then select **Next**.
11. Select the column that contains the completions in your training data, then select **Next**.
12. If you have a validation dataset, select the table or view that contains your validation data, then select **Next**.
    If you don’t have separate validation data, select **Skip this option**.
13. Verify your choices, then select **Start training**.

The final step confirms that your fine-tuning job has started and displays the **Job ID**. Use this ID to get status or job progress
using the [SNOWFLAKE.CORTEX.FINETUNE function with ‘DESCRIBE’ as the first argument](/sql-reference/functions/finetune-describe#label-cortex-finetuning-describe).

### Manage fine-tuned jobs

Fine-tuning jobs are long running, which means they are not tied to a worksheet session. You can check the status of your tuning job using the
[SNOWFLAKE.CORTEX.FINETUNE](/sql-reference/functions/finetune-snowflake-cortex) function with [SHOW](/sql-reference/functions/finetune-show#label-cortex-finetuning-show)
or [‘DESCRIBE’](/sql-reference/functions/finetune-describe#label-cortex-finetuning-describe) as the first argument.

If you no longer need a fine-tuning job, you can terminate the job using the [SNOWFLAKE.CORTEX.FINETUNE](/sql-reference/functions/finetune-snowflake-cortex)
function with [CANCEL](/sql-reference/functions/finetune-cancel#label-cortex-finetuning-cancel) as the first argument and the job ID as the second argument.

### Analyze fine-tuned models

After a fine-tuning job completes, you can analyze the results of the training
process by examining the fine-tuned model’s artifacts. The OWNERSHIP privilege on the model is
required to access the fine-tuned model’s artifacts; for details, see
[Model privileges](/user-guide/security-access-control-privileges#label-security-access-control-model-privileges).

The artifacts include a `training_results.csv` file. This CSV file
contains one header row followed by a row for each training step recorded by the
fine-tuning job. The file contains the following columns:

> | Column name | Description |
> | --- | --- |
> | step | Number of training steps completed in the entire training process. Starts at 1. |
> | epoch | The epoch in the training process. Starts at 1. |
> | training\_loss | The loss for the training batch. A lower number indicates a closer fit between the model and the data. |
> | validation\_loss | The loss on the validation dataset. This is only available at the last step in each epoch. |
>
> Expand
>
> Show lessSee more

The `training_results.csv` file can be found in the [Model Registry UI](/developer-guide/snowflake-ml/model-registry/snowsight-ui) in Snowsight
and accessed directly via SQL or Python API.
For more information, see
[Working with model artifacts](/developer-guide/snowflake-ml/model-registry/overview#label-snowpark-model-registry-model-artifacts).

## Use your fine-tuned model for inference

Use the [AI\_COMPLETE function](/sql-reference/functions/ai_complete) with the name of your fine-tuned model to make inferences.

This example shows a call to the [AI\_COMPLETE](/sql-reference/functions/ai_complete) function with
the name of your fine-tuned model.

Copy code

```
SELECT AI_COMPLETE(
  'my_tuned_model',
  'How to fine-tune mistral models'
);
```

The following is a snippet of the output from the example call:

> ```
> Mistral models are a type of deep learning model used for image recognition and classification. Fine-tuning a Mistral model involves adjusting the model's parameters to ...
> ```

## Limitations and known issues

- Fine-tuning jobs are listable at the account-level only.
- The fine-tuning jobs returned from [FINETUNE (‘SHOW’) (SNOWFLAKE.CORTEX)](/sql-reference/functions/finetune-show) are not permanent and may be garbage
  collected periodically.
- If a base model is removed from the Cortex LLM Functions, your fine-tuned model will no longer work.

## Sharing models

Fine-tuned models can be shared to other accounts with the USAGE privilege via [Data Sharing](/user-guide/data-sharing-intro).

## Replicating models

[Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) does not support fine-tuned models. Inference must take place in the same
region where the model object is located. You can use database replication to replicate the fine-tuned model object to a region you want
to make inference from if it’s different than the region the model was trained in.

For example,
if you create a fine-tuned model based on `llama3.1-8b` in your account in the AWS US West 2 region, you can use data sharing to share it
with another account in this region, or you can use database replication to replicate the model to another account in your organization
in a different region that supports the `llama3.1-8b` model, such as AWS Europe West. For details on replicating objects, see
[Replicating databases and account objects across multiple accounts](/user-guide/account-replication-config).

## Legal notices

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Generally available functions are Covered AI Features. Preview functions are Preview AI Features.  [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
