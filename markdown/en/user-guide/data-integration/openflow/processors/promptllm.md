# PromptLLM 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-llm-processors-nar

## Description

This processor sends a user defined prompt to a Large Language Model (LLM) to respond.

## Tags

ai, llm, openflow, prompt, text processing

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Assistant Message | The assistant message to send to the LLM. FlowFile attributes may be referenced via Expression Language, and the contents of the FlowFile may be referenced via the flowfile\_content variable. E.g., ${flowfile\_content}. The assistant message is added last |
| LLM Provider Service | The provider service for sending evaluation prompts to LLM |
| Output Strategy | Determines response output destination |
| Results Attribute | The name of the attribute to write the response to. |
| System Message | The system message to send to the LLM. FlowFile attributes may be referenced via Expression Language, and the contents of the FlowFile may be referenced via the flowfile\_content variable. E.g., ${flowfile\_content}. The system message is added first. |
| User Message | The user message to send to the LLM. FlowFile attributes may be referenced via Expression Language, and the contents of the FlowFile may be referenced via the flowfile\_content variable. E.g., ${flowfile\_content}. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that cannot be processed are routed to this relationship |
| success | FlowFiles that are successfully processed are routed to this relationship |

Expand

Show lessSee more
