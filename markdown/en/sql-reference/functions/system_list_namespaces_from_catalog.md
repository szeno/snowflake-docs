Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$LIST\_NAMESPACES\_FROM\_CATALOG

Lists the namespaces in a remote Apache Iceberg™ REST catalog (including [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview)).

See also:
:   - [Use Apache Iceberg™ tables with Snowflake Open Catalog in Snowflake](/user-guide/tables-iceberg-open-catalog)
    - [Configure a catalog integration for Apache Iceberg™ REST catalogs](/user-guide/tables-iceberg-configure-catalog-integration-rest)

## Syntax

Copy code

```
SYSTEM$LIST_NAMESPACES_FROM_CATALOG( '<catalog_integration_name>'
  [ , '<parent_namespace>', <levels> ] )
```

## Arguments

**Required:**

`catalog_integration_name`
:   Identifier for the catalog integration for [Iceberg REST](/sql-reference/sql/create-catalog-integration-rest) or
    [Snowflake Open Catalog](/user-guide/tables-iceberg-configure-catalog-integration-open-catalog).

**Optional:**

`parent_namespace`
:   The identifier of the namespace from which to start listing namespaces.

    If `CATALOG_NAMESPACE` is defined at the catalog integration level, to retrieve results for the 0th namespace level in the
    catalog, specify an empty string (`''`).

    If `CATALOG_NAMESPACE` is only defined at the table level, the results for the 0th namespace level are returned by default, so
    you don’t need to specify an empty string (`''`).

    Default:

    > - If `CATALOG_NAMESPACE` is defined at the catalog integration level, the namespace for the catalog integration.
    > - If `CATALOG_NAMESPACE` is only defined at the table level, you retrieve results for the 0th namespace level in the catalog.

`levels`
:   Specifies the number of levels to traverse in the namespace hierarchy for listing child namespaces.

    For example:

    - If set to 0, the function returns all of the namespaces, recursively, relative to the `parent_namespace`.
    - If set to 1, the function returns all of the namespaces one level under the `parent_namespace`.
    - If set to *n*, the function returns namespaces up to *n* levels deep, relative to the `parent_namespace`.

    Default: 1

## Returns

Returns a JSON-formatted string which lists namespaces in the Iceberg REST catalog for the specified
parent namespace and number of levels.

The JSON-formatted string has the following structure:

Copy code

```
[
  "<namespace_identifier>",
  "<namespace_identifier_n>"
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

List only the namespaces directly under the default namespace of the catalog integration:

Copy code

```
SELECT SYSTEM$LIST_NAMESPACES_FROM_CATALOG('my_catalog_integration');
```

List all namespaces recursively in the catalog:

Copy code

```
SELECT SYSTEM$LIST_NAMESPACES_FROM_CATALOG('my_catalog_integration', '', 0);
```

List only the namespaces one level under (directly under) the ‘’db1’’ namespace:

Copy code

```
SELECT SYSTEM$LIST_NAMESPACES_FROM_CATALOG('my_catalog_integration', 'db1');
```

List the namespaces three levels under the ‘’db1’’ namespace:

Copy code

```
SELECT SYSTEM$LIST_NAMESPACES_FROM_CATALOG('my_catalog_integration', 'db1', 3);
```
