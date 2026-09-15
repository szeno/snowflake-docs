# DescribeDataShare 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-salesforce-processors-nar

## Description

Describe the specified data share metadata in Salesforce Data Cloud.

## Tags

daas, data cloud, describe, object, preview, salesforce, sfdc

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Data Share Name | The name of the Data Share to describe. |
| Salesforce Data Cloud Client | Salesforce Data Cloud Client to interact with the APIs |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| comms.failure | A FlowFile is routed to this relationship if the data share metadata could not be retrieved but the operation might be retried |
| failure | A FlowFile is routed to this relationship if the data share metadata could not be retrieved |
| success | FlowFile containing the data share metadata will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| explicitDataLakeObjects | Comma-separated list of the names of the explicit data lake objects. |
| implicitDataLakeObjects | Comma-separated list of the names of the implicit data lake objects. |
| dataModelObjects | Comma-separated list of the names of the data model objects. |
| calculatedInsightObjects | Comma-separated list of the names of the calculated insights objects. |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.salesforce.ListSFDCDataShares](/user-guide/data-integration/openflow/processors/listsfdcdatashares)
