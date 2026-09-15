# QuerySplunkIndexingStatus 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-splunk-nar

## Description

Queries Splunk server in order to acquire the status of indexing acknowledgement.

## Tags

acknowledgement, http, logs, splunk

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
| max-query-size | The maximum number of acknowledgement identifiers the outgoing query contains in one batch. It is recommended not to set it too low in order to reduce network communication. |
| request-channel | Identifier of the used request channel. |
| ttl | The maximum time the processor tries to acquire acknowledgement confirmation for an index, from the point of registration. After the given amount of time, the processor considers the index as not acknowledged and transfers the FlowFile to the “unacknowledged” relationship. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | A FlowFile is transferred to this relationship when the acknowledgement was not successful due to errors during the communication. FlowFiles are timing out or unknown by the Splunk server will transferred to “undetermined” relationship. |
| success | A FlowFile is transferred to this relationship when the acknowledgement was successful. |
| unacknowledged | A FlowFile is transferred to this relationship when the acknowledgement was not successful. This can happen when the acknowledgement did not happened within the time period set for Maximum Waiting Time. FlowFiles with acknowledgement id unknown for the Splunk server will be transferred to this relationship after the Maximum Waiting Time is reached. |
| undetermined | A FlowFile is transferred to this relationship when the acknowledgement state is not determined. FlowFiles transferred to this relationship might be penalized. This happens when Splunk returns with HTTP 200 but with false response for the acknowledgement id in the flow file attribute. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.splunk.PutSplunkHTTP](/user-guide/data-integration/openflow/processors/putsplunkhttp)
