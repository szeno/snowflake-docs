# PutZendeskTicket 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-zendesk-nar

## Description

Create Zendesk tickets using the Zendesk API.

## Tags

zendesk, ticket

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| web-client-service-provider | Controller service for HTTP client operations. |
| zendesk-authentication-type-name | Type of authentication to Zendesk API. |
| zendesk-authentication-value-name | Password or authentication token for Zendesk login user. |
| zendesk-comment-body | The content or the path to the comment body in the incoming record. |
| zendesk-priority | The content or the path to the priority in the incoming record. |
| zendesk-record-reader | Specifies the Controller Service to use for parsing incoming data and determining the data’s schema. |
| zendesk-subdomain | Name of the Zendesk subdomain. |
| zendesk-subject | The content or the path to the subject in the incoming record. |
| zendesk-type | The content or the path to the type in the incoming record. |
| zendesk-user | Login user to Zendesk subdomain. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | A FlowFile is routed to this relationship if the operation failed and retrying the operation will also fail, such as an invalid data or schema. |
| success | For FlowFiles created as a result of a successful HTTP request. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| record.count | The number of records processed. |
| error.code | The error code of from the response. |
| error.message | The error message of from the response. |

Expand

Show lessSee more
