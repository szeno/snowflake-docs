Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Provisions a private connectivity endpoint in the Snowflake VPC or VNet to enable Snowflake to connect to an external service by using private
connectivity. The endpoint can be a service endpoint or a resource endpoint depending on the cloud platform that hosts your Snowflake
account.

Note

If the Snowflake account is in an Azure government region, the provider resource ID must be the ID of a resource in a government
subscription. For more information about government regions for Snowflake customers, see [U.S. SnowGov Regions](/user-guide/intro-regions#label-intro-regions-snowgov-regions).

## Syntax

**AWS:**

> Copy code
>
> ```
> SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
>   '<provider_service_name>',
>   '<host_name>'
> )
> ```

**Azure:**

> Copy code
>
> ```
> SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
>   '<provider_resource_id>',
>   '<host_name>',
>   [, '<subresource>' ]
> )
> ```

**Google Cloud:**

> Copy code
>
> ```
> SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
>   '<target_service_id>',
>   '<host_name>'
> )
> ```

## Arguments

**AWS:**

`'provider_service_name'`
:   Specifies the external service or resource to connect to. For example, `com.amazonaws.us-west-2.execute-api` for the Amazon API
    Gateway or `com.amazonaws.us-west-2.s3` for Amazon S3.

    Note

    When you connect to a VPC endpoint service in a region that is different from the Snowflake region, ensure that the VPC endpoint service supports the
    Snowflake region.

    For information about retrieving this value from AWS, see [Provision private connectivity endpoints](/user-guide/private-manage-endpoints-aws#label-private-link-external-access-aws-create-endpoints).

`'host_name'`
:   Specifies the fully-qualified host name to access the resource in your VPC or VNet.

    This value doesn’t contain any port numbers and must match what you specified in the Snowflake object that lets you to connect to the
    external service.

    > Examples include `bedrock-runtime.us-west-2.amazonaws.com` and `*.s3.us-west-2.amazonaws.com`.
    >
    > When using private connectivity for external stages and external volumes, the `host_name` must use a wildcard instead of
    > specifying a specific AWS S3 bucket.
    >
    > For information about retrieving this value from AWS, see [Provision private connectivity endpoints](/user-guide/private-manage-endpoints-aws#label-private-link-external-access-aws-create-endpoints).

**Azure:**

`'provider_resource_id'`
:   Specifies the fully qualified identifier for the resource in your VPC or VNet.

`'host_name'`
:   Specifies the fully qualified host name to access the resource in your VPC or VNet.

For examples of the host name for outbound private connectivity for external functions, see the following topics:

> - [Azure Portal](/sql-reference/external-functions-creating-azure-ui-private-connect)
> - [Azure ARM template](/sql-reference/external-functions-creating-azure-template-private-connect).

`'subresource'`
:   Specifies the name of the subresource of the Azure resource.

    This argument isn’t required for [Azure Private Link Service](https://learn.microsoft.com/en-us/azure/private-link/private-link-service-overview) and Azure API Management Service.

    For all supported values, see the [Sub-resource table](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview#private-link-resource).

**Google Cloud:**

`'target_service_id'`
:   Specifies the service attachment ID (to a custom service), or regional Google API endpoint to connect to.

`'host_name'`
:   Specifies the fully qualified host name to access the resource.

Note

When the target service ID is a regional Google API endpoint, the host name value should match the target service ID value.

## Returns

Returns a status message that the endpoint was provisioned successfully or details and instructions about why the endpoint was not
provisioned successfully.

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Usage notes

- You can modify only the host name of an existing private connectivity endpoint. To modify any other properties, you must deprovision the
  endpoint, then provision a new one. For more information about changing a host name, see [SYSTEM$SET\_PRIVATELINK\_ENDPOINT\_HOSTNAME](/sql-reference/functions/system_set_privatelink_endpoint_hostname).
- This function can take approximately 5 minutes to execute because it depends on the process to provision the private connectivity
  endpoint in the cloud platform (outside of Snowflake).
- For details about private endpoint limits, see [Scaling considerations](/user-guide/private-connectivity-outbound#label-private-connect-external-service-limits).

## Examples

AWS:
:   Set up outbound private connectivity to an external S3 service:

    Copy code

    ```
    SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
      'com.amazonaws.us-west-2.s3',
      '*.s3.us-west-2.amazonaws.com'
    );
    ```

    For more AWS examples, see the following guides:

    - [Set up private connectivity to an external Amazon S3 service](/developer-guide/external-network-access/creating-using-private-aws#label-setting-up-external-access-to-amazon-s3)
    - [Set up private connectivity to an external Amazon Bedrock service](/developer-guide/external-network-access/creating-using-private-aws#label-setting-up-external-access-to-amazon-bedrock)

Microsoft Azure:

> Provision a private endpoint to allow Snowflake on Microsoft Azure to connect to the Microsoft Azure API Management service in your Microsoft Azure VNet:
>
> Copy code
>
> ```
> SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
>   '/subscriptions/f4b00c5f-f6bf-41d6-806b-e1cac4f1f36f/resourceGroups/aztest1-external-function-rg/providers/Microsoft.ApiManagement/service/aztest1-external-function-api',
>   'aztest1-external-function-api.azure.net',
>   'Gateway'
>   );
> ```
>
> ```
> Private endpoint with ID "/subscriptions/e48379a7-2fc4-473e-b071-f94858cc83f5/resourcegroups/test_rg/providers/microsoft.network/privateendpoints/32bd3122-bfbd-417d-8620-1a02fd68fcf8" to resource "/subscriptions/f4b00c5f-f6bf-41d6-806b-e1cac4f1f36f/resourceGroups/aztest1-external-function-rg/providers/Microsoft.ApiManagement/service/aztest1-external-function-api" has been provisioned successfully. Please note down the endpoint ID and approve the connection from it on the Azure portal.
> ```
>
> Provision a private endpoint to allow Snowflake on Microsoft Azure to connect to an external service using external network access:
>
> Copy code
>
> ```
> SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
>   '/subscriptions/11111111-2222-3333-4444-5555555555/resourceGroups/leorg1/providers/Microsoft.Sql/servers/myserver',
>   'testdb.database.windows.net',
>   'sqlServer'
>   );
> ```
>
> ```
> "Resource Endpoint with id "/subscriptions/f0abb333-1b05-47c6-8c31-dd36d2512fd1/resourceGroups/privatelink-test/providers/Microsoft.Network/privateEndpoints/external-network-access-pe" provisioned successfully"
> ```
>
> Provision a private endpoint to allow Snowflake to connect to an external stage for Microsoft Azure:
>
> Copy code
>
> ```
> SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
>   '/subscriptions/cc2909f2-ed22-4c89-8e5d-bdc40e5eac26/resourceGroups/mystorage/providers/Microsoft.Storage/storageAccounts/storagedemo',
>   'storagedemo.blob.core.windows.net',
>   'blob'
> );
> ```
>
> ```
> "Resource Endpoint with id "/subscriptions/57faea9a-20c2-4d35-b283-9c0c1e9593d8/resourceGroups/privatelink-test/providers/Microsoft.Network/privateEndpoints/external-network-access-pe" provisioned successfully"
> ```

Google Cloud:

> Connect to a published service:
>
> Copy code
>
> ```
> SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
>   'projects/my-project/regions/us-west2/serviceAttachments/my-http-server',
>   'my-http-server.com'
> );
> ```
>
> After creating the endpoint, the connection must be accepted on Google Cloud by the resource provider.
>
> Provision a private endpoint to allow Snowflake on Google Cloud to connect to a service attachment in your Google Cloud VPC Network:
>
> Copy code
>
> ```
> SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
>   'projects/my-project/regions/us-east4/serviceAttachments/my-service-attachment',
>   'my-service.com'
>   );
> ```
>
> ```
> Private endpoint with ID "abcd0000000000000001" to resource "projects/my-project/regions/us-east4/serviceAttachments/my-service-attachment"
> was provisioned successfully. Please note the Private Endpoint ID and approve the corresponding connection request in the cloud provider console.
> ```
>
> Provision a private endpoint to allow Snowflake on Google Cloud to connect to the regional Cloud Key Management Service (Cloud KMS) endpoint:
>
> Copy code
>
> ```
> SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
>   'cloudkms.us-east4.rep.googleapis.com',
>   'cloudkms.us-east4.rep.googleapis.com'
>   );
> ```
>
> ```
> Private endpoint with ID "abcd0000000000000001" to resource "cloudkms.us-east4.rep.googleapis.com" was provisioned successfully.
> Please note the Private Endpoint ID and approve the corresponding connection request in the cloud provider console.
> ```
>
> Provision a private endpoint to allow Snowflake to connect to an external stage for Google Cloud:
>
> Copy code
>
> ```
> SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
>   'storage.us-east4.rep.googleapis.com',
>   'storage.us-east4.rep.googleapis.com'
> );
> ```
>
> ```
> Private endpoint with ID "abcd0000000000000001" to resource "storage.us-east4.rep.googleapis.com" was provisioned successfully.
> Please note the Private Endpoint ID and approve the corresponding connection request in the cloud provider console.
> ```
