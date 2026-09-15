# GetMongoRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-mongodb-nar

## Description

A record-based version of GetMongo that uses the Record writers to write the MongoDB result set.

## Tags

fetch, get, json, mongo, mongodb, record

## Input Requirement

ALLOWED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Batch Size | The number of elements to be returned from the server in one batch |
| Limit | The maximum number of elements to return |
| Mongo Collection Name | The name of the collection to use |
| Mongo Database Name | The name of the database to use |
| Projection | The fields to be returned from the documents in the result set; must be a valid BSON document |
| Query | The selection criteria to do the lookup. If the field is left blank, it will look for input from an incoming connection from another processor to provide the query as a valid JSON document inside of the FlowFile’s body. If this field is left blank and a timer is enabled instead of an incoming connection, that will result in a full collection fetch using a “{}” query. |
| Sort | The fields by which to sort; must be a valid BSON document |
| get-mongo-record-writer-factory | The record writer to use to write the result sets. |
| mongo-client-service | If configured, this property will use the assigned client service for connection pooling. |
| mongo-query-attribute | If set, the query will be written to a specified attribute on the output flowfiles. |
| mongodb-schema-name | The name of the schema in the configured schema registry to use for the query results. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | All input FlowFiles that are part of a failed query execution go here. |
| original | All input FlowFiles that are part of a successful query execution go here. |
| success | All FlowFiles that have the results of a successful query execution go here. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mongo.database.name | The database where the results came from. |
| mongo.collection.name | The collection where the results came from. |

Expand

Show lessSee more
