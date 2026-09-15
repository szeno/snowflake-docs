# TagS3Object 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Adds or updates a tag on an Amazon S3 Object.

## Tags

AWS, Amazon, Archive, S3, Tag

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| AWS Credentials Provider service | The Controller Service that is used to obtain AWS credentials provider |
| Append Tag | If set to true, the tag will be appended to the existing set of tags on the S3 object. Any existing tags with the same key as the new tag will be updated with the specified value. If set to false, the existing tags will be removed and the new tag will be set on the S3 object. |
| Bucket | The S3 Bucket to interact with |
| Communications Timeout | The amount of time to wait in order to establish a connection to AWS or receive data from AWS before timing out. |
| Custom Signer Class Name | Fully qualified class name of the custom signer class. The signer must implement com.amazonaws.auth. Signer interface. |
| Custom Signer Module Location | Comma-separated list of paths to files and/or directories which contain the custom signer’s JAR file and its dependencies (if any). |
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| Object Key | The S3 Object Key to use. This is analogous to a filename for traditional file systems. |
| Region | The AWS Region to connect to. |
| SSL Context Service | Specifies an optional SSL Context Service that, if provided, will be used to create connections |
| Signer Override | The AWS S3 library uses Signature Version 4 by default but this property allows you to specify the Version 2 signer to support older S3-compatible services or even to plug in your own custom signer implementation. |
| Tag Key | The key of the tag that will be set on the S3 Object |
| Tag Value | The value of the tag that will be set on the S3 Object |
| Version | The Version of the Object to tag |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If the Processor is unable to process a given FlowFile, it will be routed to this Relationship. |
| success | FlowFiles are routed to this Relationship after they have been successfully processed. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| s3.tag.\_\_\_ | The tags associated with the S3 object will be written as part of the FlowFile attributes |
| s3.exception | The class name of the exception thrown during processor execution |
| s3.additionalDetails | The S3 supplied detail from the failed operation |
| s3.statusCode | The HTTP error code (if available) from the failed operation |
| s3.errorCode | The S3 moniker of the failed operation |
| s3.errorMessage | The S3 exception message from the failed operation |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.aws.s3.CopyS3Object](/user-guide/data-integration/openflow/processors/copys3object)
- [org.apache.nifi.processors.aws.s3.DeleteS3Object](/user-guide/data-integration/openflow/processors/deletes3object)
- [org.apache.nifi.processors.aws.s3.FetchS3Object](/user-guide/data-integration/openflow/processors/fetchs3object)
- [org.apache.nifi.processors.aws.s3.GetS3ObjectMetadata](/user-guide/data-integration/openflow/processors/gets3objectmetadata)
- [org.apache.nifi.processors.aws.s3.GetS3ObjectTags](/user-guide/data-integration/openflow/processors/gets3objecttags)
- [org.apache.nifi.processors.aws.s3.ListS3](/user-guide/data-integration/openflow/processors/lists3)
- [org.apache.nifi.processors.aws.s3.PutS3Object](/user-guide/data-integration/openflow/processors/puts3object)
