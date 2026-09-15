# PutSplunkHTTP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-splunk-nar

## Description

Sends flow file content to the specified Splunk server over HTTP or HTTPS. Supports HEC Index Acknowledgement.

## Tags

http, logs, splunk

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Hostname | The ip address or hostname of the Splunk server. |
| Owner | The owner to pass to Splunk. |
| Password | The password to authenticate to Splunk. |
| Port | The HTTP Event Collector HTTP Port Number. |
| Scheme | The scheme for connecting to Splunk. |
| Security Protocol | The security protocol to use for communicating with Splunk. |
| Token | HTTP Event Collector token starting with the string Splunk. For example ‘Splunk 1234578-abcd-1234-abcd-1234abcd’ |
| Username | The username to authenticate to Splunk. |
| character-set | The name of the character set. |
| content-type | The media type of the event sent to Splunk. If not set, “mime.type” flow file attribute will be used. In case of neither of them is specified, this information will not be sent to the server. |
| host | Specify with the host query string parameter. Sets a default for all events when unspecified. |
| index | Index name. Specify with the index query string parameter. Sets a default for all events when unspecified. |
| request-channel | Identifier of the used request channel. |
| source | User-defined event source. Sets a default for all events when unspecified. |
| source-type | User-defined event sourcetype. Sets a default for all events when unspecified. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that failed to send to the destination are sent to this relationship. |
| success | FlowFiles that are sent successfully to the destination are sent to this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| splunk.acknowledgement.id | The indexing acknowledgement id provided by Splunk. |
| splunk.responded.at | The time of the response of put request for Splunk. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.splunk.QuerySplunkIndexingStatus](/user-guide/data-integration/openflow/processors/querysplunkindexingstatus)
