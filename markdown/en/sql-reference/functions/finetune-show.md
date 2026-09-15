Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# FINETUNE (‘SHOW’) (SNOWFLAKE.CORTEX)

Feature — Generally Available

Support for this feature is available to accounts in the following regions:

> - AWS US West 2 (Oregon)
> - AWS US East 1 (N. Virginia)
> - AWS Europe Central 1 (Frankfurt)
> - Azure East US 2 (Virginia)

Lists all the fine-tuning jobs in the current account.

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.FINETUNE('SHOW')
```

## Parameters

`'SHOW'`
:   Specifies that you want a list of the fine-tuning jobs in the current account.

## Output

A list of all the fine-tuning jobs in the current account.

| Column | Type | Description |
| --- | --- | --- |
| SNOWFLAKE.CORTEX.FINETUNE(‘SHOW’) | [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) | An array of objects containing the job ID and the job status.  The status is one of the following:  - PENDING - IN\_PROGRESS - SUCCESS - ERROR - CANCELLED |

Expand

Show lessSee more

## Access control requirements

For access requirements, see [Access control requirements](/user-guide/snowflake-cortex/cortex-finetuning#label-cortex-finetune-privileges).

## Usage notes

- The returned fine-tuning jobs are not permanent and may be garbage collected periodically.

## Examples

Copy code

```
SELECT SNOWFLAKE.CORTEX.FINETUNE('SHOW');
```

```
[{"id":"ft_9544250a-20a9-42b3-babe-74f0a6f88f60","status":"SUCCESS","base_model":"llama3.1-8b","created_on":1730835118114},
{"id":"ft_354cf617-2fd1-4ffa-a3f9-190633f42a25","status":"ERROR","base_model":"llama3.1-8b","created_on":1730834536632}]
```
