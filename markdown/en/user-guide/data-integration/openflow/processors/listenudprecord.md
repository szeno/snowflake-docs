# ListenUDPRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Listens for Datagram Packets on a given port and reads the content of each datagram using the configured Record Reader. Each record will then be written to a flow file using the configured Record Writer. This processor can be restricted to listening for datagrams from a specific remote host and port by specifying the Sending Host and Sending Host Port properties, otherwise it will listen for datagrams from all hosts and ports.

## Tags

ingest, listen, record, source, udp

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Character Set | Specifies the character set of the received data. |
| Local Network Interface | The name of a local network interface to be used to restrict listening to a specific LAN. |
| Max Size of Message Queue | The maximum size of the internal queue used to buffer messages being transferred from the underlying channel to the processor. Setting this value higher allows more messages to be buffered in memory during surges of incoming messages, but increases the total memory used by the processor. |
| Max Size of Socket Buffer | The maximum size of the socket buffer that should be used. This is a suggestion to the Operating System to indicate how big the socket buffer should be. If this value is set too low, the buffer may fill up before the data can be read, and incoming data will be dropped. |
| Port | The port to listen on for communication. |
| Receive Buffer Size | The size of each buffer used to receive messages. Adjust this value appropriately based on the expected size of the incoming messages. |
| batch-size | The maximum number of datagrams to write as records to a single FlowFile. The Batch Size will only be reached when data is coming in more frequently than the Poll Timeout. |
| poll-timeout | The amount of time to wait when polling the internal queue for more datagrams. If no datagrams are found after waiting for the configured timeout, then the processor will emit whatever records have been obtained up to that point. |
| record-reader | The Record Reader to use for reading the content of incoming datagrams. |
| record-writer | The Record Writer to use in order to serialize the data before writing to a flow file. |
| sending-host | IP, or name, of a remote host. Only Datagrams from the specified Sending Host Port and this host will be accepted. Improves Performance. May be a system property or an environment variable. |
| sending-host-port | Port being used by remote host to send Datagrams. Only Datagrams from the specified Sending Host and this port will be accepted. Improves Performance. May be a system property or an environment variable. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| parse.failure | If a datagram cannot be parsed using the configured Record Reader, the contents of the message will be routed to this Relationship as its own individual FlowFile. |
| success | Messages received successfully will be sent out this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| udp.sender | The sending host of the messages. |
| udp.port | The sending port the messages were received. |
| record.count | The number of records written to the flow file. |
| mime.type | The mime-type of the writer used to write the records to the flow file. |

Expand

Show lessSee more
