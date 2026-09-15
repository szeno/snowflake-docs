Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# CORTEX\_FINE\_TUNING\_USAGE\_HISTORY view

This Account Usage view can be used to query the training usage history of [Cortex Fine-tuning](/user-guide/snowflake-cortex/cortex-finetuning).
This view includes the number of tokens processed and the training credits consumed by Cortex Fine-tuning jobs, aggregated by the job’s base model and the hour in which the job completed. This view only contains credits consumed for
fine-tuning training but not costs for using the fine-tuned model in inference, costs for storage, or costs associated with data replication. For
inference usage, see [CORTEX\_FUNCTIONS\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_functions_usage_history). For more information, see
[Cost considerations](/user-guide/snowflake-cortex/cortex-finetuning#label-cortex-finetuning-costs).

Tip

In [Cortex Code](/user-guide/cortex-code/cortex-code), including the [CLI](/user-guide/cortex-code/cortex-code-cli), [Desktop](/user-guide/cortex-code/cortex-code-desktop), and [Snowsight](/user-guide/cortex-code/cortex-code-snowsight) interfaces, you can use the [`cost-intelligence`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-cost-intelligence) bundled skill to answer questions about the usage data in this view. Invoke the skill with `/cost-intelligence`, or describe your question in plain language and Cortex Code selects the skill automatically.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range in which the Cortex Fine-tuning job terminated. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range in which the Cortex Fine-tuning job terminated. |
| MODEL\_NAME | VARCHAR | Name of the base model. |
| TOKEN\_CREDITS | NUMBER | Number of credits billed for Cortex Fine-tuning usage based on tokens processed by training jobs that terminated during the specified time range. |
| TOKENS | NUMBER | Number of tokens billed for Cortex Fine-tuning jobs terminated during the specified time range. |

Expand

Show lessSee more

## Usage notes

- The view provides up-to-date credit usage for an account within the last 365 days (1 year).
- In some cases where a model is used but is not billed, the model column may be empty.
