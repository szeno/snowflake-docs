# ALTER PIPE

Modifies a limited set of properties for an existing pipe object. Also supports the following operations:

- Pausing the pipe.
- Refreshing a pipe (i.e. copying the specified staged data files to the Snowpipe ingest queue for loading into the target table).
- Adding/overwriting/removing a comment for a pipe.
- Setting/unsetting a tag on a pipe.

See also:
:   [CREATE PIPE](/sql-reference/sql/create-pipe), [DROP PIPE](/sql-reference/sql/drop-pipe) , [SHOW PIPES](/sql-reference/sql/show-pipes) , [DESCRIBE PIPE](/sql-reference/sql/desc-pipe)

## Syntax

Copy code

```
ALTER PIPE [ IF EXISTS ] <name> SET { [ objectProperties ]
                                      [ COMMENT = '<string_literal>' ] }

ALTER PIPE <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER PIPE <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER PIPE [ IF EXISTS ] <name> UNSET { <property_name> | COMMENT } [ , ... ]

ALTER PIPE [ IF EXISTS ] <name> REFRESH { [ PREFIX = '<path>' ] [ MODIFIED_AFTER = <start_time> ] }
```

Where:

> Copy code
>
> ```
> objectProperties ::=
>   ERROR_INTEGRATION = <integration_name>
>   PIPE_EXECUTION_PAUSED = TRUE | FALSE
>   LOG_EVENT_LEVEL = <log_event_level>
> ```

## Parameters

`name`
:   Specifies the identifier for the pipe to alter. If the identifier contains spaces or special characters, the entire string must be enclosed in
    double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`SET ...`
:   Specifies one (or more) properties to set for the pipe (separated by blank spaces, commas, or new lines):

    `ERROR_INTEGRATION = integration_name`
    :   Required only when configuring Snowpipe to send error notifications to a cloud messaging service. Specifies the name of the notification
        integration used to communicate with the messaging service. For more information, see [Snowpipe error notifications](/user-guide/data-load-snowpipe-errors).

    `PIPE_EXECUTION_PAUSED = TRUE | FALSE`
    :   Specifies whether to pause a running pipe, typically in preparation for transferring ownership of the pipe:

        - `TRUE` pauses the pipe. The `executionState` reported by [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status) is `PAUSED`.
          Note that the pipe owner can continue to submit files to a paused pipe; however, they won’t be processed until the pipe is resumed.
        - `FALSE` resumes the pipe. The `executionState` reported by [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status) is `RUNNING`.

          Note

          Either of the following scenarios requires forcing a pipe to resume by calling the
          [SYSTEM$PIPE\_FORCE\_RESUME](/sql-reference/functions/system_pipe_force_resume) function:

          - Transferring ownership of the pipe to another role. This requirement allows the new owner to evaluate the pipe status and
            determine how many files are waiting to be loaded by calling the [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status) function.
          - Allowing the pipe to become stale. A pipe is considered stale when it’s paused for longer than the limited retention period for
            files in the pipe’s queue (14 days by default).

        Default: `FALSE` (the pipe is running by default)

    `LOG_EVENT_LEVEL = log_event_level`
    :   Specifies the severity level of [Snowpipe events](/user-guide/data-load-snowpipe-monitor-events) that the pipe records in the active event table. For the supported values, see [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level). If you don’t set this parameter on the pipe, the pipe inherits the value from its schema, database, or account. The default is `OFF`.

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    `COMMENT = 'string'`
    :   Adds a comment or overwrites an existing comment for the pipe.

`UNSET ...`
:   Specifies one (or more) properties to unset for the pipe, which resets them to the defaults:

    - `ERROR_INTEGRATION`
    - `PIPE_EXECUTION_PAUSED`
    - `LOG_EVENT_LEVEL`
    - `TAG tag_name [ , tag_name ... ]`
    - `COMMENT`

    You can reset multiple properties with a single ALTER statement; however, each property must be separated by a comma. When resetting
    a property, specify only the name; specifying a value for the property will return an error.

    After you unset `LOG_EVENT_LEVEL`, the pipe inherits the value from its schema, database, or account.

