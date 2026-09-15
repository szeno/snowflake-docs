# ALTER ICEBERG TABLE … REFRESH

Refreshes the metadata for an [Apache Iceberg™ table](/user-guide/tables-iceberg) that uses an external Iceberg catalog.
Refreshing an Iceberg table synchronizes the table metadata with the most recent table changes.

This topic refers to Iceberg tables as simply “tables” except where specifying *Iceberg tables* avoids confusion.

See also:
:   [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) , [DROP ICEBERG TABLE](/sql-reference/sql/drop-iceberg-table) , [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) , [DESCRIBE ICEBERG TABLE](/sql-reference/sql/desc-iceberg-table)

## Syntax

Copy code

```
ALTER ICEBERG TABLE [ IF EXISTS ] <table_name> REFRESH [ '<metadata_file_relative_path>' ]
```

## Parameters

`table_name`
:   Identifier for the table to refresh.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`'metadata_file_relative_path'`
:   Specifies a metadata file path for a table created from *Iceberg* files in object storage. The path must be relative to the
    [active storage location](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-ext-vol-active-storage-location) of the external volume associated with the table.

    The following table shows what value to specify based on an example storage location:

    | **Active storage location for the table’s external volume** | `s3://mybucket_us_east_1` |
    | --- | --- |
    | **Full path to the metadata file** | `s3://mybucket_us_east_1/metadata/v1.metadata.json` |
    | **Value to specify as the** `'metadata_file_relative_path'` | `metadata/v1.metadata.json` (without a leading forward slash) |

    Expand

    Show lessSee more

    Note

    - If the table uses AWS Glue as the catalog, or is created from Delta table files, don’t specify a metadata file path.
    - Omit the leading forward slash (`/`) in the metadata file path.
    - Before Snowflake version 7.34,
      a parameter named `BASE_LOCATION` (also called `FILE_PATH` in previous versions) was required to create a table
      from Iceberg files in object storage. The parameter specified a relative path from the `EXTERNAL_VOLUME`
      location.

      To refresh a table that you created using the old syntax, specify a path relative to the `BASE_LOCATION`. For example,
      if the full path to your metadata file is `s3://mybucket_us_east_1/my_base_location/metadata/v1.metadata.json`,
      specify `metadata/v1.metadata.json` as the `{metadata-file-relative-path}`.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Iceberg table | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |
| USAGE | External volume | Not required if using [vended credentials](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials). |
| USAGE | Catalog integration |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Only the table owner (that is, the role with the OWNERSHIP privilege on the table) or higher can execute this command.
- Using the ALTER ICEBERG TABLE … REFRESH command in transactions (implicit or explicit) is not supported.
- Considerations for [Delta Direct](/sql-reference/sql/create-iceberg-table-delta) tables: When you refresh a Delta Direct table using this command, Snowflake processes up to 1,000 Delta commit files per refresh and can perform a checkpoint refresh (full refresh) under certain conditions. For the 1,000 commit file limit, checkpoint refresh triggers, and examples, see [Refresh](/sql-reference/sql/create-iceberg-table-delta#label-tables-iceberg-delta-refresh-limitations).
- Regarding metadata:

  Attention

## Examples

### Refresh a table

This example manually refreshes the metadata for a table for the following scenarios:

- The table uses AWS Glue for the Iceberg catalog.
- The table is based on Delta table files in object storage.

For these scenarios, you don’t specify a metadata file path in the refresh command.

Copy code

```
ALTER ICEBERG TABLE myIcebergTable REFRESH;
```

### Refresh a table created from Iceberg files in object storage

This example manually refreshes the table metadata based on changes in a new metadata file. In this example, the full path
to the metadata file is `<external-volume-storage-base-url>/path/to/metadata/v2.metadata.json`.

When specifying a metadata file, you don’t include a leading forward slash (`/`) in the metadata file path.

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table REFRESH 'path/to/metadata/v2.metadata.json';
```

Note

Before Snowflake version 7.34,
a parameter named `BASE_LOCATION` (also called `FILE_PATH` in previous versions) was required to create a table
from Iceberg files in object storage. The parameter specified a relative path from the `EXTERNAL_VOLUME`
location.

To refresh a table that you created using the old syntax, specify a path relative to the `BASE_LOCATION`. For example,
if the full path to your metadata file is `s3://mybucket_us_east_1/my_base_location/metadata/v1.metadata.json`,
specify `metadata/v1.metadata.json` as the `{metadata-file-relative-path}`.
