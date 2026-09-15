# UpdateByQueryElasticsearch 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-elasticsearch-restapi-nar

## Description

Update documents in an Elasticsearch index using a query. The query can be loaded from a flowfile body or from the Query parameter. The loaded Query can contain any JSON accepted by Elasticsearch’s \_update\_by\_query API, for example a “query” object to identify what documents are to be updated, plus a “script” to define the updates to perform.

## Tags

elastic, elasticsearch, elasticsearch7, elasticsearch8, elasticsearch9, query, update

## Input Requirement

ALLOWED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Client Service | An Elasticsearch client service to use for running queries. |
| Index | The name of the index to use. |
| Max JSON Field String Length | The maximum allowed length of a string value when parsing a JSON document or attribute. |
| Query | A query in JSON syntax, not Lucene syntax. Ex: {“query”:{“match”:{“somefield”:”somevalue”}}}. If this parameter is not set, the query will be read from the flowfile content. If the query (property and flowfile content) is empty, a default empty JSON Object will be used, which will result in a “match\_all” query in Elasticsearch. |
| Query Attribute | If set, the executed query will be set on each result flowfile in the specified attribute. |
| Query Clause | A “query” clause in JSON syntax, not Lucene syntax. Ex: {“match”:{“somefield”:”somevalue”}}. If the query is empty, a default JSON Object will be used, which will result in a “match\_all” query in Elasticsearch. |
| Query Definition Style | How the JSON Query will be defined for use by the processor. |
| Script | A “script” to execute during the operation, in JSON syntax. Ex: {“source”: “ctx.\_source.count++”, “lang”: “painless”} |
| Type | The type of this document (used by Elasticsearch for indexing and searching). |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If the “by query” operation fails, and a flowfile was read, it will be sent to this relationship. |
| retry | All flowfiles that fail due to server/cluster availability go to this relationship. |
| success | If the “by query” operation succeeds, and a flowfile was read, it will be sent to this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| elasticsearch.update.took | The amount of time that it took to complete the update operation in ms. |
| elasticsearch.update.error | The error message provided by Elasticsearch if there is an error running the update. |

Expand

Show lessSee more
