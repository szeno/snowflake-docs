Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$STREAM\_HAS\_DATA

Indicates whether a specified stream contains change data capture (CDC) records.

## Syntax

Copy code

```
SYSTEM$STREAM_HAS_DATA('<stream_name>')
```

## Arguments

`stream_name`
:   The name of the stream to query.

    - Note that the entire name must be enclosed in single quotes, including the database and schema (if the name is fully-qualified), i.e. `'<db>.<schema>.<stream_name>'`.
    - If the stream name is case-sensitive or includes any special characters or spaces, double quotes are required to process the case/characters. The double quotes must be enclosed within the single quotes, i.e. `'"<stream_name>"'`.

## Usage notes

- This function is intended to be used in the WHEN expression in the definition of tasks. If the specified stream contains no change data, the task skips the current run. This check can help avoid starting or resuming a warehouse unnecessarily. However, note that the function is designed to avoid false negatives (i.e. returning a false value even when the stream contains change data); however, the function is not guaranteed to avoid false positives (i.e. returning a true value when the stream contains no change data).
- This function performs a diff of the table version metadata (between the stream offset and the current transactional time) to determine whether the stream contains CDC records. If the DML activity for the table during that period consisted of the same set of rows being inserted, optionally updated, and deleted, returning to the original table state, then it is possible this function could return a TRUE value even though the stream contains no CDC records.
- When the input is a view stream, the returned value is `TRUE` when change data capture (CDC) records for the
  underlying tables change. The function performs a diff on the version metadata for the underlying tables rather than for the
  view itself. The result is a false positive when the query in the source view definition does not reference the rows in the underlying
  tables that have changed. The rate of false positives increases as a view becomes more selective.

  When this function is referenced in the optional `WHEN` parameter in a task definition, the higher false positive rate means that
  tasks may run when a view stream is empty more often than when a table stream is the input for the function. However, this check still
  avoids task runs when there is no change in the underlying table data.
- Calling this function on a stream prevents it from becoming stale, provided the stream is empty and the SYSTEM$STREAM\_HAS\_DATA function
  returns `FALSE`.
- When this function returns TRUE, you must consume the stream in a DML operation, whether it’s a false positive or actual
  change data. If you don’t consume the stream, this function keeps returning `TRUE`, and tasks that use this function in their WHEN
  clause won’t skip execution. This results in unnecessary task runs and warehouse charges.

  To consume the stream efficiently when the result is a false positive — for example, querying the stream returns no records —
  use a statement like the following example:

  Copy code

  ```
  CREATE TEMPORARY TABLE _unused_table AS SELECT * FROM my_stream WHERE 1=0;
  ```

  This statement counts as a DML operation that consumes the stream, because `CREATE TABLE AS SELECT` is a DML transaction. The
  `WHERE 1=0` clause filters out all data, so nothing gets processed or stored. This operation advances the stream offset, and
  `SYSTEM$STREAM_HAS_DATA` returns `FALSE` until new changes occur.

  Alternatively, run your regular data processing logic — INSERT, UPDATE, MERGE, or other DML statements — on the stream.
  This also consumes the stream and advances its offset, even when the stream contains no change records.

## Examples

> Copy code
>
> ```
> create table MYTABLE1 (id int);
>
> create table MYTABLE2(id int);
>
> create stream MYSTREAM on table MYTABLE1;
>
> insert into MYTABLE1 values (1);
>
> -- returns true because the stream contains change tracking information
> select system$stream_has_data('MYSTREAM');
>
> +----------------------------------------+
> | SYSTEM$STREAM_HAS_DATA('MYSTREAM')     |
> |----------------------------------------|
> | True                                   |
> +----------------------------------------+
>
>  -- consume the stream
> begin;
> insert into MYTABLE2 select id from MYSTREAM;
> commit;
>
> -- returns false because the stream was consumed
> select system$stream_has_data('MYSTREAM');
>
> +----------------------------------------+
> | SYSTEM$STREAM_HAS_DATA('MYSTREAM')     |
> |----------------------------------------|
> | False                                  |
> +----------------------------------------+
> ```
