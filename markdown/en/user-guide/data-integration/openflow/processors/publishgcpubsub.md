# PublishGCPubSub 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-gcp-nar

## Description

Publishes the content of the incoming flowfile to the configured Google Cloud PubSub topic. The processor supports dynamic properties. If any dynamic properties are present, they will be sent along with the message in the form of ‘attributes’.

## Tags

gcp, google, google-cloud, message, publish, pubsub

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| GCP Credentials Provider Service | The Controller Service used to obtain Google Cloud Platform credentials. |
| Input Batch Size | Maximum number of FlowFiles processed for each Processor invocation |
| Maximum Message Size | The maximum size of a Google PubSub message in bytes. Defaults to 1 MB (1048576 bytes) |
| Message Derivation Strategy | The strategy used to publish the incoming FlowFile to the Google Cloud PubSub endpoint. |
| Record Reader | The Record Reader to use for incoming FlowFiles |
| Record Writer | The Record Writer to use in order to serialize the data before sending to GCPubSub endpoint |
| api-endpoint | Override the gRPC endpoint in the form of [host:port] |
| gcp-batch-bytes | Publish request gets triggered based on this Batch Bytes Threshold property and the Batch Size Threshold property, whichever condition is met first. |
| gcp-project-id | Google Cloud Project ID |
| gcp-pubsub-publish-batch-delay | Indicates the delay threshold to use for batching. After this amount of time has elapsed (counting from the first element added), the elements will be wrapped up in a batch and sent. This value should not be set too high, usually on the order of milliseconds. Otherwise, calls might appear to never complete. |
| gcp-pubsub-publish-batch-size | Indicates the number of messages the cloud service should bundle together in a batch. If not set and left empty, only one message will be used in a batch |
| gcp-pubsub-topic | Name of the Google Cloud PubSub Topic |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles are routed to this relationship if the Google Cloud Pub/Sub operation fails. |
| retry | FlowFiles are routed to this relationship if the Google Cloud Pub/Sub operation fails but attempting the operation again may succeed. |
| success | FlowFiles are routed to this relationship after a successful Google Cloud Pub/Sub operation. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| gcp.pubsub.messageId | ID of the pubsub message published to the configured Google Cloud PubSub topic |
| gcp.pubsub.count.records | Count of pubsub messages published to the configured Google Cloud PubSub topic |
| gcp.pubsub.topic | Name of the Google Cloud PubSub topic the message was published to |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.gcp.pubsub.ConsumeGCPubSub](/user-guide/data-integration/openflow/processors/consumegcpubsub)
