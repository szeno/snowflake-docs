# SHOW PIPES

Lists the pipes for which you have access privileges. This command can be used to list the pipes for a specified database or schema
(or the current database/schema for the session), or your entire account.

See also:
:   [ALTER PIPE](/sql-reference/sql/alter-pipe) , [CREATE PIPE](/sql-reference/sql/create-pipe) , [DESCRIBE PIPE](/sql-reference/sql/desc-pipe) , [DROP PIPE](/sql-reference/sql/drop-pipe)

## Syntax

Copy code

```
SHOW PIPES [ LIKE '<pattern>' ]
           [ IN
                {
                  ACCOUNT                                         |

                  DATABASE                                        |
                  DATABASE <database_name>                        |

                  SCHEMA                                          |
                  SCHEMA <schema_name>                            |
                  <schema_name>

                  APPLICATION <application_name>                  |
                  APPLICATION PACKAGE <application_package_name>  |
                }
           ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`[ IN ... ]`
:   Optionally specifies the scope of the command. Specify one of the following:

    `ACCOUNT`
    :   Returns records for the entire account.

    `DATABASE`, `DATABASE db_name`
    :   Returns records for the current database in use or for a specified database (`db_name`).

        If you specify `DATABASE` without `db_name` and no database is in use, the keyword has no effect on the output.

        Note

        Using SHOW commands without an `IN` clause in a database context can result in fewer than expected results.

        Objects with the same name are only displayed once if no `IN` clause is used. For example, if you have table `t1` in
        `schema1` and table `t1` in `schema2`, and they are both in scope of the database context you’ve specified (that is, the database
        you’ve selected is the parent of `schema1` and `schema2`), then SHOW TABLES only displays one of the `t1` tables.

    `SCHEMA`, `SCHEMA schema_name`
    :   Returns records for the current schema in use or a specified schema (`schema_name`).

        `SCHEMA` is optional if a database is in use or if you specify the fully qualified `schema_name` (for example, `db.schema`).

        If no database is in use, specifying `SCHEMA` has no effect on the output.

    `APPLICATION application_name`, `APPLICATION PACKAGE application_package_name`
    :   Returns records for the named Snowflake Native App or application package.

    If you omit `IN ...`, the scope of the command depends on whether the session currently has a database in use:

    - If a database is currently in use, the command returns the objects you have privileges to view in the database. This has the
      same effect as specifying `IN DATABASE`.
    - If no database is currently in use, the command returns the objects you have privileges to view in your account. This has the
      same effect as specifying `IN ACCOUNT`.

## Usage notes

- Returns results only for the pipe owner (that is, the role with the OWNERSHIP privilege on the pipe), a role with the MONITOR or OPERATE
  privilege on the pipe, or a role with the global MONITOR EXECUTION privilege.
- To determine the current status of a pipe, query the [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status) function.

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

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command. Any records above the ten thousand records limit aren’t returned, even with a filter applied.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).

## Output

The command output provides pipe properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the pipe was created. |
| `name` | The name of the pipe object.  Manually created pipes: This is the name defined in the CREATE PIPE statement.  Default pipe (Snowpipe Streaming high-performance): The value is derived from the target table name; for example, MY\_TABLE-STREAMING. |
| `database_name` | The name of the database that contains the Snowpipe object.  Manually created pipe: The name of the database that the pipe object belongs to.  Default pipe (Snowpipe Streaming high-performance): The name of the target table’s database. |
| `schema_name` | The name of the schema that contains the Snowpipe object.  Manually created pipe: The name of the schema that the pipe object belongs to.  Default pipe: The name of the target table’s schema. |
| `definition` | COPY statement used to load data from queued files into a Snowflake table. |
| `owner` | The name of the role that possesses the OWNERSHIP privilege on the pipe object.  Named pipe: The name of the role that owns the pipe, which is the role specified in the CREATE PIPE statement or granted ownership later.  Default pipe (Snowpipe Streaming high-performance): This column displays NULL. |
| `notification_channel` | Amazon Resource Name of the Amazon SQS queue for the stage named in the DEFINITION column. |
| `comment` | A user-provided or system-generated text string that describes the pipe object.  Named pipe: The user-defined comment that is provided during the CREATE PIPE statement.  Default pipe (Snowpipe Streaming High-Performance): A system-generated string that is always the following sentences: “Default pipe for Snowpipe Streaming High Performance ingestion to a table. Created and managed by Snowflake.” |
| `integration` | Name of the notification integration for pipes that rely on notification events to trigger data loads from Google Cloud Storage or Microsoft Azure cloud storage. |
| `pattern` | PATTERN copy option value in the [COPY INTO <table>](/sql-reference/sql/copy-into-table) statement in the pipe definition, if the copy option was specified. |
| `error_integration` | Notification integration name for pipes that rely on error events in Amazon S3 cloud storage to trigger notifications. |
| `owner_role_type` | The type of entity that currently owns the object.  Standard ownership: The type of object that holds the OWNERSHIP privilege. For a standard Snowflake role owner, the value is ROLE. If a Snowflake Native App owns the object, the value is APPLICATION.  Default pipe (Snowpipe Streaming High-Performance): This column displays NULL.  Deleted objects: If the pipe object was deleted, this column displays NULL, as a deleted object no longer has an active owner role. |
| `invalid_reason` | Displays some detailed information for your pipes that might have issues. You can use the provided information to troubleshoot your pipes more effectively along with [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status). If there is no issue with the pipe, the value is NULL. |
| `kind` | The kind of the pipe, which is STAGE. |

Expand

Show lessSee more

## Examples

Show all the pipes that you have privileges to view in the `public` schema in the `mydb` database:

> Copy code
>
> ```
> use database mydb;
>
> show pipes;
> ```
