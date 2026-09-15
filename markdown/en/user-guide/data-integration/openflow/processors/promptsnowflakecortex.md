# PromptSnowflakeCortex 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-snowflake-processors-nar

## Description

Sends a prompt to Snowflake Cortex, writing the response either as a FlowFile attribute or to the contents of the incoming FlowFile. The prompt may consist of pure text interaction only.

## Tags

ai, chat, cortex, openflow, prompt, snowflake, text

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Enable Cortex Guardrails | Filters potentially unsafe and harmful responses from a language model. Either true or false. |
| Max Tokens | The maximum number of tokens to generate |
| Output Strategy | Determines response output destination |
| Response Format | The format of the response from Snowflake Cortex |
| Results Attribute | The name of the attribute to write the response to. |
| Snowflake Connection Service | Database Connection Service for accessing Snowflake |
| System Message | The system message to send to Snowflake Cortex. FlowFile attributes may be referenced via Expression Language, and the contents of the FlowFile may be referenced via the flowfile\_content variable. E.g., ${flowfile\_content} |
| Temperature | The temperature to use for generating the response. |
| Text Model Name | The name of the Snowflake Cortex model |
| Top P | The top P value to use for generating the response |
| User Message | The user message to send to Snowflake Cortex. FlowFile attributes may be referenced via Expression Language, and the contents of the FlowFile may be referenced via the flowfile\_content variable. E.g., ${flowfile\_content} |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If unable to obtain a valid response from Snowflake Cortex, the original FlowFile will be routed to this relationship |
| success | The response from Snowflake Cortex is routed to this relationship |

Expand

Show lessSee more
