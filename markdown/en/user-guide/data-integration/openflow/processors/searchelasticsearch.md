# SearchElasticsearch 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-elasticsearch-restapi-nar

## Description

A processor that allows the user to repeatedly run a paginated query (with aggregations) written with the Elasticsearch JSON DSL. Search After/Point in Time queries must include a valid “sort” field. The processor will retrieve multiple pages of results until either no more results are available or the Pagination Keep Alive expiration is reached, after which the query will restart with the first page of results being retrieved.

## Tags

elasticsearch, elasticsearch7, elasticsearch8, elasticsearch9, json, page, query, scroll, search

## Input Requirement

FORBIDDEN

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
| Pagination Keep Alive | Pagination “keep\_alive” period. Period Elasticsearch will keep the scroll/pit cursor alive in between requests (this is not the time expected for all pages to be returned, but the maximum allowed time for requests between page retrievals). |
| Pagination Type | Pagination method to use. Not all types are available for all Elasticsearch versions, check the Elasticsearch docs to confirm which are applicable and recommended for your service. |
| Query | A query in JSON syntax, not Lucene syntax. Ex: {“query”:{“match”:{“somefield”:”somevalue”}}}. If the query is empty, a default JSON Object will be used, which will result in a “match\_all” query in Elasticsearch. |
| Query Attribute | If set, the executed query will be set on each result flowfile in the specified attribute. |
| Query Clause | A “query” clause in JSON syntax, not Lucene syntax. Ex: {“match”:{“somefield”:”somevalue”}}. If the query is empty, a default JSON Object will be used, which will result in a “match\_all” query in Elasticsearch. |
| Query Definition Style | How the JSON Query will be defined for use by the processor. |
| Restart On Finish | Whether the processor should start another search with the same query once a paginated search has completed. |
| Script Fields | Fields to created using script evaluation at query runtime, in JSON syntax. Ex: {“test1”: {“script”: {“lang”: “painless”, “source”: “doc[ ‘price’].value \* 2”}}, “test2”: {“script”: {“lang”: “painless”, “source”: “doc[ ‘price’].value \* params.factor”, “params”: {“factor”: 2.0}}}} |
| Search Results Format | Format of Hits output. |
| Search Results Split | Output a flowfile containing all hits or one flowfile for each individual hit or one flowfile containing all hits from all paged responses. |
| Size | The maximum number of documents to retrieve in the query. If the query is paginated, this “size” applies to each page of the query, not the “size” of the entire result set. |
| Sort | Sort results by one or more fields, in JSON syntax. Ex: [{“price” : {“order” : “asc”, “mode” : “avg”}}, {“post\_date” : {“format”: “strict\_date\_optional\_time\_nanos”}}] |
| Type | The type of this document (used by Elasticsearch for indexing and searching). |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| LOCAL | The pagination state (scrollId, searchAfter, pitId, hitCount, pageCount, pageExpirationTimestamp) is retained in between invocations of this processor until the Scroll/PiT has expired (when the current time is later than the last query execution plus the Pagination Keep Alive interval). |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| aggregations | Aggregations are routed to this relationship. |
| failure | All flowfiles that fail for reasons unrelated to server availability go to this relationship. |
| hits | Search hits are routed to this relationship. |
| retry | All flowfiles that fail due to server/cluster availability go to this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | application/json |
| aggregation.name | The name of the aggregation whose results are in the output flowfile |
| aggregation.number | The number of the aggregation whose results are in the output flowfile |
| page.number | The number of the page (request), starting from 1, in which the results were returned that are in the output flowfile |
| hit.count | The number of hits that are in the output flowfile |
| elasticsearch.query.error | The error message provided by Elasticsearch if there is an error querying the index. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.elasticsearch.ConsumeElasticsearch](/user-guide/data-integration/openflow/processors/consumeelasticsearch)
- [org.apache.nifi.processors.elasticsearch.PaginatedJsonQueryElasticsearch](/user-guide/data-integration/openflow/processors/paginatedjsonqueryelasticsearch)
