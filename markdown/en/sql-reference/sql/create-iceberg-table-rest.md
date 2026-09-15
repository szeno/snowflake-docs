# CREATE ICEBERG TABLE (Iceberg REST catalog)

Creates or replaces an [Apache Iceberg™ table](/user-guide/tables-iceberg) in the current/specified schema for an Iceberg REST catalog.

Use this command for the following scenarios:

- You want to use a remote Iceberg catalog that complies with the open source
  [Apache Iceberg REST OpenAPI specification](https://github.com/apache/iceberg/blob/main/open-api/rest-catalog-open-api.yaml).
- You want to query a table in [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview) or Apache Polaris™. For more information, see [Query a table in Snowflake Open Catalog using Snowflake](/user-guide/tables-iceberg-open-catalog-query).
- You want to create an externally managed table in a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database).
  See [Variant syntax](#label-tables-iceberg-external-write-create-table-syntax).

Note

Before creating a table, you must create the [external volume](/sql-reference/sql/create-external-volume) where the Iceberg metadata
and data files are stored.
For instructions, see [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume).

You also need a catalog integration for the table.
For more information, see [Configure a catalog integration for Apache Iceberg™ REST catalogs](/user-guide/tables-iceberg-configure-catalog-integration-rest)
or [Configure a catalog integration for Snowflake Open Catalog](/user-guide/tables-iceberg-configure-catalog-integration-open-catalog).

See also:
:   [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table), [DROP ICEBERG TABLE](/sql-reference/sql/drop-iceberg-table), [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables), [DESCRIBE ICEBERG TABLE](/sql-reference/sql/desc-iceberg-table), [UNDROP ICEBERG TABLE](/sql-reference/sql/undrop-iceberg-table)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] ICEBERG TABLE [ IF NOT EXISTS ] <table_name>
  [ EXTERNAL_VOLUME = '<external_volume_name>' ]
  [ CATALOG = '<catalog_integration_name>' ]
  CATALOG_TABLE_NAME = '<rest_catalog_table_name>'
  [ CATALOG_NAMESPACE = '<catalog_namespace>' ]
  [ PATH_LAYOUT = { FLAT | HIERARCHICAL } ]
  [ TARGET_FILE_SIZE = '{ AUTO | 16MB | 32MB | 64MB | 128MB }' ]
  [ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
  [ AUTO_REFRESH = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]
  [ STORAGE_SERIALIZATION_POLICY = { COMPATIBLE | OPTIMIZED } ]
  [ ICEBERG_MERGE_ON_READ_BEHAVIOR = { 'AUTO' | 'ENABLED' | 'DISABLED' } ]
  [ ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE } ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]
```

Where:

Copy code

```
partitionExpression ::=
  <col_name> -- identity transform
  | BUCKET ( <num_buckets> , <col_name> )
  | TRUNCATE ( <width> , <col_name> )
  | YEAR ( <col_name> )
  | MONTH ( <col_name> )
  | DAY ( <col_name> )
  | HOUR ( <col_name> )
```

## Variant syntax

### CREATE ICEBERG TABLE (catalog-linked database)

Copy code

```
CREATE [ OR REPLACE ] ICEBERG TABLE [ IF NOT EXISTS ] <table_name>
  [
    --Column definition
    <col_name> <col_type> [ DEFAULT <col_default> ]
      [ [ WITH ] MASKING POLICY <policy_name> [ USING ( <col_name> , <cond_col1> , ... ) ] ]

    -- Additional column definitions
    [ , <col_name> <col_type> [ DEFAULT <col_default> ] [ ... ] ]
  ]
  [ PARTITION BY ( partitionExpression [ , partitionExpression , ... ] ) ]
  [ PATH_LAYOUT = { FLAT | HIERARCHICAL } ]
  [ TARGET_FILE_SIZE = '{ AUTO | 16MB | 32MB | 64MB | 128MB }' ]
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
  [ AUTO_REFRESH = { TRUE | FALSE } ]
  [ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
  [ COPY GRANTS ]
  [ PURGE ]
  [ COMMENT = '<string_literal>' ]
  [ ICEBERG_VERSION = <integer> ]
  [ ICEBERG_MERGE_ON_READ_BEHAVIOR = { 'AUTO' | 'ENABLED' | 'DISABLED' } ]
  [ ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE } ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ BASE_LOCATION = '<path_to_directory_for_table_files>' ]
  [ STORAGE_SERIALIZATION_POLICY = { COMPATIBLE | OPTIMIZED } ]
