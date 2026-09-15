# CREATE CATALOG INTEGRATION (Object storage)

Creates a new [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def)
in the account or replaces an existing catalog integration for the following sources:

- Apache Iceberg™ metadata files
- Delta Lake metadata files

See also:
:   [ALTER CATALOG INTEGRATION](/sql-reference/sql/alter-catalog-integration) , [DROP CATALOG INTEGRATION](/sql-reference/sql/drop-catalog-integration) , [SHOW CATALOG INTEGRATIONS](/sql-reference/sql/show-catalog-integrations), [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] CATALOG INTEGRATION [IF NOT EXISTS]
  <name>
  CATALOG_SOURCE = OBJECT_STORE
  TABLE_FORMAT = { ICEBERG | DELTA }
  ENABLED = { TRUE | FALSE }
  [ REFRESH_INTERVAL_SECONDS = <value> ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   String that specifies the identifier (name) for the catalog integration; must be unique in your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`CATALOG_SOURCE = OBJECT_STORE`
:   Specifies external Iceberg metadata files or Delta files in object storage as the source.

`TABLE_FORMAT = { ICEBERG | DELTA }`
:   Specifies the table format.

    - `ICEBERG`: Specifies Glue Iceberg tables or Iceberg tables from metadata in an external cloud storage location.
    - `DELTA`: Specifies Delta Lake data in object storage [CREATE ICEBERG TABLE (Delta files in object storage)](/sql-reference/sql/create-iceberg-table-delta) (**Delta Direct**).

`ENABLED = { TRUE | FALSE }`
:   Specifies whether the catalog integration is available to use for Iceberg tables.

    > - `TRUE` allows users to create new Iceberg tables that reference this integration. Existing Iceberg tables that reference
    >   this integration function normally.
    > - `FALSE` prevents users from creating new Iceberg tables that reference this integration. Existing Iceberg tables that
    >   reference this integration cannot access the catalog in the table definition.

    The value is case-insensitive.

    The default is `TRUE`.

## Optional parameters

`REFRESH_INTERVAL_SECONDS = value`
:   Specifies the number of seconds that Snowflake waits between attempts to poll the external Iceberg catalog for metadata updates
    for [automated refresh](/user-guide/tables-iceberg-auto-refresh).

    For Delta-based tables, specifies the number of seconds that Snowflake waits between attempts to poll your external cloud storage for
    new metadata.

    Values: 30 to 86400, inclusive

    Default: 30 seconds

Note

The REFRESH\_INTERVAL\_SECONDS parameter is only supported when `TABLE_FORMAT = DELTA` for this type of catalog integration.

`COMMENT = 'string_literal'`
:   String (literal) that specifies a comment for the integration.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE INTEGRATION | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You cannot modify an existing catalog integration; use a CREATE OR REPLACE CATALOG INTEGRATION statement instead.
- You can’t drop or replace a catalog integration if one or more Apache Iceberg™ tables
  are associated with the catalog integration.

  To view the tables that depend on a catalog integration,
  you can use the [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) command and
  a query using the [pipe operator](/sql-reference/operators-flow) (`->>`) that filters on
  the `catalog_name` column.

  Note

  The column identifier (`catalog_name`) is case-sensitive.
  Specify the column identifier exactly as it appears in the SHOW ICEBERG TABLES output.

  For example:

  Copy code

  ```
  SHOW ICEBERG TABLES
    ->> SELECT *
          FROM $1
          WHERE "catalog_name" = 'my_catalog_integration_1';
  ```
- [Automatically refresh Apache Iceberg™ tables](/user-guide/tables-iceberg-auto-refresh) is only supported for this type of catalog integration when `TABLE_FORMAT = DELTA`.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

The following example creates an integration that uses Iceberg metadata in external cloud storage. OBJECT\_STORE corresponds to
the object storage that you associate with an [external volume](/sql-reference/sql/create-external-volume).

> Copy code
>
> ```
> CREATE CATALOG INTEGRATION myCatalogInt
>   CATALOG_SOURCE = OBJECT_STORE
>   TABLE_FORMAT = ICEBERG
>   ENABLED = TRUE;
> ```
