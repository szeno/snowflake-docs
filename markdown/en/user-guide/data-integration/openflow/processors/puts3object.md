# PutS3Object 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Writes the contents of a FlowFile as an S3 Object to an Amazon S3 Bucket.

## Tags

AWS, Amazon, Archive, Put, S3

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| AWS Credentials Provider service | The Controller Service that is used to obtain AWS credentials provider |
| Bucket | The S3 Bucket to interact with |
| Cache Control | Sets the Cache-Control HTTP header indicating the caching directives of the associated object. Multiple directives are comma-separated. |
| Canned ACL | Amazon Canned ACL for an object, one of: BucketOwnerFullControl, BucketOwnerRead, LogDeliveryWrite, AuthenticatedRead, PublicReadWrite, PublicRead, Private; will be ignored if any other ACL/permission/owner property is specified |
| Communications Timeout | The amount of time to wait in order to establish a connection to AWS or receive data from AWS before timing out. |
| Content Disposition | Sets the Content-Disposition HTTP header indicating if the content is intended to be displayed inline or should be downloaded. Possible values are ‘inline’ or ‘attachment’. If this property is not specified, object ‘s content-disposition will be set to filename. When’ attachment ‘is selected,’; filename=’plus object key are automatically appended to form final value’ attachment; filename=”filename.jpg”’. |
| Content Type | Sets the Content-Type HTTP header indicating the type of content stored in the associated object. The value of this header is a standard MIME type. AWS S3 Java client will attempt to determine the correct content type if one hasn’t been set yet. Users are responsible for ensuring a suitable content type is set when uploading streams. If no content type is provided and cannot be determined by the filename, the default content type “application/octet-stream” will be used. |
| Custom Signer Class Name | Fully qualified class name of the custom signer class. The signer must implement com.amazonaws.auth. Signer interface. |
| Custom Signer Module Location | Comma-separated list of paths to files and/or directories which contain the custom signer’s JAR file and its dependencies (if any). |
| Encryption Service | Specifies the Encryption Service Controller used to configure requests. PutS3Object: For backward compatibility, this value is ignored when ‘Server Side Encryption’ is set. FetchS3Object: Only needs to be configured in case of Server-side Customer Key, Client-side KMS and Client-side Customer Key encryptions. |
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| Expiration Time Rule |  |
| File Resource Service | File Resource Service providing access to the local resource to be transferred |
| FullControl User List | A comma-separated list of Amazon User ID’s or E-mail addresses that specifies who should have Full Control for an object |
| Multipart Part Size | Specifies the part size for use when the PutS3Multipart Upload API is used. Flow files will be broken into chunks of this size for the upload process, but the last part sent can be smaller since it is not padded. The valid range is 50MB to 5GB. |
| Multipart Threshold | Specifies the file size threshold for switch from the PutS3Object API to the PutS3MultipartUpload API. Flow files bigger than this limit will be sent using the stateful multipart process. The valid range is 50MB to 5GB. |
| Multipart Upload AgeOff Interval | Specifies the interval at which existing multipart uploads in AWS S3 will be evaluated for ageoff. When processor is triggered it will initiate the ageoff evaluation if this interval has been exceeded. |
| Multipart Upload Max Age Threshold | Specifies the maximum age for existing multipart uploads in AWS S3. When the ageoff process occurs, any upload older than this threshold will be aborted. |
| Object Key | The S3 Object Key to use. This is analogous to a filename for traditional file systems. |
| Object Tags Prefix | Specifies the prefix which would be scanned against the incoming FlowFile ‘s attributes and the matching attribute’s name and value would be considered as the outgoing S3 object ‘s Tag name and Tag value respectively. For Ex: If the incoming FlowFile carries the attributes tagS3country, tagS3PII, the tag prefix to be specified would be’ tagS3’ |
| Owner | The Amazon ID to use for the object’s owner |
| Read ACL User List | A comma-separated list of Amazon User ID’s or E-mail addresses that specifies who should have permissions to read the Access Control List for an object |
| Read Permission User List | A comma-separated list of Amazon User ID’s or E-mail addresses that specifies who should have Read Access for an object |
| Region | The AWS Region to connect to. |
| Remove Tag Prefix | If set to ‘True’, the value provided for ‘Object Tags Prefix’ will be removed from the attribute(s) and then considered as the Tag name. For ex: If the incoming FlowFile carries the attributes tagS3country, tagS3PII and the prefix is set to ‘tagS3’ then the corresponding tag values would be ‘country’ and ‘PII’ |
| Resource Transfer Source | The source of the content to be transferred |
| SSL Context Service | Specifies an optional SSL Context Service that, if provided, will be used to create connections |
| Server Side Encryption | Specifies the algorithm used for server side encryption. |
| Signer Override | The AWS S3 library uses Signature Version 4 by default but this property allows you to specify the Version 2 signer to support older S3-compatible services or even to plug in your own custom signer implementation. |
| Storage Class |  |
| Temporary Directory Multipart State | Directory in which, for multipart uploads, the processor will locally save the state tracking the upload ID and parts uploaded which must both be provided to complete the upload. |
| Use Chunked Encoding | Enables / disables chunked encoding for upload requests. Set it to false only if your endpoint does not support chunked uploading. |
| Use Path Style Access | Path-style access can be enforced by setting this property to true. Set it to true if your endpoint does not support virtual-hosted-style requests, only path-style requests. |
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
| s3.url | The URL that can be used to access the S3 object |
| s3.bucket | The S3 bucket where the Object was put in S3 |
| s3.key | The S3 key within where the Object was put in S3 |
| s3.contenttype | The S3 content type of the S3 Object that put in S3 |
| s3.version | The version of the S3 Object that was put to S3 |
| s3.exception | The class name of the exception thrown during processor execution |
| s3.additionalDetails | The S3 supplied detail from the failed operation |
| s3.statusCode | The HTTP error code (if available) from the failed operation |
| s3.errorCode | The S3 moniker of the failed operation |
| s3.errorMessage | The S3 exception message from the failed operation |
| s3.etag | The ETag of the S3 Object |
| s3.contentdisposition | The content disposition of the S3 Object that put in S3 |
| s3.cachecontrol | The cache-control header of the S3 Object |
| s3.uploadId | The uploadId used to upload the Object to S3 |
| s3.expiration | A human-readable form of the expiration date of the S3 object, if one is set |
| s3.sseAlgorithm | The server side encryption algorithm of the object |
| s3.usermetadata | A human-readable form of the User Metadata of the S3 object, if any was set |
| s3.encryptionStrategy | The name of the encryption strategy, if any was set |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.aws.s3.CopyS3Object](/user-guide/data-integration/openflow/processors/copys3object)
- [org.apache.nifi.processors.aws.s3.DeleteS3Object](/user-guide/data-integration/openflow/processors/deletes3object)
- [org.apache.nifi.processors.aws.s3.FetchS3Object](/user-guide/data-integration/openflow/processors/fetchs3object)
- [org.apache.nifi.processors.aws.s3.GetS3ObjectMetadata](/user-guide/data-integration/openflow/processors/gets3objectmetadata)
- [org.apache.nifi.processors.aws.s3.GetS3ObjectTags](/user-guide/data-integration/openflow/processors/gets3objecttags)
- [org.apache.nifi.processors.aws.s3.ListS3](/user-guide/data-integration/openflow/processors/lists3)
- [org.apache.nifi.processors.aws.s3.TagS3Object](/user-guide/data-integration/openflow/processors/tags3object)
