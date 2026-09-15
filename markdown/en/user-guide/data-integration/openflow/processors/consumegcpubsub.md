# ConsumeGCPubSub 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-gcp-nar

## Description

Consumes messages from the configured Google Cloud PubSub subscription. The ‘Batch Size’ property specified the maximum number of messages that will be pulled from the subscription in a single request. The ‘Processing Strategy’ property specifies if each message should be its own FlowFile or if messages should be grouped into a single FlowFile. Using the Demarcator strategy will provide best throughput when the format allows it. Using Record lets you convert data format as well as doing schema enforcement. Using the FlowFile strategy will generate one FlowFile per message and will have the message’s attributes as FlowFile attributes.

## Tags

consume, gcp, google, google-cloud, message, pubsub

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| GCP Credentials Provider Service | The Controller Service used to obtain Google Cloud Platform credentials. |
| Message Demarcator | Since the PubSub client receives messages in batches, this Processor has an option to output FlowFiles which contains all the messages in a single batch. This property allows you to provide a string (interpreted as UTF-8) to use for demarcating apart multiple messages. To enter special character such as ‘new line’ use CTRL+Enter or Shift+Enter depending on the OS. |
| Output Strategy | The format used to output the Kafka Record into a FlowFile Record. |
| Processing Strategy | Strategy for processing PubSub Records and writing serialized output to FlowFiles |
| Record Reader | The Record Reader to use for incoming messages |
| Record Writer | The Record Writer to use in order to serialize the outgoing FlowFiles |
| api-endpoint | Override the gRPC endpoint in the form of [host:port] |
| gcp-project-id | Google Cloud Project ID |
| gcp-pubsub-publish-batch-size | Indicates the number of messages the cloud service should bundle together in a batch. If not set and left empty, only one message will be used in a batch |
| gcp-pubsub-subscription | Name of the Google Cloud Pub/Sub Subscription |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | FlowFiles are routed to this relationship after a successful Google Cloud Pub/Sub operation. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| gcp.pubsub.ackId | Acknowledgement Id of the consumed Google Cloud PubSub message |
| gcp.pubsub.messageSize | Serialized size of the consumed Google Cloud PubSub message |
| gcp.pubsub.attributesCount | Number of attributes the consumed PubSub message has, if any |
| gcp.pubsub.publishTime | Timestamp value when the message was published |
| gcp.pubsub.subscription | Name of the PubSub subscription |
| Dynamic Attributes | Other than the listed attributes, this processor may write zero or more attributes, if the original Google Cloud Publisher client added any attributes to the message while sending |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.gcp.pubsub.PublishGCPubSub](/user-guide/data-integration/openflow/processors/publishgcpubsub)
