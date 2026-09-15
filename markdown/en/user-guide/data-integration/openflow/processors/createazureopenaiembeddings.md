# CreateAzureOpenAiEmbeddings 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-openai-nar

## Description

Uses Azure OpenAI to create embeddings for text. The input text can be provided as a single FlowFile or as a record-oriented FlowFile.

## Tags

azure, chatbot, embeddings, gen ai, generative ai, llm, nlp, openai, openflow, text

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| API Key | The API Key for authenticating to Azure OpenAI |
| Deployment Name | The name of the OpenAI model deployment to use for creating embeddings |
| Dimensions | The number of dimensions to request the resulting output embeddings have. This is only supported in text-embedding-3 and later models. |
| Embeddings Record Path | The path to the field in the record where the embeddings are to be written. |
| Max Batch Size | The maximum number of records to include in each batch sent to OpenAI |
| OpenAI Service Name | The name of the OpenAI service to use |
| Record Reader | The record reader to use for reading record-oriented data. If the incoming data is to be treated as plaintext, this property should be left unset. |
| Record Writer | The Record Writer to use for writing the output |
| Text Record Path | The path to the field in the record that contains the text to be embedded. If the incoming data is to be treated as plaintext, this property should be left unset. |
| User | An identifier for the remote user on whose behalf the request is being made; OpenAI uses this to detect and prevent abuse. |
| Web Client Service | The Web Client Service to use for communicating with OpenAI |

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

| Create embeddings for text using Azure OpenAI’s Embeddings |
| --- |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.openai.CreateOpenAiEmbeddings](/user-guide/data-integration/openflow/processors/createopenaiembeddings)
- [com.snowflake.openflow.runtime.processors.openai.PromptAzureOpenAI](/user-guide/data-integration/openflow/processors/promptazureopenai)
