# ALTER ICEBERG TABLE … CONVERT TO MANAGED

Converts an [Apache Iceberg™ table](/user-guide/tables-iceberg) that uses
an external Iceberg catalog into a table that uses Snowflake as the catalog (a Snowflake-managed Iceberg table).

The converted table supports both read and write operations,
and Snowflake handles all life-cycle maintenance, such as compaction, for the table.
For more information, see [Before and after table conversion](/user-guide/tables-iceberg-conversion#label-tables-iceberg-conversion-before-after).

See also:
:   [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) , [DROP ICEBERG TABLE](/sql-reference/sql/drop-iceberg-table) , [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) , [DESCRIBE ICEBERG TABLE](/sql-reference/sql/desc-iceberg-table)

## Syntax

Copy code

```
ALTER ICEBERG TABLE [ IF EXISTS ] <table_name> CONVERT TO MANAGED
  [ { FILE_PATH | BASE_LOCATION } = '<directory_for_table_files>' ]
  [ DROP_FROM_SOURCE_CATALOG = { TRUE | FALSE } ]
  [ STORAGE_SERIALIZATION_POLICY = { COMPATIBLE | OPTIMIZED } ]
```

## Parameters

`table_name`
:   Identifier for the table to convert.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`[ { FILE_PATH | BASE_LOCATION } = 'directory_for_table_files' ]`
:   The path to a directory where Snowflake can write data and metadata files for the table.
    `FILE_PATH` and `BASE_LOCATION` are equivalent.
    Specify a relative path from the table’s `EXTERNAL_VOLUME` location.
    For more information, see [Data and metadata directories](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-configure-external-volume-base-location).

    You must specify a value for this property if the original CREATE ICEBERG TABLE statement did not allow or include a
    `BASE_LOCATION`.

    This directory can’t be changed after you convert a table.

`DROP_FROM_SOURCE_CATALOG = { TRUE | FALSE }`
:   Specifies whether to remove the table’s entry from the external source catalog after conversion.

    This clause applies to an unmanaged Iceberg table that is registered in an external catalog that supports dropping
    the table, such as an Iceberg REST catalog.

    - `TRUE`: Converts the table to a Snowflake-managed Iceberg table, then removes that table’s entry from the
      external source catalog.
    - `FALSE`: Converts the table and leaves the source-catalog entry in place.

    Removing the catalog entry doesn’t delete the underlying data files.

    The catalog integration’s credentials need permission to drop the table in the source catalog, for example
    `TABLE_DROP` or the equivalent privilege on that catalog.

    Default: `FALSE`

`STORAGE_SERIALIZATION_POLICY = { COMPATIBLE | OPTIMIZED }`
:   Specifies the storage serialization policy for the table.
    If not specified during conversion, the table inherits the value set at the schema, database, or account level. If the value isn’t
    specified at any level, the table uses the default value.

    You can’t change the value of this parameter after you convert a table.

    - `COMPATIBLE`: Snowflake performs encoding and compression that ensures interoperability with third-party compute engines.
    - `OPTIMIZED`: Snowflake performs encoding and compression that ensures the best table performance within Snowflake.

    Default: `OPTIMIZED`

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Iceberg table | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |
| USAGE | External volume |  |
| USAGE | Catalog integration |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Only the table owner (that is, the role with the OWNERSHIP privilege on the table) or higher can execute this command.
- Converting a table in a catalog-linked database isn’t supported.
- `DROP_FROM_SOURCE_CATALOG = TRUE` removes the table from the external catalog after conversion.
  A failed drop doesn’t undo the conversion.
- Before converting with `DROP_FROM_SOURCE_CATALOG = TRUE`, Snowflake checks that it can reach the source catalog
  and manage the table there. If the check fails, the statement fails and the table isn’t converted:

  ```
  SQL execution error: Cannot convert table to managed with DROP_FROM_SOURCE_CATALOG = TRUE: Snowflake cannot manage the source catalog table '<database_name>'.'<schema_name>'.'<table_name>'. Reason: <reason>. Either remove DROP_FROM_SOURCE_CATALOG = TRUE from the statement, or grant DROP TABLE permission on the source catalog and retry.
  ```

  The check can fail for the following reasons:

  - The catalog doesn’t support dropping the table.
  - The table isn’t in the source catalog.
  - Snowflake’s credentials can’t access the catalog.
- If the conversion succeeds but the later drop from the source catalog fails, the table remains a
  Snowflake-managed Iceberg table. The statement still reports success, with a warning:

  ```
  Statement executed successfully. Warning: source catalog entry was not dropped (<reason>); drop it manually if needed.
  ```

  If the failure is a permissions error, the reason states that Snowflake’s credentials lack permission to drop the
  table. Grant `TABLE_DROP` (or the catalog’s equivalent privilege) on the source catalog. Then either run the
  statement again with `DROP_FROM_SOURCE_CATALOG = TRUE`, or drop the source-catalog entry manually.
- If conversion is blocked because the table has active position-delete files, the error message recommends running
  `ALTER ICEBERG TABLE <table_name> OPTIMIZE (REMOVE_POSITION_DELETES)` before retrying. The optimize operation rewrites affected
  partitions and clears active position-delete files for live data files. For supported table types and limitations, see the
  [ALTER ICEBERG TABLE … OPTIMIZE](/sql-reference/sql/alter-iceberg-table-optimize) command reference.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

The following example uses the ALTER ICEBERG TABLE … CONVERT TO MANAGED statement to
convert a table that Snowflake doesn’t manage into a table that uses Snowflake as the Iceberg catalog.

Copy code

```
ALTER ICEBERG TABLE myTable CONVERT TO MANAGED
  BASE_LOCATION = 'my/relative/path/from/external_volume';
```

The following example converts a table, then removes its entry from the external source catalog:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table
  CONVERT TO MANAGED
  DROP_FROM_SOURCE_CATALOG = TRUE;
```
