Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$ADD\_PRIVATELINK\_ENDPOINT\_HOSTNAME

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Adds an additional host name to an existing [private connectivity endpoint](/user-guide/private-connectivity-outbound) that connects to a
service that supports more than one host name on the same endpoint, such as a Microsoft Fabric workspace. Use this function when Snowflake
needs to reach more than one host name through the same endpoint, for example, the Iceberg REST catalog host name and the OneLake storage
host name for the same Fabric workspace.

Note

The private endpoint connection must be in the Approved state on the target resource before you call this function. If the connection isn’t
approved yet, the function returns an error that includes the current connection state.

## Syntax

Copy code

```
SYSTEM$ADD_PRIVATELINK_ENDPOINT_HOSTNAME( '<provider_resource_id>' , '<host_name>' [ , '<subresource>' ] )
```

## Arguments

`'provider_resource_id'`
:   Specifies the fully qualified identifier for the resource in your VNet that the endpoint already connects to. This is the same identifier
    that you specified when you provisioned the endpoint using [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint).

`'host_name'`
:   Specifies the additional fully qualified host name to add to the endpoint. Snowflake uses this host name alongside the endpoint’s existing
    host names; it doesn’t replace them.

    This value doesn’t contain any port numbers.

`'subresource'`
:   Specifies the name of the subresource of the Azure resource.

    Specify this value only if you specified a subresource when you provisioned the endpoint.

    For all supported values, see the [Sub-resource table](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview#private-link-resource).

## Returns

Returns a status message that the host name was added successfully to the private connectivity endpoint, or details and instructions about
why the host name wasn’t added successfully.

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Usage notes

- This function is only supported for Snowflake accounts hosted on Microsoft Azure.
- You can add a host name only to an endpoint that connects to a resource that supports multiple host names on a single endpoint, such as a
  Microsoft Fabric workspace or a customer-managed Azure Private Link service. You can’t add a host name to an endpoint that connects to a
  resource that only supports a single, fixed host name (for example, an Azure Storage account, Azure Key Vault, or Azure Database for
  PostgreSQL flexible server).
- The host name that you add can’t collide with the endpoint’s primary host name or with another additional host name already registered
  on the same endpoint.
- To remove a host name that you added with this function, use [SYSTEM$REMOVE\_PRIVATELINK\_ENDPOINT\_HOSTNAME](/sql-reference/functions/system_remove_privatelink_endpoint_hostname).
- Deprovisioning the endpoint with [SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_deprovision_privatelink_endpoint) removes all additional
  host names on the endpoint.

## Examples

Add the OneLake storage host name to an existing endpoint that connects to a Microsoft Fabric workspace, so that Snowflake can reach both the
Iceberg REST catalog host name and the OneLake storage host name through the same endpoint:

Copy code

```
SELECT SYSTEM$ADD_PRIVATELINK_ENDPOINT_HOSTNAME(
  '/subscriptions/e29b4130-0198-4a5d-9f2c-7db3c8a1e6f4/resourceGroups/fabric-sandbox-rg/providers/Microsoft.Fabric/privateLinkServicesForFabric/fabric-workspace-capacity',
  '00112233445566778899aabbccddeeff.z01.dfs.fabric.microsoft.com',
  'workspace'
  );
```

```
Successfully added the host name 00112233445566778899aabbccddeeff.z01.dfs.fabric.microsoft.com to the privatelink endpoint /subscriptions/e29b4130-0198-4a5d-9f2c-7db3c8a1e6f4/resourceGroups/fabric-sandbox-rg/providers/Microsoft.Fabric/privateLinkServicesForFabric/fabric-workspace-capacity
```
