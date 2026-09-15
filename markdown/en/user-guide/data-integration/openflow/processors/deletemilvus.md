# DeleteMilvus 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-milvus-processors-nar

## Description

Deletes vectors from Milvus database from a collection by ID. Unmatched IDs are ignored by Milvus and not deleted.

## Tags

chatbot, delete, embeddings, gen ai, genai, generative ai, llm, metadata, milvus, openflow, text, vector

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Collection Name | The name of the Milvus collection name to use |
| Delete Filter | The filter to use in the delete request. Example: id like “prefix%” |
| Delete Strategy | The strategy to use for deleting vectors in Milvus |
| ID Record Path | The path to the ID field in the record |
| Milvus Connection Service | Connection Service for accessing Milvus Database |
| Partition | Partition of the vector database that you want to perform operations in. If the database has only one partition leave empty. |
| Record Reader | The Record Reader to use for reading the FlowFile |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that cannot be sent to Milvus, and for which a retry is not expected to be successful, are routed to this relationship |
| retry | FlowFiles that fail to be sent to Milvus, but for which a retry may help, are routed to this relationship |
| success | FlowFiles that are successfully sent to Milvus are routed to this relationship |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.milvus.UpsertMilvus](/user-guide/data-integration/openflow/processors/upsertmilvus)
