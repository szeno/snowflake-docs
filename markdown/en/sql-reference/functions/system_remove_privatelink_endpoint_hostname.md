Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$REMOVE\_PRIVATELINK\_ENDPOINT\_HOSTNAME

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Removes an additional host name from an existing [private connectivity endpoint](/user-guide/private-connectivity-outbound). Use this
function to remove a host name that you previously added with [SYSTEM$ADD\_PRIVATELINK\_ENDPOINT\_HOSTNAME](/sql-reference/functions/system_add_privatelink_endpoint_hostname).

This function doesn’t affect the endpoint’s primary host name, that is, the host name that you set at provisioning time or with
[SYSTEM$SET\_PRIVATELINK\_ENDPOINT\_HOSTNAME](/sql-reference/functions/system_set_privatelink_endpoint_hostname).

## Syntax

Copy code

```
SYSTEM$REMOVE_PRIVATELINK_ENDPOINT_HOSTNAME( '<provider_resource_id>' , '<host_name>' [ , '<subresource>' ] )
```

## Arguments

`'provider_resource_id'`
:   Specifies the fully qualified identifier for the resource in your VNet that the endpoint already connects to. This is the same identifier
    that you specified when you provisioned the endpoint using [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint).

`'host_name'`
:   Specifies the additional host name to remove from the endpoint. This must be a host name that you previously added with
    [SYSTEM$ADD\_PRIVATELINK\_ENDPOINT\_HOSTNAME](/sql-reference/functions/system_add_privatelink_endpoint_hostname), not the endpoint’s primary host name.

`'subresource'`
:   Specifies the name of the subresource of the Azure resource.

    Specify this value only if you specified a subresource when you provisioned the endpoint.

    For all supported values, see the [Sub-resource table](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview#private-link-resource).

## Returns

Returns a status message that the host name was removed successfully from the private connectivity endpoint, or details and instructions
about why the host name wasn’t removed successfully.

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Usage notes

- This function is only supported for Snowflake accounts hosted on Microsoft Azure.
- You can’t use this function to remove an endpoint’s primary host name. To change the primary host name, use
  [SYSTEM$SET\_PRIVATELINK\_ENDPOINT\_HOSTNAME](/sql-reference/functions/system_set_privatelink_endpoint_hostname).
- You don’t need to remove additional host names before you deprovision the endpoint. Deprovisioning the endpoint with
  [SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_deprovision_privatelink_endpoint) removes all additional host names on the endpoint
  automatically.

## Examples

Remove the OneLake storage host name that you previously added to an endpoint that connects to a Microsoft Fabric workspace:

Copy code

```
SELECT SYSTEM$REMOVE_PRIVATELINK_ENDPOINT_HOSTNAME(
  '/subscriptions/e29b4130-0198-4a5d-9f2c-7db3c8a1e6f4/resourceGroups/fabric-sandbox-rg/providers/Microsoft.Fabric/privateLinkServicesForFabric/fabric-workspace-capacity',
  '00112233445566778899aabbccddeeff.z01.dfs.fabric.microsoft.com',
  'workspace'
  );
```

```
Successfully removed the host name 00112233445566778899aabbccddeeff.z01.dfs.fabric.microsoft.com from the privatelink endpoint /subscriptions/e29b4130-0198-4a5d-9f2c-7db3c8a1e6f4/resourceGroups/fabric-sandbox-rg/providers/Microsoft.Fabric/privateLinkServicesForFabric/fabric-workspace-capacity
```
