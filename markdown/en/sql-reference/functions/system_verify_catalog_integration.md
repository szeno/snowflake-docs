Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$VERIFY\_CATALOG\_INTEGRATION

Verifies the configuration for a specified catalog integration for Apache Iceberg™ REST.

To check whether you’ve correctly configured authorization and access control with your Iceberg REST catalog,
the function attempts to use the catalog integration to interact with your catalog server.

See also:
:   [CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest) , [Configure a catalog integration for Apache Iceberg™ REST catalogs](/user-guide/tables-iceberg-configure-catalog-integration-rest)

## Syntax

Copy code

```
SYSTEM$VERIFY_CATALOG_INTEGRATION( '<rest_catalog_integration_name>' )
```

## Arguments

`rest_catalog_integration_name`
:   Name of the [Iceberg REST catalog integration](/sql-reference/sql/create-catalog-integration-rest) to test.

    Catalog integration names are case sensitive.

## Returns

The function returns a JSON object with the properties described below:

| Property | Description |
| --- | --- |
| `success` | Specifies whether verification was successful; `true` if successful, otherwise `false`. |
| `errorCode` | Error code of the failure (if verification fails). |
| `errorMessage` | A detailed error message (if verification fails). |

Expand

Show lessSee more

Copy code

```
{
  "success" : false,
  "errorCode" : "004140",
  "errorMessage" : "SQL Execution Error: Failed to access the REST endpoint of catalog integration CAT_INT_VERIFICATION with error: Unable to process: Unable to find warehouse my_warehouse. Check the accessibility of the REST catalog URI or warehouse."
}
```

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Catalog integration |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

The following example statement creates a REST catalog integration
using an invalid OAuth client secret (this runs without error):

Copy code

```
CREATE CATALOG INTEGRATION my_rest_cat_int
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  CATALOG_NAMESPACE = 'default'
  REST_CONFIG = (
    CATALOG_URI = 'https://abc123.us-west-2.aws.myapi.com/polaris/api/catalog'
    CATALOG_NAME = 'my_catalog_name'
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_CLIENT_ID = '123AbC ...'
    OAUTH_CLIENT_SECRET = '1365910abIncorrectSecret ...'
    OAUTH_ALLOWED_SCOPES = ('all-apis', 'sql')
  )
  ENABLED = TRUE;
```

Use the system function to verify the catalog integration, expecting failure:

Copy code

```
SELECT SYSTEM$VERIFY_CATALOG_INTEGRATION('my_rest_cat_int');
```

Output:

```
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                                                                                              SYSTEM$VERIFY_CATALOG_INTEGRATION('MY_REST_CAT_INT')                                                                                                               |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| {                                                                                                                                                                                                                                                                               |
|  "success" : false,                                                                                                                                                                                                                                                             |                                                                                                                                                                                                                                                                    |
|   "errorCode" : "004155",                                                                                                                                                                                                                                                       |
|   "errorMessage" : "SQL Execution Error: Failed to perform OAuth client credential flow for the REST Catalog integration MY_REST_CAT_INT due to error: SQL execution error: OAuth2 Access token request failed with error 'unauthorized_client:The client is not authorized'.." |
| }                                                                                                                                                                                                                                                                               |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```
