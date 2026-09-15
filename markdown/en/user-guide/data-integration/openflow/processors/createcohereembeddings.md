# CreateCohereEmbeddings 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-cohere-nar

## Description

Uses Cohere to create embeddings for text. The input text can be provided as a single FlowFile or as a record-oriented FlowFile.

## Tags

chatbot, cohere, embeddings, gen ai, generative ai, llm, nlp, openflow, text

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Cohere API Key | The API Key for authenticating to Cohere |
| Embedding Type | Specifies the types of embeddings you want to get back. |
| Embeddings Model | The model to use for embeddings, available models are listed at <https://docs.cohere.com/reference/embed> |
| Embeddings Record Path | The path to the field in the record where the embeddings are to be written. |
| Input Type | Specifies the type of input passed to the model. Required for embedding models v3 and higher. |
| Max Batch Size | The maximum number of records to include in each batch sent to Cohere |
| Record Reader | The record reader to use for reading record-oriented data. If the incoming data is to be treated as plaintext, this property should be left unset. |
| Record Writer | The Record Writer to use for writing the output |
| Text Record Path | The path to the field in the record that contains the text to be embedded. If the incoming data is to be treated as plaintext, this property should be left unset. |
| Truncate Policy | One of NONEEND to specify how the API will handle inputs longer than the maximum token length. |
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

| Create embeddings for text using Cohere’s Embedding model |
| --- |

Expand

Show lessSee more
