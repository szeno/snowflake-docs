# PutHubSpot 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-hubspot-processors-nar

## Description

Upsert a HubSpot object.

## Tags

Preview, hubspot

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Associated Object ID Property | Target HubSpot property used to uniquely identify the object to associate to from the configured object. |
| Associated Object ID Value | Target HubSpot property value for the ‘Associated Object ID Property’ to associate to from the configured object. |
| Associated Object Type | Target HubSpot object type to associate to from the configured object. |
| Association Type ID | The HubSpot defined association id from the ‘Object ID Value’ to the ‘Associated Object ID Value’. |
| HubSpot Service | HubSpot Client Service. |
| Inverse Association Type ID | The HubSpot defined association id from the ‘Associated Object ID Value’ to the ‘Object ID Value’. |
| Missing HubSpot Property Policy | What to action to take if HubSpot does not have a matching property. |
| Object ID Property | HubSpot property used to uniquely identify the object. |
| Object ID Value | Matching HubSpot property value to search for. |
| Object Override Properties | Comma-delimited list of NiFi attributes, which if exist, will be added as object properties. Any existing properties in HubSpot will be overridden. |
| Object Set Properties | Comma-delimited list of NiFi attributes, which if exist, will be added as object properties if the current object property in HubSpot is empty. |
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

## See also

- [com.snowflake.openflow.runtime.processors.hubspot.GetHubSpotObject](/user-guide/data-integration/openflow/processors/gethubspotobject)
- [com.snowflake.openflow.runtime.processors.hubspot.GetHubSpotSchema](/user-guide/data-integration/openflow/processors/gethubspotschema)
- [com.snowflake.openflow.runtime.processors.hubspot.ListArchivedHubSpotData](/user-guide/data-integration/openflow/processors/listarchivedhubspotdata)
- [com.snowflake.openflow.runtime.processors.hubspot.ListHubSpotObjects](/user-guide/data-integration/openflow/processors/listhubspotobjects)
