Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the status of all private connectivity endpoints that you provision. The endpoint can be a service endpoint or a resource endpoint
depending on the cloud platform that hosts your Snowflake account.

## Syntax

Copy code

```
SYSTEM$GET_PRIVATELINK_ENDPOINTS_INFO()
```

## Returns

Returns a JSON object with the following fields:

**AWS:**

> `provider_service_name`
> :   Name of the service or resource.
>
> `snowflake_endpoint_name`
> :   The VPC endpoint ID in your Snowflake account. This field contains a temporary name while the endpoint is
>     being created. After the endpoint is created, and `endpoint_state` changes to `CREATED`, then this name changes.
>
> `endpoint_state`
> :   The endpoint state in Snowflake. This field can contain one of the following states:
>
>     - `PENDING_CREATION`: The endpoint is still being created.
>     - `CREATED`: Indicates that Snowflake received a response from the cloud provider that the endpoint was successfully created and
>       is ready to use.
>     - `FAILED`: The endpoint is in an unexpected state on the cloud provider, and cannot be used.
>     - `PENDING_DELETION`: The endpoint is on the deletion queue, but can be restored.
>     - `DELETING`: The endpoint is being deleted on the cloud provider and cannot be restored.
>
> `host`
> :   Hostname used to connect to the service.
>
> `status`
> :   The endpoint provisioning status on AWS. This field can contain one of the following statuses:
>
>     - `Pending`: The endpoint is still being created.
>     - `Available`: The endpoint is created and ready to use.

**Azure:**

> `provider_resource_id`
> :   Azure Resource ID of the resource that the endpoint connects to.
>
> `subresource`
> :   Subresource of the Azure resource that the endpoint connects to.
>
> `snowflake_resource_id`
> :   Azure Resource ID of the private endpoint that connects to the Azure resource.
>
> `host`
> :   Hostname used to connect to the resource.
>
> `endpoint_state`
> :   The endpoint state in Snowflake. This field can contain one of the following states:
>
>     - `PENDING_CREATION`: The endpoint is still being created.
>     - `CREATED`: Indicates that Snowflake received a response from the cloud provider that the endpoint was successfully created and
>       is ready to use.
>     - `FAILED`: The endpoint is in an unexpected state on the cloud provider, and cannot be used.
>     - `PENDING_DELETION`: The endpoint is on the deletion queue, but can be restored.
>     - `DELETING`: The endpoint is being deleted on the cloud provider and cannot be restored.
>
> `status`
> :   The endpoint provisioning status on Microsoft Azure. Use this field to determine if Microsoft Azure has approved the private endpoint connection to the
>     resource. This field can contain one of the following statuses:
>
>     > - `APPROVED`
>     > - `PENDING`
>     > - `DISCONNECTED`
>     > - `REJECTED`
>
> `additional_hostnames`
> :   A list of any additional hostnames bound to the endpoint using [SYSTEM$ADD\_PRIVATELINK\_ENDPOINT\_HOSTNAME](/sql-reference/functions/system_add_privatelink_endpoint_hostname).
>     Empty if no additional hostnames are registered on the endpoint.

**Google Cloud:**

> `provider_resource_id`
> :   The resource ID (service attachment ID) that the private connectivity endpoint connects to.
>
> `snowflake_resource_id`
> :   The identifier of the private connectivity endpoint.
>
> `host`
> :   The hostname to use when accessing the provider service or resource that uses this endpoint.
>
> `endpoint_state`
> :   The state of the endpoint on the Snowflake side.
>
> `status`
> :   The connection status on Google Cloud. NO CONNECTION might appear shortly after creating the private connectivity endpoint, because the
>     cloud provider takes time to complete the connection setup. This field can contain one of the following statuses:
>
>     - `ACCEPTED`
>     - `NO CONNECTION`
>     - `REJECTED`

## Usage notes

- This function can take approximately five minutes to run because it depends on the process to retrieve the private connectivity
  endpoints in the cloud platform that are outside of Snowflake.
- The `additional_hostnames` field is only supported for Snowflake accounts hosted on Microsoft Azure.

## Examples

**AWS:**

> To list all PrivateLink endpoints with external access to Amazon S3, execute the following SQL statement:

SQLReturned value

Copy code

```
SELECT SYSTEM$GET_PRIVATELINK_ENDPOINTS_INFO();
```

Copy code

```
[
  {
    "provider_service_name": "com.amazonaws.us-west-2.s3",
    "snowflake_endpoint_name": "vpce-123456789012abcdea",
    "endpoint_state": "CREATED",
    "host": "*.s3.us-west-2.amazonaws.com",
    "status": "Available"
  },
  ...
```

**Azure:**

> For your Snowflake account on Microsoft Azure, list the private connectivity endpoints that you provisioned and the service names that
> each endpoint is associated with:
>
> SQLReturned value
>
> Copy code
>
> ```
> SELECT SYSTEM$GET_PRIVATELINK_ENDPOINTS_INFO();
> ```
>
> Copy code
>
> ```
> [
>   {
>     "provider_resource_id": "/subscriptions/11111111-2222-3333-4444-5555555555/...",
>     "subresource": "sqlServer",
>     "snowflake_resource_id": "/subscriptions/66666666-7777-8888-9999-000000000000/...",
>     "host": "testdb.database.windows.net",
>     "endpoint_state": "CREATED",
>     "status": "Approved",
>     "additional_hostnames": []
>   }
> ]
> ```

**Google Cloud:**

> For your Snowflake account on Google Cloud, list the private connectivity endpoints that you provisioned and the service names that
> each endpoint is associated with:
>
> > SQLReturned value
> >
> > Copy code
> >
> > ```
> > SELECT SYSTEM$GET_PRIVATELINK_ENDPOINTS_INFO();
> > ```
> >
> > Copy code
> >
> > ```
> > [
> >   {
> >     "provider_resource_id": "projects/my-project/regions/us-east4/serviceAttachments/...",
> >     "snowflake_resource_id": "abcd0000000000000001",
> >     "host": "my-service.com",
> >     "endpoint_state": "CREATED",
> >     "status": "ACCEPTED"
> >   }
> > ]
> > ```
