# DeleteGridFS 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-mongodb-nar

## Description

Deletes a file from GridFS using a file name or a query.

## Tags

delete, gridfs, mongodb

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| delete-gridfs-query | A valid MongoDB query to use to find and delete one or more files from GridFS. |
| gridfs-bucket-name | The GridFS bucket where the files will be stored. If left blank, it will use the default value ‘fs’ that the MongoDB client driver uses. |
| gridfs-client-service | The MongoDB client service to use for database connections. |
| gridfs-database-name | The name of the database to use |
| gridfs-file-name | The name of the file in the bucket that is the target of this processor. GridFS file names do not include path information because GridFS does not sort files into folders within a bucket. |
| mongo-query-attribute | If set, the query will be written to a specified attribute on the output flowfiles. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | When there is a failure processing the flowfile, it goes to this relationship. |
| success | When the operation succeeds, the flowfile is sent to this relationship. |

Expand

Show lessSee more
