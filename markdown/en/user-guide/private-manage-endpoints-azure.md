# Manage private connectivity endpoints: Azure

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides information on how to manage private connectivity endpoints for use with private connectivity to an external service. The examples are specific to Microsoft Azure.

## Provision private connectivity endpoints

You can create a private connectivity endpoint by calling the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system
function. For example, for your Snowflake account on Microsoft Azure:

Provision a private endpoint to allow Snowflake on Microsoft Azure to connect to the Microsoft Azure API Management service in your Microsoft Azure VNet:

Copy code

```
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  '/subscriptions/f4b00c5f-f6bf-41d6-806b-e1cac4f1f36f/resourceGroups/aztest1-external-function-rg/providers/Microsoft.ApiManagement/service/aztest1-external-function-api',
  'aztest1-external-function-api.azure.net',
  'Gateway'
  );
```

```
Private endpoint with ID "/subscriptions/e48379a7-2fc4-473e-b071-f94858cc83f5/resourcegroups/test_rg/providers/microsoft.network/privateendpoints/32bd3122-bfbd-417d-8620-1a02fd68fcf8" to resource "/subscriptions/f4b00c5f-f6bf-41d6-806b-e1cac4f1f36f/resourceGroups/aztest1-external-function-rg/providers/Microsoft.ApiManagement/service/aztest1-external-function-api" has been provisioned successfully. Please note down the endpoint ID and approve the connection from it on the Azure portal.
```

Provision a private endpoint to allow Snowflake on Microsoft Azure to connect to an external service using external network access:

Copy code

```
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  '/subscriptions/11111111-2222-3333-4444-5555555555/resourceGroups/leorg1/providers/Microsoft.Sql/servers/myserver',
  'testdb.database.windows.net',
  'sqlServer'
  );
```

```
"Resource Endpoint with id "/subscriptions/f0abb333-1b05-47c6-8c31-dd36d2512fd1/resourceGroups/privatelink-test/providers/Microsoft.Network/privateEndpoints/external-network-access-pe" provisioned successfully"
```

Provision a private endpoint to allow Snowflake to connect to an external stage for Microsoft Azure:

Copy code

```
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  '/subscriptions/cc2909f2-ed22-4c89-8e5d-bdc40e5eac26/resourceGroups/mystorage/providers/Microsoft.Storage/storageAccounts/storagedemo',
  'storagedemo.blob.core.windows.net',
  'blob'
);
```

```
"Resource Endpoint with id "/subscriptions/57faea9a-20c2-4d35-b283-9c0c1e9593d8/resourceGroups/privatelink-test/providers/Microsoft.Network/privateEndpoints/external-network-access-pe" provisioned successfully"
```

Snowflake calls the APIs for the cloud platform that hosts your Snowflake account to create the endpoint and updates the related networking
configurations.

Note

Private connectivity endpoints aren’t supported for Microsoft Fabric OneLake storage locations.

## Change the host name of a private connectivity endpoint

You can change only the host name of a previously provisioned, private connectivity endpoint without changing its network resource.
Changing the host name for an endpoint tells Snowflake that this endpoint now connects to the same service by using a different host name. To
change the host name, call the [SYSTEM$SET\_PRIVATELINK\_ENDPOINT\_HOSTNAME](/sql-reference/functions/system_set_privatelink_endpoint_hostname) system function.

## Add or remove an additional host name on a private connectivity endpoint

Some services expose more than one host name on the same private endpoint. For example, a Microsoft Fabric workspace has separate host
names for its Iceberg REST catalog and its OneLake storage, but Azure only lets you provision one private endpoint to the workspace. To
reach more than one host name through the same endpoint, provision the endpoint with the first host name as usual, then call the
[SYSTEM$ADD\_PRIVATELINK\_ENDPOINT\_HOSTNAME](/sql-reference/functions/system_add_privatelink_endpoint_hostname) system function to register each additional host name:

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

To remove a host name that you previously added, call the [SYSTEM$REMOVE\_PRIVATELINK\_ENDPOINT\_HOSTNAME](/sql-reference/functions/system_remove_privatelink_endpoint_hostname) system
function:

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

This doesn’t affect the endpoint’s primary host name. You don’t need to remove additional host names before you deprovision the endpoint;
deprovisioning removes all of an endpoint’s additional host names automatically.

## List private connectivity endpoints

You can list the private connectivity endpoints that you create by calling the
[SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info) system function. For example, for your Snowflake account on Microsoft Azure:

SQLReturned value

Copy code

```
SELECT SYSTEM$GET_PRIVATELINK_ENDPOINTS_INFO();
```

Copy code

