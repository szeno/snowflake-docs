# EvaluateRagRetrieval 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-rag-evaluation-processors-nar

## Description

Calculates retrieval metrics (Precision@N, Recall@N, FScore@N, MAP@N, MRR) for a RAG system using an LLM as a judge. For each record, it uses both Precision and Recall prompts to evaluate the response, and adds the metrics as attributes to the FlowFile.

## Tags

evaluation, fscore, llm, metrics, mrr, openai, openflow, precision, rag, recall, retrieval

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Context Identifier Record Path | The RecordPath to the array of contexts IDs in the record. |
| Context Record Path | The RecordPath to the array of contexts in the record. |
| Evaluation Results Record Path | The RecordPath to write the results of the evaluation to. |
| Ground Truth Record Path | The RecordPath to the ground truth field in the record. |
| LLM Provider Service | The provider service for sending evaluation prompts to LLM |
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
| n | The average number of retrieved documents per query. |
| precision.at.n | The average precision at N over all queries. |
| recall.at.n | The average recall at N over all queries. |
| fscore.at.n | The average F-Score at N over all queries. |
| mrr | The Mean Reciprocal Rank. |
| retrieval.eval.failures | Number of records where the eval could not be calculated. |
| json.parse.failures | Number of JSON parse failures encountered. |

Expand

Show lessSee more
