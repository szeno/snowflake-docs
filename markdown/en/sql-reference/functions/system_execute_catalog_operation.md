Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$EXECUTE\_CATALOG\_OPERATION

Executes a catalog operation against a [catalog integration](/sql-reference/sql/create-catalog-integration)
so you can inspect and validate the remote catalog that the integration connects to.

Use this function to verify connectivity, list namespaces or tables, retrieve the latest table metadata
file location, and check that scoped credentials can be retrieved. Supported operations depend on the
catalog type and the capabilities of the catalog integration (for example, Iceberg REST, Glue, Polaris,
or SAP BDC).

Call the function with the `help` operation to list the operations available for your account and the
positional arguments each operation accepts.

See also:
:   [SYSTEM$VERIFY\_CATALOG\_INTEGRATION](/sql-reference/functions/system_verify_catalog_integration) ,
    [SYSTEM$LIST\_ICEBERG\_TABLES\_FROM\_CATALOG](/sql-reference/functions/system_list_iceberg_tables_from_catalog) ,
    [SYSTEM$LIST\_NAMESPACES\_FROM\_CATALOG](/sql-reference/functions/system_list_namespaces_from_catalog) ,
    [CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest) ,
    [Configure a catalog integration for Apache Iceberg™ REST catalogs](/user-guide/tables-iceberg-configure-catalog-integration-rest)

## Syntax

Copy code

```
SYSTEM$EXECUTE_CATALOG_OPERATION( '<catalog_integration_name>' , '<operation_name>'
  [ , '<arg1>' [ , '<arg2>' [ , '<arg3>' ] ] ] )
```

## Arguments

**Required:**

`catalog_integration_name`
:   Name of the catalog integration to operate on. The name is resolved in the current account.

    Catalog integration names are case-sensitive.

`operation_name`
:   Name of the operation to run. Operation names are case-insensitive.

    For the list of operations and their arguments, see [Supported operations](#supported-operations),
    or call the function with `'help'`.

**Optional:**

`arg1`, `arg2`, `arg3`
:   Positional arguments for the operation. The meaning of each argument depends on the operation.
    Omit unused trailing arguments.

    If an operation accepts a namespace or catalog name argument and you omit it, Snowflake uses the
    default namespace or catalog name configured on the catalog integration, when available.

## Returns

Returns a string result for the operation:

- For most operations, a JSON-formatted string.
- For `help`, a formatted table that lists available operations and their arguments.
- For `verify`, a verification message string (or a JSON status object if verification is not
  supported for the catalog type).

## Supported operations

The following operations are available. Not every catalog integration supports every operation.
If you call an unsupported operation, the function returns an error that names the catalog
integration and client type.

| Operation | arg1 | arg2 | arg3 | Description |
| --- | --- | --- | --- | --- |
| `listTables` | `namespace` (optional) | `catalogName` (optional) | N/A | Lists tables in a namespace. |
| `listNamespaces` | `namespace` (optional) | `catalogName` (optional) | N/A | Lists namespaces under a parent namespace. |
| `loadTable` | `catalogTableNamespace` (optional) | `catalogTableName` (required) | `catalogName` (optional) | Returns the latest metadata file location for a table. |
| `getVendedCredentials` | `catalogTableNamespace` (optional) | `catalogTableName` (required) | `catalogName` (optional) | Checks whether scoped access credentials can be retrieved for a table. Returns a status message; does not return credential values. |
| `loadCredentials` | `catalogTableNamespace` (optional) | `catalogTableName` (required) | `catalogName` (optional) | Checks whether scoped access credentials can be retrieved by using the Iceberg REST `loadCredentials` API. Supported for specific catalog vendors (currently Microsoft OneLake). Returns a status message; does not return credential values. |
| `listShares` | `catalogName` (optional) | N/A | N/A | Lists available catalogs (shares) for catalog types that expose that capability. |
| `listCatalogs` | `catalogName` (optional) | N/A | N/A | Lists available catalogs. If you specify `catalogName`, the result is filtered to that catalog name (case-insensitive). |
| `verify` | N/A | N/A | N/A | Validates the catalog integration configuration and connectivity. |
| `help` | N/A | N/A | N/A | Returns the help listing of operations and arguments. |

Expand

Show lessSee more

### Return details

**`listTables`**

Returns a JSON array of table identifiers in the specified namespace.

**`listNamespaces`**

Returns a JSON array of namespace identifiers under the specified parent namespace.

**`loadTable`**

Returns a JSON object with the following property:

| Property | Description |
| --- | --- |
| `metadataFile` | Location of the latest metadata file for the table. |

Expand

Show lessSee more

Copy code

```
{
  "metadataFile": "s3://my_bucket/path/to/table/metadata/00001-abc.metadata.json"
}
```

**`getVendedCredentials` and `loadCredentials`**

Return a JSON object with a `status` property. The function confirms that credentials can be
retrieved; it does not return the credential values.

Copy code

```
{
  "status": "Credentials retrieved successfully"
}
```

**`listShares` and `listCatalogs`**

Return a JSON array of catalog names.

**`verify`**

Returns a verification message that describes whether the catalog integration configuration is
valid. For catalog types that do not support verification, returns:

Copy code

```
{
  "status": "Verification not supported for this catalog type"
}
```

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Catalog integration | Required on the catalog integration named in the function call. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Operation names are case-insensitive. Catalog integration names are case-sensitive.
- Namespace arguments are treated as a single namespace level. For deeper hierarchies, use the
  dedicated [SYSTEM$LIST\_ICEBERG\_TABLES\_FROM\_CATALOG](/sql-reference/functions/system_list_iceberg_tables_from_catalog) and
  [SYSTEM$LIST\_NAMESPACES\_FROM\_CATALOG](/sql-reference/functions/system_list_namespaces_from_catalog) functions when those fit your
  catalog type.
- Client-level failures (for example, network errors or catalog authorization failures) surface as
  SQL errors rather than as JSON error payloads.
- `getVendedCredentials` and `loadCredentials` return only a success or failure status. They do not
  expose temporary credential values in the query result.
- `loadCredentials` is only available for catalog vendors that support the Iceberg REST
  `loadCredentials` API. Calls against unsupported vendors return an error.

## Examples

List the operations available for a catalog integration:

Copy code

```
SELECT SYSTEM$EXECUTE_CATALOG_OPERATION('my_catalog_integration', 'help');
```

Verify connectivity for a catalog integration:

Copy code

```
SELECT SYSTEM$EXECUTE_CATALOG_OPERATION('my_catalog_integration', 'verify');
```

List tables in the default catalog namespace:

Copy code

```
SELECT SYSTEM$EXECUTE_CATALOG_OPERATION('my_catalog_integration', 'listTables');
```

List tables under the `db1` namespace:

Copy code

```
SELECT SYSTEM$EXECUTE_CATALOG_OPERATION('my_catalog_integration', 'listTables', 'db1');
```

List child namespaces under `db1`:

Copy code

```
SELECT SYSTEM$EXECUTE_CATALOG_OPERATION('my_catalog_integration', 'listNamespaces', 'db1');
```

Get the latest metadata file location for table `t1` in namespace `db1`:

Copy code

```
SELECT SYSTEM$EXECUTE_CATALOG_OPERATION(
  'my_catalog_integration',
  'loadTable',
  'db1',
  't1'
);
```

Confirm that scoped credentials can be retrieved for a table:

Copy code

```
SELECT SYSTEM$EXECUTE_CATALOG_OPERATION(
  'my_catalog_integration',
  'getVendedCredentials',
  'db1',
  't1'
);
```
