Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# FINETUNE (‘CANCEL’) (SNOWFLAKE.CORTEX)

Feature — Generally Available

Support for this feature is available to accounts in the following regions:

> - AWS US West 2 (Oregon)
> - AWS US East 1 (N. Virginia)
> - AWS Europe Central 1 (Frankfurt)
> - Azure East US 2 (Virginia)

Cancels the specified fine-tuning job from the current schema.

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.FINETUNE(
  'CANCEL',
  '<finetune_job_id>'
)
```

## Parameters

`'CANCEL'`
:   Specifies that you want to cancel a fine-tuning job.

`finetune_job_id`
:   The ID of the fine-tuning job that was generated when you created the job.

## Output

| Column | Type | Description |
| --- | --- | --- |
| SNOWFLAKE.CORTEX.FINETUNE | [STRING](/sql-reference/data-types-text#label-character-datatypes) | Message that the job was canceled. |

Expand

Show lessSee more

## Access control requirements

For access requirements, see [Access control requirements](/user-guide/snowflake-cortex/cortex-finetuning#label-cortex-finetune-privileges).

## Examples

Copy code

```
SELECT SNOWFLAKE.CORTEX.FINETUNE(
  'CANCEL',
  'ft_194bbea4-1208-42f3-88c6-cfb202086125'
);
```

```
Canceled Cortex Fine-tuning job: ft_194bbea4-1208-42f3-88c6-cfb202086125
```
