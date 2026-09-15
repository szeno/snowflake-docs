# Configure Iceberg as the default metadata format for tables

By default, Snowflake creates standard Snowflake tables when you run `CREATE TABLE`. To create an Apache Iceberg™ table, you must
use the `ICEBERG` keyword in `CREATE ICEBERG TABLE` and related DDL commands.

You can set [DEFAULT\_METADATA\_WRITE\_FORMAT](#label-tables-iceberg-default-metadata-write-format) at the account, database, or schema
level so that `CREATE TABLE` and `ALTER TABLE` create Apache Iceberg™ tables without the `ICEBERG` keyword. This helps when you migrate
tools and scripts that use standard SQL DDL and can’t add Snowflake-specific keywords.

## Set the default metadata write format

Set the parameter with [ALTER DATABASE](/sql-reference/sql/alter-database) or [ALTER SCHEMA](/sql-reference/sql/alter-schema). You can also set it when you
create a database or schema.

### DEFAULT\_METADATA\_WRITE\_FORMAT

This parameter sets the default metadata write format for `CREATE TABLE` and `ALTER TABLE` in the parameter’s scope.

| Value | Behavior |
| --- | --- |
| `SNOWFLAKE` (default) | `CREATE TABLE` creates a standard Snowflake table. |
| `ICEBERG` | `CREATE TABLE` creates an Apache Iceberg™ table when `CATALOG = 'SNOWFLAKE'` is set at the database level. |

Expand

Show lessSee more

Important

To set `DEFAULT_METADATA_WRITE_FORMAT` to `ICEBERG`, you must also set `CATALOG = 'SNOWFLAKE'` at the
database level before you create tables. Snowflake returns an error if you try to set `DEFAULT_METADATA_WRITE_FORMAT` to `ICEBERG`
without `CATALOG = 'SNOWFLAKE'` at the database level.

Combine this parameter with [EXTERNAL\_VOLUME](/sql-reference/parameters#label-external-volume) and [BASE\_LOCATION\_PREFIX](/sql-reference/parameters#label-base-location-prefix) at the
database or schema level so that `CREATE TABLE` doesn’t need table-level storage parameters.

## Examples

### Create an Iceberg table without the ICEBERG keyword

The following example sets the default write format to Iceberg on a mixed-mode database, then creates a table with `CREATE TABLE`:

Copy code

```
ALTER DATABASE mydb SET
  DEFAULT_METADATA_WRITE_FORMAT = 'ICEBERG'
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'my_ext_vol';

CREATE OR REPLACE TABLE my_iceberg_table (
  boolean_col BOOLEAN,
  int_col INT
);
```

Snowflake creates an Apache Iceberg™ table. The storage path uses the database and schema name because
`BASE_LOCATION` isn’t specified.

### Use the default write format in a catalog-linked database

In a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database), `DEFAULT_METADATA_WRITE_FORMAT` is always `ICEBERG`
and can’t be changed. You can create tables without the `ICEBERG` keyword:

Copy code

```
CREATE OR REPLACE DATABASE my_cld
  LINKED_CATALOG = (
    CATALOG = 'my_polaris_catalog',
    EXTERNAL_VOLUME = 'my_ext_vol'
  );

USE DATABASE my_cld;

CREATE OR REPLACE TABLE my_iceberg_table (
  boolean_col BOOLEAN,
  int_col INT
);
```

Snowflake creates an externally managed Apache Iceberg™ table in the external catalog.

## DDL behavior

The following table summarizes how Snowflake treats common DDL commands when you set `DEFAULT_METADATA_WRITE_FORMAT`.

| Default write format | Command | Result |
| --- | --- | --- |
| `SNOWFLAKE` | `CREATE TABLE t (a INT)` | Standard Snowflake table |
| `ICEBERG` | `CREATE TABLE t (a INT)` | Apache Iceberg™ table |
| `ICEBERG` | `CREATE ICEBERG TABLE t (a INT)` | Apache Iceberg™ table (no change) |

Expand

Show lessSee more

`ALTER TABLE` on existing tables follows the same format resolution. `DROP TABLE` works for both standard and Apache Iceberg™ tables
without the `ICEBERG` keyword.

Explicit `CREATE ICEBERG TABLE` and `ALTER ICEBERG TABLE` commands continue to work and aren’t changed by this parameter.

## Considerations and limitations

- Setting `DEFAULT_METADATA_WRITE_FORMAT` to `ICEBERG` doesn’t convert existing standard Snowflake tables in the database or schema
  into Apache Iceberg™ tables. It only affects how Snowflake resolves DDL commands: `CREATE TABLE` creates an Apache Iceberg™ table, and
  `ALTER TABLE` assumes the target is an Apache Iceberg™ table. Existing standard Snowflake tables remain unchanged and can’t be altered
  while the parameter is set to `ICEBERG`. To alter existing standard tables, temporarily set the parameter back to `SNOWFLAKE`.
- When `DEFAULT_METADATA_WRITE_FORMAT` is `ICEBERG`, you can’t create standard Snowflake tables with `CREATE TABLE` in that scope
  unless you change the parameter back to `SNOWFLAKE`. Snowflake doesn’t support `CREATE SNOWFLAKE TABLE` syntax.
- The parameter applies only to regular `CREATE TABLE` and `ALTER TABLE` commands. It doesn’t apply to `TEMPORARY`,
  `EXTERNAL`, `EVENT`, or other table types that are not compatible with Iceberg formats. Dynamic and transient tables, however, are supported.
- Temporary tables aren’t blocked, but Snowflake creates them as standard Snowflake tables regardless of the parameter value.
- `SHOW TABLES` continues to list all tables. To list only Apache Iceberg™ tables, use `SHOW ICEBERG TABLES` or
  `SHOW ICEBERG DYNAMIC TABLES`.
- `DESCRIBE TABLE` and `DESCRIBE ICEBERG TABLE` behavior is unchanged. Use `DESCRIBE ICEBERG TABLE` when you want
  Apache Iceberg™-specific output.
- Some `ALTER ICEBERG TABLE` commands, such as `REFRESH` and `CONVERT TO MANAGED`, still require the `ICEBERG` keyword.
- Link-only creation of externally managed tables in mixed-mode databases (without the `ICEBERG` keyword) isn’t supported.
- While query history shows the SQL text you submitted, [GET\_DDL](/sql-reference/functions/get_ddl) returns the fully qualified
  statement with the `ICEBERG` keyword.

## Access control

Snowflake checks the privilege that matches the resolved table type. If `CREATE TABLE` resolves to an Apache Iceberg™ table, the role
needs the `CREATE ICEBERG TABLE` privilege. If it resolves to a standard Snowflake table, the role needs the `CREATE TABLE`
privilege.

Ownership and usage semantics are unchanged.

## Next steps

- To set related defaults for Apache Iceberg™ tables, see [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume) and
  [Configure a catalog integration](/user-guide/tables-iceberg-configure-catalog-integration).
- For parameter reference details, see [DEFAULT\_METADATA\_WRITE\_FORMAT](/sql-reference/parameters#default-metadata-write-format).
