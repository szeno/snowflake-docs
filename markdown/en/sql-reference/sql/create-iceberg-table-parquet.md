# CREATE ICEBERG TABLE (Parquet files in object storage)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Creates or replaces a read-only [Apache Iceberg™ table](/user-guide/tables-iceberg) in the current or specified schema
from Apache Parquet™ files in external cloud object storage. Snowflake reads Parquet files in place;
it doesn’t copy or rewrite your data. You pair this command with a
catalog integration where `CATALOG_SOURCE = OBJECT_STORE` and `TABLE_FORMAT` is one of the following values:

- `TABLE_FORMAT = NONE`: Use when your file paths aren’t Hive-style, or when you want to define partition columns
  explicitly with expressions on the `METADATA$FILENAME` pseudocolumn.
- `TABLE_FORMAT = HIVE`: Use when your files use Hive-style `key=value` directory partitioning (for example,
  `year=2024/month=01/`). Snowflake infers the partition columns from the paths. You can’t define explicit partition columns.

For the catalog integration, see [CREATE CATALOG INTEGRATION (Object storage)](/sql-reference/sql/create-catalog-integration-object-storage). For a conceptual
overview, best practices, monitoring, and billing, see [Parquet Direct](/user-guide/tables-iceberg-parquet-direct).

This topic refers to Iceberg tables as simply “tables” except where specifying *Iceberg tables* avoids confusion.

Note

Before creating a table, you must create the [external volume](/sql-reference/sql/create-external-volume) where the Iceberg metadata
and data files are stored.
For instructions, see [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume).

You also need a catalog integration for the table.
For more information, see [Configure a catalog integration for files in object storage](/user-guide/tables-iceberg-configure-catalog-integration-object-storage).

