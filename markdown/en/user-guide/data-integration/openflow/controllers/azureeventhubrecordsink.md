# AzureEventHubRecordSink

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Format and send Records to Azure Event Hubs

## Tags

azure, record, sink

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Authentication Strategy \* | Authentication Strategy | DEFAULT\_AZURE\_CREDENTIAL | - Shared Access Key - Default Azure Credential | Strategy for authenticating to Azure Event Hubs |
| Event Hub Name \* | Event Hub Name |  |  | Provides the Event Hub Name for connections |
| Event Hub Namespace \* | Event Hub Namespace |  |  | Provides provides the host for connecting to Azure Event Hubs |
| Partition Key | Partition Key |  |  | A hint for Azure Event Hub message broker how to distribute messages across one or more partitions |
| Service Bus Endpoint \* | Service Bus Endpoint | .servicebus.windows.net | - Azure - Azure China - Azure Germany - Azure US Government | Provides the domain for connecting to Azure Event Hubs |
| Shared Access Policy | Shared Access Policy |  |  | The name of the shared access policy. This policy must have Send claims |
| Shared Access Policy Key | Shared Access Policy Key |  |  | The primary or secondary key of the shared access policy |
| Transport Type \* | Transport Type | Amqp | - AMQP - AMQP\_WEB\_SOCKETS | Advanced Message Queuing Protocol Transport Type for communication with Azure Event Hubs |
| Record Writer \* | record-sink-record-writer |  |  | Specifies the Controller Service to use for writing out the records. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
