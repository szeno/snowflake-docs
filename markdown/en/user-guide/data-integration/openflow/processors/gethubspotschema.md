# GetHubSpotSchema 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-hubspot-processors-nar

## Description

Retrieves schema information for HubSpot object types including field names, types, and labels. Outputs detailed field metadata as JSON for schema discovery and mapping purposes.

## Tags

Preview, crm, hubspot, metadata, schema

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| HubSpot Service | HubSpot Client Service. |
| Object Type | HubSpot object type |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | HubSpot fail relationship |
| retry | HubSpot retry relationship. FlowFiles that failed to process due to a server timeout or rate limit related error. FlowFiles routed here should be routed back into the processor. |
| success | HubSpot success relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| hubspot.object.type | The HubSpot object type |
| hubspot.field.count | Number of fields retrieved |
| mime.type | MIME type of the output (application/json) |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.hubspot.GetHubSpotObject](/user-guide/data-integration/openflow/processors/gethubspotobject)
- [com.snowflake.openflow.runtime.processors.hubspot.ListArchivedHubSpotData](/user-guide/data-integration/openflow/processors/listarchivedhubspotdata)
- [com.snowflake.openflow.runtime.processors.hubspot.ListHubSpotObjects](/user-guide/data-integration/openflow/processors/listhubspotobjects)
- [com.snowflake.openflow.runtime.processors.hubspot.PutHubSpot](/user-guide/data-integration/openflow/processors/puthubspot)
