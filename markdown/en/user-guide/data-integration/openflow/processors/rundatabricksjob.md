# RunDatabricksJob 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-databricks-processors-nar

## Description

Triggers a pre-defined Databricks job to run with custom parameters. Job parameters can be set using dynamic properties

## Tags

databricks, jobs, openflow

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Databricks Client | Databricks Client Service. |
| Job ID | Databricks Job ID |
| Job Name | Databricks Job Name |
| Wait for Job Completion | Wait for the Databricks job to complete before transferring the FlowFile to success |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Databricks failure relationship |
| success | Databricks success relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| job.run.id | The run id assigned to the invoked job |
| job.result.state | The result state for the invoked job |
| error.code | The error code for the SQL statement if an error occurred. |
| error.message | The error message for the SQL statement if an error occurred. |

Expand

Show lessSee more
