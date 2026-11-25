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
:   Truncates the error table associated with the specified base table. It doesn’t delete the rows or the load metadata of
    the base table. For more information about error tables, see [Error tables](/user-guide/data-engineering/error-tables). To clear the
    error table after you load the rows that `COPY INTO` or Snowpipe rejected, see
    [Clear the error table and resume loads](/user-guide/data-load-error-tables-reload#label-data-load-error-tables-clear).

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes. Identifiers
    enclosed in double quotes are also case-sensitive (for example, `"My Object"`).

    If the table identifier is not fully-qualified (in the form of `db_name.schema_name.table_name` or
    `schema_name.table_name`), the command looks for the table in the current schema for the session.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| TRUNCATE | Table | Required on the table to truncate, unless the role owns the table. Truncating an error table with `ERROR_TABLE( <base_table_name> )` requires the TRUNCATE or OWNERSHIP privilege on the base table. The SELECT ERROR TABLE privilege isn’t enough. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Both [DELETE](/sql-reference/sql/delete) and TRUNCATE TABLE maintain deleted data for recovery purposes (using Time Travel) for the data
  retention period. However, when a table is truncated, the load metadata cannot be recovered.
- To protect against an accidental truncate, you can use Time Travel, zero-copy cloning, backups, Fail-safe (Snowflake-only recovery),
  and transactions with ROLLBACK. For a description of each safeguard, see
  . For Time Travel details, see [Understanding & using Time Travel](/user-guide/data-time-travel).
- Unlike rows that you truncate from a table, errors that you truncate from an error table can’t be recovered.
- Truncating an error table removes every error in it, including errors from DML statements and from every load that
  writes to the base table. You can’t delete individual errors. To keep errors, copy them to another table before you
  truncate the error table. For an example, see [Copy errors and then truncate an error table](#label-truncate-table-error-table-example).
- The `TABLE` keyword is optional if the table name is fully qualified or a database and schema are currently in use for the session.

## Examples

### Truncate a table

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

### Recover a truncated table

To recover the rows after an accidental truncate, clone the table as it was before the TRUNCATE statement, replacing `<query_id>` with
the query ID of the TRUNCATE statement:

Copy code

```
CREATE TABLE temp_test_truncate_restored CLONE temp_test_truncate
  BEFORE(STATEMENT => '<query_id>');

SELECT COUNT(*) FROM temp_test_truncate_restored;
```

```
+----------+
| COUNT(*) |
|----------|
|       20 |
+----------+
```

### Copy errors and then truncate an error table

Errors that are recorded after you copy the error table and before you truncate it are lost, so first stop the loads
and statements that write to the base table, as described in
[Stop loads into the table](/user-guide/data-load-error-tables-reload#label-data-load-error-tables-stop-loads). The following example then
copies the errors in the error table of the `my_table` table to another table, with the time that you archived them,
and truncates the error table:

Copy code

```
CREATE TABLE my_table_errors_archive AS
  SELECT CURRENT_TIMESTAMP() AS archived_at, *
    FROM ERROR_TABLE(my_table);

TRUNCATE ERROR_TABLE(my_table);
```

The copy is a regular table, so the access controls on the error table don’t apply to it. Grant access to the copy
only to roles that are allowed to see the source data. After you truncate the error table, resume the loads and
statements that you stopped, as described in
[Clear the error table and resume loads](/user-guide/data-load-error-tables-reload#label-data-load-error-tables-clear). Before you resume a task or restart
an application that runs `COPY INTO` on the base table on a schedule, use the copy of the errors to find the files that
the next run would load again and move them, as described in that section.
