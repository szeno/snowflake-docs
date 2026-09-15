# ListS3 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Retrieves a listing of objects from an S3 bucket. For each object that is listed, creates a FlowFile that represents the object so that it can be fetched in conjunction with FetchS3Object. This Processor is designed to run on Primary Node only in a cluster. If the primary node changes, the new Primary Node will pick up where the previous node left off without duplicating all of the data.

## Tags

AWS, Amazon, S3, list

## Input Requirement

FORBIDDEN

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
| Delimiter | The string used to delimit directories within the bucket. Please consult the AWS documentation for the correct use of this field. |
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| Entity Tracking Initial Listing Target | Specify how initial listing should be handled. Used by ‘Tracking Entities’strategy. |
| Entity Tracking State Cache | Listed entities are stored in the specified cache storage so that this processor can resume listing across NiFi restart or in case of primary node change. ‘Tracking Entities’strategy require tracking information of all listed entities within the last ‘Tracking Time Window’. To support large number of entities, the strategy uses DistributedMapCache instead of managed state. Cache key format is ‘ListedEntities::{processorId}(::{nodeId})’. If it tracks per node listed entities, then the optional ‘::{nodeId}’ part is added to manage state separately. E.g. cluster wide cache key =’ListedEntities::8dda2321-0164-1000-50fa-3042fe7d6a7b’, per node cache key =’ListedEntities::8dda2321-0164-1000-50fa-3042fe7d6a7b::nifi-node3’ The stored cache content is Gzipped JSON string. The cache key will be deleted when target listing configuration is changed. Used by ‘Tracking Entities’strategy. |
| Entity Tracking Time Window | Specify how long this processor should track already-listed entities. ‘Tracking Entities’strategy can pick any entity whose timestamp is inside the specified time window. For example, if set to ’30 minutes’, any entity having timestamp in recent 30 minutes will be the listing target when this processor runs. A listed entity is considered ‘new/updated’ and a FlowFile is emitted if one of following condition meets: 1. does not exist in the already-listed entities, 2. has newer timestamp than the cached entity, 3. has different size than the cached entity. If a cached entity ‘s timestamp becomes older than specified time window, that entity will be removed from the cached already-listed entities. Used by’Tracking Entities’strategy. |
| List Type | Specifies whether to use the original List Objects or the newer List Objects Version 2 endpoint. |
| Listing Batch Size | If not using a Record Writer, this property dictates how many S3 objects should be listed in a single batch. Once this number is reached, the FlowFiles that have been created will be transferred out of the Processor. Setting this value lower may result in lower latency by sending out the FlowFiles before the complete listing has finished. However, it can significantly reduce performance. Larger values may take more memory to store all of the information before sending the FlowFiles out. This property is ignored if using a Record Writer, as one of the main benefits of the Record Writer is being able to emit the entire listing as a single FlowFile. |
| Listing Strategy | Specify how to determine new/updated entities. See each strategy descriptions for detail. |
| Maximum Object Age | The maximum age that an S3 object can be in order to be considered; any object older than this amount of time (according to last modification date) will be ignored |
| Minimum Object Age | The minimum age that an S3 object must be in order to be considered; any object younger than this amount of time (according to last modification date) will be ignored |
| Prefix | The prefix used to filter the object list. Do not begin with a forward slash ‘/’. In most cases, it should end with a forward slash ‘/’. |
| Record Writer | Specifies the Record Writer to use for creating the listing. If not specified, one FlowFile will be created for each entity that is listed. If the Record Writer is specified, all entities will be written to a single FlowFile instead of adding attributes to individual FlowFiles. |
| Region | The AWS Region to connect to. |
| Requester Pays | If true, indicates that the requester consents to pay any charges associated with listing the S3 bucket. This sets the ‘x-amz-request-payer’ header to ‘requester’. Note that this setting is not applicable when ‘Use Versions’ is ‘true’. |
| SSL Context Service | Specifies an optional SSL Context Service that, if provided, will be used to create connections |
| Signer Override | The AWS S3 library uses Signature Version 4 by default but this property allows you to specify the Version 2 signer to support older S3-compatible services or even to plug in your own custom signer implementation. |
| Use Versions | Specifies whether to use S3 versions, if applicable. If false, only the latest version of each object will be returned. |
| Write Object Tags | If set to ‘True’, the tags associated with the S3 object will be written as FlowFile attributes |
| Write User Metadata | If set to ‘True’, the user defined metadata associated with the S3 object will be added to FlowFile attributes/records |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | After performing a listing of keys, the timestamp of the newest key is stored, along with the keys that share that same timestamp. This allows the Processor to list only keys that have been added or modified after this date the next time that the Processor is run. State is stored across the cluster so that this Processor can be run on Primary Node only and if a new Primary Node is selected, the new node can pick up where the previous node left off, without duplicating the data. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | FlowFiles are routed to this Relationship after they have been successfully processed. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| s3.bucket | The name of the S3 bucket |
| s3.region | The region of the S3 bucket |
| filename | The name of the file |
| s3.etag | The ETag that can be used to see if the file has changed |
| s3.isLatest | A boolean indicating if this is the latest version of the object |
| s3.lastModified | The last modified time in milliseconds since epoch in UTC time |
| s3.length | The size of the object in bytes |
| s3.storeClass | The storage class of the object |
| s3.version | The version of the object, if applicable |
| s3.tag.\_\_\_ | If ‘Write Object Tags’ is set to ‘True’, the tags associated to the S3 object that is being listed will be written as part of the flowfile attributes |
| s3.user.metadata.\_\_\_ | If ‘Write User Metadata’ is set to ‘True’, the user defined metadata associated to the S3 object that is being listed will be written as part of the flowfile attributes |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.aws.s3.CopyS3Object](/user-guide/data-integration/openflow/processors/copys3object)
- [org.apache.nifi.processors.aws.s3.DeleteS3Object](/user-guide/data-integration/openflow/processors/deletes3object)
- [org.apache.nifi.processors.aws.s3.FetchS3Object](/user-guide/data-integration/openflow/processors/fetchs3object)
- [org.apache.nifi.processors.aws.s3.GetS3ObjectMetadata](/user-guide/data-integration/openflow/processors/gets3objectmetadata)
- [org.apache.nifi.processors.aws.s3.GetS3ObjectTags](/user-guide/data-integration/openflow/processors/gets3objecttags)
- [org.apache.nifi.processors.aws.s3.PutS3Object](/user-guide/data-integration/openflow/processors/puts3object)
- [org.apache.nifi.processors.aws.s3.TagS3Object](/user-guide/data-integration/openflow/processors/tags3object)
