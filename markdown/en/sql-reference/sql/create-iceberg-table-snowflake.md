# CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)

Creates or replaces an [Apache Iceberg™ table](/user-guide/tables-iceberg) that uses
[Snowflake as the Iceberg catalog](/user-guide/tables-iceberg#label-tables-iceberg-snowflake-as-catalog)
in the current/specified schema.

This command supports the following variants:

- CREATE ICEBERG TABLE … AS SELECT (creates a populated table; also referred to as CTAS)
- CREATE ICEBERG TABLE … LIKE (creates an empty copy of an existing table)

This topic refers to Iceberg tables as simply “tables” except where specifying *Iceberg tables* avoids confusion.

Note

To store Iceberg data and metadata in **your** cloud storage, create an [external volume](/sql-reference/sql/create-external-volume) and reference it from the table.
For instructions, see [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume).

To use **Snowflake Storage** instead, set `EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'` (or rely on defaults when the catalog is Snowflake). You don’t need to create a separate external volume object in this case.
For more information, see [Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-internal-storage).

See also:
:   [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table) , [DROP ICEBERG TABLE](/sql-reference/sql/drop-iceberg-table) , [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) , [DESCRIBE ICEBERG TABLE](/sql-reference/sql/desc-iceberg-table) , [UNDROP ICEBERG TABLE](/sql-reference/sql/undrop-iceberg-table)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] [ TRANSIENT ] ICEBERG TABLE [ IF NOT EXISTS ] <table_name> (
    -- Column definition
    <col_name> <col_type> [ DEFAULT <col_default> ]
      [ inlineConstraint ]
      [ NOT NULL ]
      [ [ WITH ] MASKING POLICY <policy_name> [ USING ( <col_name> , <cond_col1> , ... ) ] ]
      [ [ WITH ] PROJECTION POLICY <policy_name> ]
      [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
      [ COMMENT '<string_literal>' ]

    -- Additional column definitions
    [ , <col_name> <col_type> [ DEFAULT <col_default> ] [ ... ] ]

    -- Out-of-line constraints
    [ , outoflineConstraint [ ... ] ]
  )
  [ PARTITION BY ( partitionExpression [, partitionExpression , ...] ) ]
  [ PATH_LAYOUT = { FLAT | HIERARCHICAL } ]
  [ CLUSTER BY ( <expr> [ , <expr> , ... ] ) ]
  [ EXTERNAL_VOLUME = '<external_volume_name>' ]
  [ CATALOG = 'SNOWFLAKE' ]
  [ BASE_LOCATION = '<directory_for_table_files>' ]
  [ TARGET_FILE_SIZE = '{ AUTO | 16MB | 32MB | 64MB | 128MB }' ]
  [ CATALOG_SYNC = '<open_catalog_integration_name>']
  [ STORAGE_SERIALIZATION_POLICY = { COMPATIBLE | OPTIMIZED } ]
  [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
  [ CHANGE_TRACKING = { TRUE | FALSE } ]
  [ COPY GRANTS ]
  [ COPY TAGS ]
  [ ERROR_LOGGING = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]
  [ ICEBERG_VERSION = <integer> ]
  [ ICEBERG_MERGE_ON_READ_BEHAVIOR = { 'AUTO' | 'ENABLED' | 'DISABLED' } ]
  [ ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE } ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
  [ [ WITH ] AGGREGATION POLICY <policy_name> ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]
  [ ENABLE_DATA_COMPACTION = { TRUE | FALSE } ]
```

Where:

> Copy code
>
> ```
> inlineConstraint ::=
>   [ CONSTRAINT <constraint_name> ]
>   {   UNIQUE
>     | PRIMARY KEY
>     | [ FOREIGN KEY ] REFERENCES <ref_table_name> [ ( <ref_col_name> ) ]
>     | CHECK ( <expr> )
>   }
>   [ <constraint_properties> ]
> ```
>
> For additional inline constraint details, see [Create Table Constraint](create-table-constraint).
>
> Copy code
>
> ```
> outoflineConstraint ::=
>   [ CONSTRAINT <constraint_name> ]
>   {   UNIQUE [ ( <col_name> [ , <col_name> , ... ] ) ]
>     | PRIMARY KEY [ ( <col_name> [ , <col_name> , ... ] ) ]
>     | [ FOREIGN KEY ] [ ( <col_name> [ , <col_name> , ... ] ) ]
>       REFERENCES <ref_table_name> [ ( <ref_col_name> [ , <ref_col_name> , ... ] ) ]
>     | CHECK ( <expr> )
>   }
>   [ <constraint_properties> ]
> ```
>
> Note
>
> - Snowflake represents columns defined as PRIMARY KEY as identifier fields in the Iceberg metadata. The IDs for these columns are populated
>   in the metadata as [identifier field IDs](https://iceberg.apache.org/spec/#identifier-field-ids).
> - Snowflake doesn’t enforce NOT NULL and UNIQUE constraints on PRIMARY KEY columns for Iceberg tables.
>
> For additional out-of-line constraint details, see [Create Table Constraint](create-table-constraint).
>
> Copy code
>
> ```
> partitionExpression ::=
>   <col_name> -- identity transform
>   | BUCKET ( <num_buckets> , <col_name> )
>   | TRUNCATE ( <width> , <col_name> )
>   | YEAR ( <col_name> )
>   | MONTH ( <col_name> )
>   | DAY ( <col_name> )
>   | HOUR ( <col_name> )
> ```

## Variant syntax

### CREATE ICEBERG TABLE … AS SELECT (also referred to as CTAS)

Creates a new table populated with the data returned by a query. Place the AS SELECT clause at the end of the statement.

> Copy code
>
> ```
> CREATE [ OR REPLACE ] [ TRANSIENT ] ICEBERG TABLE <table_name> [ ( <col_name> [ <col_type> ] [ DEFAULT <col_default> ] , <col_name> [ <col_type> ] [ DEFAULT <col_default> ] , ... ) ]
>   [ CLUSTER BY ( <expr> [ , <expr> , ... ] ) ]
>   [ EXTERNAL_VOLUME = '<external_volume_name>' ]
>   [ CATALOG = 'SNOWFLAKE' ]
>   [ BASE_LOCATION = '<relative_path_from_external_volume>' ]
>   [ COPY GRANTS ]
>   [ COPY TAGS ]
>   [ ICEBERG_VERSION = <integer> ]
>   [ ICEBERG_MERGE_ON_READ_BEHAVIOR = { 'AUTO' | 'ENABLED' | 'DISABLED' } ]
>   [ ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE } ]
>   [ ... ]
>   AS SELECT <query>
> ```

A masking policy can be applied to a column in a CTAS statement. Specify the masking policy after the column data type. Similarly, a
row access policy can be applied to the table. For example:

> Copy code
>
> ```
> CREATE ICEBERG TABLE <table_name> ( <col1> <data_type> [ DEFAULT <col_default> ] [ WITH ] MASKING POLICY <policy_name> [ , ... ] )
>   [ EXTERNAL_VOLUME = '<external_volume_name>' ]
>   [ CATALOG = 'SNOWFLAKE' ]
>   [ BASE_LOCATION = '<directory_for_table_files>' ]
>   [ ICEBERG_VERSION = <integer> ]
>   [ ICEBERG_MERGE_ON_READ_BEHAVIOR = { 'AUTO' | 'ENABLED' | 'DISABLED' } ]
>   [ ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE } ]
>   [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col1> [ , ... ] )
>   [ ... ]
>   AS SELECT <query>
> ```

Note

In a CTAS, the COPY GRANTS parameter is valid only when combined with the OR REPLACE clause. COPY GRANTS copies
privileges from the table being replaced with CREATE OR REPLACE (if it already exists), not from the source
table(s) being queried in the SELECT statement. CTAS with COPY GRANTS lets you overwrite a table with a new
set of data while keeping existing grants on that table.

For more information about the COPY GRANTS parameter, see [COPY GRANTS](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-copy-grants) in this document.

For more information about this variant syntax, see the [usage notes](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-variant-usage-notes).

### CREATE ICEBERG TABLE … LIKE

Creates a new table with the same column definitions as an existing table, but without copying data from the existing table. Column
names, types, defaults, and constraints are copied to the new table:

> Copy code
>
> ```
> CREATE [ OR REPLACE ] [ TRANSIENT ] ICEBERG TABLE <table_name> LIKE <source_table>
>   [ CLUSTER BY ( <expr> [ , <expr> , ... ] ) ]
>   [ COPY GRANTS ]
>   [ COPY TAGS ]
>   [ ... ]
> ```

For more information about the COPY GRANTS parameter, see [COPY GRANTS](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-copy-grants) in this document.

> Note
>
> CREATE TABLE … LIKE isn’t supported for tables with an auto-increment sequence accessed through a data share.

For more information about this variant syntax, see the [usage notes](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-variant-usage-notes).

### CREATE ICEBERG TABLE … CLONE

Creates a new Iceberg table with the same column definitions and containing all the existing data from the source table, without actually
copying the data. You can also use this variant to clone a table at a specific time or point in the past (using
[Time Travel](/user-guide/data-time-travel)):

> Copy code
>
> ```
> CREATE [ OR REPLACE ] ICEBERG TABLE [ IF NOT EXISTS ] <name>
>   CLONE <source_iceberg_table>
>     [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ]
>     [COPY GRANTS]
>     [COPY TAGS]
>     ...
> ```

Note

If the statement replaces an existing Iceberg table of the same name, Snowflake copies the grants from the table
being replaced. If there is no existing table of that name, Snowflake copies the grants from the source table
being cloned.

For more information about the COPY GRANTS parameter, see [COPY GRANTS](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-copy-grants) in this document.

For more information about cloning, see [CREATE <object> … CLONE](/sql-reference/sql/create-clone) and [Cloning and Apache Iceberg™ tables](/user-guide/object-clone#label-cloning-and-iceberg-tables).

## Required parameters

`table_name`
:   Specifies the identifier (name) for the table; must be unique for the schema in which the table is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`col_name`
:   Specifies the column identifier (name). All the requirements for table identifiers also apply to column identifiers.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax) and [Reserved & limited keywords](/sql-reference/reserved-keywords).

    Note

    In addition to the standard reserved keywords, the following keywords cannot be used as column identifiers because they are
    reserved for ANSI-standard context functions:

    - `CURRENT_DATE`
    - `CURRENT_ROLE`
    - `CURRENT_TIME`
    - `CURRENT_TIMESTAMP`
    - `CURRENT_USER`

    For the list of reserved keywords, see [Reserved & limited keywords](/sql-reference/reserved-keywords).

`col_type`
:   Specifies the data type for the column.

    For information about the data types that can be specified for table columns, see [Data types for Apache Iceberg™ tables](/user-guide/tables-iceberg-data-types).

    Note

    You can’t use `float` or `double` as primary keys (in accordance with the
    [Apache Iceberg spec](https://iceberg.apache.org/spec/#identifier-field-ids)).

## Optional parameters

`TRANSIENT`

> Creates a transient Iceberg table. Transient tables don’t have a [Fail-safe](/user-guide/data-failsafe) period, so they don’t incur
> Fail-safe storage costs.
>
> For Iceberg tables that use Snowflake-provided storage (`EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'`), the TRANSIENT keyword determines whether
> the table data is protected by Fail-safe. For more information, see [Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-internal-storage).
>
> Note
>
> Transient Iceberg tables are only supported with Snowflake-provided storage (`EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'`). You cannot
> create a transient Iceberg table with any other external volume.

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

