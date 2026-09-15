Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# FINETUNE (SNOWFLAKE.CORTEX)

[Preview Feature](/release-notes/preview-features) — Open

Support for this feature is available to accounts in the following regions:

> - AWS US West 2 (Oregon)
> - AWS US East 1 (N. Virginia)
> - AWS Europe Central 1 (Frankfurt)
> - Azure East US 2 (Virginia)

This function lets you create and manage large language models customized for your specific task.

## Syntax

Copy code

```
FINETUNE (
  { 'CREATE' | 'SHOW' | 'DESCRIBE' | 'CANCEL' }
  ...
  )
```

The syntax varies considerably between the different commands. For specific syntax, usage notes, and examples, see:

- [FINETUNE (‘CREATE’) (SNOWFLAKE.CORTEX)](/sql-reference/functions/finetune-create)
- [FINETUNE (‘DESCRIBE’) (SNOWFLAKE.CORTEX)](/sql-reference/functions/finetune-describe)
- [FINETUNE (‘SHOW’) (SNOWFLAKE.CORTEX)](/sql-reference/functions/finetune-show)
- [FINETUNE (‘CANCEL’) (SNOWFLAKE.CORTEX)](/sql-reference/functions/finetune-cancel)

## Access control requirements

For access requirements, see [Access control requirements](/user-guide/snowflake-cortex/cortex-finetuning#label-cortex-finetune-privileges).
