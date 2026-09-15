# UNDROP EXTERNAL VOLUME

Restores the most recent version of a dropped [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def).

See also:
:   [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume) , [ALTER EXTERNAL VOLUME](/sql-reference/sql/alter-external-volume), [DESCRIBE EXTERNAL VOLUME](/sql-reference/sql/desc-external-volume) , [SHOW EXTERNAL VOLUMES](/sql-reference/sql/show-external-volumes) ,
    [DROP EXTERNAL VOLUME](/sql-reference/sql/drop-external-volume)

## Syntax

Copy code

```
UNDROP EXTERNAL VOLUME <name>
```

## Parameters

`name`
:   Specifies the identifier for the external volume to restore.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Usage notes

- If an external volume with the same name already exists, the UNDROP command returns an error.

- UNDROP relies on the Snowflake [Time Travel](/user-guide/data-time-travel) feature. An object can be restored only if
  the object was deleted within the [Data retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period). The default value is 24 hours.

## Examples

Restore the most recent version of a dropped external volume named `my_external_volume`:

Copy code

```
UNDROP EXTERNAL VOLUME my_external_volume;
```
