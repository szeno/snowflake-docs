# UpsertSFDCObjects 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-salesforce-processors-nar

## Description

Upserts the records from the incoming FlowFile into Salesforce

## Tags

insert, objects, preview, salesforce, sfdc, update, upsert

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Object Name | The name of the object type for the records included in the FlowFile. |
| Record Reader | Specifies the Controller Service to use for reading incoming data. Each record will be converted into a JSON object and upserted into Salesforce using a dedicated API call. |
| Salesforce Client | Salesforce Client to interact with the APIs |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| comms.failure | The FlowFile is routed to this relationship if any record could not be upserted in Salesforce but the operation might be retried |
| failure | The FlowFile is routed to this relationship if any record could not be upserted in Salesforce |
| success | The FlowFile is routed to this relationship after all records have been successfully upserted |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| sObjectId | ID of the created object in Salesforce when using this processor with a single record. |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.salesforce.DeleteQueryJob](/user-guide/data-integration/openflow/processors/deletequeryjob)
- [com.snowflake.openflow.runtime.processors.salesforce.DescribeSFDCObject](/user-guide/data-integration/openflow/processors/describesfdcobject)
- [com.snowflake.openflow.runtime.processors.salesforce.GetQueryJobResult](/user-guide/data-integration/openflow/processors/getqueryjobresult)
- [com.snowflake.openflow.runtime.processors.salesforce.SubmitQueryJob](/user-guide/data-integration/openflow/processors/submitqueryjob)
