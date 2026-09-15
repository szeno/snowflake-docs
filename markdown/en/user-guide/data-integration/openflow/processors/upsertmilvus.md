# UpsertMilvus 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-milvus-processors-nar

## Description

Upserts vectors into Milvus database for a given collection

## Tags

chatbot, embeddings, gen ai, genai, generative ai, insert, llm, metadata, milvus, openflow, publish, text, upsert, vector

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Collection Name | The name of the Milvus collection name to use |
| ID Field Name | The name of the field in Milvus to use for storing the IDs of vectors. If a record path is not provided along with the field name the IDs will be generated based on the filename in the format of a string. |
| ID Record Path | The path to the ID field in the record |
| Max Batch Size | If the number of Records in a FlowFile is large, creating a single request to Milvus can consume significant amounts of NiFi heap. In order to avoid this, the Max Batch Size can limit the number of Records to send in a single request. |
| Metadata Field Name | The name of the field to use for storing other metadata associated with the vectors. This data must be in the format of valid json. |
| Metadata Record Path | The path to the metadata field in the record |
| Milvus Connection Service | Connection Service for accessing Milvus Database |
| Partition | Partition of the vector database that you want to perform operations in. If the database has only one partition leave empty. |
| Record Reader | The Record Reader to use for reading the FlowFile |
| Sparse Vector Field Name | The name of the field to use for storing the sparse vectors. |
| Sparse Vector Indices Path | If, Sparse Vectors are to be provided, this RecordPath points to the indices of the sparse data to use. |
| Sparse Vector Values Path | If, Sparse Vectors are to be provided, this RecordPath points to the values of the sparse data to use. |
| Text Field Name | The name of the field in Milvus to use for storing the text associated with the vectors. |
| Text Record Path | The path to the field in the record that contains the text associated with the vectors. If specified, the text will be inserted under the text field in Milvus. If not specified, the text will not be sent to the Milvus database. |
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

- [com.snowflake.openflow.runtime.processors.milvus.DeleteMilvus](/user-guide/data-integration/openflow/processors/deletemilvus)
