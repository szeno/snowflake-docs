# GetShopify 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-shopify-nar

## Description

Retrieves objects from a custom Shopify store. The processor yield time must be set to the account’s rate limit accordingly.

## Tags

shopify

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| CUSTOMERS | Customer resource to query |
| DISCOUNTS | Discount resource to query |
| INVENTORY | Inventory resource to query |
| ONLINE\_STORE | Online Store resource to query |
| ORDERS | Order resource to query |
| PRODUCT | Product resource to query |
| SALES\_CHANNELS | Sales Channel resource to query |
| STORE\_PROPERTIES | Store Property resource to query |
| access-token | Access Token to authenticate requests |
| api-version | The Shopify REST API version |
| incremental-delay | The ending timestamp of the time window will be adjusted earlier by the amount configured in this property. For example, with a property value of 10 seconds, an ending timestamp of 12:30:45 would be changed to 12:30:35. Set this property to avoid missing objects when the clock of your local machines and Shopify servers’ clock are not in sync. |
| incremental-initial-start-time | This property specifies the start time when running the first request. Represents an ISO 8601-encoded date and time string. For example, 3:50 pm on September 7, 2019 in the time zone of UTC (Coordinated Universal Time) is represented as “2019-09-07T15:50:00Z”. |
| is-incremental | The processor can incrementally load the queried objects so that each object is queried exactly once. For each query, the processor queries objects which were created or modified after the previous run time but before the current time. |
| object-category | Shopify object category |
| result-limit | The maximum number of results to request for each invocation of the Processor |
| store-domain | The domain of the Shopify store, e.g. nifistore.myshopify.com |
| web-client-service-provider | Controller service for HTTP client operations |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | For a few resources the processor supports incremental loading. The list of the resources with the supported parameters can be found in the additional details. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | For FlowFiles created as a result of a successful query. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | Sets the MIME type to application/json |

Expand

Show lessSee more
