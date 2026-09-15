# DROP STREAM

Removes a stream from the current/specified schema.

See also:
:   [CREATE STREAM](/sql-reference/sql/create-stream) , [ALTER STREAM](/sql-reference/sql/alter-stream) , [SHOW STREAMS](/sql-reference/sql/show-streams) , [DESCRIBE STREAM](/sql-reference/sql/desc-stream)

## Syntax

Copy code

```
DROP STREAM [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the stream to drop. If the identifier contains spaces, special characters, or mixed-case characters, the
    entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive
    (e.g. `"My Object"`).

    If the stream identifier is not fully-qualified (in the form of `db_name.schema_name.stream_name` or
    `schema_name.stream_name`), the command looks for the stream in the current schema for the session.

## Usage notes

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Drop a stream:

> Copy code
>
> ```
> SHOW STREAMS LIKE 't2%';
>
>
> DROP STREAM t2;
>
>
> SHOW STREAMS LIKE 't2%';
> ```

Drop the stream again, but don’t raise an error if the stream does not exist:

> Copy code
>
> ```
> DROP STREAM IF EXISTS t2;
> ```
