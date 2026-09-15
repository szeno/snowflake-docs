# HandleHttpResponse 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Sends an HTTP Response to the Requestor that generated a FlowFile. This Processor is designed to be used in conjunction with the HandleHttpRequest in order to create a web service.

## Tags

egress, http, https, response, web service

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Attributes to add to the HTTP Response (Regex) | Specifies the Regular Expression that determines the names of FlowFile attributes that should be added to the HTTP response |
| HTTP Context Map | The HTTP Context Map Controller Service to use for caching the HTTP Request Information |
| HTTP Status Code | The HTTP Status Code to use when responding to the HTTP Request. See Section 10 of RFC 2616 for more information. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles will be routed to this Relationship if the Processor is unable to respond to the requestor. This may happen, for instance, if the connection times out or if NiFi is restarted before responding to the HTTP Request. |
| success | FlowFiles will be routed to this Relationship after the response has been successfully sent to the requestor |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.HandleHttpRequest](/user-guide/data-integration/openflow/processors/handlehttprequest)
