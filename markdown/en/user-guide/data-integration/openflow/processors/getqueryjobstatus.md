# GetQueryJobStatus 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-salesforce-processors-nar

## Description

Gets the status of a Query Job in Salesforce using the Bulk API 2.0.

## Tags

bulk, job, preview, query, salesforce, status

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
| job.aborted | If the Query Job has been aborted, the FlowFile is routed to this relationship |
| job.completed | If the Query Job completed, the FlowFile is routed to this relationship |
| job.failed | If the Query Job failed, the FlowFile is routed to this relationship |
| wait | If the Query Job is in the processing queue or in progress, the FlowFile is routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| jobState | The current state of processing for the job. |
| systemModstamp | The UTC date and time when the API last updated the job information. |
| numberRecordsProcessed | The number of records processed in this job. |
| retries | The number of times that Salesforce attempted to save the results of an operation. Repeated attempts indicate a problem such as a lock contention. |
| totalProcessingTime | The number of milliseconds taken to process the job. |
| isPkChunkingSupported | Whether PK chunking is supported for the queried object (true), or isn’t supported (false). |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.salesforce.AbortQueryJob](/user-guide/data-integration/openflow/processors/abortqueryjob)
- [com.snowflake.openflow.runtime.processors.salesforce.DeleteQueryJob](/user-guide/data-integration/openflow/processors/deletequeryjob)
- [com.snowflake.openflow.runtime.processors.salesforce.GetQueryJobResult](/user-guide/data-integration/openflow/processors/getqueryjobresult)
- [com.snowflake.openflow.runtime.processors.salesforce.SubmitQueryJob](/user-guide/data-integration/openflow/processors/submitqueryjob)
