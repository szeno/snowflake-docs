# PutGridFS 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-mongodb-nar

## Description

Writes a file to a GridFS bucket.

## Tags

file, gridfs, mongo, put, store

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
| gridfs-file-name | The name of the file in the bucket that is the target of this processor. GridFS file names do not include path information because GridFS does not sort files into folders within a bucket. |
| putgridfs-chunk-size | Controls the maximum size of each chunk of a file uploaded into GridFS. |
| putgridfs-enforce-uniqueness | When enabled, this option will ensure that uniqueness is enforced on the bucket. It will do so by creating a MongoDB index that matches your selection. It should ideally be configured once when the bucket is created for the first time because it could take a long time to build on an existing bucket wit a lot of data. |
| putgridfs-hash-attribute | If uniquness enforcement is enabled and the file hash is part of the constraint, this must be set to an attribute that exists on all incoming flowfiles. |
| putgridfs-properties-prefix | Attributes that have this prefix will be added to the file stored in GridFS as metadata. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| duplicate | Flowfiles that fail the duplicate check are sent to this relationship. |
| failure | When there is a failure processing the flowfile, it goes to this relationship. |
| success | When the operation succeeds, the flowfile is sent to this relationship. |

Expand

Show lessSee more
