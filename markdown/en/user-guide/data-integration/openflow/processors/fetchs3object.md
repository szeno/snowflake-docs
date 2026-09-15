# FetchS3Object 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Retrieves the contents of an S3 Object and writes it to the content of a FlowFile

## Tags

AWS, Amazon, Fetch, Get, S3

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| AWS Credentials Provider service | The Controller Service that is used to obtain AWS credentials provider |
| Bucket | The S3 Bucket to interact with |
| Communications Timeout | The amount of time to wait in order to establish a connection to AWS or receive data from AWS before timing out. |
| Custom Signer Class Name | Fully qualified class name of the custom signer class. The signer must implement com.amazonaws.auth. Signer interface. |
| Custom Signer Module Location | Comma-separated list of paths to files and/or directories which contain the custom signer’s JAR file and its dependencies (if any). |
| Encryption Service | Specifies the Encryption Service Controller used to configure requests. PutS3Object: For backward compatibility, this value is ignored when ‘Server Side Encryption’ is set. FetchS3Object: Only needs to be configured in case of Server-side Customer Key, Client-side KMS and Client-side Customer Key encryptions. |
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| Object Key | The S3 Object Key to use. This is analogous to a filename for traditional file systems. |
| Range Length | The number of bytes to download from the object, starting from the Range Start. An empty value or a value that extends beyond the end of the object will read to the end of the object. |
| Range Start | The byte position at which to start reading from the object. An empty value or a value of zero will start reading at the beginning of the object. |
| Region | The AWS Region to connect to. |
| Requester Pays | If true, indicates that the requester consents to pay any charges associated with retrieving objects from the S3 bucket. This sets the ‘x-amz-request-payer’ header to ‘requester’. |
| SSL Context Service | Specifies an optional SSL Context Service that, if provided, will be used to create connections |
| Signer Override | The AWS S3 library uses Signature Version 4 by default but this property allows you to specify the Version 2 signer to support older S3-compatible services or even to plug in your own custom signer implementation. |
| Version | The Version of the Object to download |
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
| s3.url | The URL that can be used to access the S3 object |
| s3.bucket | The name of the S3 bucket |
| path | The path of the file |
| absolute.path | The path of the file |
| filename | The name of the file |
| hash.value | The MD5 sum of the file |
| hash.algorithm | MD5 |
| mime.type | If S3 provides the content type/MIME type, this attribute will hold that file |
| s3.etag | The ETag that can be used to see if the file has changed |
| s3.exception | The class name of the exception thrown during processor execution |
| s3.additionalDetails | The S3 supplied detail from the failed operation |
| s3.statusCode | The HTTP error code (if available) from the failed operation |
| s3.errorCode | The S3 moniker of the failed operation |
| s3.errorMessage | The S3 exception message from the failed operation |
| s3.expirationTime | If the file has an expiration date, this attribute will be set, containing the milliseconds since epoch in UTC time |
| s3.expirationTimeRuleId | The ID of the rule that dictates this object’s expiration time |
| s3.sseAlgorithm | The server side encryption algorithm of the object |
| s3.version | The version of the S3 object |
| s3.encryptionStrategy | The name of the encryption strategy that was used to store the S3 object (if it is encrypted) |

Expand

Show lessSee more

## Use cases

| Fetch a specific file from S3 |
| --- |

Expand

Show lessSee more

## Use Cases Involving Other Components

| Retrieve all files in an S3 bucket |
| --- |
| Retrieve only files from S3 that meet some specified criteria |
| Retrieve new files as they arrive in an S3 bucket |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.aws.s3.CopyS3Object](/user-guide/data-integration/openflow/processors/copys3object)
- [org.apache.nifi.processors.aws.s3.DeleteS3Object](/user-guide/data-integration/openflow/processors/deletes3object)
- [org.apache.nifi.processors.aws.s3.GetS3ObjectMetadata](/user-guide/data-integration/openflow/processors/gets3objectmetadata)
- [org.apache.nifi.processors.aws.s3.GetS3ObjectTags](/user-guide/data-integration/openflow/processors/gets3objecttags)
- [org.apache.nifi.processors.aws.s3.ListS3](/user-guide/data-integration/openflow/processors/lists3)
- [org.apache.nifi.processors.aws.s3.PutS3Object](/user-guide/data-integration/openflow/processors/puts3object)
- [org.apache.nifi.processors.aws.s3.TagS3Object](/user-guide/data-integration/openflow/processors/tags3object)
