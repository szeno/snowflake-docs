# JsonQueryElasticsearch 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-elasticsearch-restapi-nar

## Description

A processor that allows the user to run a query (with aggregations) written with the Elasticsearch JSON DSL. It does not automatically paginate queries for the user. If an incoming relationship is added to this processor, it will use the flowfile’s content for the query. Care should be taken on the size of the query because the entire response from Elasticsearch will be loaded into memory all at once and converted into the resulting flowfiles.

## Tags

elasticsearch, elasticsearch7, elasticsearch8, elasticsearch9, get, json, query, read

## Input Requirement

ALLOWED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Aggregation Results Format | Format of Aggregation output. |
| Aggregation Results Split | Output a flowfile containing all aggregations or one flowfile for each individual aggregation. |
| Aggregations | One or more query aggregations (or “aggs”), in JSON syntax. Ex: {“items”: {“terms”: {“field”: “product”, “size”: 10}}} |
| Client Service | An Elasticsearch client service to use for running queries. |
| Fields | Fields of indexed documents to be retrieved, in JSON syntax. Ex: [“user.id”, “http.response.\*”, {“field”: “@timestamp”, “format”: “epoch\_millis”}] |
| Index | The name of the index to use. |
| Max JSON Field String Length | The maximum allowed length of a string value when parsing a JSON document or attribute. |
| Output No Hits | Output a “hits” flowfile even if no hits found for query. If true, an empty “hits” flowfile will be output even if “aggregations” are output. |
| Query | A query in JSON syntax, not Lucene syntax. Ex: {“query”:{“match”:{“somefield”:”somevalue”}}}. If this parameter is not set, the query will be read from the flowfile content. If the query (property and flowfile content) is empty, a default empty JSON Object will be used, which will result in a “match\_all” query in Elasticsearch. |
| Query Attribute | If set, the executed query will be set on each result flowfile in the specified attribute. |
| Query Clause | A “query” clause in JSON syntax, not Lucene syntax. Ex: {“match”:{“somefield”:”somevalue”}}. If the query is empty, a default JSON Object will be used, which will result in a “match\_all” query in Elasticsearch. |
| Query Definition Style | How the JSON Query will be defined for use by the processor. |
| Script Fields | Fields to created using script evaluation at query runtime, in JSON syntax. Ex: {“test1”: {“script”: {“lang”: “painless”, “source”: “doc[ ‘price’].value \* 2”}}, “test2”: {“script”: {“lang”: “painless”, “source”: “doc[ ‘price’].value \* params.factor”, “params”: {“factor”: 2.0}}}} |
| Search Results Format | Format of Hits output. |
| Search Results Split | Output a flowfile containing all hits or one flowfile for each individual hit. |
| Size | The maximum number of documents to retrieve in the query. If the query is paginated, this “size” applies to each page of the query, not the “size” of the entire result set. |
| Sort | Sort results by one or more fields, in JSON syntax. Ex: [{“price” : {“order” : “asc”, “mode” : “avg”}}, {“post\_date” : {“format”: “strict\_date\_optional\_time\_nanos”}}] |
| Type | The type of this document (used by Elasticsearch for indexing and searching). |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| aggregations | Aggregations are routed to this relationship. |
| failure | All flowfiles that fail for reasons unrelated to server availability go to this relationship. |
| hits | Search hits are routed to this relationship. |
| original | All original flowfiles that don’t cause an error to occur go to this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | application/json |
| aggregation.name | The name of the aggregation whose results are in the output flowfile |
| aggregation.number | The number of the aggregation whose results are in the output flowfile |
| hit.count | The number of hits that are in the output flowfile |
| elasticsearch.query.error | The error message provided by Elasticsearch if there is an error querying the index. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.elasticsearch.PaginatedJsonQueryElasticsearch](/user-guide/data-integration/openflow/processors/paginatedjsonqueryelasticsearch)
