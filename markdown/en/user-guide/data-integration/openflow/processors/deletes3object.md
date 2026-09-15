# DeleteS3Object 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Deletes a file from an Amazon S3 Bucket. If attempting to delete a file that does not exist, FlowFile is routed to success.

## Tags

AWS, Amazon, Archive, Delete, S3

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
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| FullControl User List | A comma-separated list of Amazon User ID’s or E-mail addresses that specifies who should have Full Control for an object |
| Object Key | The S3 Object Key to use. This is analogous to a filename for traditional file systems. |
| Owner | The Amazon ID to use for the object’s owner |
| Read ACL User List | A comma-separated list of Amazon User ID’s or E-mail addresses that specifies who should have permissions to read the Access Control List for an object |
| Read Permission User List | A comma-separated list of Amazon User ID’s or E-mail addresses that specifies who should have Read Access for an object |
| Region | The AWS Region to connect to. |
| SSL Context Service | Specifies an optional SSL Context Service that, if provided, will be used to create connections |
| Signer Override | The AWS S3 library uses Signature Version 4 by default but this property allows you to specify the Version 2 signer to support older S3-compatible services or even to plug in your own custom signer implementation. |
| Version | The Version of the Object to delete |
| Write ACL User List | A comma-separated list of Amazon User ID’s or E-mail addresses that specifies who should have permissions to change the Access Control List for an object |
| Write Permission User List | A comma-separated list of Amazon User ID’s or E-mail addresses that specifies who should have Write Access for an object |
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
| s3.exception | The class name of the exception thrown during processor execution |
| s3.additionalDetails | The S3 supplied detail from the failed operation |
| s3.statusCode | The HTTP error code (if available) from the failed operation |
| s3.errorCode | The S3 moniker of the failed operation |
| s3.errorMessage | The S3 exception message from the failed operation |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.aws.s3.CopyS3Object](/user-guide/data-integration/openflow/processors/copys3object)
- [org.apache.nifi.processors.aws.s3.FetchS3Object](/user-guide/data-integration/openflow/processors/fetchs3object)
- [org.apache.nifi.processors.aws.s3.GetS3ObjectMetadata](/user-guide/data-integration/openflow/processors/gets3objectmetadata)
- [org.apache.nifi.processors.aws.s3.GetS3ObjectTags](/user-guide/data-integration/openflow/processors/gets3objecttags)
- [org.apache.nifi.processors.aws.s3.ListS3](/user-guide/data-integration/openflow/processors/lists3)
- [org.apache.nifi.processors.aws.s3.PutS3Object](/user-guide/data-integration/openflow/processors/puts3object)
- [org.apache.nifi.processors.aws.s3.TagS3Object](/user-guide/data-integration/openflow/processors/tags3object)
