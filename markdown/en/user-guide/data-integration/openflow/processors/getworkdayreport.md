# GetWorkdayReport 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-workday-processors-nar

## Description

A processor which can interact with a configurable Workday Report. The processor can forward the content without modification, or you can transform it by providing the specific Record Reader and Record Writer services based on your needs. You can also remove fields by defining schema in the Record Writer. Supported Workday report formats are: csv, simplexml, json

## Tags

Workday, report

## Input Requirement

ALLOWED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Access Token Provider | Enables managed retrieval of OAuth2 Bearer Token. |
| Authorization Type | The type of authorization for retrieving data from Workday resources. |
| Web Client Service Provider | Web client which is used to communicate with the Workday API. |
| Workday Password | The password provided for authentication of Workday requests. Encoded using Base64 for HTTP Basic Authentication as described in RFC 7617. |
| Workday Report URL | HTTP remote URL of Workday report including a scheme of http or https, as well as a hostname or IP address with optional port and path elements. |
| Workday Username | The username provided for authentication of Workday requests. Encoded using Base64 for HTTP Basic Authentication as described in RFC 7617. |
| record-reader | Specifies the Controller Service to use for parsing incoming data and determining the data’s schema. |
| record-writer | The Record Writer to use for serializing Records to an output FlowFile. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Request FlowFiles transferred when receiving socket communication errors. |
| original | Request FlowFiles transferred when receiving HTTP responses with a status code between 200 and 299. |
| success | Response FlowFiles transferred when receiving HTTP responses with a status code between 200 and 299. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| getworkdayreport.java.exception.class | The Java exception class raised when the processor fails |
| getworkdayreport.java.exception.message | The Java exception message raised when the processor fails |
| mime.type | Sets the mime.type attribute to the MIME Type specified by the Source / Record Writer |
| record.count | The number of records in an outgoing FlowFile. This is only populated on the ‘success’ relationship when Record Reader and Writer is set. |

Expand

Show lessSee more
