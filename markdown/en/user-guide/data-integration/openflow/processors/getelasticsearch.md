# GetElasticsearch 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-elasticsearch-restapi-nar

## Description

Elasticsearch get processor that uses the official Elastic REST client libraries to fetch a single document from Elasticsearch by \_id. Note that the full body of the document will be read into memory before being written to a FlowFile for transfer.

## Tags

elasticsearch, elasticsearch7, elasticsearch8, elasticsearch9, index, json, put, record

## Input Requirement

ALLOWED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Attribute Name | The name of the FlowFile attribute to use for the retrieved document output. |
| Client Service | An Elasticsearch client service to use for running queries. |
| Destination | Indicates whether the retrieved document is written to the FlowFile content or a FlowFile attribute. |
| Document Id | The \_id of the document to retrieve. |
| Index | The name of the index to use. |
| Type | The type of this document (used by Elasticsearch for indexing and searching). |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| document | Fetched documents are routed to this relationship. |
| failure | All flowfiles that fail for reasons unrelated to server availability go to this relationship. |
| not\_found | A FlowFile is routed to this relationship if the specified document does not exist in the Elasticsearch cluster. |
| retry | All flowfiles that fail due to server/cluster availability go to this relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| filename | The filename attribute is set to the document identifier |
| elasticsearch.index | The Elasticsearch index containing the document |
| elasticsearch.type | The Elasticsearch document type |
| elasticsearch.get.error | The error message provided by Elasticsearch if there is an error fetching the document. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.elasticsearch.JsonQueryElasticsearch](/user-guide/data-integration/openflow/processors/jsonqueryelasticsearch)
