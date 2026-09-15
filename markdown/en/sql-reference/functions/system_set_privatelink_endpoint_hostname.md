Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$SET\_PRIVATELINK\_ENDPOINT\_HOSTNAME

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Modifies only the host name of an existing [private connectivity endpoint](/user-guide/private-connectivity-outbound).

Note

If the Snowflake account is in an Azure government region, the provider resource ID must be the ID of a resource in a government
subscription. For more information about government regions for Snowflake customers, see [U.S. SnowGov Regions](/user-guide/intro-regions#label-intro-regions-snowgov-regions).

## Syntax

**AWS:**

Copy code

```
SYSTEM$SET_PRIVATELINK_ENDPOINT_HOSTNAME( '<provider_service_name>' , '<host_name>' )
```

**Azure:**

Copy code

```
SYSTEM$SET_PRIVATELINK_ENDPOINT_HOSTNAME( '<provider_resource_id>' , '<host_name>' [ , '<subresource>' ] )
```

**Google Cloud:**

Copy code

```
SYSTEM$SET_PRIVATELINK_ENDPOINT_HOSTNAME( '<target_service_id>' , '<host_name>' )
```

## Arguments

**AWS:**

`'provider_service_name'`
:   Specifies the external service or resource to connect to. For example, `com.amazonaws.us-west-2.execute-api` for the Amazon API
    Gateway or `com.amazonaws.us-west-2.s3` for Amazon S3.

    For information about retrieving this value from AWS, see [Provision private connectivity endpoints](/user-guide/private-manage-endpoints-aws#label-private-link-external-access-aws-create-endpoints).

`'host_name'`
:   Specifies the new fully qualified host name that should be used to access the resource in your VPC or VNet.

    This value doesn’t contain any port numbers and must match what you specified in the Snowflake object that you use to connect to the
    external service.

    Examples include `bedrock-runtime.us-west-2.amazonaws.com` and `*.s3.us-west-2.amazonaws.com`.

    When you use private connectivity for external stages and external volumes, the `host_name` must use a wildcard instead of
    specifying an AWS S3 bucket.

    For information about retrieving this value from AWS, see [Provision private connectivity endpoints](/user-guide/private-manage-endpoints-aws#label-private-link-external-access-aws-create-endpoints).

**Azure:**

`'provider_resource_id'`
:   Specifies the fully qualified identifier for the resource in your VPC or VNet.

`'host_name'`
:   Specifies the new fully qualified host name to access the resource in your VPC or VNet.

    For examples of the host name for outbound private connectivity for external functions, see the following topics:

    - [Azure Portal](/sql-reference/external-functions-creating-azure-ui-private-connect)
    - [Azure ARM template](/sql-reference/external-functions-creating-azure-template-private-connect)

`'subresource'`
:   Specifies the name of the subresource of the Azure resource.

    This argument isn’t required for [Azure Private Link Service](https://learn.microsoft.com/en-us/azure/private-link/private-link-service-overview) and Azure API Management Service.

    For all supported values, see the [Sub-resource table](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview#private-link-resource).

**Google Cloud:**

`'target_service_id'`
:   Specifies the service attachment ID (to a custom service), or regional Google API endpoint to connect to.

`'host_name'`
:   Specifies the new fully qualified host name to access the resource.

## Returns

Returns a status message that the host name for the private connectivity endpoint was updated successfully.

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Usage notes

- You can only modify the host name of an existing private connectivity endpoint.
- On Microsoft Azure, this function rejects a new host name that collides with any additional host name already registered on the same
  endpoint using [SYSTEM$ADD\_PRIVATELINK\_ENDPOINT\_HOSTNAME](/sql-reference/functions/system_add_privatelink_endpoint_hostname).

## Examples

**AWS:**

> Update the hostname of a private endpoint to allow Snowflake on Amazon Web Services to connect to the VPCE service in your Amazon Web Services VPC:
>
> Copy code
>
> ```
> SELECT SYSTEM$SET_PRIVATELINK_ENDPOINT_HOSTNAME(
>   'com.amazonaws.vpce.us-west-2.vpce-svc-01234567890abcdef',
>   'my-new-service-name.com'
>   );
> ```
>
> ```
> Successfully set the host name of the privatelink endpoint ``com.amazonaws.vpce.us-west-2.vpce-svc-01234567890abcdef`` to ``my-new-service-name.com``
> ```

**Azure:**

> Update the host name of a private endpoint to allow Snowflake on Microsoft Azure to connect to the Microsoft Azure API Management service in your Microsoft Azure VNet:
>
> Copy code
>
> ```
> SELECT SYSTEM$SET_PRIVATELINK_ENDPOINT_HOSTNAME(
>   '/subscriptions/f4b00c5f-f6bf-41d6-806b-e1cac4f1f36f/resourceGroups/aztest1-external-function-rg/providers/Microsoft.ApiManagement/service/aztest1-external-function-api',
>   'my-new-custom-api-endpoint.net',
>   'Gateway'
>   );
> ```
>
> ```
> Successfully set the host name of the privatelink endpoint ``/subscriptions/f4b00c5f-f6bf-41d6-806b-e1cac4f1f36f/resourceGroups/aztest1-external-function-rg/providers/Microsoft.ApiManagement/service/aztest1-external-function-api`` to ``my-new-custom-api-endpoint.net``
> ```

**Google Cloud:**

> Update the host name of a private endpoint to allow Snowflake on Google Cloud Platform to connect to the service attachment in your Google Cloud Platform VPC network:
>
> Copy code
>
> ```
> SELECT SYSTEM$SET_PRIVATELINK_ENDPOINT_HOSTNAME(
>   'projects/my-project/regions/us-west2/serviceAttachments/my-http-server',
>   'my-new-custom-api-endpoint.com'
>   );
> ```
>
> ```
> Successfully set the host name of the privatelink endpoint ``projects/my-project/regions/us-west2/serviceAttachments/my-http-server`` to ``my-new-custom-api-endpoint.com``
> ```
