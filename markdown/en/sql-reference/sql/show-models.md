# SHOW MODELS

Lists the machine learning models that you have privileges to access.

The output returns table metadata and properties, ordered lexicographically by database, schema, and model name (see [Output](#output) in this
topic for descriptions of the output columns). This is important to note if you wish to filter the results using the provided filters.

See also:
:   [CREATE MODEL](/sql-reference/sql/create-model) , [DROP MODEL](/sql-reference/sql/drop-model) , [ALTER MODEL](/sql-reference/sql/alter-model), [SHOW VERSIONS IN MODEL](/sql-reference/sql/show-versions-in-model)

## Syntax

Copy code

```
SHOW MODELS [ LIKE '<pattern>' ]
            [ IN { DATABASE [ <db_name> ] | SCHEMA [ <schema_name> ] } ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN DATABASE [ db_name ] | SCHEMA [ schema_name ]`
:   Optionally specifies the scope of the command, which determines whether the command lists models only in the current/specified
    database or schema.

    If you specify the keyword `ACCOUNT`, then the command retrieves records for all schemas in all databases
    of the current account.

    If you specify the keyword `DATABASE`, then:

    - If you specify a `db_name`, then the command retrieves records for all schemas of the specified database.
    - If you don’t specify a `db_name`, then:
      - If there is a current database, then the command retrieves records for all schemas in the current database.
      - If there is no current database, then the command retrieves records for all databases and schemas in the account.

    If you specify the keyword `SCHEMA`, then:

    - If you specify a qualified schema name (for example, `my_database.my_schema`), then the command
      retrieves records for the specified database and schema.
    - If you specify an unqualified `schema_name`, then:

      - If there is a current database, then the command retrieves records for the specified schema in the current database.
      - If there is no current database, then the command displays the error
        `SQL compilation error: Object does not exist, or operation cannot be performed`.
    - If you don’t specify a `schema_name`, then:

      - If there is a current database, then:

        - If there is a current schema, then the command retrieves records for the current schema in the current database.
        - If there is no current schema, then the command retrieves records for all schemas in the current database.
      - If there is no current database, then the command retrieves records for all databases and all schemas in the account.

    Default: Depends on whether the session currently has a database in use:

    - Database: `DATABASE` is the default (i.e. the command returns the models you have privileges to view in the current
      database).
    - No database: Account scope is the default (i.e. the command returns the models you have privileges to view in your account).

## Output

The command output provides table properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| created\_on | Date and time when the model was created. |
| name | Name of the model. |
| model\_type | The type of the model, either USER\_MODEL for models that contain user code, or CORTEX\_FINETUNED for models created with [Cortex Fine-tuning](/user-guide/snowflake-cortex/cortex-finetuning) |
| database\_name | Database in which the model is stored. |
| schema\_name | Schema in which the model is stored. |
| owner | Role that owns the model. |
| comment | Comment for the model. |
| versions | JSON array listing versions of the model. |
| default\_version\_name | Version of the model used when referring to the model without a version. |
| aliases | A SQL object mapping [model version aliases](/developer-guide/snowflake-ml/model-registry/overview#label-snowpark-model-registry-model-version-aliases) to the corresponding model version name. |

Expand

Show lessSee more

## Usage notes

- Results are sorted by database name, schema name, and then model name. This means results for a database can contain models from multiple schemas
  and might break pagination. In order for pagination to work as expected, you must execute the SHOW MODELS statement for a single schema. You can
  use the IN SCHEMA `schema_name` parameter to the SHOW MODELS command. Alternatively, you can use the schema in the current context by
  executing a USE SCHEMA `schema_name` before executing SHOW MODELS.

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
