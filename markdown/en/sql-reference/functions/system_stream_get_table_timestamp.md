Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$STREAM\_GET\_TABLE\_TIMESTAMP

Returns the timestamp in nanoseconds of the latest table version at or before the current offset for the specified stream. When the stream is
queried (or consumed), the records returned include all transactions committed after this table version and before the current time.

Note

This function was created primarily as a means to “bootstrap” a stream (i.e. return the set of records inserted between the period when the table was created (at table version `t0`) and the specified stream was created). Since this function was introduced, [CREATE STREAM](/sql-reference/sql/create-stream) and [SELECT](/sql-reference/sql/select) statements that include the [CHANGES](/sql-reference/constructs/changes) clause now support Time Travel using the [AT | BEFORE](/sql-reference/constructs/at-before) clause. These options provide greater flexibility for querying historical table records.

## Syntax

Copy code

```
SYSTEM$STREAM_GET_TABLE_TIMESTAMP('<stream_name>')
```

## Arguments

`stream_name`
:   The name of the stream to query.

    - Note that the entire name must be enclosed in single quotes, including the database and schema (if the name is fully-qualified), i.e. `'<db>.<schema>.<stream_name>'`.
    - If the stream name is case-sensitive or includes any special characters or spaces, double quotes are required to process the case/characters. The double quotes must be enclosed within the single quotes, i.e. `'"<stream_name>"'`.

## Usage notes

- This function returns an error when the input is a stream on a view.

  To create a stream at or before the current offset for an existing stream, we recommend providing the existing stream name as input to
  the AT | BEFORE clause for simplicity and maximum compatibility with existing streams:

  Copy code

  ```
  CREATE STREAM ... AT ( STREAM => '<stream-name>' )
  ```

## Examples

Query the timestamp for the current offset for a stream:

Copy code

```
create table MYTABLE1 (id int);

create table MYTABLE2(id int);

create or replace stream MYSTREAM on table MYTABLE1;

insert into MYTABLE1 values (1);

-- consume the stream
begin;
insert into MYTABLE2 select id from MYSTREAM;
commit;

-- return the current offset for the stream
select system$stream_get_table_timestamp('MYSTREAM');
```
