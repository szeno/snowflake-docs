# ListArchivedHubSpotData 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-hubspot-processors-nar

## Description

Lists archived data from HubSpot for the chosen object type and generates one FlowFile per listed object with the corresponding metadata as FlowFile attributes. The object type must be searchable, which means it supports access to the /search endpoint. For more information about searchable object types, see: <https://developers.hubspot.com/docs/reference/api/crm/objects/objects#search>”)

## Tags

Preview, hubspot

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| HubSpot Service | HubSpot Client Service. |
| Object Type | HubSpot object type |
| Updated After | Filter objects updated after specified date (format: yyyy-MM-dd) |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | Maintains pagination state and last sync timestamp to continue data retrieval from the last known position after restarts and to fetch only changed data. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | HubSpot fail relationship |
| original | The input Flow File is routed to the original relationship. |
| retry | HubSpot retry relationship. FlowFiles that failed to process due to a server timeout or rate limit related error. FlowFiles routed here should be routed back into the processor. |
| success | HubSpot success relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | application/json |
| statement.type | DELETE |
| hubspot.object.type | HubSpot Object Type for this fetch |
| hubspot.object.id | HubSpot Object ID for this fetch |
| hubspot.run.id | Timestamp of the start of this run. Obtained from the incoming FlowFile or current time if not available |
| hubspot.is\_last | Whether this is the last paged object of the ingestion |

Expand

Show lessSee more

## Use cases

| This processor is typically used in conjunction with a GenerateFlowFile processor |
| --- |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.hubspot.GetHubSpotObject](/user-guide/data-integration/openflow/processors/gethubspotobject)
- [com.snowflake.openflow.runtime.processors.hubspot.GetHubSpotSchema](/user-guide/data-integration/openflow/processors/gethubspotschema)
- [com.snowflake.openflow.runtime.processors.hubspot.ListHubSpotObjects](/user-guide/data-integration/openflow/processors/listhubspotobjects)
- [com.snowflake.openflow.runtime.processors.hubspot.PutHubSpot](/user-guide/data-integration/openflow/processors/puthubspot)
