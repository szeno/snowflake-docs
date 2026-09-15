# SHOW CHANNELS

Lists the [Snowpipe Streaming channels](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview) for which you have access privileges. This command can be used to list the channels for a specified table, database or schema
(or the current database/schema for the session), or your entire account.

See also:

> - [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview)
> - [SYSTEM$SNOWPIPE\_STREAMING\_UPDATE\_CHANNEL\_OFFSET\_TOKEN](/sql-reference/functions/system_snowpipe_streaming_update_channel_offset_token)

## Syntax

Copy code

```
SHOW CHANNELS [ LIKE '<pattern>' ]
           [ IN
                {
                  ACCOUNT                  |

                  DATABASE                 |
                  DATABASE <database_name> |

                  SCHEMA                   |
                  SCHEMA <schema_name>     |
                  <schema_name>            |

                  TABLE                    |
                  TABLE <table_name>       |

                  PIPE                     |
                  PIPE <pipe_name>
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

    `TABLE`, `TABLE table_name`
    :   Returns records for the table.

    If you omit `IN ...`, the scope of the command depends on whether the session currently has a database in use:

    - If a database is currently in use, the command returns the objects you have privileges to view in the database. This has the
      same effect as specifying `IN DATABASE`.
    - If no database is currently in use, the command returns the objects you have privileges to view in your account. This has the
      same effect as specifying `IN ACCOUNT`.

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

## Output

The command output provides pipe properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| created\_on | Date and time when the channel is created. |
| name | Name of the channel. |
| database\_name | The name of the database where the Snowpipe Streaming channel is logically stored.  Named channel: The name of the database where the user-defined channel is created.  Default pipe (high-performance): The name of the target table’s database. |
| schema\_name | The name of the schema where the Snowpipe Streaming channel is logically stored.  Named channel: The name of the schema where the user-defined channel is created.  Default pipe (high-performance): The name of the target table’s schema. |
| table\_name | The name of the Snowflake table that the channel is mapped to for data ingestion.  For Snowpipe Streaming classic channels: The column shows the name of the target table, establishing the channel’s mapping.  For default pipes (High-Performance): The column is populated with the name of the target table, providing context for the default pipe’s destination. |
| client\_sequencer | For internal use. |
| row\_sequencer | For internal use. |
| offset\_token | String used to track the ingestion process. |
| parent\_name | Table or pipe where the channel is mapped to. |
| parent\_domain | Domain (table or pipe) where the channel is mapped to. |

Expand

Show lessSee more

## Examples

Show all the channels that you have privileges to view in the `public` schema in the `mydb` database:

> Copy code
>
> ```
> use database mydb;
>
> show channels;
>
> +-------------------------------+-----------+---------------+------------------+------------------------+------------------+---------------+--------------+
> | created_on                    | name      | database_name | schema_name      | table_name             | client_sequencer | row_sequencer | offset_token |
> |-------------------------------+-----------+---------------+------------------+------------------------+------------------+---------------+--------------+
> | 2023-05-05 17:13:17.579 -0700 | CHANNEL8  | TEST_DB1      | STREAMING_INGEST | STREAMING_INGEST_TABLE | 7                | 1             | 0            |
> |                               |           |               |                  |                        |                  |               |              |
> +-------------------------------+-----------+---------------+------------------+------------------------+------------------+---------------+--------------+
> ```

Show all the channels for a specific pipe:

> Copy code
>
> ```
> show channels in pipe MY_PIPE;
> ```