```

Where:

Copy code

```
partitionExpression ::=
  <col_name> -- identity transform
  | BUCKET ( <num_buckets> , <col_name> )
  | TRUNCATE ( <width> , <col_name> )
  | YEAR ( <col_name> )
  | MONTH ( <col_name> )
  | DAY ( <col_name> )
  | HOUR ( <col_name> )
```

### CREATE ICEBERG TABLE (catalog-linked database) … AS SELECT

> Copy code
>
> ```
> CREATE [ OR REPLACE ] ICEBERG TABLE <table_name> [ ( <col_name> [ <col_type> ] , <col_name> [ <col_type> ] , ... ) ]
>   [ ... ]
>   [ PURGE ]
>   AS SELECT <query>
> ```

You can apply a masking policy to a column in a CTAS statement. Specify the masking policy after the column data type. For example:

> Copy code
>
> ```
> CREATE [ OR REPLACE ] ICEBERG TABLE <table_name> ( <col1> <data_type> [ WITH ] MASKING POLICY <policy_name> [ , ... ] )
>   [ ... ]
>   [ PURGE ]
>   AS SELECT <query>
> ```

## Required parameters

`table_name`
:   Specifies the identifier (name) for the table in Snowflake; must be unique for the schema in which the table is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

    Note

    To retrieve a list of tables or namespaces in your remote catalog, you can use the following functions:

    - [SYSTEM$LIST\_ICEBERG\_TABLES\_FROM\_CATALOG](/sql-reference/functions/system_list_iceberg_tables_from_catalog)
    - [SYSTEM$LIST\_NAMESPACES\_FROM\_CATALOG](/sql-reference/functions/system_list_namespaces_from_catalog)
    - [SYSTEM$EXECUTE\_CATALOG\_OPERATION](/sql-reference/functions/system_execute_catalog_operation)

`CATALOG_TABLE_NAME = 'rest_catalog_table_name'`
:   Specifies the table name as recognized by your external catalog. This parameter can’t be changed after
    you create the table.

    Note

    Don’t specify a namespace with the table name (`mynamespace.mytable`). To specify a namespace for this table, and override the default
    namespace set for the catalog integration, use the [CATALOG\_NAMESPACE](/sql-reference/sql/create-iceberg-table-rest#label-create-catalog-table-rest-namespace) parameter.

`col_name`
:   For creating a table in a [catalog-linked database (preview)](/user-guide/tables-iceberg-catalog-linked-database).

    Specifies a column identifier (name). All the requirements for table identifiers also apply to column identifiers.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax) and [Reserved & limited keywords](/sql-reference/reserved-keywords).

    Note

    In addition to the standard reserved keywords, the following keywords can’t be used as column identifiers because they are
    reserved for ANSI-standard context functions:

    - `CURRENT_DATE`
    - `CURRENT_ROLE`
    - `CURRENT_TIME`
    - `CURRENT_TIMESTAMP`
    - `CURRENT_USER`

    For the list of reserved keywords, see [Reserved & limited keywords](/sql-reference/reserved-keywords).

`col_type`
:   For creating a table in a [catalog-linked database (preview)](/user-guide/tables-iceberg-catalog-linked-database).

    Specifies the data type for the column.

    For information about the data types that can be specified for table columns, see [Data types for Apache Iceberg™ tables](/user-guide/tables-iceberg-data-types).

## Optional parameters

`col_name col_type DEFAULT col_default`
:   For a table that conforms to Iceberg v3, specifies both the initial default and write default for the specified column. If the data type for the
    column is string, you must surround the default value with single quotes.

    Important

    When you specify a default value for a column, you must specify a static value; you can’t specify an expression or
    function for the value. This requirement is in accordance with the Iceberg v3 specification and applies to both the initial default
    and write default.

    Default values is an Iceberg v3 feature, so you can’t specify a default value for a table that conforms to Iceberg v2. For more
    information about using default values with Iceberg tables, see [Use default values with Iceberg tables](/user-guide/tables-iceberg-manage#label-tables-iceberg-default-values).

    Note

    To change the write default for the column after you create the table, run [ALTER ICEBERG TABLE … ALTER COLUMN … SET WRITE DEFAULT](/sql-reference/sql/alter-iceberg-table).

`PARTITION BY = ( partitionExpression [ , partitionExpression , ... ] )`
:   Specifies one or more [partition expressions](#label-create-iceberg-table-rest-partitionexpressions).

`PATH_LAYOUT = { FLAT | HIERARCHICAL }`
:   Specifies the path layout that Snowflake uses when writing Parquet data files to the table:

    - `FLAT`: Snowflake writes all Parquet data files under the `data/` directory for the table.
    - `HIERARCHICAL`: Snowflake writes partitioned data under the `data/` directory for the table by using a hierarchical
      path layout. With this layout, each partition column is represented
      as a directory level in the path. To define these partition
      columns, use the PARTITION BY parameter. This layout is also called “Hive-style” partitioning.

      If you specify PATH\_LAYOUT = HIERARCHICAL without a PARTITION BY clause,
      Snowflake stores the Parquet data files by using a flat layout path. You can use the
      ALTER ICEBERG TABLE command to set PATH\_LAYOUT for an existing table.

    Note

    For externally managed tables that you create in a standard Snowflake database, Snowflake infers and honors the partitioning scheme
    that is specified by the remote catalog.

    Default: `FLAT`

`MASKING POLICY = policy_name`
:   For creating a table in a [catalog-linked database (preview)](/user-guide/tables-iceberg-catalog-linked-database).

    Specifies the [masking policy](/user-guide/security-column-intro) to set on a column.
    The masking policy must belong to a standard Snowflake database (not the catalog-linked database).

`EXTERNAL_VOLUME = 'external_volume_name'`
:   Specifies the identifier (name) for the external volume where the Iceberg table stores its metadata files and data in Parquet
    format. Iceberg metadata and manifest files store the table schema, partitions, snapshots, and other metadata.

    If you don’t specify this parameter, the Iceberg table defaults to the external volume for the schema, database, or account.
    The schema takes precedence over the database, and the database takes precedence over the account.

`CATALOG = 'catalog_integration_name'`
:   Specifies the identifier (name) of the catalog integration for this table.

    If you don’t specify this parameter, the Iceberg table defaults to the catalog integration for the schema, database, or account.
    The schema takes precedence over the database, and the database takes precedence over the account.

`CATALOG_NAMESPACE = 'catalog_namespace'`
:   - Optionally specifies the namespace (for example, `my_database`) for the
      REST catalog source. By specifying a namespace with the
      catalog integration and then at the table level, you can use a single REST catalog integration to create Iceberg tables across different
      databases. If you don’t specify a namespace with the table, the table uses the default catalog namespace associated with the catalog
      integration.
    - If a default namespace isn’t specified with the catalog integration, you must specify the namespace for the REST catalog source to set
      a catalog namespace for the table.

    Note

    To retrieve a list of tables or namespaces in your remote catalog, you can use the following functions:

    - [SYSTEM$LIST\_ICEBERG\_TABLES\_FROM\_CATALOG](/sql-reference/functions/system_list_iceberg_tables_from_catalog)
    - [SYSTEM$LIST\_NAMESPACES\_FROM\_CATALOG](/sql-reference/functions/system_list_namespaces_from_catalog)
    - [SYSTEM$EXECUTE\_CATALOG\_OPERATION](/sql-reference/functions/system_execute_catalog_operation)

`TARGET_FILE_SIZE = '{ AUTO | 16MB | 32MB | 64MB | 128MB }'`
:   Specifies a target Parquet file size for the table.

    - `'{ 16MB | 32MB | 64MB | 128MB }'` specifies a fixed target file size for the table.
    - `'AUTO'` works differently, depending on the table type:
      - Snowflake-managed tables: AUTO specifies that Snowflake should choose the file size for the table based on table characteristics
        such as size, DML patterns, ingestion workload, and clustering configuration. Snowflake automatically
        adjusts the file size, starting at 16 MB, for better read and write performance in Snowflake. Use this option to optimize table performance
        in Snowflake.
      - Externally managed tables: AUTO specifies that Snowflake should aggressively scale to the largest file size (128 MB).

    For more information, see [Set a target file size](/user-guide/tables-iceberg-manage#label-tables-iceberg-target-file-size).

    Default: AUTO

`MAX_DATA_EXTENSION_TIME_IN_DAYS = integer`
:   Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for the table to
    prevent streams on the table from becoming stale.

    For a detailed description of this parameter, see [MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-max-data-extension-time-in-days).

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
:   Specifies whether Snowflake should automatically poll the external Iceberg catalog that is associated with the table for metadata updates.

    If no value is specified for the `REFRESH_INTERVAL_SECONDS` parameter on the catalog integration, Snowflake uses a default
    refresh interval of 30 seconds.

    For more information, see [automated refresh](/user-guide/tables-iceberg-auto-refresh).

    Default: FALSE

    > Note
    >
    > Using AUTO\_REFRESH with INFER\_SCHEMA isn’t supported.

`COPY GRANTS`
:   Specifies to retain the access privileges from the original table when a new table is created using any of the following
    CREATE TABLE variants:

    - CREATE OR REPLACE TABLE

    The parameter copies all privileges, except OWNERSHIP, from the existing table to the new table. The new table does not
    inherit any future grants defined for the object type in the schema. By default, the role that executes the CREATE TABLE statement
    owns the new table.

    If the parameter is not included in the CREATE ICEBERG TABLE statement, then the new table does not inherit any explicit access
    privileges granted on the original table, but does inherit any future grants defined for the object type in the schema.

    Note:

    - With [data sharing](/guides-overview-sharing):

      - If the existing table was shared to another account, the replacement table is also shared.
      - If the existing table was shared with your account as a data consumer, and access was further granted to other roles in
        the account (using `GRANT IMPORTED PRIVILEGES` on the parent database), access is also granted to the replacement
        table.
    - The [SHOW GRANTS](/sql-reference/sql/show-grants) output for the replacement table lists the grantee for the copied privileges as the
      role that executed the CREATE ICEBERG TABLE statement, with the current timestamp when the statement was executed.
    - The operation to copy grants occurs atomically in the CREATE ICEBERG TABLE command (that is, within the same transaction).

`COMMENT = 'string_literal'`
:   Specifies a comment for the table.

    Default: No value

`PURGE`
:   When combined with `OR REPLACE`, forwards the purge intent to the external Iceberg catalog on the implicit drop
    of the replaced table. Snowflake does not delete data files directly; it forwards the purge intent in the drop-table
    request to the external catalog, which is responsible for removing the old table’s underlying data and metadata
    files from storage.

    `PURGE` is only meaningful with `OR REPLACE`. Using `PURGE` without `OR REPLACE` results in a compilation error.
    `PURGE` can only be used with tables in a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database).

    As an alternative to specifying `PURGE` on each statement, you can set the `PURGE_ON_DROP_TABLE` parameter on
    the table, schema, or catalog-linked database so that every implicit drop caused by `CREATE OR REPLACE TABLE`
    automatically forwards the purge intent to the catalog. For more information, see
    [Dropping an Iceberg table](/user-guide/tables-iceberg-externally-managed-writes#label-tables-iceberg-external-writes-drop-table).

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`BASE_LOCATION = 'path_to_directory_for_table_files'`
:   The path to a directory, which Snowflake uses to construct write paths for the table’s data and metadata files.

    If you use an `EXTERNAL_VOLUME`, this path must be included with the storage paths that are specified for the external volume
    and you have the option to specify a relative path. If you specify a relative path, it is relative to the `STORAGE_BASE_URL`
    for the external volume.
    If not specified, Snowflake constructs a write path
    by using attributes such as the value of the [BASE\_LOCATION\_PREFIX](/sql-reference/parameters#label-base-location-prefix) parameter and
    the table name.

    If you’re using vended credentials, you must also specify an absolute path.

    Note

    This directory can’t be changed after you create a table.

`ICEBERG_VERSION = integer`
:   Specifies the version of the Apache Iceberg™ specification that the table conforms to.

    Caution

    Before you use other engines to upgrade an Iceberg tables format-version in table properties to v3, ensure that the table isn’t used by
    engines or applications that don’t yet support v3. Downgrading format versions isn’t supported in the Apache Iceberg specification. Therefore, all
    readers and writers must support v3. The default version for Iceberg tables in Snowflake is v2, which can be configured to v3 if
    needed. Using Snowflake to perform in-place version upgrades isn’t supported at this time.

    If you don’t set this parameter, the Iceberg table defaults to the Iceberg version for the schema, database, or account. The schema
    takes precedence over the database, and the database takes precedence over the account.

    > - `2`: The table conforms with Iceberg version 2.
    > - `3`: The table conforms with Iceberg version 3.
    >
    > Default: `2`
    >
    > For more information about this parameter, see [ICEBERG\_VERSION](/sql-reference/parameters#label-iceberg-version).

`ICEBERG_MERGE_ON_READ_BEHAVIOR = { 'AUTO' | 'ENABLED' | 'DISABLED' }`
:   Specifies how Snowflake performs row-level updates (UPDATE, DELETE, MERGE) on this Apache Iceberg™ table. Selects between merge-on-read
    (which writes Iceberg delete files alongside the data) and copy-on-write (which rewrites entire data files).

    If you don’t set this parameter, the Iceberg table inherits the setting from the schema, database, or account. The schema takes
    precedence over the database, and the database takes precedence over the account.

    The parameter values are case-insensitive.

    Values:
    :   `'AUTO'`: Snowflake selects merge-on-read or copy-on-write based on the table’s Iceberg format version and management mode. For details,
        see [ICEBERG\_MERGE\_ON\_READ\_BEHAVIOR parameter](/user-guide/tables-iceberg-manage#label-iceberg-merge-on-read-behavior).

        `'ENABLED'`: The table uses merge-on-read. For tables that conform to v2 of the Apache Iceberg™ table specification, Snowflake writes positional
        delete files for row-level deletes. For tables that conform to v3, Snowflake writes deletion vectors when conditions are met.

        `'DISABLED'`: The table uses copy-on-write for all DML operations.

    Default:
    :   `'AUTO'`

    For a detailed description of this parameter, see [ICEBERG\_MERGE\_ON\_READ\_BEHAVIOR parameter](/user-guide/tables-iceberg-manage#label-iceberg-merge-on-read-behavior).

`ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE }`
:   Warning

    This parameter is deprecated. Use [`ICEBERG_MERGE_ON_READ_BEHAVIOR`](/user-guide/tables-iceberg-manage#label-iceberg-merge-on-read-behavior) instead.
    The legacy parameter is still honored when `ICEBERG_MERGE_ON_READ_BEHAVIOR` is at its default (`'AUTO'`), but it will return an
    error in a future release.

    Specifies whether the table uses merge-on-read behavior.

    If you don’t set this parameter, the Iceberg table defaults to the merge-on-read behavior that is specified for the schema, database,
    or account. The schema takes precedence over the database, and the database takes precedence over the account.

    Values:

    `TRUE`: The table uses merge-on-read behavior. Depending on whether the table conforms to v2 or v3 of the
    Apache Iceberg™ table specification, the behavior is as described in the following list:

    - If the table conforms with v2, Snowflake uses positional delete files for row-level deletes.
    - If the table conforms with v3, Snowflake uses deletion vectors for row-level deletes when conditions are met.

    **Note:** Setting this parameter to `TRUE` does **not** enable merge-on-read for Snowflake-managed v2 Iceberg tables. When `ICEBERG_MERGE_ON_READ_BEHAVIOR` is at its default (`'AUTO'`), this setting routes through the auto matrix, which keeps Snowflake-managed v2 tables on copy-on-write. To enable merge-on-read for a Snowflake-managed v2 table, set `ICEBERG_MERGE_ON_READ_BEHAVIOR = 'ENABLED'` on the table, schema, database, or account.

    `FALSE`: The table uses copy-on-write behavior.

    Default: `TRUE`

    For a detailed description of this parameter, see [Deprecated: ENABLE\_ICEBERG\_MERGE\_ON\_READ](/user-guide/tables-iceberg-manage#label-enable-iceberg-merge-on-read).

`WITH CONTACT ( purpose = contact [ , purpose = contact ...] )`
:   Associate the new object with one or more [contacts](/user-guide/contacts-using).

    Specify the WITH CONTACT clause after all other clauses except the AS clause (if that clause is supported by this command).

## Partition expression parameters (`partitionExpression`)

Snowflake supports all partition transforms in version 2 of the Apache Iceberg specification. For more information, see
[Partition Transforms](https://iceberg.apache.org/spec/#partition-transforms).

For more information about partitioning Iceberg tables, see [Iceberg partitioning](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning).

`col_name`
:   Specifies the identifier (name) for the source column to partition.

    When used alone, without a transform such as YEAR, specifies an identity transform on the source column.
    For more information, see [identity](https://iceberg.apache.org/spec/#partition-transforms).

`BUCKET`
:   Specifies a bucket transform. For more information, see [Bucket Transform Details](https://iceberg.apache.org/spec/#bucket-transform-details).

    `num_buckets` is the number of buckets to group the data into.

`TRUNCATE`
:   Specifies a truncate transform, which partitions the data based on the truncated values of the specified source column.
    For more information, see [Truncate Transform Details](https://iceberg.apache.org/spec/#truncate-transform-details).

`YEAR`
:   Specifies a year transform, which extracts the year from a date or timestamp source-column value.
    For more information, see [Partition Transforms](https://iceberg.apache.org/spec/#partition-transforms).

`MONTH`
:   Specifies a month transform.
    For more information, see [Partition Transforms](https://iceberg.apache.org/spec/#partition-transforms).

`DAY`
:   Specifies a day transform, which extracts the day from a date or timestamp source-column value.
    For more information, see [Partition Transforms](https://iceberg.apache.org/spec/#partition-transforms).

`HOUR`
:   Specifies an hour transform, which extracts the hour from a timestamp source-column value.
    For more information, see [Partition Transforms](https://iceberg.apache.org/spec/#partition-transforms).

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

- If you created your external volume or catalog integration using a double-quoted identifier,
  you must specify the identifier exactly as created (including the double quotes) in your CREATE ICEBERG TABLE statement.
  Failure to include the quotes might result in an `Object does not exist` error or
  a similar type of error.
- In a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database), the `OR REPLACE` option performs a non-atomic operation,
  which in this case is a DROP operation followed by CREATE, in your external Iceberg catalog. The new table has a new `table-uuid`.
  In a standard Snowflake database (not linked to a catalog), `OR REPLACE` drops and recreates only the Snowflake table object;
  the table in the remote catalog is unchanged.
- By default, the implicit drop does not signal the catalog to delete the replaced
  table’s data files. Specify `PURGE` (or set `PURGE_ON_DROP_TABLE` on the table, schema, or database) to forward
  the purge intent to the catalog on the implicit drop. Snowflake never deletes external data files directly. The
  catalog is responsible for the actual file deletion.
- For creating an [Iceberg table with write support](/user-guide/tables-iceberg-externally-managed-writes):

  - If you use a standard Snowflake database, you must first create an Iceberg table in your remote catalog. For example, you might use Spark to write
    an Iceberg table to Open Catalog. Don’t specify column definitions in your CREATE ICEBERG TABLE statement.
  - If you use a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database), you must specify column definitions when you create the table.
    Alternatively, you can write to Iceberg tables that Snowflake automatically discovers in your remote catalog.
- The TARGET\_FILE\_SIZE property is only supported for tables with [write support (preview)](/user-guide/tables-iceberg-externally-managed-writes).
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
- Using variant syntax:

  - CREATE ICEBERG TABLE … LIKE:

    - For [partitioned Iceberg tables](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning), the partitioning of the source table is ignored. To
      override this behavior, specify the PARTITION BY clause with the command.
  - CREATE ICEBERG TABLE … CLONE:

    - For [partitioned Iceberg tables](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning), the cloned table retains the partitioning information of
      the source table.
  - CREATE ICEBERG TABLE (catalog-linked database) … AS SELECT:

    - Currently not supported if you use AWS Glue as your remote catalog.

      Alternatively, you can use the [CREATE ICEBERG TABLE (Iceberg REST catalog)](/sql-reference/sql/create-iceberg-table-rest) syntax to create an empty Iceberg table and then use
      an [INSERT INTO … SELECT](/sql-reference/sql/insert) statement to insert data into the empty table. However, this alternative
      uses two separate transactions, so it doesn’t guarantee atomicity.
- Using default values:

  - You can’t use expressions or functions, such as CURRENT\_TIMESTAMP(), for default values on v3 Iceberg tables. Only constant values are
    permitted in the Apache Iceberg v3 table specification.
    - For v2 Iceberg tables, you can use expressions such as CURRENT\_TIMESTAMP() with Snowflake. However, this property isn’t persisted into
      Iceberg metadata because the default values specification was introduced in version 3. Columns in v2 Iceberg tables with default values as
      expressions are only used with Snowflake, but the table remains interoperable with other engines and compliant with the
      version 2 specification.

  - Using default values with CREATE ICEBERG TABLE (catalog-linked database) … *is* supported.
  - Using default values with CREATE ICEBERG TABLE (catalog-linked database) … AS SELECT *isn’t* supported.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

### Create an Iceberg table that uses a remote Iceberg REST catalog

Copy code

```
CREATE OR REPLACE ICEBERG TABLE my_iceberg_table
  EXTERNAL_VOLUME = 'my_external_volume'
  CATALOG = 'my_rest_catalog_integration'
  CATALOG_TABLE_NAME = 'my_remote_table'
  AUTO_REFRESH = TRUE;
