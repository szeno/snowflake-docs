# CREATE ICEBERG TABLE (Delta files in object storage)

Creates or replaces an [Apache Iceberg™ table](/user-guide/tables-iceberg) in the current/specified schema
using Delta Lake metadata files in object storage (external cloud storage).
This type of Iceberg table requires a [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def).

In Snowflake documentation, **Delta Direct** means this exact pattern: an Iceberg table in Snowflake that reads Delta Lake
transaction logs and Parquet files in your external volume. You pair this command with a catalog integration
where `CATALOG_SOURCE = OBJECT_STORE` and `TABLE_FORMAT = DELTA`. For that integration, see
[Delta table files](/user-guide/tables-iceberg-configure-catalog-integration-object-storage#label-tables-iceberg-create-cat-int-delta) in [Configure a catalog integration for files in object storage](/user-guide/tables-iceberg-configure-catalog-integration-object-storage).

This topic refers to Iceberg tables as simply “tables” except where specifying *Iceberg tables* avoids confusion.

Note

Before creating a table, you must create the [external volume](/sql-reference/sql/create-external-volume) where the Iceberg metadata
and data files are stored.
For instructions, see [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume).

You also need a catalog integration for the table.
For more information, see [Configure a catalog integration for files in object storage](/user-guide/tables-iceberg-configure-catalog-integration-object-storage).

See also:
:   [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table) , [DROP ICEBERG TABLE](/sql-reference/sql/drop-iceberg-table) , [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) , [DESCRIBE ICEBERG TABLE](/sql-reference/sql/desc-iceberg-table) , [UNDROP ICEBERG TABLE](/sql-reference/sql/undrop-iceberg-table)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] ICEBERG TABLE [ IF NOT EXISTS ] <table_name>
  [ EXTERNAL_VOLUME = '<external_volume_name>' ]
  [ CATALOG = '<catalog_integration_name>' ]
  BASE_LOCATION = '<relative_path_from_external_volume>'
  [ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
  [ AUTO_REFRESH = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]
```

## Required parameters

`table_name`
:   Specifies the identifier (name) for the table; must be unique for the schema in which the table is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`BASE_LOCATION = 'relative_path_from_external_volume'`
:   Specifies a relative path from the table’s `EXTERNAL_VOLUME` location to a directory where Snowflake can access your Delta
    table files.

    The base location must point to a directory and cannot point to a single file.
    It must contain the Delta transaction log subfolder (for example, `my/base/location/_delta_log/`).

## Optional parameters

`EXTERNAL_VOLUME = 'external_volume_name'`
:   Specifies the identifier (name) for the external volume where the Iceberg table stores its metadata files and data in Parquet
    format. Iceberg metadata and manifest files store the table schema, partitions, snapshots, and other metadata.

    If you don’t specify this parameter, the Iceberg table defaults to the external volume for the schema, database, or account.
    The schema takes precedence over the database, and the database takes precedence over the account.

`CATALOG = 'catalog_integration_name'`
:   Specifies the identifier (name) of the catalog integration for this table.

    If not specified, the Iceberg table defaults to the catalog integration for the schema, database, or account.
    The schema takes precedence over the database, and the database takes precedence over the account.

`REPLACE_INVALID_CHARACTERS = { TRUE | FALSE }`
:   Specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�) in query results.
    You can only set this parameter for tables that use an external Iceberg catalog.

    - `TRUE` replaces invalid UTF-8 characters with the Unicode replacement character.
    - `FALSE` leaves invalid UTF-8 characters unchanged. Snowflake returns a user error message when it encounters invalid UTF-8
      characters in a Parquet data file.

    If not specified, the Iceberg table defaults to the parameter value for the schema, database, or account.
    The schema takes precedence over the database, and the database takes precedence over the account.

    Default: `FALSE`

`AUTO_REFRESH = { TRUE | FALSE }`
:   Specifies whether Snowflake should automatically poll your external cloud storage for updates.

    If no value is specified for the `REFRESH_INTERVAL_SECONDS` parameter on the catalog integration, Snowflake uses a default
    refresh interval of 30 seconds.

    For more information, see [automated refresh](/user-guide/tables-iceberg-auto-refresh).

    Default: FALSE

    > Note
    >
    > Using AUTO\_REFRESH with INFER\_SCHEMA isn’t supported.

`COMMENT = 'string_literal'`
:   Specifies a comment for the table.

    Default: No value

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`WITH CONTACT ( purpose = contact [ , purpose = contact ...] )`
:   Associate the new object with one or more [contacts](/user-guide/contacts-using).

    Specify the WITH CONTACT clause after all other clauses except the AS clause (if that clause is supported by this command).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE ICEBERG TABLE | Schema |  |
| CREATE EXTERNAL VOLUME | Account | Required to create a new external volume. |
| USAGE | External Volume | Required to reference an existing external volume. |
| CREATE INTEGRATION | Account | Required to create a new catalog integration. |
| USAGE | Catalog integration | Required to reference an existing catalog integration. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Considerations for running this command:

  - If you created your external volume or catalog integration using a double-quoted identifier,
    you must specify the identifier exactly as created (including the double quotes) in your CREATE ICEBERG TABLE statement.
    Failure to include the quotes might result in an `Object does not exist` error (or
    similar type of error).
- Considerations for Iceberg tables created from Delta table files (Delta Direct):

  - You can use [Time Travel](/user-guide/data-time-travel) to query Iceberg tables created from Delta table files.
    The table versions correspond to the individual Delta log commit files.

  - Snowflake supports minReaderVersion 3 and can read all tables written by engines that use the latest version of Delta Lake,
    which is 4.0.0. Delta Lake version 4.0.0 includes support for deletion vectors and liquid clustering.
  - Snowflake streams aren’t supported for Iceberg tables created from Delta table files with partition columns.
    However, insert-only streams for tables created from Delta files *without* partition columns are supported.
  - Iceberg tables created from Delta files that were created before the [2024\_04](/release-notes/bcr-bundles/2025_04_bundle) release bundle are not supported in dynamic tables.
  - Snowflake doesn’t support creating Iceberg tables from Delta table definitions in the AWS Glue Data Catalog.

  - Parquet files (data files for Delta tables) that use any of the following features or data types aren’t supported:

    - Field IDs.
    - The INTERVAL data type.
    - The DECIMAL data type with precision higher than 38.
    - LIST or MAP types with one-level or two-level representation.
    - Unsigned integer types (INT(signed = false)).
    - The FLOAT16 data type.
  - You can use the Parquet physical type `int96` for TIMESTAMP, but Snowflake doesn’t support `int96` for TIMESTAMP\_NTZ.

  - For more information about Delta data types and Iceberg tables, see [Delta data types](/user-guide/tables-iceberg-data-types#label-tables-iceberg-delta-source-data-types).
  - The following Delta Lake features aren’t currently supported: Row Tracking, change data files, change metadata,
    DataChange, CDC, protocol evolution.
- Considerations for creating tables:

  > - A schema cannot contain tables and/or views with the same name. When creating a table:
  > > - If a view with the same name already exists in the schema, an error is returned and the table is not created.
  > > - If a table with the same name already exists in the schema, an error is returned and the table is not created, unless the optional
  > >   `OR REPLACE` keyword is included in the command.
  >
  > - CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.
  >
  >   This means that any queries concurrent with the CREATE OR REPLACE ICEBERG
  >   TABLE operation use either the old or new table version.
  > - The `OR REPLACE` and `IF NOT EXISTS` clauses are mutually exclusive. They can’t both be used in the same statement.
  > - Similar to [reserved keywords](/sql-reference/reserved-keywords), ANSI-reserved function names
  >   ([CURRENT\_DATE](/sql-reference/functions/current_date), [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp), etc.) cannot be used as column names.
  > - Recreating a table (using the optional `OR REPLACE` keyword) drops its history, which makes any stream on the table stale. A stale
  >   stream is unreadable.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Refresh

Snowflake processes a maximum of 1000 Delta commit files each time you refresh a table using CREATE/ALTER … REFRESH.
If your table has over 1000 commit files to process, you can run additional manual refreshes.
Each time, the refresh process continues from where the last one stopped.

Snowflake uses Delta checkpoint files when creating an Iceberg table.
The 1,000 commit file limit only applies to commits after the latest checkpoint.

When you refresh an existing table, Snowflake normally processes Delta commit files incrementally from the table’s current version.
Snowflake performs a checkpoint refresh (full refresh) when either of the following is true:

- There is a gap in the Delta transaction log between the latest checkpoint file and the current table version (for example, Delta table maintenance removed intermediate commit files).
- The gap between the latest checkpoint file version and the table’s current version in Snowflake is larger than 1,000 commit files.

During a checkpoint refresh, Snowflake processes the latest checkpoint file and at most 1,000 commit files that follow it.
If neither condition applies, Snowflake processes up to 1,000 Delta commit files without reading a checkpoint file.

If table maintenance removes stale log and data files for the source Delta table, you should refresh Delta Direct tables in Snowflake more frequently than the retention period of Delta logs and data files.

### Examples

The following examples illustrate how Snowflake applies the 1,000 commit file limit:

- **Table creation:** The Delta log contains checkpoint version 5000 and commit files through version 5600. Snowflake reads checkpoint 5000 and processes commit files 5001 through 5600 (600 commits).
- **Incremental refresh:** The Snowflake table is at version 5600, and the Delta log has new commits through version 5700. `ALTER ICEBERG TABLE my_delta_table REFRESH` processes commit files 5601 through 5700 (100 commits).
- **Multiple incremental refreshes:** The Snowflake table is at version 5600, and the Delta log has new commits through version 6700. The first refresh processes commit files 5601 through 6600 (1,000 commits). A second refresh processes commit files 6601 through 6700 (100 commits).
- **Checkpoint refresh after a large gap:** The Snowflake table is at version 5000. The latest Delta checkpoint is at version 8500, and the current Delta table version is 9200. The gap between the Snowflake table version and the latest checkpoint (3,500 commits) is larger than 1,000. The refresh processes checkpoint 8500, then commit files 8501 through 9200 (700 commits).
- **Checkpoint refresh after log maintenance:** The Snowflake table is at version 4800. Delta table maintenance removed commit files between versions 4800 and 8000, but checkpoint 8000 remains. The current Delta table version is 8100. The refresh processes checkpoint 8000, then commit files 8001 through 8100 (100 commits).

## Examples

The following example command creates an Iceberg table from Delta table files in object storage with
[automated refresh](/user-guide/tables-iceberg-auto-refresh).

The example specifies an external volume associated with the cloud location of the Delta table files,
a [catalog integration configured for Delta](/user-guide/tables-iceberg-configure-catalog-integration-object-storage#label-tables-iceberg-create-cat-int-delta),
and a value for the required `BASE_LOCATION` parameter.

Copy code

```
CREATE ICEBERG TABLE my_delta_iceberg_table
  CATALOG = delta_catalog_integration
  EXTERNAL_VOLUME = delta_external_volume
  BASE_LOCATION = 'relative/path/from/ext/vol/'
  AUTO_REFRESH = TRUE;
```

If the Delta table uses a partitioning scheme, Snowflake automatically interprets the scheme from the Delta log.
