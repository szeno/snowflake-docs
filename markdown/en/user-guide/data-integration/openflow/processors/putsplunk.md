# PutSplunk 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-splunk-nar

## Description

Sends logs to Splunk Enterprise over TCP, TCP + TLS/SSL, or UDP. If a Message Delimiter is provided, then this processor will read messages from the incoming FlowFile based on the delimiter, and send each message to Splunk. If a Message Delimiter is not provided then the content of the FlowFile will be sent directly to Splunk as if it were a single message.

## Tags

logs, splunk, tcp, udp

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Character Set | Specifies the character set of the data being sent. |
| Hostname | Destination hostname or IP address |
| Idle Connection Expiration | The amount of time a connection should be held open without being used before closing the connection. A value of 0 seconds will disable this feature. |
| Max Size of Socket Send Buffer | The maximum size of the socket send buffer that should be used. This is a suggestion to the Operating System to indicate how big the socket buffer should be. If this value is set too low, the buffer may fill up before the data can be read, and incoming data will be dropped. |
| Message Delimiter | Specifies the delimiter to use for splitting apart multiple messages within a single FlowFile. If not specified, the entire content of the FlowFile will be used as a single message. If specified, the contents of the FlowFile will be split on this delimiter and each section sent as a separate message. Note that if messages are delimited and some messages for a given FlowFile are transferred successfully while others are not, the messages will be split into individual FlowFiles, such that those messages that were successfully sent are routed to the ‘success’ relationship while other messages are sent to the ‘failure’ relationship. |
| Port | Destination port number |
| Protocol | The protocol for communication. |
| SSL Context Service | Specifies the SSL Context Service to enable TLS socket communication |
| Timeout | The timeout for connecting to and communicating with the destination. Does not apply to UDP |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that failed to send to the destination are sent out this relationship. |
| success | FlowFiles that are sent successfully to the destination are sent out this relationship. |

Expand

Show lessSee more