See also:
:   [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table) , [ALTER ICEBERG TABLE … REFRESH](/sql-reference/sql/alter-iceberg-table-refresh) , [DROP ICEBERG TABLE](/sql-reference/sql/drop-iceberg-table) , [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) , [DESCRIBE ICEBERG TABLE](/sql-reference/sql/desc-iceberg-table) , [UNDROP ICEBERG TABLE](/sql-reference/sql/undrop-iceberg-table)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] ICEBERG TABLE [ IF NOT EXISTS ] <table_name>
  [
    -- Data column definition
    <col_name> <col_type>
    [ NOT NULL ]
    [ [ WITH ] MASKING POLICY <policy_name> [ USING ( <col_name> , <cond_col1> , ... ) ] ]
    [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
    [ COMMENT '<string_literal>' ]
    -- In-line constraint
    [ inlineConstraint ]
    -- Additional column definitions (data, virtual, or partition columns)
    [ , <col_name> <col_type> ...
      -- Virtual column definition
      | <col_name> <col_type> AS <expr>
      -- Partition column definition (TABLE_FORMAT = NONE only)
      | <part_col_name> <col_type> AS <part_expr>
      -- In-line constraint
      [ inlineConstraint ]
      [ , ... ]
    ]
    -- Out-of-line constraints
    [ , outoflineConstraint [ ... ] ]
  ]
  [ PARTITION BY ( <part_col_name> [, <part_col_name> ... ] ) ]
  [ EXTERNAL_VOLUME = '<external_volume_name>' ]
  [ CATALOG = '<catalog_integration_name>' ]
  BASE_LOCATION = '<relative_path_from_external_volume>'
  [ ENABLE_SCHEMA_INFERENCE = { TRUE | FALSE } ]
  [ ENABLE_SCHEMA_EVOLUTION = { TRUE | FALSE } ]
  [ MATCH_BY_COLUMN_NAME = { CASE_INSENSITIVE | CASE_SENSITIVE } ]
  [ AUTO_REFRESH = { TRUE | FALSE } ]
  [ REFRESH_ON_CREATE = { TRUE | FALSE } ]
  [ PATTERN = '<regex_pattern>' ]
  [ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ COMMENT = '<string_literal>' ]
```

Where:

> Copy code
>
> ```
> inlineConstraint ::=
>   [ CONSTRAINT <constraint_name> ]
>   { UNIQUE
>     | PRIMARY KEY
>     | [ FOREIGN KEY ] REFERENCES <ref_table_name> [ ( <ref_col_name> ) ]
>   }
>   [ <constraint_properties> ]
> ```
>
> For additional inline constraint details, see [CREATE | ALTER TABLE … CONSTRAINT](/sql-reference/sql/create-table-constraint).
>
> Copy code
>
> ```
> outoflineConstraint ::=
>   [ CONSTRAINT <constraint_name> ]
>   { UNIQUE [ ( <col_name> [ , <col_name> , ... ] ) ]
>     | PRIMARY KEY [ ( <col_name> [ , <col_name> , ... ] ) ]
>     | [ FOREIGN KEY ] [ ( <col_name> [ , <col_name> , ... ] ) ]
>       REFERENCES <ref_table_name> [ ( <ref_col_name> [ , <ref_col_name> , ... ] ) ]
>   }
>   [ <constraint_properties> ]
> ```
>
> For additional out-of-line constraint details, see [CREATE | ALTER TABLE … CONSTRAINT](/sql-reference/sql/create-table-constraint).

## Required parameters

`table_name`
:   Specifies the identifier (name) for the table; must be unique for the schema in which the table is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`BASE_LOCATION = 'relative_path_from_external_volume'`
:   Specifies a relative path from the table’s `EXTERNAL_VOLUME` location to a directory where Snowflake can access your
    Parquet files. The base location must point to a directory and can’t point to a single Parquet file.

    As a best practice, give each table its own base location that doesn’t overlap with the base location of any other
    table. For more information, see [Give each table its own storage folder](/user-guide/tables-iceberg-parquet-direct#label-tables-iceberg-parquet-direct-best-practices-disjoint).

## Optional parameters

`col_name`
:   Specifies the column identifier (name). All the requirements for table identifiers also apply to column identifiers.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax) and [Reserved & limited keywords](/sql-reference/reserved-keywords).

    Note

    In addition to the standard reserved keywords, the following keywords can’t be used as column identifiers because they’re
    reserved for ANSI-standard context functions:

    - `CURRENT_DATE`
    - `CURRENT_ROLE`
    - `CURRENT_TIME`
    - `CURRENT_TIMESTAMP`
    - `CURRENT_USER`

`col_type`
:   Specifies the data type for the column.

    For information about how Parquet types map to Snowflake data types, see
    [Parquet data types](/user-guide/tables-iceberg-data-types#label-tables-iceberg-parquet-direct-data-types).

`expr`
:   String that specifies the expression for a virtual column. When queried, the column returns results derived from this
    expression.

    You can use the `METADATA$FILENAME` pseudocolumn in the expression. `METADATA$FILENAME` identifies the name of each Parquet
    data file included in the table, relative to its path on the external volume.

    For example, if the external volume location is `s3://bucket-name/data/warehouse/` and the `BASE_LOCATION` of the table is
    `default_db/schema_name/table_name/`, the absolute location of a Parquet file might be
    `s3://bucket-name/data/warehouse/default_db/schema_name/table_name/ds=2023-01-01/file1.parquet`. The `METADATA$FILENAME`
    value for this file is `default_db/schema_name/table_name/ds=2023-01-01/file1.parquet`.

`CONSTRAINT ...`
:   Defines an inline or out-of-line constraint for the specified columns in the table. Parquet Direct tables support the
    following constraints:

    - `NOT NULL`
    - `UNIQUE`
    - `PRIMARY KEY`
    - `FOREIGN KEY`

    You can specify the `RELY` or `NORELY` constraint property. Snowflake doesn’t enforce these constraints on Parquet Direct
    tables. Default values, `AUTOINCREMENT`, and `IDENTITY` aren’t supported.

    For syntax details, see [CREATE | ALTER TABLE … CONSTRAINT](/sql-reference/sql/create-table-constraint).
    For more information about constraints, see [Constraints](/sql-reference/constraints).

`MASKING POLICY = policy_name`
:   Specifies the [masking policy](/user-guide/security-column-intro) to set on a column.

`EXTERNAL_VOLUME = 'external_volume_name'`
:   Specifies the identifier (name) for the external volume where Snowflake can access your Parquet data files.

    You must specify an external volume if you haven’t set one at the database or schema level. Otherwise, the Iceberg table
    defaults to the external volume for the schema, database, or account.
    The schema takes precedence over the database, and the database takes precedence over the account.

`CATALOG = 'catalog_integration_name'`
:   Specifies the identifier (name) of the catalog integration for this table. The catalog integration must use
    `CATALOG_SOURCE = OBJECT_STORE` and `TABLE_FORMAT = NONE` or `TABLE_FORMAT = HIVE`.

    You must specify a catalog integration if you haven’t set one at the database or schema level. Otherwise, the Iceberg table
    defaults to the catalog integration for the schema, database, or account.
    The schema takes precedence over the database, and the database takes precedence over the account.

`ENABLE_SCHEMA_INFERENCE = { TRUE | FALSE }`
:   Specifies whether Snowflake automatically detects column definitions from your Parquet files when you create the table.

    - `TRUE`: Snowflake reads sample files at creation time and generates column definitions automatically. For tables that use
      `TABLE_FORMAT = HIVE`, partition columns are also inferred from the `key=value` directory structure.
      If you include explicit column definitions, Snowflake uses them for those columns and infers the remaining columns.
    - `FALSE`: You must provide explicit column definitions.

    Default: `TRUE` if no column definition is provided; otherwise `FALSE`.

    Schema inference applies only when you create the table. To also evolve the schema during later refreshes, set
    `ENABLE_SCHEMA_EVOLUTION = TRUE`.

`ENABLE_SCHEMA_EVOLUTION = { TRUE | FALSE }`
:   Specifies whether Snowflake automatically evolves the table schema when Parquet file schemas change during later refreshes.

    - `TRUE`: When a refresh detects new columns or eligible type widening in source files, Snowflake adds those changes to the
      table schema automatically. For supported changes, see [Schema evolution](/user-guide/tables-iceberg-parquet-direct#label-tables-iceberg-parquet-direct-schema-evolution).
    - `FALSE`: Snowflake doesn’t modify the table schema on refresh, even if the source files change.

    `ENABLE_SCHEMA_EVOLUTION = TRUE` requires schema inference. If you set `ENABLE_SCHEMA_EVOLUTION = TRUE` without specifying
    `ENABLE_SCHEMA_INFERENCE`, Snowflake enables inference automatically.

    You can only enable schema evolution when you create the table. After the table is created, you can use
    ALTER ICEBERG TABLE to disable schema evolution, but you can’t enable it again. To enable schema evolution on an existing
    table, re-create the table.

    Default: `FALSE`

`MATCH_BY_COLUMN_NAME = { CASE_INSENSITIVE | CASE_SENSITIVE }`
:   Controls how column names in Parquet files are matched against the table schema during refresh.

    - `CASE_INSENSITIVE`: Snowflake matches columns regardless of differences in casing between the Parquet file schema and the
      table definition. Each time a refresh encounters a new casing for a column, Snowflake records it, so data from files that
      use different casings (for example, `id`, `ID`, and `Id`) populates the same table column. For tables that use Hive-style
      partitioning, partition key segments in the file path are also matched case-insensitively, so paths like `Status=active/`
      and `status=pending/` resolve to the same partition column.
    - `CASE_SENSITIVE`: Column names must match exactly, including casing. Files with differently cased column names don’t
      populate the mismatched columns. If a table previously used `CASE_INSENSITIVE` and recorded multiple casings for a column,
      Snowflake keeps honoring those recorded casings after you switch to `CASE_SENSITIVE`.

    Default: `CASE_INSENSITIVE`

    Note

    Regardless of this setting, you can’t define two columns in the same table whose names differ only in casing (for example,
    `id` and `ID`).

`AUTO_REFRESH = { TRUE | FALSE }`
:   Specifies whether Snowflake automatically refreshes the table when it receives event notifications from your cloud storage
    for new, changed, or deleted Parquet files. To use auto-refresh, configure event notifications for your external volume.
    For setup instructions, see [Auto-refresh](/user-guide/tables-iceberg-parquet-direct#label-tables-iceberg-parquet-direct-auto-refresh).

    When you enable auto-refresh on a table that previously had auto-refresh disabled, Snowflake processes a full backfill
    refresh asynchronously to register files that were added while auto-refresh was off.

    Default: `FALSE`

`REFRESH_ON_CREATE = { TRUE | FALSE }`
:   Specifies whether Snowflake registers the existing Parquet files in the `BASE_LOCATION` when it creates the table.

    - `TRUE`: Snowflake scans the `BASE_LOCATION` at creation time and registers all matching Parquet files. The CREATE
      statement completes when registration finishes.
    - `FALSE`: Snowflake creates an empty table with no registered files. Snowflake doesn’t register files when you query the
      table; the table returns no rows until you refresh it. Use this option when your data lake contains a very
      large number of files and you want to register files incrementally after creation, either with manual refreshes of
      specific paths or by enabling auto-refresh.

    When you use `REFRESH_ON_CREATE = FALSE`, you must provide explicit column definitions, because schema inference requires
    files at creation time.

    Default: `TRUE`

`PATTERN = 'regex_pattern'`
:   A regular expression pattern string, enclosed in single quotes, that specifies the file names and paths under the
    `BASE_LOCATION` to include in the table. Files that don’t match the pattern aren’t registered.

    Tip

    For the best performance, avoid patterns that filter out a large number of files.

`REPLACE_INVALID_CHARACTERS = { TRUE | FALSE }`
:   Specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�) in query results.
    You can only set this parameter for tables that use an external Iceberg catalog.

    - `TRUE` replaces invalid UTF-8 characters with the Unicode replacement character.
    - `FALSE` leaves invalid UTF-8 characters unchanged. Snowflake returns a user error message when it encounters invalid UTF-8
      characters in a Parquet data file.

    If not specified, the Iceberg table defaults to the parameter value for the schema, database, or account.
    The schema takes precedence over the database, and the database takes precedence over the account.

    Default: `FALSE`

`ROW ACCESS POLICY policy_name ON ( col_name [ , col_name ... ] )`
:   Specifies the [row access policy](/user-guide/security-row-intro) to set on a table.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`COMMENT 'string_literal'`
:   Specifies a comment for the column or the table.

    Comments can be specified at the column level or the table level. The syntax for each is slightly different.

## Partitioning parameters (TABLE\_FORMAT = NONE)

Use these parameters to partition your table when the catalog integration uses `TABLE_FORMAT = NONE`.
For tables that use `TABLE_FORMAT = HIVE`, Snowflake infers partition columns from `key=value` directory names, and you
can’t define explicit partition columns.

Tip

If your files use Hive-style `key=value` partition directories (for example, `region=us/date=2026-10-01/`), use a
catalog integration with `TABLE_FORMAT = HIVE` instead of defining partition columns. Snowflake infers the partition
columns and their values from the directory names. For more information, see
[Infer Hive partitions](#label-sql-create-iceberg-table-parquet-example-hive).

`part_col_name col_type AS part_expr`
:   Defines one or more partition columns in the table.

    A partition column must evaluate as an expression that parses the path or file name information in the `METADATA$FILENAME`
    pseudocolumn. A partition consists of all data files that match the path or file name in the expression for the partition
    column.

    |  |  |
    | --- | --- |
    | `part_col_name` | String that specifies the partition column identifier (the name). All the requirements for table identifiers also apply to column identifiers. |
    | `col_type` | String (constant) that specifies the data type for the column. The data type must match the result of `part_expr` for the column. |
    | `part_expr` | String that specifies the expression for the column. The expression must include the `METADATA$FILENAME` pseudocolumn. |

    Expand

    Show lessSee more

    Partition expressions support the following operators and functions:

    - `=`, `<>`, `>`, `>=`, `<`, `<=`
    - `||`
    - `+`, `-`
    - `-` (negate)
    - `*`
    - `AND`, `OR`
    - `NOT`
    - [ARRAY\_CONSTRUCT](/sql-reference/functions/array_construct)
    - [CASE](/sql-reference/functions/case)
    - [CAST , ::](/sql-reference/functions/cast)
    - [CONCAT , ||](/sql-reference/functions/concat)
    - [ENDSWITH](/sql-reference/functions/endswith)
    - [IS [ NOT ] NULL](/sql-reference/functions/is-null)
    - [IFF](/sql-reference/functions/iff)
    - [IFNULL](/sql-reference/functions/ifnull)
    - [[ NOT ] IN](/sql-reference/functions/in)
    - [LOWER](/sql-reference/functions/lower)
    - [NULLIF](/sql-reference/functions/nullif)
    - [NVL2](/sql-reference/functions/nvl2)
    - [SPLIT\_PART](/sql-reference/functions/split_part)
    - [STARTSWITH](/sql-reference/functions/startswith)
    - [SUBSTR , SUBSTRING](/sql-reference/functions/substr)
    - [UPPER](/sql-reference/functions/upper)
    - [ZEROIFNULL](/sql-reference/functions/zeroifnull)

`PARTITION BY ( part_col_name [, part_col_name ... ] )`
:   Specifies the partition columns to evaluate for the table.

    When you query the table, include one or more partition columns in a WHERE clause so that Snowflake scans only the
    matching partitions; for example:

    `... WHERE part_col_name = 'filter_value'`

    A common practice is to partition data files by increments of time or, if the files come from multiple sources, by a source
    identifier and a date or timestamp.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE ICEBERG TABLE | Schema |  |
| CREATE EXTERNAL VOLUME | Account | Required to create a new external volume. |
| USAGE | External volume | Required to reference an existing external volume. |
| CREATE INTEGRATION | Account | Required to create a new catalog integration. |
| USAGE | Catalog integration | Required to reference an existing catalog integration. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- If you created your external volume or catalog integration by using a double-quoted identifier, you must specify the
  identifier exactly as created (including the double quotes) in your CREATE ICEBERG TABLE
  statement. Otherwise, you might get an `Object does not exist` error.
- Creating the table and each refresh register Parquet files and incur data registration charges. Auto-refresh also uses
  serverless compute. For more information, see [Billing](/user-guide/tables-iceberg-parquet-direct#label-tables-iceberg-parquet-direct-billing).
- To refresh the table after creation, use [ALTER ICEBERG TABLE … REFRESH](/sql-reference/sql/alter-iceberg-table-refresh)
  or enable auto-refresh.
- Considerations for Parquet Direct tables:

  - Parquet files that use any of the following features or data types aren’t supported:

    - Invalid or duplicate field IDs. Files with valid field IDs are supported; Snowflake matches columns by name, not by
      field ID.
    - The DECIMAL data type with precision higher than 38.
    - LIST or MAP types with one-level or two-level representation.
    - Unsigned integer types (`INT(signed=false)`).
    - The FLOAT16 data type.
  - Snowflake currently only supports creating Parquet Direct tables with an [object storage-based catalog integration](/sql-reference/sql/create-catalog-integration-object-storage). Other catalog integration types are not supported.
  - When auto-refresh is enabled on a table, you can’t manually refresh the table. To manually refresh the table, disable
    auto-refresh first.
  - Parquet Direct tables are read-only:

    - You can’t perform DML operations (INSERT, UPDATE, DELETE, MERGE) on these tables in Snowflake. Use other engines to
      modify the files in your cloud storage.
    - You can’t convert these tables to Snowflake-managed Iceberg tables.
    - You can’t perform table maintenance on these tables.
  - The following Snowflake features aren’t supported for Parquet Direct tables:

    - Cloning
    - Clustering (`CLUSTER BY`)
    - Replication
    - Standard streams and append-only streams (insert-only streams are supported)
    - Dynamic tables
    - Native Apps
  - You can’t create a Parquet Direct table by using CREATE TABLE … AS SELECT (CTAS) or CREATE TABLE … LIKE.
    You can use a Parquet Direct table as the source for either statement.
  - You can’t undrop a Parquet Direct table. After you drop a Parquet Direct table, re-create it to register the files
    again.
  - You can’t set the `DATA_RETENTION_TIME_IN_DAYS` parameter on a Parquet Direct table.
  - You can’t enable schema evolution on an existing Parquet Direct table. To use schema evolution, set
    `ENABLE_SCHEMA_EVOLUTION = TRUE` when you create the table.
  - Data sharing is supported for Parquet Direct tables, including local sharing, cross-region sharing, and listings that use
    Cross-Cloud Auto-Fulfillment.
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

## Examples

### Infer the schema

The following example omits the column list, so Snowflake infers the column definitions from the Parquet files. It
also sets `ENABLE_SCHEMA_EVOLUTION = TRUE` so that Snowflake evolves the schema on later refreshes:

Copy code

```
CREATE ICEBERG TABLE auto_schema_table
  EXTERNAL_VOLUME = 'my_ext_vol'
  CATALOG = 'parquet_catalog_int'
  BASE_LOCATION = 'auto_schema_table/'
  ENABLE_SCHEMA_EVOLUTION = TRUE;
```

You can also define some columns explicitly and let Snowflake infer the rest. In this case, you must specify
`ENABLE_SCHEMA_INFERENCE = TRUE`:

Copy code

```
CREATE ICEBERG TABLE auto_schema_table_col_spec (col1 INT)
  EXTERNAL_VOLUME = 'my_ext_vol'
  CATALOG = 'parquet_catalog_int'
  BASE_LOCATION = 'auto_schema_table_col_spec/'
  ENABLE_SCHEMA_INFERENCE = TRUE
  ENABLE_SCHEMA_EVOLUTION = TRUE;
```

### Infer Hive partitions

The following example creates a table over files with Hive-style partitioning, such as `sales/year=2024/month=01/data.parquet`.
Because the catalog integration uses `TABLE_FORMAT = HIVE`, Snowflake infers the `year` and `month` partition columns from
the directory names:

Copy code

```
CREATE CATALOG INTEGRATION hive_catalog_int
  CATALOG_SOURCE = OBJECT_STORE
  TABLE_FORMAT = HIVE
  ENABLED = TRUE;

CREATE ICEBERG TABLE sales_data
  EXTERNAL_VOLUME = 'my_ext_vol'
  CATALOG = 'hive_catalog_int'
  BASE_LOCATION = 'sales/'
  AUTO_REFRESH = TRUE
  ENABLE_SCHEMA_EVOLUTION = TRUE;
```

### Match column names case-insensitively

The following example creates a table that resolves column name casing differences across Parquet files:

Copy code

```
CREATE ICEBERG TABLE my_table
  CATALOG = 'parquet_catalog_int'
  EXTERNAL_VOLUME = 'my_ext_vol'
  BASE_LOCATION = 'path/to/parquet/files/'
  ENABLE_SCHEMA_INFERENCE = TRUE
  MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
  ENABLE_SCHEMA_EVOLUTION = TRUE;
```

### Create an empty table and register files later

For data lakes with a very large number of files, you can skip the initial file registration and register files
incrementally. You must provide explicit column definitions:

Copy code

```
CREATE ICEBERG TABLE my_large_table (
    id INT,
    event_type STRING,
    event_date DATE
  )
  EXTERNAL_VOLUME = 'my_ext_vol'
  CATALOG = 'parquet_catalog_int'
  BASE_LOCATION = 'data-lake/'
  REFRESH_ON_CREATE = FALSE
  AUTO_REFRESH = FALSE
  ENABLE_SCHEMA_EVOLUTION = TRUE;
```

Then register files with manual refreshes of specific paths, or enable auto-refresh to register existing files in the
background while the table remains queryable:

Copy code

```
-- Option 1: Register specific partitions
ALTER ICEBERG TABLE my_large_table REFRESH '/year=2024/month=01/';

-- Option 2: Let auto-refresh register existing files asynchronously
ALTER ICEBERG TABLE my_large_table SET AUTO_REFRESH = TRUE;
```

For more information, see [Use auto-refresh when creating large tables](/user-guide/tables-iceberg-parquet-direct#label-tables-iceberg-parquet-direct-best-practices-create).

### Specify data columns

The following example creates a table from Parquet files with explicit column definitions:

Copy code

```
CREATE ICEBERG TABLE my_parquet_table (
    first_name STRING,
    last_name STRING,
    amount NUMBER,
    create_date DATE
  )
  CATALOG = 'parquet_catalog_int'
  EXTERNAL_VOLUME = 'my_ext_vol'
  BASE_LOCATION = 'my_parquet_table/';
```

### Define a partition column with an expression

The following example uses a catalog integration with `TABLE_FORMAT = NONE` and defines a partition column named
`sr_returned_date_sk` by parsing `METADATA$FILENAME`:

Copy code

```
CREATE ICEBERG TABLE store_returns (
  sr_returned_date_sk INTEGER AS
    IFF(
      REGEXP_SUBSTR(METADATA$FILENAME, 'sr_returned_date_sk=(.*)/', 1, 1, 'e') = '__HIVE_DEFAULT_PARTITION__',
      NULL,
      TO_NUMBER(REGEXP_SUBSTR(METADATA$FILENAME, 'sr_returned_date_sk=(.*)/', 1, 1, 'e'))
    ),
  sr_return_time_sk     INTEGER,
  sr_item_sk            INTEGER,
  sr_customer_sk        INTEGER,
  sr_ticket_number      BIGINT,
  sr_return_quantity    INTEGER,
  sr_return_amt         DECIMAL(7,2),
  sr_net_loss           DECIMAL(7,2)
)
  PARTITION BY (sr_returned_date_sk)
  EXTERNAL_VOLUME = 'my_ext_vol'
  CATALOG = 'parquet_catalog_int'
  BASE_LOCATION = 'store_returns/';
```
