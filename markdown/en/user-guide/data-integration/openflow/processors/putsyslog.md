# PutSyslog 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Sends Syslog messages to a given host and port over TCP or UDP. Messages are constructed from the “Message \_\_\_” properties of the processor which can use expression language to generate messages from incoming FlowFiles. The properties are used to construct messages of the form: (<PRIORITY>)(VERSION )(TIMESTAMP) (HOSTNAME) (BODY) where version is optional. The constructed messages are checked against regular expressions for RFC5424 and RFC3164 formatted messages. The timestamp can be an RFC5424 timestamp with a format of “yyyy-MM-dd ‘T’HH:mm:ss. S ‘Z’” or “yyyy-MM-dd ‘T’HH:mm:ss. S+hh:mm”, or it can be an RFC3164 timestamp with a format of “MMM d HH:mm:ss”. If a message is constructed that does not form a valid Syslog message according to the above description, then it is routed to the invalid relationship. Valid messages are sent to the Syslog server and successes are routed to the success relationship, failures routed to the failure relationship.

## Tags

logs, put, syslog, tcp, udp

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Batch Size | The number of incoming FlowFiles to process in a single execution of this processor. |
| Character Set | Specifies the character set of the Syslog messages. Note that Expression language is not evaluated per FlowFile. |
| Hostname | The IP address or hostname of the Syslog server. |
| Idle Connection Expiration | The amount of time a connection should be held open without being used before closing the connection. |
| Max Size of Socket Send Buffer | The maximum size of the socket send buffer that should be used. This is a suggestion to the Operating System to indicate how big the socket buffer should be. If this value is set too low, the buffer may fill up before the data can be read, and incoming data will be dropped. |
| Message Body | The body for the Syslog messages. |
| Message Hostname | The hostname for the Syslog messages. |
| Message Priority | The priority for the Syslog messages, excluding < >. |
| Message Timestamp | The timestamp for the Syslog messages. The timestamp can be an RFC5424 timestamp with a format of “yyyy-MM-dd ‘T’HH:mm:ss. S ‘Z’” or “yyyy-MM-dd ‘T’HH:mm:ss. S+hh:mm”, “ or it can be an RFC3164 timestamp with a format of “MMM d HH:mm:ss”. |
| Message Version | The version for the Syslog messages. |
| Port | The port for Syslog communication. Note that Expression language is not evaluated per FlowFile. |
| Protocol | The protocol for Syslog communication. |
| SSL Context Service | The Controller Service to use in order to obtain an SSL Context. If this property is set, syslog messages will be sent over a secure connection. |
| Timeout | The timeout for connecting to and communicating with the syslog server. Does not apply to UDP. Note that Expression language is not evaluated per FlowFile. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that failed to send to Syslog are sent out this relationship. |
| invalid | FlowFiles that do not form a valid Syslog message are sent out this relationship. |
| success | FlowFiles that are sent successfully to Syslog are sent out this relationship. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.ListenSyslog](/user-guide/data-integration/openflow/processors/listensyslog)
- [org.apache.nifi.processors.standard.ParseSyslog](/user-guide/data-integration/openflow/processors/parsesyslog)
