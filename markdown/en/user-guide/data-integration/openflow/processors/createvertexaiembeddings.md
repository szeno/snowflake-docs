# CreateVertexAIEmbeddings 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-vertexai-nar

## Description

Uses VertexAI to create embeddings for text. The input text can be provided as a single FlowFile or as a record-oriented FlowFile.

## Tags

chatbot, cloud, embeddings, gcp, gen ai, generative ai, google, llm, nlp, openflow, text, vertex

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Auto Truncate | If set to false, text that exceeds the token limit causes the request to fail. |
| Embeddings Model | The model to use for embeddings, available models are listed at <https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models#models> |
| Embeddings Record Path | The path to the field in the record where the embeddings are to be written. |
| GCP Credentials Service | The Controller Service used to obtain Google Cloud Platform credentials. |
| GCP Location | The location to configure the Vertex client with |
| GCP Project ID | The project ID to configure the Vertex client with |
| Max Batch Size | The maximum number of records to include in each batch sent to VertexAI |
| Model Publisher | The publisher of the model |
| Output Dimensionality | Used to specify output embedding size. If set, output embeddings will be truncated to the size specified. |
| Record Reader | The record reader to use for reading record-oriented data. If the incoming data is to be treated as plaintext, this property should be left unset. |
| Record Writer | The Record Writer to use for writing the output |
| Task Type | Used to convey intended downstream application of embeddings to help the model tune embeddings for a specific purpose. |
| Text Record Path | The path to the field in the record that contains the text to be embedded. If the incoming data is to be treated as plaintext, this property should be left unset. |
| User | An identifier for the remote user on whose behalf the request is being made. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | The original FlowFile will be routed to this relationship if the embeddings could not be created |
| success | The embeddings will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| record.count | The number of records written to the output |
| mime.type | The MIME type of the output data, based on the chosen Record Writer |

Expand

Show lessSee more

## Use cases

| Create embeddings for text using VertexAI’s Embedding model |
| --- |

Expand

Show lessSee more
