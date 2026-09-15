# PutLambda 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Sends the contents to a specified Amazon Lambda Function. The AWS credentials used for authentication must have permissions execute the Lambda function (lambda:InvokeFunction).The FlowFile content must be JSON.

## Tags

amazon, aws, lambda, put

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| AWS Credentials Provider service | The Controller Service that is used to obtain AWS credentials provider |
| Amazon Lambda Name | The Lambda Function Name |
| Amazon Lambda Qualifier (version) | The Lambda Function Version |
| Communications Timeout |  |
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| Region |  |
| SSL Context Service | Specifies an optional SSL Context Service that, if provided, will be used to create connections |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles are routed to failure relationship |
| success | FlowFiles are routed to success relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| aws.lambda.result.function.error | Function error message in result on posting message to AWS Lambda |
| aws.lambda.result.status.code | Status code in the result for the message when posting to AWS Lambda |
| aws.lambda.result.payload | Payload in the result from AWS Lambda |
| aws.lambda.result.log | Log in the result of the message posted to Lambda |
| aws.lambda.exception.message | Exception message on invoking from AWS Lambda |
| aws.lambda.exception.cause | Exception cause on invoking from AWS Lambda |
| aws.lambda.exception.error.code | Exception error code on invoking from AWS Lambda |
| aws.lambda.exception.request.id | Exception request id on invoking from AWS Lambda |
| aws.lambda.exception.status.code | Exception status code on invoking from AWS Lambda |

Expand

Show lessSee more