`REFRESH`
:   Copies a set of staged data files to the Snowpipe ingest queue for loading into the target table. This clause accepts an optional path and can
    further filter the list of files to load based on a specified start time.

    Note

    - This SQL command can only load data files that were staged within the last 7 days.
    - This SQL command checks the load history for both the pipe and the target table. As a result, the command queues only those files
      that were not loaded already using either:
      - The same pipe, provided the pipe owner did not recreate the pipe after the files were loaded.
      - A [COPY INTO <table>](/sql-reference/sql/copy-into-table) statement.

    Important

    The REFRESH functionality is intended for short term use to resolve specific issues when Snowpipe fails to load a subset of files and is not
    intended for regular use.

    `PREFIX = 'path'`
    :   Path (or *prefix*) appended to the stage reference in the pipe definition. The path limits the set of files to load. Only files that start
        with the specified path are included in the data load.

        For example, suppose the pipe definition references `@mystage/path1/`. If the `path` value is `d1/`, the ALTER
        PIPE statement limits loads to files in the `@mystage` stage with the `/path1/d1/` path. See the examples for more
        information.

        Note that the path must be enclosed in single quotes.

    `MODIFIED_AFTER = 'start_time'`
    :   Timestamp (in ISO-8601 format) of the oldest data files to copy into the Snowpipe ingest queue based on the LAST\_MODIFIED date (i.e. date
        when a file was staged).

        The default and maximum allowed value is 7 days.

## Access control requirements

Executing this SQL command requires [roles](/user-guide/security-access-control-overview#label-access-control-overview-roles) with the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

- To set or unset properties on a pipe, the role must have the `OWNERSHIP` privilege on the pipe, with the following exceptions:

  - To pause or resume the pipe (using `ALTER PIPE ... SET PIPE_EXECUTION_PAUSED = TRUE | FALSE`), the `OPERATE` privilege on the pipe is enough.
  - To set `LOG_EVENT_LEVEL`, the role needs the `OPERATE` or `OWNERSHIP` privilege on the pipe and the `MODIFY LOG EVENT LEVEL` privilege on the account.
  - To set `ERROR_INTEGRATION`, the role needs the `OPERATE` or `OWNERSHIP` privilege on the pipe and the `USAGE` privilege on the notification integration.
- To refresh a pipe (using `ALTER PIPE ... REFRESH`), a role that doesn’t own the pipe needs the following privileges:

  | Privilege | Object | Notes |
  | --- | --- | --- |
  | OPERATE | Pipe |  |
  | USAGE | Stage in the pipe definition | External stages only |
  | READ | Stage in the pipe definition | Internal stages only |
  | USAGE | Named file format in the pipe definition | Only if the pipe uses a named file format |
  | SELECT, INSERT | Table in the pipe definition |  |

  Expand

  Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Currently, it is not possible to modify the following pipe properties using an ALTER PIPE statement:

  - [COPY INTO <table>](/sql-reference/sql/copy-into-table) statement
  - `AWS_SNS_TOPIC` parameter
  - `INTEGRATION` parameter

  Instead, recreate the pipe using a [CREATE OR REPLACE PIPE](/sql-reference/sql/create-pipe) statement.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Pause the `mypipe` pipe:

> Copy code
>
> ```
> alter pipe mypipe SET PIPE_EXECUTION_PAUSED = true;
> ```

Add or modify the comment for pipe `mypipe`:

> Copy code
>
> ```
> alter pipe mypipe SET COMMENT = "Pipe for North American sales data";
> ```

Record [Snowpipe events](/user-guide/data-load-snowpipe-monitor-events) at the `INFO` level and more severe levels for pipe `mypipe` in the active event table:

> Copy code
>
> ```
> ALTER PIPE mypipe SET LOG_EVENT_LEVEL = INFO;
> ```

### Refreshing a pipe

Set up for examples:

> Copy code
>
> ```
> CREATE PIPE mypipe AS COPY INTO mytable FROM @mystage/path1/;
> ```

Load data files from the `@mystage/path1/` stage and path into the `mytable` table, as defined in the `mypipe` pipe definition:

> Copy code
>
> ```
> ALTER PIPE mypipe REFRESH;
> ```

Same as the previous example, but append `d1` to the path to further limit the list of files to load. In the current example, the statement
loads files from the `@mystage/path1/d1/` stage and path:

> Copy code
>
> ```
> ALTER PIPE mypipe REFRESH PREFIX='d1/';
> ```

Same as the previous example, but only load files staged after a specified timestamp:

> Copy code
>
> ```
> ALTER PIPE mypipe REFRESH PREFIX='d1/' MODIFIED_AFTER='2018-07-30T13:56:46-07:00';
> ```
