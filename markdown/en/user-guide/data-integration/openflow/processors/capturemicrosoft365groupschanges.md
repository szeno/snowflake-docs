# CaptureMicrosoft365GroupsChanges 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-msgraph-nar

## Description

Captures Microsoft365 groups changes and emits a FlowFile for each change that occurs. This includes membership changes.

## Tags

cdc, document, graph, library, microsoft, sharepoint, unstructured

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Authentication Service | The service that provides authentication for the SharePoint API |
| Fallback Retry Duration | The time to wait before retrying the operation after a communication failure. This value is used when the response doesn’t contain a Retry-After header. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | Stores a delta token for Microsoft365 groups |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| deleted | A FlowFile is routed to this relationship for each Microsoft365 group that has been deleted. |
| updated | A FlowFile is routed to this relationship for each Microsoft365 group whose membership has changed. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| microsoft365.group.id | An id of a changed group |
| microsoft365.group.email | An email of the changed group |

Expand

Show lessSee more
