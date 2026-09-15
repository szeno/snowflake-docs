# RunMongoAggregation 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-mongodb-nar

## Description

A processor that runs an aggregation query whenever a flowfile is received.

## Tags

aggregate, aggregation, mongo

## Input Requirement

ALLOWED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Batch Size | The number of elements returned from the server in one batch. |
| Mongo Collection Name | The name of the collection to use |
| Mongo Database Name | The name of the database to use |
| allow-disk-use | Set this to true to enable writing data to temporary files to prevent exceeding the maximum memory use limit during aggregation pipeline staged when handling large datasets. |
| json-type | By default, MongoDB’s Java driver returns “extended JSON”. Some of the features of this variant of JSON may cause problems for other JSON parsers that expect only standard JSON types and conventions. This configuration setting controls whether to use extended JSON or provide a clean view that conforms to standard JSON. |
| mongo-agg-query | The aggregation query to be executed. |
| mongo-charset | Specifies the character set of the document data. |
| mongo-client-service | If configured, this property will use the assigned client service for connection pooling. |
| mongo-date-format | The date format string to use for formatting Date fields that are returned from Mongo. It is only applied when the JSON output format is set to Standard JSON. |
| mongo-query-attribute | If set, the query will be written to a specified attribute on the output flowfiles. |
| results-per-flowfile | How many results to put into a flowfile at once. The whole body will be treated as a JSON array of results. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | The input flowfile gets sent to this relationship when the query fails. |
| original | The input flowfile gets sent to this relationship when the query succeeds. |
| results | The result set of the aggregation will be sent to this relationship. |

Expand

Show lessSee more