```

### Create an Iceberg table to query a table in Snowflake Open Catalog

This example creates an Iceberg table that you can use to
[Query a table in Snowflake Open Catalog using Snowflake](/user-guide/tables-iceberg-open-catalog-query).

Copy code

```
CREATE ICEBERG TABLE open_catalog_iceberg_table
  EXTERNAL_VOLUME = 'my_external_volume'
  CATALOG = 'open_catalog_int'
  CATALOG_TABLE_NAME = 'my_open_catalog_table'
  AUTO_REFRESH = TRUE;
```

### Create an Iceberg table in a catalog-linked database

The following example creates a writable Iceberg table in a
[catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database)
with column definitions:

Copy code

```
USE DATABASE my_catalog_linked_db;

USE SCHEMA 'my_namespace';

CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (
  first_name string,
  last_name string,
  amount int,
  create_date date
);
```

### Create a partitioned table in a catalog-linked database

The following example creates an [externally managed Iceberg table](/user-guide/tables-iceberg-externally-managed-writes)
by using the value of a timestamp column named `start_date` to
partition the table by day:

Copy code

```
USE DATABASE my_catalog_linked_db;

USE SCHEMA 'my_namespace';

CREATE OR REPLACE ICEBERG TABLE iceberg_partitioned_date_time (start_date timestamp)
  PARTITION BY (DAY(start_date));
