# GetDynamoDB 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Retrieves a document from DynamoDB based on hash and range key. The key can be string or number. For any get request all the primary keys are required (hash or hash and range based on the table keys).A Json Document ( ‘Map’) attribute of the DynamoDB item is read into the content of the FlowFile.

## Tags

AWS, Amazon, DynamoDB, Fetch, Get

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| AWS Credentials Provider service | The Controller Service that is used to obtain AWS credentials provider |
| Batch items for each request (between 1 and 50) | The items to be retrieved in one batch |
| Communications Timeout |  |
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| Hash Key Name | The hash key name of the item |
| Hash Key Value | The hash key value of the item |
| Hash Key Value Type | The hash key value type of the item |
| Json Document attribute | The Json document to be retrieved from the dynamodb item ( ‘s’ type in the schema) |
| Range Key Name | The range key name of the item |
| Range Key Value |  |
| Range Key Value Type | The range key value type of the item |
| Region |  |
| SSL Context Service | Specifies an optional SSL Context Service that, if provided, will be used to create connections |
| Table Name | The DynamoDB table name |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles are routed to failure relationship |
| not found | FlowFiles are routed to not found relationship if key not found in the table |
| success | FlowFiles are routed to success relationship |
| unprocessed | FlowFiles are routed to unprocessed relationship when DynamoDB is not able to process all the items in the request. Typical reasons are insufficient table throughput capacity and exceeding the maximum bytes per request. Unprocessed FlowFiles can be retried with a new request. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| dynamodb.key.error.unprocessed | DynamoDB unprocessed keys |
| dynmodb.range.key.value.error | DynamoDB range key error |
| dynamodb.key.error.not.found | DynamoDB key not found |
| dynamodb.error.exception.message | DynamoDB exception message |
| dynamodb.error.code | DynamoDB error code |
| dynamodb.error.message | DynamoDB error message |
| dynamodb.error.service | DynamoDB error service |
| dynamodb.error.retryable | DynamoDB error is retryable |
| dynamodb.error.request.id | DynamoDB error request id |
| dynamodb.error.status.code | DynamoDB status code |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.aws.dynamodb.DeleteDynamoDB](/user-guide/data-integration/openflow/processors/deletedynamodb)
- [org.apache.nifi.processors.aws.dynamodb.PutDynamoDB](/user-guide/data-integration/openflow/processors/putdynamodb)
- [org.apache.nifi.processors.aws.dynamodb.PutDynamoDBRecord](/user-guide/data-integration/openflow/processors/putdynamodbrecord)
