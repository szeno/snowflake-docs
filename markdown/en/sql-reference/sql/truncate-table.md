# TRUNCATE TABLE

Removes all rows from a table but leaves the table intact (including all privileges and constraints on the table). Also deletes the load
metadata for the table, which allows the same files to be loaded into the table again after the command completes.

Note that this is different from [DROP TABLE](/sql-reference/sql/drop-table), which removes the table from the system but retains a version of the table
(along with its load history) so that they can be recovered.

See also:
:   [CREATE TABLE](/sql-reference/sql/create-table)

## Syntax

Copy code

```
TRUNCATE [ TABLE ] [ IF EXISTS ] <name>

TRUNCATE [ TABLE ] [ IF EXISTS ] ERROR_TABLE( <base_table_name> )
```

## Parameters

`name`
:   Specifies the identifier for the table to truncate. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive (for example, `"My Object"`).

    If the table identifier is not fully-qualified (in the form of `db_name.schema_name.table_name` or
    `schema_name.table_name`), the command looks for the table in the current schema for the session.

`ERROR_TABLE( base_table_name )`
:   Truncates the error table associated with the specified base table. For more information about error tables, see
    [DML error logging](/user-guide/data-load-overview#label-data-load-overview-dml-error-logging).

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes. Identifiers
    enclosed in double quotes are also case-sensitive (for example, `"My Object"`).

    If the table identifier is not fully-qualified (in the form of `db_name.schema_name.table_name` or
    `schema_name.table_name`), the command looks for the table in the current schema for the session.

## Usage notes

- Both [DELETE](/sql-reference/sql/delete) and TRUNCATE TABLE maintain deleted data for recovery purposes (i.e. using Time Travel) for the data retention period.
  However, when a table is truncated, the load metadata cannot be recovered.
- The `TABLE` keyword is optional if the table name is fully qualified or a database and schema are currently in use for the session.

## Examples

The following example truncates a table:

1. Create a basic table and insert data:

   Copy code

   ```
   CREATE OR REPLACE TABLE temp_test_truncate (i number);

   INSERT INTO temp_test_truncate SELECT seq8() FROM table(generator(rowcount=>20)) v;

   SELECT COUNT (*) FROM temp_test_truncate;
   ```

   ```
   +-----------+
   | COUNT (*) |
   |-----------|
   |        20 |
   +-----------+
   ```
2. Truncate the table:

   Copy code

   ```
   TRUNCATE TABLE IF EXISTS temp_test_truncate;
   ```
3. Verify that the table is now empty:

   Copy code

   ```
   SELECT COUNT (*) FROM temp_test_truncate;
   ```

   ```
   +-----------+
   | COUNT (*) |
   |-----------|
   |         0 |
   +-----------+
   ```
