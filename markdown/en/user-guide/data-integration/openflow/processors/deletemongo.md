# DeleteMongo 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-mongodb-nar

## Description

Executes a delete query against a MongoDB collection. The query is provided in the body of the flowfile and the user can select whether it will delete one or many documents that match it.

## Tags

delete, mongo, mongodb

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Mongo Collection Name | The name of the collection to use |
| Mongo Database Name | The name of the database to use |
| delete-mongo-delete-mode | Choose between deleting one document by query or many documents by query. |
| delete-mongo-fail-on-no-delete | Determines whether to send the flowfile to the success or failure relationship if nothing is successfully deleted. |
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
