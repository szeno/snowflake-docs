# FetchGridFS 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-mongodb-nar

## Description

Retrieves one or more files from a GridFS bucket by file name or by a user-defined query.

## Tags

fetch, gridfs, mongo

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| gridfs-bucket-name | The GridFS bucket where the files will be stored. If left blank, it will use the default value ‘fs’ that the MongoDB client driver uses. |
| gridfs-client-service | The MongoDB client service to use for database connections. |
| gridfs-database-name | The name of the database to use |
| gridfs-file-name | The name of the file in the bucket that is the target of this processor. |
| gridfs-query | A valid MongoDB query to use to fetch one or more files from GridFS. |
| mongo-operation-mode | This option controls when results are made available to downstream processors. If Stream Query Results is enabled, provenance will not be tracked relative to the input flowfile if an input flowfile is received and starts the query. In Stream Query Results mode errors will be handled by sending a new flowfile with the original content and attributes of the input flowfile to the failure relationship. Streaming should only be used if there is reliable connectivity between MongoDB and NiFi. |
| mongo-query-attribute | If set, the query will be written to a specified attribute on the output flowfiles. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | When there is a failure processing the flowfile, it goes to this relationship. |
| original | The original input flowfile goes to this relationship if the query does not cause an error |
| success | When the operation succeeds, the flowfile is sent to this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| gridfs.file.metadata | The custom metadata stored with a file is attached to this property if it exists. |

Expand

Show lessSee more
