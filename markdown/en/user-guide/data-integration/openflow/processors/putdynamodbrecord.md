# PutDynamoDBRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Inserts items into DynamoDB based on record-oriented data. The record fields are mapped into DynamoDB item fields, including partition and sort keys if set. Depending on the number of records the processor might execute the insert in multiple chunks in order to overcome DynamoDB’s limitation on batch writing. This might result partially processed FlowFiles in which case the FlowFile will be transferred to the “unprocessed” relationship with the necessary attribute to retry later without duplicating the already executed inserts.

## Tags

AWS, Amazon, DynamoDB, Insert, Put, Record

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| AWS Credentials Provider service | The Controller Service that is used to obtain AWS credentials provider |
| Communications Timeout |  |
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| Partition Key Attribute | Specifies the FlowFile attribute that will be used as the value of the partition key when using “Partition by attribute” partition key strategy. |
| Partition Key Field | Defines the name of the partition key field in the DynamoDB table. Partition key is also known as hash key. Depending on the “Partition Key Strategy” the field value might come from the incoming Record or a generated one. |
| Partition Key Strategy | Defines the strategy the processor uses to assign partition key value to the inserted Items. |
| Record Reader | Specifies the Controller Service to use for parsing incoming data and determining the data’s schema. |
| Region |  |
| SSL Context Service | Specifies an optional SSL Context Service that, if provided, will be used to create connections |
| Sort Key Field | Defines the name of the sort key field in the DynamoDB table. Sort key is also known as range key. |
| Sort Key Strategy | Defines the strategy the processor uses to assign sort key to the inserted Items. |
| Table Name | The DynamoDB table name |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles are routed to failure relationship |
| success | FlowFiles are routed to success relationship |
| unprocessed | FlowFiles are routed to unprocessed relationship when DynamoDB is not able to process all the items in the request. Typical reasons are insufficient table throughput capacity and exceeding the maximum bytes per request. Unprocessed FlowFiles can be retried with a new request. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| dynamodb.chunks.processed | Number of chunks successfully inserted into DynamoDB. If not set, it is considered as 0 |
| dynamodb.key.error.unprocessed | DynamoDB unprocessed keys |
| dynmodb.range.key.value.error | DynamoDB range key error |
| dynamodb.key.error.not.found | DynamoDB key not found |
| dynamodb.error.exception.message | DynamoDB exception message |
| dynamodb.error.code | DynamoDB error code |
| dynamodb.error.message | DynamoDB error message |
| dynamodb.error.service | DynamoDB error service |
| dynamodb.error.retryable | DynamoDB error is retryable |
| dynamodb.error.request.id | DynamoDB error request id |
| dynamodb.error.status.code | DynamoDB error status code |
| dynamodb.item.io.error | IO exception message on creating item |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.aws.dynamodb.DeleteDynamoDB](/user-guide/data-integration/openflow/processors/deletedynamodb)
- [org.apache.nifi.processors.aws.dynamodb.GetDynamoDB](/user-guide/data-integration/openflow/processors/getdynamodb)
- [org.apache.nifi.processors.aws.dynamodb.PutDynamoDB](/user-guide/data-integration/openflow/processors/putdynamodb)
