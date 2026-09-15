# GetHubSpot 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-hubspot-nar

## Description

Retrieves JSON data from a private HubSpot application. This processor is intended to be run on the Primary Node only.

## Tags

hubspot

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| access-token | Access Token to authenticate requests |
| incremental-delay | The ending timestamp of the time window will be adjusted earlier by the amount configured in this property. For example, with a property value of 10 seconds, an ending timestamp of 12:30:45 would be changed to 12:30:35. Set this property to avoid missing objects when the clock of your local machines and HubSpot servers ‘clock are not in sync and to protect against HubSpot’s mechanism that changes last updated timestamps after object creation. |
| incremental-initial-start-time | This property specifies the start time that the processor applies when running the first request. The expected format is a UTC date-time such as ’2011-12-03T10:15:30Z’ |
| is-incremental | The processor can incrementally load the queried objects so that each object is queried exactly once. For each query, the processor queries objects within a time window where the objects were modified between the previous run time and the current time (optionally adjusted by the Incremental Delay property). |
| object-type | The HubSpot Object Type requested |
| result-limit | The maximum number of results to request for each invocation of the Processor |
| web-client-service-provider | Controller service for HTTP client operations |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | In case of incremental loading, the start and end timestamps of the last query time window are stored in the state. When the ‘Result Limit’ property is set, the paging cursor is saved after executing a request. Only the objects after the paging cursor will be retrieved. The maximum number of retrieved objects can be set in the ‘Result Limit’ property. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | For FlowFiles created as a result of a successful HTTP request. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | Sets the MIME type to application/json |

Expand

Show lessSee more
