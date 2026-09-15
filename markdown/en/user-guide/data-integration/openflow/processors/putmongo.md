# PutMongo 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-mongodb-nar

## Description

Writes the contents of a FlowFile to MongoDB

## Tags

insert, mongodb, put, update, write

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Character Set | The Character Set in which the data is encoded |
| Mode | Indicates whether the processor should insert or update content |
| Mongo Collection Name | The name of the collection to use |
| Mongo Database Name | The name of the database to use |
| Update Method | MongoDB method for running collection update operations, such as updateOne or updateMany |
| Update Query Key | One or more comma-separated document key names used to build the update query criteria, such as \_id |
| Upsert | When true, inserts a document if no document matches the update query criteria; this property is valid only when using update mode, otherwise it is ignored |
| mongo-client-service | If configured, this property will use the assigned client service for connection pooling. |
| put-mongo-update-mode | Choose an update mode. You can either supply a JSON document to use as a direct replacement or specify a document that contains update operators like $set, $unset, and $inc. When Operators mode is enabled, the flowfile content is expected to be the operator part for example: {$set:{“key”: “value”},$inc:{“count”:1234}} and the update query will come from the configured Update Query property. |
| putmongo-update-query | Specify a full MongoDB query to be used for the lookup query to do an update/upsert. NOTE: this field is ignored if the ‘Update Query Key’ value is not empty. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | All FlowFiles that cannot be written to MongoDB are routed to this relationship |
| success | All FlowFiles that are written to MongoDB are routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mongo.put.update.match.count | The match count from result if update/upsert is performed, otherwise not set. |
| mongo.put.update.modify.count | The modify count from result if update/upsert is performed, otherwise not set. |
| mongo.put.upsert.id | The ‘\_id’ hex value if upsert is performed, otherwise not set. |

Expand

Show lessSee more
