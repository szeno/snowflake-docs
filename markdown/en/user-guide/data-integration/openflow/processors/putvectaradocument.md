# PutVectaraDocument 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-vectara-processors-nar

## Description

Generate and upload a JSON document to Vectara’s upload endpoint. The input text can be JSON Object, JSON Array, or JSONL format.

## Tags

ai, llm, openflow, rag, vectara

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Corpus ID | Identifier of the Vectara corpus |
| Document Attributes | A comma delimited list of NiFi attributes fields, which if present will be included in the document metadata. |
| Document Author | Author of the document |
| Document Creation Time | Timestamp in epoch seconds when the document was created |
| Document Date | Date of document creation |
| Document Description | Description of the document |
| Document ID | A unique identifier for the document constructed either from the source path of the document or a hash of the document’s content. |
| Document Source URL | Source URL for document |
| Document Title | Document Title |
| Index Input Format | Input format for indexing service. JSON Object: Load FlowFile content directly as JSON payload. JSON Lines: Create a new section for each line of JSON. JSON Array: Load FlowFile content as a JSON array and create a new section for each element in the JSON array. |
| Section Custom Dimensions | A comma delimited list of metadata fields, which if present in the metadata path will be included as a section’s custom dimension. The values for custom dimensions must be valid numbers. |
| Section Filter Attributes | A comma delimited list of metadata fields, which if present in the metadata path will be included as a section metadata filter. |
| Section ID Attribute | The field for setting section id, which is populated if present in the metadata path. |
| Section Metadata Attributes | A comma delimited list of metadata fields, which if present in the metadata path will be included will be included in the section metadata. |
| Section Metadata JSON Path | A JSON Path expression to a metadata JSON Object. The JSON Object needs to contain the list of metadata fields. These fields will be included in Section metadata. |
| Section Text JSON Path | A JSON Path expression to the text field. |
| Section Title Attribute | The field for setting the section title, which is populated if present in the metadata path. |
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

## Use Cases Involving Other Components

| Publish a PDF file to a Vectara corpus. |
| --- |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.vectara.PutVectaraFile](/user-guide/data-integration/openflow/processors/putvectarafile)