```

You can insert data into the table by using supported table-loading features. For example, use an INSERT INTO statement to
insert the following data into the empty `iceberg_partitioned_date_time` table created previously:

Copy code

```
INSERT INTO iceberg_partitioned_date_time (start_date)
  VALUES
    (to_timestamp_ntz('2023-01-02 00:00:00')),
    (to_timestamp_ntz('2023-02-03 00:00:00')),
    (to_timestamp_ntz('2023-01-02 01:00:00')),
    (to_timestamp_ntz('2023-02-03 02:00:00'));
```

For more information, see [Iceberg partitioning](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning).

### Create an externally managed Iceberg v3 table

Note

For more information about other Iceberg v3 features that Snowflake supports, see [Apache Iceberg™ tables: Support for Apache Iceberg™ v3](/user-guide/tables-iceberg-v3-specification-support).

The following example creates an Apache Iceberg™ table that uses a remote Iceberg REST catalog and conforms to v3 of the Apache Iceberg™ specification:

Note

You don’t need to specify `ICEBERG_VERSION = 3` with the command because the format version is already defined in the
external catalog’s metadata, so Snowflake retrieves this version from the metadata.

Copy code

```
CREATE ICEBERG TABLE my_v3_iceberg_table
  EXTERNAL_VOLUME = 'my_external_volume'
  CATALOG = 'my_rest_catalog_integration'
  CATALOG_TABLE_NAME = 'my_remote_table'
  AUTO_REFRESH = TRUE;
