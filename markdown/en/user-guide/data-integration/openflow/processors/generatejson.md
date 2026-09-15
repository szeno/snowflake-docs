# GenerateJSON 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-record-generation-nar

## Description

Produces a batch of JSON Objects with random field values based on a configurable JSON Schema.

## Tags

JSON, JSON Schema, generate, random

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Batch Size | Number of records generated per FlowFile produced |
| JSON Schema | JSON Schema version 2020-12 describing an object with properties indicating type and format for each field |
| Output Structure | Structure for writing batches of records to each FlowFile |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | FlowFiles with generated JSON records |

Expand

Show lessSee more
