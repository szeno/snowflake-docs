# CopyS3Object 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Copies a file from one bucket and key to another in AWS S3

## Tags

AWS, Amazon, Archive, Copy, S3

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| AWS Credentials Provider service | The Controller Service that is used to obtain AWS credentials provider |
| Canned ACL | Amazon Canned ACL for an object, one of: BucketOwnerFullControl, BucketOwnerRead, LogDeliveryWrite, AuthenticatedRead, PublicReadWrite, PublicRead, Private; will be ignored if any other ACL/permission/owner property is specified |
| Communications Timeout | The amount of time to wait in order to establish a connection to AWS or receive data from AWS before timing out. |
| Custom Signer Class Name | Fully qualified class name of the custom signer class. The signer must implement com.amazonaws.auth. Signer interface. |
| Custom Signer Module Location | Comma-separated list of paths to files and/or directories which contain the custom signer’s JAR file and its dependencies (if any). |
| Destination Bucket | The bucket that will receive the copy. |
| Destination Key | The target key in the target bucket |
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| FullControl User List | A comma-separated list of Amazon User ID’s or E-mail addresses that specifies who should have Full Control for an object |
| Owner | The Amazon ID to use for the object’s owner |
| Read ACL User List | A comma-separated list of Amazon User ID’s or E-mail addresses that specifies who should have permissions to read the Access Control List for an object |
| Read Permission User List | A comma-separated list of Amazon User ID’s or E-mail addresses that specifies who should have Read Access for an object |
| Region | The AWS Region to connect to. |
| SSL Context Service | Specifies an optional SSL Context Service that, if provided, will be used to create connections |
| Signer Override | The AWS S3 library uses Signature Version 4 by default but this property allows you to specify the Version 2 signer to support older S3-compatible services or even to plug in your own custom signer implementation. |
| Source Bucket | The bucket that contains the file to be copied. |
| Source Key | The source key in the source bucket |
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

## See also

- [org.apache.nifi.processors.aws.s3.DeleteS3Object](/user-guide/data-integration/openflow/processors/deletes3object)
- [org.apache.nifi.processors.aws.s3.FetchS3Object](/user-guide/data-integration/openflow/processors/fetchs3object)
- [org.apache.nifi.processors.aws.s3.GetS3ObjectMetadata](/user-guide/data-integration/openflow/processors/gets3objectmetadata)
- [org.apache.nifi.processors.aws.s3.GetS3ObjectTags](/user-guide/data-integration/openflow/processors/gets3objecttags)
- [org.apache.nifi.processors.aws.s3.ListS3](/user-guide/data-integration/openflow/processors/lists3)
- [org.apache.nifi.processors.aws.s3.PutS3Object](/user-guide/data-integration/openflow/processors/puts3object)
- [org.apache.nifi.processors.aws.s3.TagS3Object](/user-guide/data-integration/openflow/processors/tags3object)
