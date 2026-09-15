# PutAzureEventHub 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-azure-nar

## Description

Send FlowFile contents to Azure Event Hubs

## Tags

azure, cloud, eventhub, events, microsoft, streaming, streams

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Event Hub Name | Name of Azure Event Hubs destination |
| Event Hub Namespace | Namespace of Azure Event Hubs prefixed to Service Bus Endpoint domain |
| Maximum Batch Size | Maximum number of FlowFiles processed for each Processor invocation |
| Partitioning Key Attribute Name | If specified, the value from argument named by this field will be used as a partitioning key to be used by event hub. |
| Service Bus Endpoint | To support namespaces not in the default windows.net domain. |
| Shared Access Policy Key | The key of the shared access policy. Either the primary or the secondary key can be used. |
| Shared Access Policy Name | The name of the shared access policy. This policy must have Send claims. |
| Transport Type | Advanced Message Queuing Protocol Transport Type for communication with Azure Event Hubs |
| Use Azure Managed Identity | Choose whether or not to use the managed identity of Azure VM/VMSS |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Any FlowFile that could not be sent to the event hub will be transferred to this Relationship. |
| success | Any FlowFile that is successfully sent to the event hubs will be transferred to this Relationship. |

Expand

Show lessSee more
