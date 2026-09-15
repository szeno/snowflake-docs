# ListenTCP 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Listens for incoming TCP connections and reads data from each connection using a line separator as the message demarcator. The default behavior is for each message to produce a single FlowFile, however this can be controlled by increasing the Batch Size to a larger value for higher throughput. The Receive Buffer Size must be set as large as the largest messages expected to be received, meaning if every 100kb there is a line separator, then the Receive Buffer Size must be greater than 100kb. The processor can be configured to use an SSL Context Service to only allow secure connections. When connected clients present certificates for mutual TLS authentication, the Distinguished Names of the client certificate’s issuer and subject are added to the outgoing FlowFiles as attributes. The processor does not perform authorization based on Distinguished Name values, but since these values are attached to the outgoing FlowFiles, authorization can be implemented based on these attributes.

## Tags

listen, ssl, tcp, tls

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Batching Message Delimiter | Specifies the delimiter to place between messages when multiple messages are bundled together (see <Max Batch Size> property). |
| Character Set | Specifies the character set of the received data. |
| Client Auth | The client authentication policy to use for the SSL Context. Only used if an SSL Context Service is provided. |
| Local Network Interface | The name of a local network interface to be used to restrict listening to a specific LAN. |
| Max Batch Size | The maximum number of messages to add to a single FlowFile. If multiple messages are available, they will be concatenated along with the <Message Delimiter> up to this configured maximum number of messages |
| Max Size of Message Queue | The maximum size of the internal queue used to buffer messages being transferred from the underlying channel to the processor. Setting this value higher allows more messages to be buffered in memory during surges of incoming messages, but increases the total memory used by the processor during these surges. |
| Max Size of Socket Buffer | The maximum size of the socket buffer that should be used. This is a suggestion to the Operating System to indicate how big the socket buffer should be. If this value is set too low, the buffer may fill up before the data can be read, and incoming data will be dropped. |
| Port | The port to listen on for communication. |
| Receive Buffer Size | The size of each buffer used to receive messages. Adjust this value appropriately based on the expected size of the incoming messages. |
| SSL Context Service | The Controller Service to use in order to obtain an SSL Context. If this property is set, messages will be received over a secure connection. |
| Worker Threads | The maximum number of worker threads available for servicing TCP connections. |
| idle-timeout | The amount of time a client’s connection will remain open if no data is received. The default of 0 seconds will leave connections open until they are closed by the client. |
| pool-receive-buffers | Enable or disable pooling of buffers that the processor uses for handling bytes received on socket connections. The framework allocates buffers as needed during processing. |

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
| tcp.sender | The sending host of the messages. |
| tcp.port | The sending port the messages were received. |
| client.certificate.issuer.dn | For connections using mutual TLS, the Distinguished Name of the Certificate Authority that issued the client’s certificate is attached to the FlowFile. |
| client.certificate.subject.dn | For connections using mutual TLS, the Distinguished Name of the client certificate’s owner (subject) is attached to the FlowFile. |

Expand

Show lessSee more
