# UpsertPinecone 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-pinecone-nar

## Description

Publishes vectors, including metadata, and optionally text, to a Pinecone index.

## Tags

chatbot, embeddings, gen ai, genai, generative ai, llm, metadata, openflow, pinecone, publish, text, upsert, vector

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| ID Record Path | The path to the ID field in the record |
| Max Batch Size | If the number of Records in a FlowFile is large, creating a single request to Pinecone can consume significant amounts of NiFi heap. In order to avoid this, the Max Batch Size can limit the number of Records to send in a single request. If the number of Records exceeds this value, multiple requests will be sent to Pinecone. |
| Metadata Record Path | The path to the metadata field in the record |
| Pinecone API Key | The API key for the Pinecone service |
| Pinecone Index | The name of the Pinecone index to use |
| Pinecone Namespace | The name of the Pinecone namespace to use |
| Record Reader | The Record Reader to use for reading the FlowFile |
| Sparse Vector Indices Path | If, Sparse Vectors are to be provided, this RecordPath points to the indices of the sparse data to use. |
| Sparse Vector Values Path | If, Sparse Vectors are to be provided, this RecordPath points to the values of the sparse data to use. |
| Text Field Name | The name of the field in the metadata to use for storing the text associated with the vectors. |
| Text Record Path | The path to the field in the record that contains the text associated with the vectors. If specified, the text will be inserted into the metadata when publishing to Pinecone. If not specified, the text will not be sent to Pinecone. |
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

| Create embeddings for raw text data, or text that exists in a Record field such as JSON, using OpenAI’s embeddings model and publish the vectors to Pinecone. |
| --- |
| Add embeddings for a document to a Pinecone index, replacing any embeddings that already exist for the document. |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.openai.CreateOpenAiEmbeddings](/user-guide/data-integration/openflow/processors/createopenaiembeddings)
- [com.snowflake.openflow.runtime.processors.pinecone.DeletePinecone](/user-guide/data-integration/openflow/processors/deletepinecone)
