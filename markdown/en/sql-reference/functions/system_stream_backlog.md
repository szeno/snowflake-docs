Categories:
:   [Table functions](/sql-reference/functions-table) , [System functions](/sql-reference/functions-system) (Information)

# SYSTEM$STREAM\_BACKLOG

Returns the set of table versions between the current [offset](/user-guide/streams-intro#label-streams-introduction-offset) for a specified stream and the
current timestamp. This function accepts any stream type as input (e.g. table, external table, or view) with the exception of streams on
directory tables.

For each table version, the function provides the estimated number of change data capture (CDC) records that comprise the table version,
as well as the DML operation (INSERT, UPDATE, DELETE, TRUNCATE) associated with the table version.

Use this function to analyze the volume of CDC records generated for each stream, enabling you to estimate the compute resources required
for a task to process the records.

## Syntax

Copy code

```
SYSTEM$STREAM_BACKLOG('<stream_name>')
```

## Arguments

`stream_name`
:   The name of the stream to query.

    - Note that the entire name must be enclosed in single quotes, including the database and schema, if the name is fully-qualified,
      (i.e. `'<db>.<schema>.<stream_name>'`).
    - If the stream name is case-sensitive or includes any special characters or spaces, double quotes are required to process the
      case/characters. The double quotes must be enclosed within the single quotes, i.e. `'"<stream_name>"'`.

## Usage notes

N/A

## Examples

Retrieve the current set of unconsumed table versions for stream `db1.schema1.s1`:

> Copy code
>
> ```
> SELECT * FROM TABLE(SYSTEM$STREAM_BACKLOG('db1.schema1.s1'));
> ```
