# DeletePinecone 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-pinecone-nar

## Description

Deletes vectors from a Pinecone index.

## Tags

delete, embeddings, genai, generative ai, openflow, pinecone, rag, retrieval augmented generation, vector store

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| ID Prefix | The Pinecone vector ID prefix. If specified, only the vectors whose IDs start with the given value will be deleted. |
| Pinecone API Key | The API key for the Pinecone service |
| Pinecone Index | The name of the Pinecone index to use |
| Pinecone Namespace | The name of the Pinecone namespace to use |
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

## Use cases

| Delete all vectors from a Pinecone index. |
| --- |
| Delete a namespace, along with all of its vectors, from a Pinecone index. |
| Delete all vectors for a particular document from a Pinecone index. |

Expand

Show lessSee more
