Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_CATALOG\_LINKED\_DATABASE\_CONFIG

Returns the configuration parameters set on the specified [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database). The output is in JSON format.

## Syntax

Copy code

```
SYSTEM$GET_CATALOG_LINKED_DATABASE_CONFIG('<catalog_linked_database_name>');
```

## Arguments

`catalog_linked_database_name`
:   The name of the catalog-linked database you want to get the configuration for.

    Specify it as a string literal enclosed in single quotes.

## Returns

The function returns a string that contains a JSON object with the database’s configuration parameters.

| Field | Description |
| --- | --- |
| `catalog_integration` | Name of the catalog integration used by the catalog-linked database. |
| `catalog_name` | Name of the catalog namespace in the external catalog. Returns `null` if not specified. |
| `external_volume` | Name of the external volume used for table storage. |
| `sync_interval_seconds` | Interval (in seconds) that Snowflake polls the remote catalog to detect changes. |
| `namespace_mode` | Mode for handling namespaces. Possible values: `FLATTEN_NESTED_NAMESPACE`, `HIERARCHICAL`. |
| `namespace_flatten_delimiter` | Delimiter used when flattening nested namespaces. Only applicable when `namespace_mode` is `FLATTEN_NESTED_NAMESPACE`. |
| `allowed_write_operations` | Types of write operations allowed on the catalog-linked database. Possible values: `NONE`, `ALL`. |
| `catalog_case_sensitivity` | Case sensitivity setting for the catalog. Possible values: `CASE_SENSITIVE`, `CASE_INSENSITIVE`. |
| `is_suspended` | Whether the catalog-linked database synchronization is suspended. Returns `true` if suspended, `false` otherwise. |
| `allowed_namespaces` | List of namespaces that are allowed to be synced. Returns `null` if all namespaces are allowed. |
| `blocked_namespaces` | List of namespaces that are blocked from being synced. Returns `null` if no namespaces are blocked. |

Expand

Show lessSee more

For a sample output, see [Examples](#label-functions-get-catalog-linked-database-config-examples).

## Access control requirements

A role used to execute this operation must have the MONITOR, USAGE, OWNERSHIP, or ALL privilege.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

Get the configuration for a catalog-linked database named `my_db`:

Copy code

```
SELECT SYSTEM$GET_CATALOG_LINKED_DATABASE_CONFIG('my_db');
```

An example output:

Copy code

```
{
  "catalog_integration": "TEST_GET_CLD_CONFIG_EBEC9E22_44BD_4945_A4C3_A402CCBB86AF_CAT",
  "catalog_name": null,
  "external_volume": "EXVOL_GET_CLD_CONFIG",
  "sync_interval_seconds": 600,
  "namespace_mode": "FLATTEN_NESTED_NAMESPACE",
  "namespace_flatten_delimiter": "_",
  "allowed_write_operations": "NONE",
  "catalog_case_sensitivity": "CASE_INSENSITIVE",
  "is_suspended": false,
  "allowed_namespaces": ["'ns1'", "'ns2'"],
  "blocked_namespaces": ["'blocked_ns1'"]
}
```
