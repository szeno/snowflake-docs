Categories:
:   [Table functions](/sql-reference/functions-table)

# GET\_TABLE\_VERSIONS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns one row for each data snapshot that Snowflake has indexed for an [Apache Iceberg™ table](/user-guide/tables-iceberg).

Use this function to find the snapshot that you want to query, or to create a version tag on. To query a snapshot, pass its
snapshot ID to the AT clause. For more information, see [Time Travel for Apache Iceberg™ tables](/user-guide/tables-iceberg-time-travel).

## Syntax

Copy code

```
GET_TABLE_VERSIONS(
  '<table_name>'
)
```

## Arguments

`'table_name'`
:   The name of the Iceberg table whose version history you want to retrieve. The table name is a string, so it must be enclosed in
    single quotes. If the table name is fully qualified, such as `'<db>.<schema>.<table_name>'`, enclose the entire name in single
    quotes.

## Output

The function returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| VERSION\_ID | NUMBER | The Iceberg snapshot ID. Pass this value to `AT(VERSION =&gt; ...)` to query the snapshot. |
| VERSION\_CREATED\_AT | TEXT | The time when the snapshot was committed. |
| QUERY\_ID | TEXT | The ID of the query that produced the snapshot. For tables that use [automated refresh](/user-guide/tables-iceberg-auto-refresh), this column is a string of zeros. |

Expand

Show lessSee more

## Usage notes

- The argument must be a literal string. You can’t pass a column or an expression.
- The output contains only data-changing snapshots that Snowflake still has indexed. Snapshots that have left the retained
  history don’t appear. Operations that update table metadata without writing data, such as adding a column or creating a version
  tag, don’t produce a snapshot and don’t appear in the output.

## Examples

List the snapshots available for an Iceberg table named `my_iceberg_table`:

Copy code

```
SELECT * FROM TABLE(INFORMATION_SCHEMA.GET_TABLE_VERSIONS('my_db.my_schema.my_iceberg_table'));
```

Output:

```
+---------------------+---------------------------------+--------------------------------------+
| VERSION_ID          | VERSION_CREATED_AT              | QUERY_ID                             |
|---------------------+---------------------------------+--------------------------------------|
| 6201065399847600377 | Mon, 09 Dec 2024 11:00:50 -0800 | 01b8ebb4-0002-3a10-0000-012903c7e42a |
| 7742318844925117331 | Mon, 09 Dec 2024 14:22:07 -0800 | 01b8ebb5-0002-3a14-0000-012903c7f336 |
+---------------------+---------------------------------+--------------------------------------+
```

Query the table as it was in the earlier snapshot:

Copy code

```
SELECT * FROM my_iceberg_table AT(VERSION => 6201065399847600377);
```
