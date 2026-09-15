# DESCRIBE STAGE

Describes the values specified for the properties in a stage (file format, copy, and location), as well as the default values for
each property.

DESCRIBE can be abbreviated to DESC.

See also:
:   [DROP STAGE](/sql-reference/sql/drop-stage) , [ALTER STAGE](/sql-reference/sql/alter-stage) , [CREATE STAGE](/sql-reference/sql/create-stage) , [SHOW STAGES](/sql-reference/sql/show-stages)

## Syntax

Copy code

```
DESC[RIBE] STAGE <name>
```

## Parameters

`name`
:   Specifies the identifier for the stage to describe. If the identifier contains spaces or special characters, the entire string must
    be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Output

The command output provides stage properties and metadata in the following columns.

| Column | Description |
| --- | --- |
| `parent_property` | The parent property to which each stage property belongs. Possible values include STAGE\_FILE\_FORMAT, STAGE\_COPY\_OPTIONS, STAGE\_LOCATION, STAGE\_CREDENTIALS, and DIRECTORY. |
| `property` | The name of the property. For property descriptions, refer to [CREATE STAGE](/sql-reference/sql/create-stage). |
| `property_type` | The property type. |
| `property_value` | The value assigned to the property. |
| `property_default` | The default property value. |

Expand

Show lessSee more

Note

For stages with a directory table, the output includes a property named LAST\_REFRESHED\_ON of type TIMESTAMP. LAST\_REFRESHED\_ON indicates when the
metadata for the directory table was last synchronized with the associated files on the stage, either manually or automatically.

## Examples

Describe an internal stage named `my_s3_stage`:

> Copy code
>
> ```
> DESC STAGE my_s3_stage;
> +--------------------+--------------------------------+---------------+-------------------------------------------------------+------------------+
> | parent_property    | property                       | property_type | property_value                                        | property_default |
> |--------------------+--------------------------------+---------------+-------------------------------------------------------+------------------|
> | STAGE_FILE_FORMAT  | TYPE                           | String        | CSV                                                   | CSV              |
> | STAGE_FILE_FORMAT  | RECORD_DELIMITER               | String        | \n                                                    | \n               |
> | STAGE_FILE_FORMAT  | FIELD_DELIMITER                | String        | ,                                                     | ,                |
> | STAGE_FILE_FORMAT  | FILE_EXTENSION                 | String        |                                                       |                  |
> | STAGE_FILE_FORMAT  | SKIP_HEADER                    | Integer       | 0                                                     | 0                |
> | STAGE_FILE_FORMAT  | DATE_FORMAT                    | String        | AUTO                                                  | AUTO             |
> | STAGE_FILE_FORMAT  | TIME_FORMAT                    | String        | AUTO                                                  | AUTO             |
> | STAGE_FILE_FORMAT  | TIMESTAMP_FORMAT               | String        | AUTO                                                  | AUTO             |
> | STAGE_FILE_FORMAT  | BINARY_FORMAT                  | String        | HEX                                                   | HEX              |
> | STAGE_FILE_FORMAT  | ESCAPE                         | String        | NONE                                                  | NONE             |
> | STAGE_FILE_FORMAT  | ESCAPE_UNENCLOSED_FIELD        | String        | \\                                                    | \\               |
> | STAGE_FILE_FORMAT  | TRIM_SPACE                     | Boolean       | false                                                 | false            |
> | STAGE_FILE_FORMAT  | FIELD_OPTIONALLY_ENCLOSED_BY   | String        | NONE                                                  | NONE             |
> | STAGE_FILE_FORMAT  | NULL_IF                        | List          | [\\N]                                                 | [\\N]            |
> | STAGE_FILE_FORMAT  | COMPRESSION                    | String        | AUTO                                                  | AUTO             |
> | STAGE_FILE_FORMAT  | ERROR_ON_COLUMN_COUNT_MISMATCH | Boolean       | true                                                  | true             |
> | STAGE_FILE_FORMAT  | VALIDATE_UTF8                  | Boolean       | true                                                  | true             |
> | STAGE_FILE_FORMAT  | SKIP_BLANK_LINES               | Boolean       | false                                                 | false            |
> | STAGE_FILE_FORMAT  | REPLACE_INVALID_CHARACTERS     | Boolean       | false                                                 | false            |
> | STAGE_FILE_FORMAT  | EMPTY_FIELD_AS_NULL            | Boolean       | true                                                  | true             |
> | STAGE_FILE_FORMAT  | SKIP_BYTE_ORDER_MARK           | Boolean       | true                                                  | true             |
> | STAGE_FILE_FORMAT  | ENCODING                       | String        | UTF8                                                  | UTF8             |
> | STAGE_COPY_OPTIONS | ON_ERROR                       | String        | ABORT_STATEMENT                                       | ABORT_STATEMENT  |
> | STAGE_COPY_OPTIONS | SIZE_LIMIT                     | Long          |                                                       |                  |
> | STAGE_COPY_OPTIONS | PURGE                          | Boolean       | false                                                 | false            |
> | STAGE_COPY_OPTIONS | RETURN_FAILED_ONLY             | Boolean       | false                                                 | false            |
> | STAGE_COPY_OPTIONS | ENFORCE_LENGTH                 | Boolean       | true                                                  | true             |
> | STAGE_COPY_OPTIONS | TRUNCATECOLUMNS                | Boolean       | false                                                 | false            |
> | STAGE_COPY_OPTIONS | FORCE                          | Boolean       | false                                                 | false            |
> | STAGE_LOCATION     | URL                            | String        | ["s3://EXAMPLE-S3-PATH/my-csvfiles/"] |                  |
> | STAGE_CREDENTIALS  | AWS_KEY_ID                     | String        |                                                       |                  |
> | DIRECTORY          | LAST_REFRESHED_ON              | Timestamp     | 2023-05-03 12:50:28.000 -0700                         |                  |
> | DIRECTORY          | ENABLE                         | Boolean       | true                                                  | false            |
> | DIRECTORY          | AUTO_REFRESH                   | Boolean       | false                                                 | false            |
> +--------------------+--------------------------------+---------------+-------------------------------------------------------+------------------+
> ```
