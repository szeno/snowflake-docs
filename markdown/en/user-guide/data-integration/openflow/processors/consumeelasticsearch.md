# ConsumeElasticsearch 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-elasticsearch-restapi-nar

## Description

A processor that repeatedly runs a paginated query against a field using a Range query to consume new Documents from an Elasticsearch index/query. The processor will retrieve multiple pages of results until either no more results are available or the Pagination Keep Alive expiration is reached, after which the Range query will automatically update the field constraint based on the last retrieved Document value.

## Tags

elasticsearch, elasticsearch7, elasticsearch8, elasticsearch9, json, page, query, scroll, search

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Additional Filters | One or more query filters in JSON syntax, not Lucene syntax. Ex: [{“match”:{“somefield”:”somevalue”}}, {“match”:{“anotherfield”:”anothervalue”}}]. These filters wil be used as part of a Bool query’s filter. |
| Aggregation Results Format | Format of Aggregation output. |
| Aggregation Results Split | Output a flowfile containing all aggregations or one flowfile for each individual aggregation. |
| Aggregations | One or more query aggregations (or “aggs”), in JSON syntax. Ex: {“items”: {“terms”: {“field”: “product”, “size”: 10}}} |
| Client Service | An Elasticsearch client service to use for running queries. |
| Fields | Fields of indexed documents to be retrieved, in JSON syntax. Ex: [“user.id”, “http.response.\*”, {“field”: “@timestamp”, “format”: “epoch\_millis”}] |
| Index | The name of the index to use. |
| Initial Value | The initial value to use for the query if the processor has not run previously. If the processor has run previously and stored a value in its state, this property will be ignored. If no value is provided, and the processor has not previously run, no Range query bounds will be used, i.e. all documents will be retrieved in the specified “Sort Order”. |
| Initial Value Date Format | If the “Range Query Field” is a Date field, convert the “Initial Value” to a date with this format. If not specified, Elasticsearch will use the date format provided by the “Range Query Field”’s mapping. For valid syntax, see <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html> |
| Initial Value Date Time Zone | If the “Range Query Field” is a Date field, convert the “Initial Value” to UTC with this time zone. Valid values are ISO 8601 UTC offsets, such as “+01:00” or “-08:00”, and IANA time zone IDs, such as “Europe/London”. |
| Max JSON Field String Length | The maximum allowed length of a string value when parsing a JSON document or attribute. |
| Output No Hits | Output a “hits” flowfile even if no hits found for query. If true, an empty “hits” flowfile will be output even if “aggregations” are output. |
| Pagination Keep Alive | Pagination “keep\_alive” period. Period Elasticsearch will keep the scroll/pit cursor alive in between requests (this is not the time expected for all pages to be returned, but the maximum allowed time for requests between page retrievals). |
| Pagination Type | Pagination method to use. Not all types are available for all Elasticsearch versions, check the Elasticsearch docs to confirm which are applicable and recommended for your service. |
| Query Attribute | If set, the executed query will be set on each result flowfile in the specified attribute. |
| Range Query Field | Field to be tracked as part of an Elasticsearch Range query using a “gt” bound match. This field must exist within the Elasticsearch document for it to be retrieved. |
| Script Fields | Fields to created using script evaluation at query runtime, in JSON syntax. Ex: {“test1”: {“script”: {“lang”: “painless”, “source”: “doc[ ‘price’].value \* 2”}}, “test2”: {“script”: {“lang”: “painless”, “source”: “doc[ ‘price’].value \* params.factor”, “params”: {“factor”: 2.0}}}} |
| Search Results Format | Format of Hits output. |
| Search Results Split | Output a flowfile containing all hits or one flowfile for each individual hit or one flowfile containing all hits from all paged responses. |
| Size | The maximum number of documents to retrieve in the query. If the query is paginated, this “size” applies to each page of the query, not the “size” of the entire result set. |
| Sort | Sort results by one or more fields, in JSON syntax. Ex: [{“price” : {“order” : “asc”, “mode” : “avg”}}, {“post\_date” : {“format”: “strict\_date\_optional\_time\_nanos”}}] |
| Sort Order | The order in which to sort the “Range Query Field”. A “sort” clause for the “Range Query Field” field will be prepended to any provided “Sort” clauses. If a “sort” clause already exists for the “Range Query Field” field, it will not be updated. |
| Type | The type of this document (used by Elasticsearch for indexing and searching). |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | The pagination state (scrollId, searchAfter, pitId, hitCount, pageCount, pageExpirationTimestamp, trackingRangeValue) is retained in between invocations of this processor until the Scroll/PiT has expired (when the current time is later than the last query execution plus the Pagination Keep Alive interval). |

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
| page.number | The number of the page (request), starting from 1, in which the results were returned that are in the output flowfile |
| hit.count | The number of hits that are in the output flowfile |
| elasticsearch.query.error | The error message provided by Elasticsearch if there is an error querying the index. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.elasticsearch.PaginatedJsonQueryElasticsearch](/user-guide/data-integration/openflow/processors/paginatedjsonqueryelasticsearch)
- [org.apache.nifi.processors.elasticsearch.SearchElasticsearch](/user-guide/data-integration/openflow/processors/searchelasticsearch)
