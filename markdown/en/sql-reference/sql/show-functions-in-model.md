# SHOW FUNCTIONS IN MODEL

Lists functions defined in machine learning models.

For more information, see [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview).

See also:
:   [SHOW FUNCTIONS](/sql-reference/sql/show-functions) , [SHOW MODELS](/sql-reference/sql/show-models) , [SHOW VERSIONS IN MODEL](/sql-reference/sql/show-versions-in-model)

## Syntax

Copy code

```
SHOW FUNCTIONS [ LIKE '<pattern>' ] IN MODEL <model_name>
               [ VERSION <version_name> ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`MODEL model_name`, `MODEL model_name VERSION version_name`
:   Returns records for the specified version (`version_name`) of the specified machine learning model (`model_name`).

    If a version is not specified, records are displayed for the model’s default version.

## Output

The SHOW FUNCTIONS IN MODEL command output provides function properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | The timestamp at which the function was created. |
| `name` | The function’s name. |
| `version_name` | The name of the model version that the function belongs to. |
| `min_num_arguments` | The minimum number of arguments to the function. |
| `max_num_arguments` | The maximum number of arguments to the function. |
| `arguments` | The data types of the arguments as a JSON-formatted string. |
| `return_type` | The data type of the return value. |
| `description` | Description of the function. |
| `language` | The language in which the function was written, such as “PYTHON”. |

Expand

Show lessSee more

## Usage notes

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

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
