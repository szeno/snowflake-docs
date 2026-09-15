# ListSFDCObjects 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-salesforce-processors-nar

## Description

List the available objects in the organization that are available to the identified user.

## Tags

list, objects, preview, salesforce, sfdc

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Salesforce Client | Salesforce Client to interact with the APIs |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | FlowFile containing the list of available objects will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| nbObjects | The number of objects listed in the organization that are available to the identified user. |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.salesforce.DeleteQueryJob](/user-guide/data-integration/openflow/processors/deletequeryjob)
- [com.snowflake.openflow.runtime.processors.salesforce.DescribeSFDCObject](/user-guide/data-integration/openflow/processors/describesfdcobject)
- [com.snowflake.openflow.runtime.processors.salesforce.GetQueryJobResult](/user-guide/data-integration/openflow/processors/getqueryjobresult)
- [com.snowflake.openflow.runtime.processors.salesforce.SubmitQueryJob](/user-guide/data-integration/openflow/processors/submitqueryjob)
