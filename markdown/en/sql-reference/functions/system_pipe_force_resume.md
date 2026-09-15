Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$PIPE\_FORCE\_RESUME

Forces a pipe paused using [ALTER PIPE](/sql-reference/sql/alter-pipe) to resume. This is necessary in either of the following scenarios:

- The pipe owner transfers ownership of the pipe to another role while the pipe is paused.
- The paused pipe is allowed to become stale.

  A pipe is considered stale when it is paused for longer than the limited retention period for event messages received for the pipe
  (14 days by default). As each notification reaches the end of this period, Snowflake schedules it to be dropped from the internal
  metadata. If the pipe is later resumed, Snowpipe may process notifications older than 14 days on a best effort basis. Snowflake cannot
  guarantee that these older notifications are processed.

  This scenario only pertains to pipe objects that leverage cloud messaging to trigger data loads (i.e. where `AUTO_INGEST = TRUE` in
  the pipe definition).

Executing this function resumes the specified pipe.

To determine how many files are queued, query [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status).

For more information, see [Snowpipe](/user-guide/data-load-snowpipe-intro).

## Syntax

Copy code

```
SYSTEM$PIPE_FORCE_RESUME( '<pipe_name>' , '[ STALENESS_CHECK_OVERRIDE ] [ , OWNERSHIP_TRANSFER_CHECK_OVERRIDE ]')
```

## Arguments

`pipe_name`
:   Pipe to resume running.

`STALENESS_CHECK_OVERRIDE`
:   Specifies to resume a stale pipe. A pipe is considered stale when it is paused for longer than the limited retention period for event
    messages received for the pipe (14 days by default).

    Note

    This argument only pertains to pipe objects that leverage cloud messaging to trigger data loads.

`OWNERSHIP_TRANSFER_CHECK_OVERRIDE`
:   Specifies to resume a pipe after ownership of the pipe was transferred to another role.

    Note

    To ensure backward compatibility, passing `pipe_name` as the only input is syntactically equivalent to passing both
    `pipe_name` and `OWNERSHIP_TRANSFER_CHECK_OVERRIDE`.

If both `STALENESS_CHECK_OVERRIDE` and `OWNERSHIP_TRANSFER_CHECK_OVERRIDE` are required, these arguments can be input in either
order.

## Usage notes

- Only the pipe owner (i.e. the role with the OWNERSHIP privilege on the pipe) or a role with the OPERATE privilege on the pipe can call this SQL
  function:

  SQL operations on schema objects also require USAGE or any other privilege on the database and schema that contain the object.
- `pipe_name` is a string so it must be enclosed in single quotes:

  - Note that the entire name must be enclosed in single quotes, including the database and schema (if the name is fully-qualified), i.e. `'<db>.<schema>.<pipe_name>'`.
  - If the pipe name is case-sensitive or includes any special characters or spaces, double quotes are required to process the case/characters. The double quotes must be enclosed within the single quotes, i.e. `'"<pipe_name>"'`.

## Examples

Force a pipe with a case-insensitive name to resume:

> Copy code
>
> ```
> SELECT SYSTEM$PIPE_FORCE_RESUME('mydb.myschema.mypipe');
> ```

Force a pipe with a case-sensitive name to resume:

> Copy code
>
> ```
> SELECT SYSTEM$PIPE_FORCE_RESUME('mydb.myschema."myPipe"');
> ```

Force a stale pipe to resume after its ownership was transferred to another role:

> Copy code
>
> ```
> SELECT SYSTEM$PIPE_FORCE_RESUME('mydb.myschema.stalepipe','staleness_check_override, ownership_transfer_check_override');
> ```
