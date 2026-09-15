# GenerateAnswersFromContext 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-rag-evaluation-processors-nar

## Description

Generates synthetic answers for each question present in the incoming records using a Large Language Model (LLM). For every record, the processor extracts the question and its associated context based on the specified RecordPaths, constructs a prompt, and sends it to an LLM provider to obtain a synthetic answer. The generated answer is then inserted into the record at the designated RecordPath.

## Tags

ai, answers, contextual, generation, llm, nlp, openai, openflow, rag, synthetic

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Answer Record Path | The RecordPath to the synthetically generated answers |
| Context Record Path | The RecordPath to the array of contexts in the record. |
| LLM Provider Service | The provider service for sending evaluation prompts to LLM |
| Max Character Context Length | Maximum character length of context window. |
| Question Record Path | The RecordPath to the question field in the record. |
| Record Reader | The Record Reader to use for reading the FlowFile. |
| Record Writer | The Record Writer to use for writing the results. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that cannot be processed are routed to this relationship |
| success | FlowFiles that are successfully processed are routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| answers.successfully.generated | The total number of successfully generated synthetic answers for the FlowFile. |
| answers.failed.generated | The total number of synthetic answer generation attempts that failed for the FlowFile. |
| json.parse.failures | Number of JSON parse failures encountered. |

Expand

Show lessSee more
