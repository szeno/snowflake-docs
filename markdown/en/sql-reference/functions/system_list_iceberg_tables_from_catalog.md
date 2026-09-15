Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$LIST\_ICEBERG\_TABLES\_FROM\_CATALOG

Lists tables in a remote Apache Iceberg™ REST catalog (including [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview)).

See also:
:   - [Use Apache Iceberg™ tables with Snowflake Open Catalog in Snowflake](/user-guide/tables-iceberg-open-catalog)
    - [Configure a catalog integration for Apache Iceberg™ REST catalogs](/user-guide/tables-iceberg-configure-catalog-integration-rest)
    - [CREATE ICEBERG TABLE (Iceberg REST catalog)](/sql-reference/sql/create-iceberg-table-rest)

## Syntax

Copy code

```
SYSTEM$LIST_ICEBERG_TABLES_FROM_CATALOG( '<catalog_integration_name>'
  [ , '<parent_namespace>', <levels> ] )
```

## Arguments

**Required:**

`catalog_integration_name`
:   Identifier for the catalog integration for [Iceberg REST](/sql-reference/sql/create-catalog-integration-rest) or
    [Snowflake Open Catalog](/user-guide/tables-iceberg-configure-catalog-integration-open-catalog).

**Optional:**

`parent_namespace`
:   The identifier of the namespace from which to start listing tables. To retrieve
    results for the 0th namespace level in the catalog, specify an empty string (`''`).

    Default: The default namespace for the catalog integration (`CATALOG_NAMESPACE`), if specified. If you don’t specify a default
    namespace at the catalog integration level, the default is the 0th namespace level in the catalog. To list tables when the default is the
    0th namespace, you must specify an empty string (`CATALOG_NAMESPACE`) and the `<levels>` parameter.

`levels`
:   Specifies the number of levels to traverse in the namespace hierarchy for listing tables.

    For example:

    - If set to 0, the function returns all of the tables recursively, relative to the `parent_namespace`.
    - If set to 1, the function returns all of the tables within the `parent_namespace`.
    - If set to *n*, the function returns tables up to *n* levels deep, relative to the `parent_namespace`.

    Default: 1

## Returns

Returns a JSON-formatted string which lists tables in the Iceberg REST catalog for the specified
namespace and number of levels.

The JSON-formatted string has the following structure:

Copy code

```
[
  {
    "namespace": "<namespace_identifier>",
    "name": "<table_name>"
  },
  {
    "namespace": "<namespace_identifier>",
    "name": "<table_name_n>"
  },
]
```

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Integration (catalog) |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

List only the tables in the default catalog namespace:

Copy code

```
SELECT SYSTEM$LIST_ICEBERG_TABLES_FROM_CATALOG('myCatalogIntegration');
```

List *every* table in the catalog:

Copy code

```
SELECT SYSTEM$LIST_ICEBERG_TABLES_FROM_CATALOG('myCatalogIntegration', '', 0);
```

List all of the tables recursively under the `db1` namespace:

Copy code

```
SELECT SYSTEM$LIST_ICEBERG_TABLES_FROM_CATALOG('myCatalogIntegration', 'db1', 0);
```

List all of the tables three levels under the `db1` namespace:

Copy code

```
SELECT SYSTEM$LIST_ICEBERG_TABLES_FROM_CATALOG('myCatalogIntegration', 'db1', 3);
```
