# GetHubSpotObject 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-hubspot-processors-nar

## Description

Get a HubSpot object and its associations by ID or unique value.

## Tags

Preview, hubspot

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| HubSpot Service | HubSpot Client Service. |
| Object ID Property | HubSpot property used to uniquely identify the object. |
| Object ID Value | Matching HubSpot property value to search for. |
| Object Type | HubSpot object type |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | HubSpot fail relationship |
| missing | HubSpot object does not exist. |
| retry | HubSpot retry relationship. FlowFiles that failed to process due to a server timeout or rate limit related error. FlowFiles routed here should be routed back into the processor. |
| success | HubSpot success relationship |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.hubspot.GetHubSpotSchema](/user-guide/data-integration/openflow/processors/gethubspotschema)
- [com.snowflake.openflow.runtime.processors.hubspot.ListArchivedHubSpotData](/user-guide/data-integration/openflow/processors/listarchivedhubspotdata)
- [com.snowflake.openflow.runtime.processors.hubspot.ListHubSpotObjects](/user-guide/data-integration/openflow/processors/listhubspotobjects)
- [com.snowflake.openflow.runtime.processors.hubspot.PutHubSpot](/user-guide/data-integration/openflow/processors/puthubspot)