```

### Create an Iceberg v3 table in a catalog-linked database

Note

For more information about other Iceberg v3 features that Snowflake supports, see [Apache Iceberg™ tables: Support for Apache Iceberg™ v3](/user-guide/tables-iceberg-v3-specification-support).

The following example creates a writable Iceberg table in a
[catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database)
with column definitions and conforms to v3 of the Apache Iceberg™ specification:

Copy code

```
USE DATABASE my_catalog_linked_db;

USE SCHEMA 'my_namespace';

CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (
  first_name string,
  last_name string,
  amount int,
  create_date date
)
  ICEBERG_VERSION = 3;
```

### Create a partitioned table in a catalog-linked database with hierarchical path layout

The following example creates an [externally managed Iceberg table](/user-guide/tables-iceberg-externally-managed-writes)
by using the value of a timestamp column named `start_date` to
partition the table by day. Because PATH\_LAYOUT = HIERARCHICAL, Snowflake writes data to the partitioned Iceberg table by using a hierarchical
path layout for files where partitioning information is included in the file paths:

Copy code

```
USE DATABASE my_catalog_linked_db;

USE SCHEMA 'my_namespace';

CREATE OR REPLACE ICEBERG TABLE iceberg_partitioned_date_time (start_date timestamp)
  PARTITION BY (DAY(start_date))
  PATH_LAYOUT = HIERARCHICAL;
```

You can insert data into the table by using supported table-loading features. For example, use an INSERT INTO statement to
insert the following data into the empty `iceberg_partitioned_date_time` table created previously:

Copy code

```
INSERT INTO iceberg_partitioned_date_time (start_date)
  VALUES
    (to_timestamp_ntz('2023-01-02 00:00:00')),
    (to_timestamp_ntz('2023-02-03 00:00:00')),
    (to_timestamp_ntz('2023-01-02 01:00:00')),
    (to_timestamp_ntz('2023-02-03 02:00:00'));
```

For more information, see [Partitioning with hierarchical paths](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning-hierarchical-paths).
