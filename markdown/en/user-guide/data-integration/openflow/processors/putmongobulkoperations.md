# PutMongoBulkOperations 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-mongodb-nar

## Description

Writes the contents of a FlowFile to MongoDB as bulk-update

## Tags

bulk, insert, mongodb, put, update, write

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Character Set | The Character Set in which the data is encoded |
| Mongo Collection Name | The name of the collection to use |
| Mongo Database Name | The name of the database to use |
| Ordered | Ordered execution of bulk-writes and break on error - otherwise arbitrary order and continue on error |
| mongo-client-service | If configured, this property will use the assigned client service for connection pooling. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | All FlowFiles that cannot be written to MongoDB are routed to this relationship |
| success | All FlowFiles that are written to MongoDB are routed to this relationship |

Expand

Show lessSee more
