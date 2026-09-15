# DROP STAGE

Removes the specified named internal or external stage from the current/specified schema. The status of the files in the stage depends on
the stage type:

- For an internal stage, all of the files in the stage are purged from Snowflake, regardless of their load status. This
  prevents the files from continuing to using storage and, consequently, accruing storage charges. However, this also means that the
  staged files cannot be recovered after a stage is dropped.
- For an external stage, only the stage itself is dropped; any data files in the referenced external location (Amazon S3, Google Cloud
  Storage, or Microsoft Azure) are not removed.

See also:
:   [CREATE STAGE](/sql-reference/sql/create-stage) , [ALTER STAGE](/sql-reference/sql/alter-stage) , [SHOW STAGES](/sql-reference/sql/show-stages) , [DESCRIBE STAGE](/sql-reference/sql/desc-stage)

## Syntax

Copy code

```
DROP STAGE [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the stage to drop. If the identifier contains spaces, special characters, or mixed-case characters, the
    entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- Dropped stages cannot be recovered; they must be recreated.
- This command cannot be used to drop the stage associated with a table or user; only named stages (internal or external) can be dropped.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

> Copy code
>
> ```
> DROP STAGE my_stage;
>
> --------------------------------+
>              status             |
> --------------------------------+
>  MY_STAGE successfully dropped. |
> --------------------------------+
> ```
