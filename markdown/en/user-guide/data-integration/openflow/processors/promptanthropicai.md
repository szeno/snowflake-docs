# PromptAnthropicAI 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-anthropic-nar

## Description

Sends a prompt to Anthropic, writing the response either as a FlowFile attribute or to the contents of the incoming FlowFile. The prompt may consist of pure text interaction or may include an image. Use dynamic properties to enable beta features in the Anthropic endpoint.

## Tags

ai, anthropic, chat, image, openflow, prompt, text

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Anthropic API Key | The API Key for authenticating to Anthropic |
| Assistant Message | The assistant message to send to Anthropic. FlowFile attributes may be referenced via Expression Language, and the contents of the FlowFile may be referenced via the flowfile\_content variable. E.g., ${flowfile\_content}. The assistant message is added last |
| Image MIME Type | The MIME type of the image in the FlowFile content. Supported types are image/jpeg, image/png, image/gif, and image/webp. |
| Max File Size | The maximum size of a FlowFile that can be sent to Anthropic as an image. If the FlowFile is larger than this, it will be routed to ‘failure’. |
| Max Tokens | The maximum number of tokens to generate |
| Model Name | The name of the Anthropic model |
| Output Strategy | Determines response output destination |
| Prompt Type | The type of prompt to send to Anthropic. TEXT to send a simple prompt. IMAGE to send an image first and then a prompt. Use JSON for advanced use of Anthropic’s /v1/messages endpoint. |
| Response Format | The format of the response from Anthropic |
| Results Attribute | The name of the attribute to write the response to. |
| Stop Sequences | A comma delimited list of strings act as stop sequences. The model will halt after encountering one of the stop sequences. |
| System Message | The system message to send to Anthropic. FlowFile attributes may be referenced via Expression Language, and the contents of the FlowFile may be referenced via the flowfile\_content variable. E.g., ${flowfile\_content} |
| Temperature | The temperature to use for generating the response. Defaults to 1.0. Ranges from 0.0 to 1.0. Use temperature closer to 0.0 for analytical / multiple choice, and closer to 1.0 for creative and generative tasks. |
| Top K | The top K value to use for generating the response. Only sample from the top K options for each subsequent token. Recommended for advanced use cases only. You usually only need to use temperature. |
| Top P | The top P value to use for generating the response. Top P is for nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by top\_p. Recommended for advanced use cases only. You usually only need to use temperature. |
| User ID | The user id to set in the request metadata |
| User Message | The user message to send to Anthropic. FlowFile attributes may be referenced via Expression Language, and the contents of the FlowFile may be referenced via the flowfile\_content variable. E.g., ${flowfile\_content}. The user message is added first, unless an image is present. |
| Web Client Service | The Web Client Service to use for communicating with Anthropic |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If unable to obtain a valid response from Anthropic, the original FlowFile will be routed to this relationship |
| retry | If a 5XX response from Anthropic is returned, the original FlowFile will be routed to this relationship |
| success | The response from Anthropic is routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| anthropic.usage.inputTokens | The number of input tokens read in the request. |
| anthropic.usage.outputTokens | The number of output tokens generated in the response. |
| anthropic.chat.completion.id | A unique id assigned to the conversation |
| anthropic.chat.completion.stop.reason | The reason that we stopped. |
| anthropic.chat.completion.stop.sequence | Which custom stop sequence was generated, if any, may be ‘null’. |
| mime.type | The mime type of the response. |
| filename | An updated filename for the response. |

Expand

Show lessSee more
