# PutTCP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Sends serialized FlowFiles or Records over TCP to a configurable destination with optional support for TLS

## Tags

egress, put, remote, tcp

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Character Set | Specifies the character set of the data being sent. |
| Connection Per FlowFile | Specifies whether to send each FlowFile’s content on an individual connection. |
| Hostname | Destination hostname or IP address |
| Idle Connection Expiration | The amount of time a connection should be held open without being used before closing the connection. A value of 0 seconds will disable this feature. |
| Max Size of Socket Send Buffer | The maximum size of the socket send buffer that should be used. This is a suggestion to the Operating System to indicate how big the socket buffer should be. If this value is set too low, the buffer may fill up before the data can be read, and incoming data will be dropped. |
| Outgoing Message Delimiter | Specifies the delimiter to use when sending messages out over the same TCP stream. The delimiter is appended to each FlowFile message that is transmitted over the stream so that the receiver can determine when one message ends and the next message begins. Users should ensure that the FlowFile content does not contain the delimiter character to avoid errors. In order to use a new line character you can enter ‘n’. For a tab character use ‘t’. Finally for a carriage return use ‘r’. |
| Port | Destination port number |
| Record Reader | Specifies the Controller Service to use for reading Records from input FlowFiles |
| Record Writer | Specifies the Controller Service to use for writing Records to the configured socket address |
| SSL Context Service | Specifies the SSL Context Service to enable TLS socket communication |
| Timeout | The timeout for connecting to and communicating with the destination. Does not apply to UDP |
| Transmission Strategy | Specifies the strategy used for reading input FlowFiles and transmitting messages to the destination socket address |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that failed to send to the destination are sent out this relationship. |
| success | FlowFiles that are sent successfully to the destination are sent out this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| record.count.transmitted | Count of records transmitted to configured destination address |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.ListenTCP](/user-guide/data-integration/openflow/processors/listentcp)
- [org.apache.nifi.processors.standard.PutUDP](/user-guide/data-integration/openflow/processors/putudp)
