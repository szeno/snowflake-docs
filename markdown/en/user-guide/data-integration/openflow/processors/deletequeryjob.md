# DeleteQueryJob 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-salesforce-processors-nar

## Description

Deletes a Query Job in Salesforce using the Bulk API 2.0.

## Tags

bulk, delete, job, preview, query, salesforce

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Job ID | The ID of the job for which the status is checked. |
| Salesforce Client | Salesforce Client to interact with the APIs |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| comms.failure | A FlowFile is routed to this relationship if the Query Job status could not be retrieved but the operation might be retried |
| failure | A FlowFile is routed to this relationship if the Query Job status could not be retrieved |
| success | If the Query Job has been successfully deleted, the FlowFile is routed to this relationship |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.salesforce.AbortQueryJob](/user-guide/data-integration/openflow/processors/abortqueryjob)
- [com.snowflake.openflow.runtime.processors.salesforce.GetQueryJobResult](/user-guide/data-integration/openflow/processors/getqueryjobresult)
- [com.snowflake.openflow.runtime.processors.salesforce.GetQueryJobStatus](/user-guide/data-integration/openflow/processors/getqueryjobstatus)
- [com.snowflake.openflow.runtime.processors.salesforce.SubmitQueryJob](/user-guide/data-integration/openflow/processors/submitqueryjob)
