Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$GET\_PRIVATELINK\_ENDPOINT\_REGISTRATIONS

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the registered private endpoints that can route your connection to the Snowflake service.

## Syntax

Copy code

```
SYSTEM$GET_PRIVATELINK_ENDPOINT_REGISTRATIONS()
```

## Arguments

None.

## Returns

Returns a list of JSON objects, with each JSON object specifying a registered private connectivity endpoint. A string containing an
empty JSON array (`"[]"`) is returned if the account doesn’t have any registered private connectivity endpoints to the Snowflake Service.

Where:

> `consumerEndpointId`
> :   Specifies the AWS account id containing the registered VPC endpoint, or the Azure resource group identifier
>     containing the registered private endpoint.
>
> `consumerEndpointType`
> :   Specifies the type of registered private connectivity endpoint.
>
> `pinnedConsumerEndpointId`
> :   Specifies the private connectivity endpoint identifier that is registered with Snowflake.
>
> `providerServiceEndpoint`
> :   Specifies the identifier for the private connectivity service endpoint in the Snowflake VPC.

## Usage notes

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Examples

Return the registered private connectivity endpoints that route your connection to the Snowflake service:

**AWS:**

Copy code

```
 use role accountadmin;

SELECT SYSTEM$GET_PRIVATELINK_ENDPOINT_REGISTRATIONS();
```

Copy code

```
[
  {
    "consumerEndpointId": "148896251...",
    "consumerEndpointType": "Aws Id",
    "pinnedConsumerEndpointId": "vpce-0be92fc5953c0...",
    "providerServiceEndpoint": "vpce-svc-0dcda6d2e9d14..."
  }
]
```

**Azure:**

Copy code

```
 use role accountadmin;

SELECT SYSTEM$GET_PRIVATELINK_ENDPOINT_REGISTRATIONS();
```

Copy code

```
[
  {
    "consumerEndpointId": "/subscriptions/a92a429f-83ba-4249.../..../snowflake-private-link",
    "consumerEndpointType": "Azure Endpoint Connection Id",
    "pinnedConsumerEndpointId": "184549...",
    "providerServiceEndpoint": "sf-pvlinksvc-azcanadacentral.70f..."
  }
]
```
