# SubmitQueryJob 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-salesforce-processors-nar

## Description

Submits a Query Job to Salesforce using the Bulk API 2.0. In SIMPLE mode, per-object state (previousLast/currentLast and status) is stored in the configured controller service. In ADVANCED mode, a single ‘last’ timestamp is stored at processor scope to support incremental queries across objects.

## Tags

bulk, job, preview, query, salesforce

## Input Requirement

ALLOWED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Column Delimiter | The column delimiter used for CSV job data. |
| Configuration Mode | The configuration mode for configuring this processor. If using advanced mode, the SOQL query has to be provided and the processor ‘s state will only store the timestamp of the last query job submission regardless of the object queried. If using simple mode, the object name and the fields to be queried have to be provided and the processor’s state will store the timestamp of the last query job submission for each object queried. |
| Incremental Offload | Whether the processor should perform incremental offload. If true, the processor will only fetch the records that have been modified since the last query job submission by using a WHERE clause on the SystemModstamp field. |
| Line Ending | The line ending used for CSV job data, marking the end of a data row. |
| Object Fields | Comma separated list of the name of the fields to be queried for the specified object. |
| Object Name | The name of the object to be queried. |
| Operation | The type of query to submit. |
| Query | The query to be performed. In order to perform incremental retrieval (ie. only the added/modified/deleted elements since the last submission of the query are retrieved), this processor exposes two attributes: ${nowTs} and ${lastJobTimestamp}. It is possible to use those placeholders like SELECT Id FROM Account WHERE SystemModstamp > ${lastJobTimestamp} AND SystemModstamp <= ${nowTs}. |
| Result Format | The format to be used for the results. Currently the only supported value is CSV. |
| Salesforce Bulk Job State Service | Controller Service to store Bulk Jobs state per object type (used in SIMPLE mode). In ADVANCED mode, the processor stores a single ‘last’ timestamp in processor state. |
| Salesforce Client | Salesforce Client to interact with the APIs |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | In case the placeholders for incremental retrieval are used in the query field, the timestamp of the last Query Job submission time minus 30 seconds will be stored in the state. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| comms.failure | An incoming FlowFile is routed to this relationship if the Query Job could not be submitted but the operation might be retried |
| failure | An incoming FlowFile is routed to this relationship if the Query Job could not be submitted |
| in.progress | An incoming FlowFile is routed to this relationship when a previous job for the same object is still IN\_PROGRESS |
| success | When a Query Job is successfully submitted, a FlowFile is routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| jobId | The unique ID for this job. |
| operationType | The type of query. |
| objectType | The object type being queried. |
| createdById | The ID of the user who created the job. |
| createdDate | The UTC date and time when the job was created. |
| systemModstamp | The UTC date and time when the API last updated the job information. |
| jobState | The current state of processing for the job. |
| concurrencyMode | How the request is processed. |
| contentType | The format to be used for the results. |
| apiVersion | The API version that the job was created in. |
| lineEnding | The line ending used for CSV job data, marking the end of a data row. |
| columnDelimiter | The column delimiter used for CSV job data. |
| nowTs | Upper limit of the time range used in the WHERE close to construct the Query Job. |
| lastJobTimestamp | Lower limit of the time range used in the WHERE close to construct the Query Job. |

Expand

Show lessSee more

## Use cases

| Submits a Query Job to Salesforce using the Bulk API 2.0. |
| --- |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.salesforce.AbortQueryJob](/user-guide/data-integration/openflow/processors/abortqueryjob)
- [com.snowflake.openflow.runtime.processors.salesforce.DeleteQueryJob](/user-guide/data-integration/openflow/processors/deletequeryjob)
- [com.snowflake.openflow.runtime.processors.salesforce.GetQueryJobResult](/user-guide/data-integration/openflow/processors/getqueryjobresult)
- [com.snowflake.openflow.runtime.processors.salesforce.GetQueryJobStatus](/user-guide/data-integration/openflow/processors/getqueryjobstatus)
