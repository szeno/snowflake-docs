# PutUDP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

The PutUDP processor receives a FlowFile and packages the FlowFile content into a single UDP datagram packet which is then transmitted to the configured UDP server. The user must ensure that the FlowFile content being fed to this processor is not larger than the maximum size for the underlying UDP transport. The maximum transport size will vary based on the platform setup but is generally just under 64KB. FlowFiles will be marked as failed if their content is larger than the maximum transport size.

## Tags

egress, put, remote, udp

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Hostname | Destination hostname or IP address |
| Idle Connection Expiration | The amount of time a connection should be held open without being used before closing the connection. A value of 0 seconds will disable this feature. |
| Max Size of Socket Send Buffer | The maximum size of the socket send buffer that should be used. This is a suggestion to the Operating System to indicate how big the socket buffer should be. If this value is set too low, the buffer may fill up before the data can be read, and incoming data will be dropped. |
| Port | Destination port number |
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

## See also

- [org.apache.nifi.processors.standard.ListenUDP](/user-guide/data-integration/openflow/processors/listenudp)
- [org.apache.nifi.processors.standard.PutTCP](/user-guide/data-integration/openflow/processors/puttcp)
