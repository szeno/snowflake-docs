# UDPEventRecordSink

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Format and send Records as UDP Datagram Packets to a configurable destination

## Tags

UDP, event, record, sink

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Hostname \* | hostname |  |  | Destination hostname or IP address |
| Port \* | port |  |  | Destination port number |
| Record Writer \* | record-sink-record-writer |  |  | Specifies the Controller Service to use for writing out the records. |
| Sender Threads \* | sender-threads | 2 |  | Number of worker threads allocated for handling socket communication |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
