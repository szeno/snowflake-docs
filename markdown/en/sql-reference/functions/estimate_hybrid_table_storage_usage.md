Categories:
:   [Table functions](/sql-reference/functions-table)

# ESTIMATE\_HYBRID\_TABLE\_STORAGE\_USAGE

Returns a near-real-time estimate of the total storage usage, in bytes, of a
[hybrid table](/user-guide/tables-hybrid).

See also:
:   [DATABASE\_STORAGE\_USAGE\_HISTORY](/sql-reference/functions/database_storage_usage_history)

## Syntax

Copy code

```
ESTIMATE_HYBRID_TABLE_STORAGE_USAGE( '<table_name>' )
```

## Arguments

`'table_name'`
:   The name of the hybrid table for which to estimate storage usage.

    The name must be a string. If the table identifier is not fully qualified (in the form
    `db_name.schema_name.table_name`), the function resolves it using the database and schema in
    use for the current session.

    Because the value is a string, it must be enclosed in single quotes. If the identifier itself
    requires a double-quoted identifier (for example, mixed-case letters), enclose the
    double-quoted identifier inside single quotes (for example, `'mydb.myschema."MyTable"'`).

## Usage notes

- The function operates only on hybrid tables. Calling it on a standard table, view, or other
  object returns an error.
- To call the function, the role in use must have the SELECT privilege on the target table.
  Otherwise, the function returns an error indicating that the table does not exist or that
  you are not authorized.
- The reported value is an *estimate*. It is derived from sampled storage metadata, so it can
  differ from exact byte counts and can lag recent writes. For a table that was just created,
  or that contains only a small amount of data, the function can report `0` bytes until enough
  data accumulates for the estimate to register.
- `TOTAL_ESTIMATED_BYTES` reflects the total storage used by the table, including base
  (primary key) data, secondary indexes, and older versions of the table’s data still retained
  in the underlying store. It does not include data stored in cloud object storage.
- The function must be called in the `FROM` clause of a query and wrapped in `TABLE(...)`. For
  more information, see [Table functions](/sql-reference/functions-table).

## Output

The function returns a single row with the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| TABLE\_NAME | VARCHAR | Fully qualified name of the hybrid table. |
| TOTAL\_ESTIMATED\_BYTES | NUMBER | Estimated total storage usage of the table, in bytes. |

Expand

Show lessSee more

## Examples

Estimate the storage usage of a hybrid table:

Copy code

```
SELECT * FROM TABLE(ESTIMATE_HYBRID_TABLE_STORAGE_USAGE('my_db.my_schema.my_hybrid_table'));
```

```
+---------------------------------+-----------------------+
| TABLE_NAME                      | TOTAL_ESTIMATED_BYTES |
|---------------------------------+-----------------------|
| MY_DB.MY_SCHEMA.MY_HYBRID_TABLE |              11475750 |
+---------------------------------+-----------------------+
```

Return just the estimated byte count:

Copy code

```
SELECT TOTAL_ESTIMATED_BYTES
  FROM TABLE(ESTIMATE_HYBRID_TABLE_STORAGE_USAGE('my_db.my_schema.my_hybrid_table'));
```
