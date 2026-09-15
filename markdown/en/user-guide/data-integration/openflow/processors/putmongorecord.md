# PutMongoRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-mongodb-nar

## Description

This processor is a record-aware processor for inserting/upserting data into MongoDB. It uses a configured record reader and schema to read an incoming record set from the body of a flowfile and then inserts/upserts batches of those records into a configured MongoDB collection. This processor does not support deletes. The number of documents to insert/upsert at a time is controlled by the “Batch Size” configuration property. This value should be set to a reasonable size to ensure that MongoDB is not overloaded with too many operations at once.

## Tags

insert, mongodb, put, record, update, upsert

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Mongo Collection Name | The name of the collection to use |
| Mongo Database Name | The name of the database to use |
| bypass-validation | Enable or disable bypassing document schema validation during insert or update operations. Bypassing document validation is a Privilege Action in MongoDB. Enabling this property can result in authorization errors for users with limited privileges. |
| insert\_count | The number of records to group together for one single insert/upsert operation against MongoDB. |
| mongo-client-service | If configured, this property will use the assigned client service for connection pooling. |
| ordered | Perform ordered or unordered operations |
| record-reader | Specifies the Controller Service to use for parsing incoming data and determining the data’s schema |
| update-key-fields | Comma separated list of fields based on which to identify documents that need to be updated. If this property is set NiFi will attempt an upsert operation on all documents. If this property is not set all documents will be inserted. |
| update-mode | Choose between updating a single document or multiple documents per incoming record. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | All FlowFiles that cannot be written to MongoDB are routed to this relationship |
| success | All FlowFiles that are written to MongoDB are routed to this relationship |

Expand

Show lessSee more
