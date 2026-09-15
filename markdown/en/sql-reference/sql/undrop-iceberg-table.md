# UNDROP ICEBERG TABLE

Restores the most recent version of a dropped [Apache Iceberg™ table](/user-guide/tables-iceberg).

This topic refers to Iceberg tables as simply “tables” except where specifying *Iceberg tables* avoids confusion.

See also:
:   [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) , [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table) , [DROP ICEBERG TABLE](/sql-reference/sql/drop-iceberg-table) ,
    [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) , [DESCRIBE ICEBERG TABLE](/sql-reference/sql/desc-iceberg-table)

## Syntax

Copy code

```
UNDROP ICEBERG TABLE <name>
```

## Parameters

`name`
:   Specifies the identifier for the table to restore. If the identifier contains spaces or special characters, the entire string must
    be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- This command isn’t supported for tables in a catalog-linked database.
- Restoring Iceberg tables is only supported in the current schema or current database, even if the table name is fully qualified.
- If an Iceberg table with the same name already exists, an error is returned.
- To undrop an Iceberg table whose external volume has been dropped, undrop the external volume first. You can’t undrop the Iceberg table
  by creating a new external volume with same name as the dropped external volume.
- You can’t restore a table that uses an external catalog if the associated catalog integration has been dropped.

- UNDROP relies on the Snowflake [Time Travel](/user-guide/data-time-travel) feature. An object can be restored only if
  the object was deleted within the [Data retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period). The default value is 24 hours.

## Examples

Restore the most recent version of a dropped table `my_iceberg_table`:

Copy code

```
UNDROP ICEBERG TABLE my_iceberg_table;
```
