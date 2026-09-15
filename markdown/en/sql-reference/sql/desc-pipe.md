# DESCRIBE PIPE

Describes the properties specified for a pipe, as well as the default values of the properties.

DESCRIBE can be abbreviated to DESC.

See also:
:   [DROP PIPE](/sql-reference/sql/drop-pipe) , [ALTER PIPE](/sql-reference/sql/alter-pipe) , [CREATE PIPE](/sql-reference/sql/create-pipe) , [SHOW PIPES](/sql-reference/sql/show-pipes)

## Syntax

Copy code

```
DESC[RIBE] PIPE <name>
```

## Parameters

`name`
:   Specifies the identifier for the pipe to describe. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- Returns results only for the pipe owner (i.e. the role with the OWNERSHIP privilege on the pipe), a role with the MONITOR or OPERATE
  privilege on the pipe, or a role with the global MONITOR EXECUTION privilege.
- To determine the current status of a pipe, query the [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status) function.

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

Copy code

```
| created_on | name | database_name | schema_name | definition | owner | notification_channel | comment | integration | pattern | error_integration | invalid_reason | kind |
```

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the pipe was created. |
| `name` | The name of the pipe object.  Manually created pipes: This is the name defined in the CREATE PIPE statement.  Default pipe (Snowpipe Streaming high-performance): The value is derived from the target table name; for example, MY\_TABLE-STREAMING. |
| `database_name` | The name of the database that contains the Snowpipe object.  Manually created pipe: The name of the database that the pipe object belongs to.  Default pipe (Snowpipe Streaming high-performance): The name of the target table’s database. |
| `schema_name` | The name of the schema that contains the Snowpipe object.  Manually created pipe: The name of the schema that the pipe object belongs to.  Default pipe: The name of the target table’s schema. |
| `definition` | COPY statement that is used to load data from queued files into a Snowflake table. |
| `owner` | The name of the role that possesses the OWNERSHIP privilege on the pipe object.  Named pipe: The name of the role that owns the pipe, which is the role specified in the CREATE PIPE statement or granted ownership later.  Default pipe (Snowpipe Streaming high-performance): This column displays NULL. |
| `notification_channel` | Amazon Resource Name of the Amazon SQS queue for the stage that is named in the DEFINITION column. |
| `comment` | A user-provided or system-generated text string that describes the pipe object.  Named pipe: The user-defined comment that is provided during the CREATE PIPE statement.  Default pipe (Snowpipe Streaming High-Performance): A system-generated string that is always the following sentences: “Default pipe for Snowpipe Streaming High Performance ingestion to a table. Created and managed by Snowflake.” |
| `integration` | Name of the notification integration for pipes that rely on notification events to trigger data loads from Google Cloud Storage or Microsoft Azure cloud storage. |
| `pattern` | PATTERN copy option value in the [COPY INTO <table>](/sql-reference/sql/copy-into-table) statement in the pipe definition, if the copy option was specified. |
| `error_integration` | Notification integration name for pipes that rely on error events in Amazon S3 cloud storage to trigger notifications. |
| `invalid_reason` | Displays some detailed information for your pipes that may have issues. You can use the provided information to troubleshoot your pipes more effectively along with [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status). If there is no issue with the pipe, the value is NULL. |
| `kind` | The kind of the pipe, which is STAGE. |

Expand

Show lessSee more

Kafka-related columns

| Column | Description |
| --- | --- |
| `broker_integration` | Name of the external access integration used with Kafka. |
| `broker_secret` | Name of the secret used with Kafka. |
| `row_format` | Row format of records: `JSON` or `AVRO`. |
| `schema` | Schema of records represented as variant. |
| `topic` | Name of a synchronized topic. |

Expand

Show lessSee more

## Examples

Describe the `mypipe` pipe created in the examples in [CREATE PIPE](/sql-reference/sql/create-pipe):

> Copy code
>
> ```
> desc pipe mypipe;
>
> +-------------------------------+--------+---------------+-------------+---------------------------------+----------+---------+
> | created_on                    | name   | database_name | schema_name | definition                      | owner    | comment |
> |-------------------------------+--------+---------------+-------------+---------------------------------+----------+---------|
> | 2017-08-15 06:11:05.703 -0700 | MYPIPE | MYDATABASE    | PUBLIC      | copy into mytable from @mystage | SYSADMIN |         |
> +-------------------------------+--------+---------------+-------------+---------------------------------+----------+---------+
> ```
