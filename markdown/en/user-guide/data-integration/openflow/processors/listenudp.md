# ListenUDP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Listens for Datagram Packets on a given port. The default behavior produces a FlowFile per datagram, however for higher throughput the Max Batch Size property may be increased to specify the number of datagrams to batch together in a single FlowFile. This processor can be restricted to listening for datagrams from a specific remote host and port by specifying the Sending Host and Sending Host Port properties, otherwise it will listen for datagrams from all hosts and ports.

## Tags

ingest, listen, source, udp

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Batching Message Delimiter | Specifies the delimiter to place between messages when multiple messages are bundled together (see <Max Batch Size> property). |
| Character Set | Specifies the character set of the received data. |
| Local Network Interface | The name of a local network interface to be used to restrict listening to a specific LAN. |
| Max Batch Size | The maximum number of messages to add to a single FlowFile. If multiple messages are available, they will be concatenated along with the <Message Delimiter> up to this configured maximum number of messages |
| Max Size of Message Queue | The maximum size of the internal queue used to buffer messages being transferred from the underlying channel to the processor. Setting this value higher allows more messages to be buffered in memory during surges of incoming messages, but increases the total memory used by the processor. |
| Max Size of Socket Buffer | The maximum size of the socket buffer that should be used. This is a suggestion to the Operating System to indicate how big the socket buffer should be. If this value is set too low, the buffer may fill up before the data can be read, and incoming data will be dropped. |
| Port | The port to listen on for communication. |
| Receive Buffer Size | The size of each buffer used to receive messages. Adjust this value appropriately based on the expected size of the incoming messages. |
| Sending Host | IP, or name, of a remote host. Only Datagrams from the specified Sending Host Port and this host will be accepted. Improves Performance. May be a system property or an environment variable. |
| Sending Host Port | Port being used by remote host to send Datagrams. Only Datagrams from the specified Sending Host and this port will be accepted. Improves Performance. May be a system property or an environment variable. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | Messages received successfully will be sent out this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| udp.sender | The sending host of the messages. |
| udp.port | The sending port the messages were received. |

Expand

Show lessSee more
