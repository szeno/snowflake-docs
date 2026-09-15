# PutVectaraFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-vectara-processors-nar

## Description

Upload a FlowFile content to Vectara’s index endpoint. Document filter attributes and metadata attributes can be set by referencing FlowFile attributes.

## Tags

ai, llm, openflow, rag, vectara

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Corpus ID | Identifier of the Vectara corpus |
| Document Filter Attributes | A comma delimited list of metadata fields, which if present in the FlowFile attributes will be included in as a document metadata filter. |
| Document ID | A unique identifier for the document constructed either from the source path of the document or a hash of the document’s content. |
| Document Metadata Attributes | A comma delimited list of metadata fields, which if present in the FlowFile attributes will be included will be included in the document metadata. |
| Vectara Client | Vectara Client Service. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Vectara failure relationship |
| original | Original relationship |
| success | Vectara success relationship |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.vectara.PutVectaraDocument](/user-guide/data-integration/openflow/processors/putvectaradocument)
