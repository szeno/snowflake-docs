# PutSalesforceObject 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-salesforce-nar

## Description

Creates new records for the specified Salesforce sObject. The type of the Salesforce object must be set in the input flowfile ‘s’ objectType’ attribute. This processor cannot update existing records.

## Tags

put, salesforce, sobject

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| oauth2-access-token-provider | Service providing OAuth2 Access Tokens for authenticating using the HTTP Authorization Header |
| read-timeout | Maximum time allowed for reading a response from the Salesforce REST API |
| record-reader | Specifies the Controller Service to use for parsing incoming data and determining the data’s schema |
| salesforce-api-version | The version number of the Salesforce REST API appended to the URL after the services/data path. See Salesforce documentation for supported versions |
| salesforce-url | The URL of the Salesforce instance including the domain without additional path information, such as <https://MyDomainName.my.salesforce.com> |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | For FlowFiles created as a result of an execution error. |
| success | For FlowFiles created as a result of a successful execution. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| error.message | The error message returned by Salesforce. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.salesforce.QuerySalesforceObject](/user-guide/data-integration/openflow/processors/querysalesforceobject)