`BASE_LOCATION = 'directory_for_table_files'`
:   The path to a directory, which Snowflake uses to construct write paths for the table’s data and metadata files.
    Specify a relative path from the table’s `EXTERNAL_VOLUME` location.

    If not specified, Snowflake constructs a write path
    using attributes such as the value of the [BASE\_LOCATION\_PREFIX](/sql-reference/parameters#label-base-location-prefix) parameter and
    the table name.

    For more information, see [Data and metadata directories](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-configure-external-volume-base-location).

    This directory can’t be changed after you create a table.

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

`CONSTRAINT ...`
:   Defines an inline or out-of-line constraint for the specified column(s) in the table.

    For syntax information, see [CREATE | ALTER TABLE … CONSTRAINT](/sql-reference/sql/create-table-constraint). For more information about constraints, see [Constraints](/sql-reference/constraints).

`MASKING POLICY = policy_name`
:   Specifies the [masking policy](/user-guide/security-column-intro) to set on a column.

`PROJECTION POLICY policy_name`
:   Specifies the [projection policy](/user-guide/projection-policies) to set on a column.

`COMMENT 'string_literal'`
:   Specifies a comment for the column.

    (Note that comments can be specified at the column level or the table level. The syntax for each is slightly different.)

`USING ( col_name , cond_col_1 ... )`
:   Specifies the arguments to pass into the SQL expression for the conditional masking policy.

    The first column in the list specifies the column for the policy conditions to mask or tokenize the data and must match the
    column to which the masking policy is set.

    The additional columns specify the columns to evaluate to determine whether to mask or tokenize the data in each row of the query result
    when a query selects from the first column.

    If the USING clause is omitted, Snowflake treats the conditional masking policy as a normal
    [masking policy](/user-guide/security-column-intro).

`PARTITION BY = ( partitionExpression [ , partitionExpression , ... ] )`
:   Specifies one or more [partition expressions](#label-create-iceberg-table-snowflake-partitionexpressions).

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

`CLUSTER BY ( expr [ , expr , ... ] )`
:   Specifies one or more columns or column expressions in the table as the clustering key. For more information, see
    [Clustering Keys & Clustered Tables](/user-guide/tables-clustering-keys).

    When using variant syntax (LIKE, AS SELECT), see the [variant syntax usage notes](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-variant-usage-notes).

    Default: No value (no clustering key is defined for the table)

    Important

    Clustering keys are not intended or recommended for all tables; they typically benefit very large (that is, multi-terabyte)
    tables.

    Before you specify a clustering key for a table, you should understand micro-partitions.
    For more information, see [Understanding Snowflake Table Structures](/user-guide/tables-micro-partitions).

`EXTERNAL_VOLUME = 'external_volume_name'`
:   Specifies where the Iceberg table stores its metadata files and data in Parquet format. Iceberg metadata and manifest files store the table schema, partitions, snapshots, and other metadata.

    Use one of the following:

    - The identifier for an [external volume](/sql-reference/sql/create-external-volume) that you created in your account. Iceberg data and metadata are stored in your cloud storage according to that volume’s storage locations.
    - The reserved value `SNOWFLAKE_MANAGED` to use Snowflake-provided storage. `SNOWFLAKE_MANAGED` is not a user-created external volume object; you don’t run `CREATE EXTERNAL VOLUME` for it. For more information, see [Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-internal-storage).

    If you don’t specify this parameter, the Iceberg table defaults to the external volume for the schema, database, or account.
    The schema takes precedence over the database, and the database takes precedence over the account.
    When the effective catalog is Snowflake (`CATALOG = 'SNOWFLAKE'`), the default external volume is `SNOWFLAKE_MANAGED` unless a different default is set at the schema, database, or account level.

`CATALOG = 'SNOWFLAKE'`
:   Specifies Snowflake as the Iceberg catalog. Snowflake handles all life-cycle maintenance, such as compaction, for the table.

`CATALOG_SYNC = 'open_catalog_integration_name'`
:   Optionally specifies the name of a catalog integration configured for [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview). If specified, Snowflake syncs
    the table with an external catalog in your Snowflake Open Catalog account. For more information about syncing Snowflake-managed Iceberg tables with Open Catalog, see [Sync a Snowflake-managed table with Snowflake Open Catalog](/user-guide/tables-iceberg-open-catalog-sync).

    For more information about this parameter, see [CATALOG\_SYNC](/sql-reference/parameters#label-catalog-sync).

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

`STORAGE_SERIALIZATION_POLICY = { COMPATIBLE | OPTIMIZED }`
:   Specifies the storage serialization policy for the table.
    If not specified at table creation, the table inherits the value set at the schema, database, or account level. If the value isn’t
    specified at any level, the table uses the default value.

    You can’t change the value of this parameter after table creation.

    - `COMPATIBLE`: Snowflake performs encoding and compression that ensures interoperability with third-party compute engines.
    - `OPTIMIZED`: Snowflake performs encoding and compression that ensures the best table performance within Snowflake.

    Default: `OPTIMIZED`

`DATA_RETENTION_TIME_IN_DAYS = integer`
:   Specifies the retention period for a Snowflake-managed table so that Time Travel actions (SELECT, CLONE, UNDROP) can be performed on historical
    data in the table. For more information, see [Understanding & using Time Travel](/user-guide/data-time-travel).

    For a detailed description of this object-level parameter, as well as more information about object parameters, see
    [Parameters](/sql-reference/parameters).

    Values:

    > - Standard Edition: `0` or `1`
    > - Enterprise Edition: `0` to `90` for permanent tables

    Default:

    > - Standard Edition: `1`
    > - Enterprise Edition (or higher): `1` (unless a different default value was specified at the schema, database, or account level)

    Note

    A value of `0` effectively disables Time Travel for the table.

`MAX_DATA_EXTENSION_TIME_IN_DAYS = integer`
:   Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for the table to
    prevent streams on the table from becoming stale.

    For a detailed description of this parameter, see [MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-max-data-extension-time-in-days).

`CHANGE_TRACKING = { TRUE | FALSE }`
:   Specifies whether to enable change tracking on the table.

    - `TRUE` enables change tracking on the table. This setting adds a pair of hidden columns to the source table and begins
      storing change tracking metadata in the columns. These columns consume a small amount of storage.

      The change tracking metadata can be queried using the [CHANGES](/sql-reference/constructs/changes) clause for
      [SELECT](/sql-reference/sql/select) statements, or by creating and querying one or more streams on the table.
    - `FALSE` does not enable change tracking on the table.

    Default: FALSE

`COPY GRANTS`
:   Specifies to retain the access privileges from the original table when a new table is created using any of the following
    CREATE TABLE variants:

    > - CREATE OR REPLACE TABLE
    > - CREATE TABLE … LIKE
    > - CREATE TABLE … CLONE

    The parameter copies all privileges, except OWNERSHIP, from the existing table to the new table. The new table does not
    inherit any future grants defined for the object type in the schema. By default, the role that executes the CREATE TABLE statement
    owns the new table.

    If the parameter is not included in the CREATE ICEBERG TABLE statement, then the new table does not inherit any explicit access
    privileges granted on the original table, but does inherit any future grants defined for the object type in the schema.

    Note:

    > - With [data sharing](/guides-overview-sharing):
    >
    >   - If the existing table was shared to another account, the replacement table is also shared.
    >   - If the existing table was shared with your account as a data consumer, and access was further granted to other roles in
    >     the account (using `GRANT IMPORTED PRIVILEGES` on the parent database), access is also granted to the replacement
    >     table.
    > - The [SHOW GRANTS](/sql-reference/sql/show-grants) output for the replacement table lists the grantee for the copied privileges as the
    >   role that executed the CREATE ICEBERG TABLE statement, with the current timestamp when the statement was executed.
    > - The operation to copy grants occurs atomically in the CREATE ICEBERG TABLE command (that is, within the same transaction).

`COPY TAGS`
:   Applies [tags](/user-guide/object-tagging/introduction) when you use any of these CREATE ICEBERG TABLE forms:

    > - CREATE OR REPLACE ICEBERG TABLE
    > - CREATE ICEBERG TABLE … LIKE
    > - CREATE ICEBERG TABLE … CLONE

    If the statement uses CREATE OR REPLACE ICEBERG TABLE … COPY TAGS without LIKE, CLONE, or a WITH TAG clause, tags from the replaced
    table and its columns are retained on the new table.

    If the statement uses LIKE, CLONE, or WITH TAG together with COPY TAGS, Snowflake combines tags from the applicable sources. If both
    sources set the same tag, the value from the replaced table (carried over by COPY TAGS) takes precedence.

    For more information, including the effect when you alter columns in the CREATE OR REPLACE statement, see
    [the usage notes for COPY TAGS](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-usage-notes-copy-tags).

`ERROR_LOGGING = { TRUE | FALSE }`
:   Specifies whether to turn on DML error logging for the table.

    - `TRUE` turns on DML error logging for the table.
    - `FALSE` turns off DML error logging for the table.

    For more information, see [DML error logging](/user-guide/data-load-overview#label-data-load-overview-dml-error-logging).

    Note

    If the [OPT\_OUT\_ERROR\_LOGGING](/sql-reference/parameters#label-opt-out-error-logging) parameter is set to `TRUE` for a session,
    DML error logging isn’t turned on, regardless of whether it is turned on for specific tables.

`COMMENT = 'string_literal'`
:   Specifies a comment. You can specify a comment at the column level or the table level.
    The syntax for each is slightly different.

    Default: No value

`WITH CONTACT ( purpose = contact [ , purpose = contact ...] )`
:   Associate the new object with one or more [contacts](/user-guide/contacts-using).

    Specify the WITH CONTACT clause after all other clauses except the AS clause (if that clause is supported by this command).

`ROW ACCESS POLICY policy_name ON ( col_name [ , col_name ... ] )`
:   Specifies the [row access policy](/user-guide/security-row-intro) to set on a table.

`AGGREGATION POLICY policy_name`
:   Specifies the [aggregation policy](/user-guide/aggregation-policies) to set on a table.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`ENABLE_DATA_COMPACTION = { TRUE | FALSE }`
:   Specifies whether Snowflake should enable data compaction on the table.

    - `TRUE`: Snowflake performs data compaction on the table.
    - `FALSE`: Snowflake doesn’t perform data compaction on the table.

    Default: `TRUE`

    For more information, see [ENABLE\_DATA\_COMPACTION](/sql-reference/parameters#label-enable-data-compaction) and [Set data compaction](/user-guide/tables-iceberg-manage#label-tables-iceberg-manage-set-data-compaction).

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
:   Specifies how Snowflake performs row-level updates (UPDATE, DELETE, MERGE) on Apache Iceberg™ tables. Selects between merge-on-read
    (which writes Iceberg delete files alongside the data) and copy-on-write (which rewrites entire data files).

    The parameter values are case-insensitive.

    Values:
    :   `'AUTO'`: Snowflake selects merge-on-read or copy-on-write based on the table’s Iceberg format version and management mode. For details,
        see [ICEBERG\_MERGE\_ON\_READ\_BEHAVIOR parameter](/user-guide/tables-iceberg-manage#label-iceberg-merge-on-read-behavior).

        `'ENABLED'`: Merge-on-read is enabled for all Apache Iceberg™ tables to which this parameter applies, regardless of format version or management
        mode.

        `'DISABLED'`: Merge-on-read is disabled for all Apache Iceberg™ tables to which this parameter applies. All DML uses copy-on-write.

    Default:
    :   `'AUTO'`

    For a detailed description of this parameter, see [ICEBERG\_MERGE\_ON\_READ\_BEHAVIOR parameter](/user-guide/tables-iceberg-manage#label-iceberg-merge-on-read-behavior). For more information about merge-on-read
    and copy-on-write behavior in Snowflake, see [Use row-level deletes](/user-guide/tables-iceberg-manage#label-tables-iceberg-row-level-deletes).

`ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE }`
:   Warning

    This parameter is deprecated. Use [`ICEBERG_MERGE_ON_READ_BEHAVIOR`](/user-guide/tables-iceberg-manage#label-iceberg-merge-on-read-behavior) instead.
    The legacy parameter is still honored when `ICEBERG_MERGE_ON_READ_BEHAVIOR` is at its default (`'AUTO'`), but it will return an
    error in a future release.

    Specifies whether to enable merge-on-read behavior for Apache Iceberg™ tables.

    Values:
    :   `TRUE`: New tables use merge-on-read behavior. For **v2** tables, Snowflake uses positional delete files for row-level deletes. For **v3** tables, Snowflake uses deletion vectors when conditions are met.

        **Note:** Setting this parameter to `TRUE` does **not** enable merge-on-read for Snowflake-managed v2 Iceberg tables. When `ICEBERG_MERGE_ON_READ_BEHAVIOR` is at its default (`'AUTO'`), this setting routes through the auto matrix, which keeps Snowflake-managed v2 tables on copy-on-write. To enable merge-on-read for Snowflake-managed v2 tables, set `ICEBERG_MERGE_ON_READ_BEHAVIOR = 'ENABLED'` explicitly.

        `FALSE`: New tables use copy-on-write behavior.

    Default:
    :   `TRUE`

    For a detailed description of this parameter, see [Deprecated: ENABLE\_ICEBERG\_MERGE\_ON\_READ](/user-guide/tables-iceberg-manage#label-enable-iceberg-merge-on-read). For more information about merge-on-read
    and copy-on-write behavior in Snowflake, see [Use row-level deletes](/user-guide/tables-iceberg-manage#label-tables-iceberg-row-level-deletes).

## Partition expression parameters (`partitionExpression`)

Snowflake supports all partition transforms in version 2 of the Apache Iceberg specification. For more information, see
[Partition Transforms](https://iceberg.apache.org/spec/#partition-transforms) in the Apache Iceberg specification.

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

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Considerations for running this command:

  - Cross-cloud and cross-region Iceberg tables are not currently supported when you use Snowflake as the Iceberg catalog.
    If CREATE ICEBERG TABLE returns an error message like `"External volume <volume_name> must have a STORAGE_LOCATION defined in the local region ..."`, make sure that your external volume uses an active storage location
    in the same region as your Snowflake account.
  - If you created your external volume using a double-quoted identifier,
    you must specify the identifier exactly as created (including the double quotes) in your CREATE ICEBERG TABLE statement.
    Failure to include the quotes might result in an `Object does not exist` error (or
    similar type of error).

    To view an example, see the [Examples](#examples) (in this topic) section.
  - To create an [Iceberg table](/user-guide/tables-iceberg) with the USING TEMPLATE clause (and column definitions derived from
    INFER\_SCHEMA output), you must specify `KIND => 'ICEBERG'` for the [INFER\_SCHEMA](/sql-reference/functions/infer_schema) function.
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

    - If you don’t specify a clustering key, the table inherits the clustering key of the source table (if one exists).
    - By default, [Automatic Clustering](/user-guide/tables-auto-reclustering) is not suspended for the new table even if Automatic Clustering is
      suspended for the source table.
    - For [partitioned Iceberg tables](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning), the partitioning of the source table is ignored. To override this behavior, specify the PARTITION BY clause with the command.
  - CREATE ICEBERG TABLE … AS SELECT (CTAS):

    When clustering keys are specified in a CTAS statement:

    - Column definitions are required and must be explicitly specified in the statement.
    - By default, [Automatic Clustering](/user-guide/tables-auto-reclustering) is enabled for the new table even if Automatic Clustering is
      suspended for the source table.
    - The data is clustered when the new table is created. A clustered table generates a query plan
      that includes a sort operation and takes longer to create than an equivalent table that is not clustered.

      Alternatively, you can create a table with rows in sorted order by using an ORDER BY clause in the CTAS query.
  - CREATE ICEBERG TABLE … CLONE:

    - For [partitioned Iceberg tables](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning), the cloned table retains the partitioning information of
      the source table.

- CREATE OR REPLACE … COPY TAGS

  - You don’t need privileges on the tags to use COPY TAGS.
  - You can use COPY TAGS with a CREATE OR REPLACE … CLONE statement, a CREATE OR REPLACE … LIKE statement,
    or a WITH TAG clause. Tags from both sources are combined. If both sources set the same tag, the value from
    the replaced table (carried over by COPY TAGS) takes precedence.
  - If you rename a tagged column in the statement, the column in the new table will not retain the tag.
  - If you change the data type of a tagged column — for example, changing `NUMBER(8)` to `NUMBER(16)` — the column in the new table
    will not retain the tag.
  - If you swap column names in the statement, the tag stays with the column based on its name. For example, suppose only column `a` has a
    tag and you run the following command to swap the names of columns `a` and `b`:

    Copy code

    ```
    CREATE OR REPLACE ICEBERG TABLE dst1 COPY TAGS AS SELECT b AS a, a AS b FROM src1
    ```

    Only column `a` is still tagged in the new table, although it contains the data from column `b` in the source table.
- Using default values:

  - You can’t use expressions or functions, such as CURRENT\_TIMESTAMP(), for default values on v3 Iceberg tables. Only constant values are
    permitted in the Apache Iceberg v3 table specification.
    - For v2 Iceberg tables, you can use expressions such as CURRENT\_TIMESTAMP() with Snowflake. However, this property isn’t persisted into
      Iceberg metadata because the default values specification was introduced in version 3. Columns in v2 Iceberg tables with default values as
      expressions are only used with Snowflake, but the table remains interoperable with other engines and compliant with the
      version 2 specification.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- If you’re creating a table that you will sync with Snowflake Open Catalog, keep the following in mind:

  Important

  To ensure that access privileges in Open Catalog are enforced correctly on the table, make sure the table meets certain conditions
  before creating it. These conditions relate to the directory structure hierarchy for the catalog. For these conditions and instructions on
  how to meet them, see the note in
  [Organize catalog content](https://other-docs.snowflake.com/en/opencatalog/organize-catalog-content#conditions-correct-access-privileges)
  in the Snowflake Open Catalog documentation.

To troubleshoot issues with creating a Snowflake-managed table, see [You can’t create a Snowflake-managed table](/user-guide/tables-iceberg-open-catalog-troubleshooting#label-create-iceberg-table-snowflake-troubleshooting).

## Examples

### Create an Iceberg table with Snowflake as the catalog

This example creates an Iceberg table with Snowflake as the Iceberg catalog.
The resulting table is managed by Snowflake and supports read and write access.

The example sets the table name (`my_iceberg_table`) as the `BASE_LOCATION`. This way,
Snowflake writes data and metadata to a directory that uses the name of the table in your external volume
location.

Copy code

```
CREATE ICEBERG TABLE my_iceberg_table (amount int)
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'my_external_volume'
  BASE_LOCATION = 'my_iceberg_table';
```

### Create a partitioned Iceberg table

The following example creates a Snowflake-managed Iceberg table by using the value of a column named `c_nationkey` to partition the table:

Copy code

```
CREATE OR REPLACE ICEBERG TABLE customer_iceberg_partitioned (
  c_custkey INTEGER,
  c_name STRING,
  c_address STRING,
  c_nationkey INTEGER,
  c_phone STRING,
  c_acctbal INTEGER,
  c_mktsegment STRING,
  c_comment STRING
)
  PARTITION BY (c_nationkey)
  EXTERNAL_VOLUME = 'my_ext_vol'
  CATALOG = 'SNOWFLAKE'
  BASE_LOCATION = 'customer_iceberg_partitioned';
```

For more information, see [Iceberg partitioning](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning).

### Create a partitioned Iceberg table with hierarchical layout

The following example creates a Snowflake-managed Iceberg table by using the value of a column named `c_nationkey` to
partition the table. Because PATH\_LAYOUT = HIERARCHICAL, Snowflake writes data to the partitioned Iceberg table by using a hierarchical
path layout for files where partitioning information is included in the file paths:

Copy code

```
CREATE OR REPLACE ICEBERG TABLE customer_iceberg_partitioned (
  c_custkey INTEGER,
  c_name STRING,
  c_address STRING,
  c_nationkey INTEGER,
  c_phone STRING,
  c_acctbal INTEGER,
  c_mktsegment STRING,
  c_comment STRING
)
  PARTITION BY (c_nationkey)
  PATH_LAYOUT = HIERARCHICAL
  EXTERNAL_VOLUME = 'my_ext_vol'
  CATALOG = 'SNOWFLAKE'
  BASE_LOCATION = 'customer_iceberg_partitioned';
```

For more information, see [Partitioning with hierarchical paths](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning-hierarchical-paths).

### Create an Iceberg table by using the CTAS variant syntax

This example use the CREATE ICEBERG TABLE … AS SELECT variant syntax to create a *new* Iceberg table from a table named
`base_iceberg_table`. The AS SELECT clause must be at the end of the statement.

Copy code

```
CREATE OR REPLACE ICEBERG TABLE iceberg_table_copy (column1 int)
  EXTERNAL_VOLUME = 'my_external_volume'
  CATALOG = 'SNOWFLAKE'
  BASE_LOCATION = 'iceberg_table_copy'
  AS SELECT * FROM base_iceberg_table;
```

### Specify an external volume with a double-quoted identifier

This example creates an Iceberg table with an external volume whose identifier contains double quotes.
Identifiers enclosed in double quotes are case-sensitive and often contain special characters.

The identifier `"external_volume_1"` is specified exactly as created (including the double quotes).
Failure to include the quotes might result in an `Object does not exist` error (or similar type of error).

To learn more, see [Double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier).

Copy code

```
CREATE OR REPLACE ICEBERG TABLE table_with_quoted_external_volume
  EXTERNAL_VOLUME = '"external_volume_1"'
  CATALOG = 'SNOWFLAKE'
  BASE_LOCATION = 'my/relative/path/from/external_volume';
```

### Create a v3 Iceberg table

Note

For more information about other Iceberg v3 features that Snowflake supports, see [Apache Iceberg™ tables: Support for Apache Iceberg™ v3](/user-guide/tables-iceberg-v3-specification-support).

The following example creates a Snowflake-managed Apache Iceberg™ table that conforms to v3 of the Apache Iceberg™ specification:

Copy code

```
CREATE ICEBERG TABLE my_v3_iceberg_table (
  record VARIANT,
  event_timestamp TIMESTAMP_LTZ(6)
)
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'my_external_volume'
  BASE_LOCATION = 'my_iceberg_table'
  ICEBERG_VERSION = 3;
```
