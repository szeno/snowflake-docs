# QueryMilvus 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-milvus-processors-nar

## Description

Queries a given collection in a Milvus database using vectors. Results of query are added to current record under the results record path for each vector searched.

## Tags

chatbot, embeddings, gen ai, genai, generative ai, llm, metadata, milvus, openflow, publish, query, search, text, vector

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Collection Name | The name of the Milvus collection name to use |
| Max Query Batch Size | This is the number of vectors that are contained in a single request to Milvus during a query. Milvus is unable to support batch queries of more than 10 vectors at a time. |
| Maximum Results | The maximum number of results to return (i.e., Top K) |
| Milvus Connection Service | Connection Service for accessing Milvus Database |
| Output Search Fields | Comma separated list of additional fields to return from a search against the Milvus database. Milvus will return the score and id fields by default. |
| Partition | Partition of the vector database that you want to perform operations in. If the database has only one partition leave empty. |
| Record Reader | The Record Reader to use for reading the FlowFile |
| Record Writer | The Record Writer to use for writing the results |
| Reranking Smoothing Parameter | Smoothing Parameter of the Reciprocal Rank Fusion (RRFRanker) during Hybrid Search |
| Results Record Path | Specifies where in the record to place the results. |
| Sparse Vector Field Name | The name of the field to use for storing the sparse vectors. |
| Sparse Vector Indices Path | If, Sparse Vectors are to be provided, this RecordPath points to the indices of the sparse data to use. |
| Sparse Vector Values Path | If, Sparse Vectors are to be provided, this RecordPath points to the values of the sparse data to use. |
| Vector Field Name | The name of the field in Milvus to use for storing the vectors. |
| Vector Record Path | The path to the vector field in the record |

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