```
[
  {
    "provider_resource_id": "/subscriptions/11111111-2222-3333-4444-5555555555/...",
    "subresource": "sqlServer",
    "snowflake_resource_id": "/subscriptions/66666666-7777-8888-9999-000000000000/...",
    "host": "testdb.database.windows.net",
    "endpoint_state": "CREATED",
    "status": "Approved",
    "additional_hostnames": []
  }
]
```

Note

You can also query the [OUTBOUND\_PRIVATELINK\_ENDPOINTS](/sql-reference/account-usage/outbound_privatelink_endpoints) view in the
ACCOUNT\_USAGE schema to list the private endpoints in your account.

## Deprovision private connectivity endpoints

You can delete an existing private connectivity endpoint by calling the
[SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_deprovision_privatelink_endpoint) system function. For example, for your Snowflake account on Microsoft Azure:

Deprovision a private endpoint to prevent Snowflake on Microsoft Azure from connecting to the Microsoft Azure API Management service in your
Microsoft Azure VNet:

Copy code

```
SELECT SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT(
  '/subscriptions/f4b00c5f-f6bf-41d6-806b-e1cac4f1f36f/resourceGroups/aztest1-external-function-rg/providers/Microsoft.ApiManagement/service/aztest1-external-function-api',
  'Gateway'
  );
```

```
Private endpoint with id "/subscriptions/e48379a7-2fc4-473e-b071-f94858cc83f5/resourcegroups/test_rg/providers/microsoft.network/privateendpoints/5ef8fd34-07db-4583-b0dd-0e2360398ed3" successfully marked for deletion. Before it is fully deleted in 7-8 days, it can be restored.
```

Deprovision a private endpoint to prevent Snowflake on Microsoft Azure from connecting to an external service using external network access:

Copy code

```
SELECT SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT(
  '/subscriptions/11111111-2222-3333-4444-5555555555/resourceGroups/leorg1/providers/Microsoft.Sql/servers/myserver/databases/testdb',
  'sqlServer'
  );
```

```
"Resource Endpoint with id "/subscriptions/f0abb333-1b05-47c6-8c31-dd36d2512fd1/resourceGroups/privatelink-test/providers/Microsoft.Network/privateEndpoints/external-network-access-pe" deprovisioned successfully"
```

Deprovision a private endpoint to prevent Snowflake from connecting to an external stage for Microsoft Azure:

Copy code

```
SELECT SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT(
  '/subscriptions/cb72345g5-d347-4sdc-r3ee-70d234551a78/resourceGroups/rg-db-dev/providers/Microsoft.Storage/storageAccounts/dbasdfffext',
  'blob'
);
```

```
"Resource Endpoint with id "/subscriptions/57faea9a-20c2-4d35-b283-9c0c1e9593d8/resourceGroups/privatelink-test/providers/Microsoft.Network/privateEndpoints/external-network-access-pe" deprovisioned successfully"
```

## Restore a deprovisioned private connectivity endpoint

You can restore a private connectivity endpoint that you deprovisioned within 7 days of deprovisioning it by calling the
[SYSTEM$RESTORE\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_restore_privatelink_endpoint) system function. After 7 days, the endpoint cannot be restored and you
need to provision a new endpoint.

Restore a private endpoint to allow Snowflake on Microsoft Azure to connect to the Azure API Management service in your Azure VNet:

Copy code

```
SELECT SYSTEM$RESTORE_PRIVATELINK_ENDPOINT(
  '/subscriptions/11111111-2222-3333-4444-5555555555/resourceGroups/my_rg/providers/Microsoft.Sql/servers/my_db_server',
  'sqlServer'
);
```

```
Private endpoint with id ''/subscriptions/66666666-7777-8888-9999-0000000000/resourcegroups/rg/providers/microsoft.network/privateendpoints/00000000-1111-2222-3333-4444444444'' restored successfully.
```

## Troubleshooting

### Microsoft Azure external services: You cannot access a specified subscription

|  |  |
| --- | --- |
| Error | ``` (LinkedAuthorizationFailed) The client has permission to perform action '<action_name>' on scope '<service_name>', however the current tenant '<tenant_id>' is not authorized to access linked subscription '<subscription_id'.  Code: LinkedAuthorizationFailed  Message: The client has permission to perform action '<action_name>' on scope '<service_name>', however the current tenant '<tenant_id>' is not authorized to access linked subscription '<subscription_id>'. ``` |
| Cause | The private endpoint that maps to the external service does not have the correct information to access the subscription. |
| Solution | 1. Call the [SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_deprovision_privatelink_endpoint) system function to delete the endpoint for the    external service. 2. Call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to recreate the endpoint for the    external service. Be sure    to specify the correct subscription, host name, and subresource values. 3. [Replace](/sql-reference/sql/create-network-rule) the network rule and be sure to specify the correct host name value in the    `VALUE_LIST` property. |

Expand

Show lessSee more
