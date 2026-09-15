# ListenSyslog 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Listens for Syslog messages being sent to a given port over TCP or UDP. Incoming messages are checked against regular expressions for RFC5424 and RFC3164 formatted messages. The format of each message is: (<PRIORITY>)(VERSION )(TIMESTAMP) (HOSTNAME) (BODY) where version is optional. The timestamp can be an RFC5424 timestamp with a format of “yyyy-MM-dd ‘T’HH:mm:ss. SZ” or “yyyy-MM-dd ‘T’HH:mm:ss. S+hh:mm”, or it can be an RFC3164 timestamp with a format of “MMM d HH:mm:ss”. If an incoming messages matches one of these patterns, the message will be parsed and the individual pieces will be placed in FlowFile attributes, with the original message in the content of the FlowFile. If an incoming message does not match one of these patterns it will not be parsed and the syslog.valid attribute will be set to false with the original message in the content of the FlowFile. Valid messages will be transferred on the success relationship, and invalid messages will be transferred on the invalid relationship.

## Tags

listen, logs, syslog, tcp, udp

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Character Set | Specifies the character set of the Syslog messages. Note that Expression language is not evaluated per FlowFile. |
| Client Auth | The client authentication policy to use for the SSL Context. Only used if an SSL Context Service is provided. |
| Local Network Interface | The name of a local network interface to be used to restrict listening to a specific LAN. |
| Max Batch Size | The maximum number of Syslog events to add to a single FlowFile. If multiple events are available, they will be concatenated along with the <Message Delimiter> up to this configured maximum number of messages |
| Max Size of Message Queue | The maximum size of the internal queue used to buffer messages being transferred from the underlying channel to the processor. Setting this value higher allows more messages to be buffered in memory during surges of incoming messages, but increases the total memory used by the processor. |
| Max Size of Socket Buffer | The maximum size of the socket buffer that should be used. This is a suggestion to the Operating System to indicate how big the socket buffer should be. If this value is set too low, the buffer may fill up before the data can be read, and incoming data will be dropped. |
| Message Delimiter | Specifies the delimiter to place between Syslog messages when multiple messages are bundled together (see <Max Batch Size> property). |
| Parse Messages | Indicates if the processor should parse the Syslog messages. If set to false, each outgoing FlowFile will only contain the sender, protocol, and port, and no additional attributes. |
| Port | The port for Syslog communication. Note that Expression language is not evaluated per FlowFile. |
| Protocol | The protocol for Syslog communication. |
| Receive Buffer Size | The size of each buffer used to receive Syslog messages. Adjust this value appropriately based on the expected size of the incoming Syslog messages. When UDP is selected each buffer will hold one Syslog message. When TCP is selected messages are read from an incoming connection until the buffer is full, or the connection is closed. |
| SSL Context Service | The Controller Service to use in order to obtain an SSL Context. If this property is set, syslog messages will be received over a secure connection. |
| Socket Keep Alive | Whether or not to have TCP socket keep alive turned on. Timing details depend on operating system properties. |
| Worker Threads | Number of threads responsible for decoding and queuing incoming syslog messages |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| invalid | Syslog messages that do not match one of the expected formats will be sent out this relationship as a FlowFile per message. |
| success | Syslog messages that match one of the expected formats will be sent out this relationship as a FlowFile per message. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| syslog.priority | The priority of the Syslog message. |
| syslog.severity | The severity of the Syslog message derived from the priority. |
| syslog.facility | The facility of the Syslog message derived from the priority. |
| syslog.version | The optional version from the Syslog message. |
| syslog.timestamp | The timestamp of the Syslog message. |
| syslog.hostname | The hostname or IP address of the Syslog message. |
| syslog.sender | The hostname of the Syslog server that sent the message. |
| syslog.body | The body of the Syslog message, everything after the hostname. |
| syslog.valid | An indicator of whether this message matched the expected formats. If this value is false, the other attributes will be empty and only the original message will be available in the content. |
| syslog.protocol | The protocol over which the Syslog message was received. |
| syslog.port | The port over which the Syslog message was received. |
| mime.type | The mime.type of the FlowFile which will be text/plain for Syslog messages. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.ParseSyslog](/user-guide/data-integration/openflow/processors/parsesyslog)
- [org.apache.nifi.processors.standard.PutSyslog](/user-guide/data-integration/openflow/processors/putsyslog)
