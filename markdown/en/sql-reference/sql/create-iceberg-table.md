# CREATE ICEBERG TABLE

Creates or replaces an [Apache Iceberg™ table](/user-guide/tables-iceberg) in the current/specified schema.

See also:
:   [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table), [DROP ICEBERG TABLE](/sql-reference/sql/drop-iceberg-table) , [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) , [DESCRIBE ICEBERG TABLE](/sql-reference/sql/desc-iceberg-table)

## Syntax

This section provides an overview of the syntax for *all* types of Iceberg tables.
The syntax for creating an Iceberg table varies considerably depending on whether you use Snowflake as the Iceberg catalog
or an external Iceberg catalog.

To view the syntax, parameter descriptions, usage notes, and examples for specific use cases, see the following pages:

- **Snowflake as the Iceberg catalog**

  - [CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)](/sql-reference/sql/create-iceberg-table-snowflake) (includes the `COPY TAGS` parameter for CREATE OR REPLACE operations)
- **External Iceberg catalog**

  - [CREATE ICEBERG TABLE (REST or Snowflake Open Catalog)](/sql-reference/sql/create-iceberg-table-rest)

    Tip

    To automatically bring the tables in your remote REST catalog into Snowflake, you can [create a catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database). With a
    catalog-linked database, you don’t need to create individual externally managed
    Iceberg tables to access the existing tables in your remote catalog from Snowflake. In addition, you can use the [Variant syntax](/sql-reference/sql/create-iceberg-table-rest#label-tables-iceberg-external-write-create-table-syntax)
    or [CREATE ICEBERG TABLE (catalog-linked database) … AS SELECT](/sql-reference/sql/create-iceberg-table-rest#label-tables-iceberg-external-write-create-table-ctas-syntax) variant syntax with your catalog-linked database to create
    new remote Iceberg tables from Snowflake.
  - [CREATE ICEBERG TABLE (Delta files in object storage)](/sql-reference/sql/create-iceberg-table-delta)
  - [CREATE ICEBERG TABLE (Iceberg files in object storage)](/sql-reference/sql/create-iceberg-table-iceberg-files)

### Snowflake as the Iceberg catalog

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

For more information, see [CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)](/sql-reference/sql/create-iceberg-table-snowflake).

#### CREATE ICEBERG TABLE … AS SELECT (also referred to as CTAS)

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

For more information, see [CREATE ICEBERG TABLE … AS SELECT](/sql-reference/sql/create-iceberg-table-snowflake#label-iceberg-create-table-as-select-syntax).

#### CREATE ICEBERG TABLE … LIKE

> Copy code
>
> ```
> CREATE [ OR REPLACE ] [ TRANSIENT ] ICEBERG TABLE <table_name> LIKE <source_table>
>   [ CLUSTER BY ( <expr> [ , <expr> , ... ] ) ]
>   [ COPY GRANTS ]
>   [ COPY TAGS ]
>   [ ... ]
> ```

For more information, see [CREATE ICEBERG TABLE … LIKE](/sql-reference/sql/create-iceberg-table-snowflake#label-iceberg-ctlike).

### External Iceberg catalog

#### Iceberg REST (including Snowflake Open Catalog)

Tip

To automatically bring the tables in your remote REST catalog into Snowflake, [create a catalog linked database](/user-guide/tables-iceberg-catalog-linked-database).
With a catalog-linked database, you don’t have to create individual externally managed Iceberg tables to bring your remote tables into
Snowflake.

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

For more information, see [CREATE ICEBERG TABLE (Iceberg REST catalog)](/sql-reference/sql/create-iceberg-table-rest).

#### Iceberg REST in a catalog-linked database

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

For more information, see [CREATE ICEBERG TABLE (Iceberg REST catalog)](/sql-reference/sql/create-iceberg-table-rest).

#### Delta files

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

For more information, see [CREATE ICEBERG TABLE (Delta files in object storage)](/sql-reference/sql/create-iceberg-table-delta).

#### Iceberg files in object storage

Copy code

```
CREATE [ OR REPLACE ] ICEBERG TABLE [ IF NOT EXISTS ] <table_name>
  [ EXTERNAL_VOLUME = '<external_volume_name>' ]
  [ CATALOG = '<catalog_integration_name>' ]
  METADATA_FILE_PATH = '<metadata_file_path>'
  [ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]
```

For more information, see [CREATE ICEBERG TABLE (Iceberg files in object storage)](/sql-reference/sql/create-iceberg-table-iceberg-files).
