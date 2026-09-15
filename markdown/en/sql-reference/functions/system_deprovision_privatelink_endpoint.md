Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deprovisions a private connectivity endpoint in the Snowflake VPC or VNet to prevent Snowflake from connecting to an external service by using
private connectivity. The endpoint can be a service endpoint or a resource endpoint depending on the cloud platform that hosts your
Snowflake account.

If you call this function and specify the wrong private connectivity endpoint, call the [SYSTEM$RESTORE\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_restore_privatelink_endpoint) system
function to restore the endpoint within a seven day period. After seven days, the endpoint is deleted and cannot be recovered; you
will need to recreate the endpoint with the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function.

## Syntax

**AWS:**

> Copy code
>
> ```
> SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT(
>  '<provider_service_name>' )
> ```

**Azure:**

> Copy code
>
> ```
> SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT(
>  '<provider_resource_id>'
>  [, '<subresource>' ]
> )
> ```

**Google Cloud**

Copy code

```
 SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT(
   '<service_attachment_id>'
);
```

## Arguments

**AWS**

`provider_service_name`
:   Specifies the external service or resource endpoint to restore. For example, `com.amazonaws.us-west-2.execute-api` for the Amazon API
    Gateway or `com.amazonaws.us-west-2.s3` for Amazon S3.

**Azure**

`'provider_resource_id'`
:   Specifies the fully-qualified identifier for the resource in your VPC or VNet.

`'subresource'`
:   Specifies the name of the subresource of the Azure resource.

    This argument is not required for [Azure Private Link Service](https://learn.microsoft.com/en-us/azure/private-link/private-link-service-overview) and Azure API Management Service.

    For all supported values, see the [Sub-resource table](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview#private-link-resource).

**Google Cloud**

`'target_service_id'`
:   Specifies the ID of the service attachment in your VPC network or the regional Google API.

## Returns

Returns a status message stating that the endpoint, with its identifier, is deprovisioned successfully.

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Usage notes

- An error message occurs if a private connectivity endpoint is not associated with the specified arguments.

## Examples

**AWS:**

> Deprovision a private endpoint with external access to Amazon S3:

Copy code

```
SELECT SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT('com.amazonaws.us-west-2.s3');
```

**Azure:**

> Deprovision a private endpoint to prevent Snowflake on Microsoft Azure from connecting to the Microsoft Azure API Management service in your
> Microsoft Azure VNet:
>
> Copy code
>
> ```
> SELECT SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT(
>   '/subscriptions/f4b00c5f-f6bf-41d6-806b-e1cac4f1f36f/resourceGroups/aztest1-external-function-rg/providers/Microsoft.ApiManagement/service/aztest1-external-function-api',
>   'Gateway'
>   );
> ```
>
> ```
> Private endpoint with id "/subscriptions/e48379a7-2fc4-473e-b071-f94858cc83f5/resourcegroups/test_rg/providers/microsoft.network/privateendpoints/5ef8fd34-07db-4583-b0dd-0e2360398ed3" successfully marked for deletion. Before it is fully deleted in 7-8 days, it can be restored.
> ```
>
> Deprovision a private endpoint to prevent Snowflake on Microsoft Azure from connecting to an external service using external network access:
>
> Copy code
>
> ```
> SELECT SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT(
>   '/subscriptions/11111111-2222-3333-4444-5555555555/resourceGroups/leorg1/providers/Microsoft.Sql/servers/myserver/databases/testdb',
>   'sqlServer'
>   );
> ```
>
> ```
> "Resource Endpoint with id "/subscriptions/f0abb333-1b05-47c6-8c31-dd36d2512fd1/resourceGroups/privatelink-test/providers/Microsoft.Network/privateEndpoints/external-network-access-pe" deprovisioned successfully"
> ```
>
> Deprovision a private endpoint to prevent Snowflake from connecting to an external stage for Microsoft Azure:
>
> Copy code
>
> ```
> SELECT SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT(
>   '/subscriptions/cb72345g5-d347-4sdc-r3ee-70d234551a78/resourceGroups/rg-db-dev/providers/Microsoft.Storage/storageAccounts/dbasdfffext',
>   'blob'
> );
> ```
>
> ```
> "Resource Endpoint with id "/subscriptions/57faea9a-20c2-4d35-b283-9c0c1e9593d8/resourceGroups/privatelink-test/providers/Microsoft.Network/privateEndpoints/external-network-access-pe" deprovisioned successfully"
> ```

**Google Cloud**

> Deprovision a private endpoint to prevent Snowflake on Google Cloud from connecting to the service attachment in your Google Cloud VPC
> Network:
>
> Copy code
>
> ```
> SELECT SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT(
>   'projects/my-project/regions/us-east4/serviceAttachments/my-service-attachment'
>   );
> ```
>
> ```
> Private endpoint with id "abcd0000000000000001" successfully marked for deletion. Before it is fully deleted in 7-8 days, it can be restored.
> ```
>
> Deprovision a private endpoint to prevent Snowflake on Google Cloud from connecting to a regional Google service endpoint (CloudKMS):
>
> Copy code
>
> ```
> SELECT SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT(
>  'cloudkms.us-east4.rep.googleapis.com'
>  );
> ```
>
> ```
> Private endpoint with id "abcd0000000000000001" successfully marked for deletion. Before it is fully deleted in 7-8 days, it can be restored.
> ```
>
> Deprovision a private endpoint to prevent Snowflake from connecting to an external stage for Google Cloud:
>
> Copy code
>
> ```
> SELECT SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT(
>  'storage.us-east4.rep.googleapis.com'
>  );
> ```
>
> ```
> Private endpoint with id "abcd0000000000000001" successfully marked for deletion. Before it is fully deleted in 7-8 days, it can be restored.
> ```
