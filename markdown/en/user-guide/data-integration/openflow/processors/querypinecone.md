# QueryPinecone 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-pinecone-nar

## Description

Queries Pinecone for vectors that are similar to the input vector, or retrieves a vector by ID.

## Tags

chatbot, gen ai, generative ai, llm, openflow, pinecone, query, similarity, vector

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| ID Record Path | The path to the ID field in the record |
| Include Metadata | Specifies whether to include metadata in the results |
| Include Vectors | Specifies whether to include vectors in the results |
| Number of Results | The number of results to return (i.e., Top K) |
| Pinecone API Key | The API key for the Pinecone service |
| Pinecone Index | The name of the Pinecone index to use |
| Pinecone Namespace | The name of the Pinecone namespace to use |
| Query Filter | A JSON representation of the query filter to use |
| Query Strategy | The strategy to use for querying Pinecone |
| Record Reader | The Record Reader to use for reading the FlowFile |
| Record Writer | The Record Writer to use for writing the results |
| Results Record Path | Specifies where in the record to place the results. |
| Sparse Dense Vector Weighting | Ranges from 0.0 to 1.0. Weight to apply on dense and sparse vectors when doing an hybrid search. (1 - weight) will be applied to the values of the sparse vector and (weight) will be applied to the dense vector. |
| Sparse Vector Indices Path | If, Sparse Vectors are to be provided, this RecordPath points to the indices of the sparse data to use. |
| Sparse Vector Values Path | If, Sparse Vectors are to be provided, this RecordPath points to the values of the sparse data to use. |
| Vector Record Path | The path to the vector field in the record |
| Web Client Service | The Web Client Service to use for communicating with Pinecone |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that cannot be sent to Pinecone, and for which a retry is not expected to be successful, are routed to this relationship |
| retry | FlowFiles that fail to be sent to Pinecone, but for which a retry may help, are routed to this relationship |
| success | FlowFiles that are successfully sent to Pinecone are routed to this relationship |

Expand

Show lessSee more

## Use Cases Involving Other Components

| Query Pinecone for vectors that are similar to some input text |
| --- |

Expand

Show lessSee more
