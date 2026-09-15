# PromptVertexAI 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-vertexai-nar

## Description

Sends a prompt to VertexAI, writing the response either as a FlowFile attribute or to the contents of the incoming FlowFile. The prompt may consist of pure text interaction or may include multimedia.

## Tags

ai, chat, cloud, gcp, google, image, openflow, pdf, prompt, text, video

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| GCP Credentials Service | The Controller Service used to obtain Google Cloud Platform credentials. |
| GCP Location | The location to configure the Vertex client with |
| GCP Project ID | The project ID to configure the Vertex client with |
| Max File Size | The maximum size of a FlowFile that can be sent to Vertex as an image. If the FlowFile is larger than this, it will be routed to ‘failure’. |
| Max Tokens | The maximum number of tokens to generate |
| Media MIME Type | The MIME type of the media in the FlowFile content. Supported media types are listed here: <https://firebase.google.com/docs/vertex-ai/input-file-requirements> |
| Model Name | The name of the Vertex model |
| Output Strategy | Determines response output destination |
| Prompt Type | The type of prompt to send to Vertex. Text to send a simple prompt. Media to send a multimedia type first followed by a text prompt. |
| Response Format | The format of the response from Vertex |
| Results Attribute | The name of the attribute to write the response to. |
| Stop Sequences | A comma delimited list of strings act as stop sequences. The model will halt after encountering one of the stop sequences. |
| System Message | The system message to send to Vertex. FlowFile attributes may be referenced via Expression Language, and the contents of the FlowFile may be referenced via the flowfile\_content variable. E.g., ${flowfile\_content} |
| Temperature | The temperature to use for generating the response. Defaults to 1.0. Ranges from 0.0 to 1.0. Use temperature closer to 0.0 for analytical / multiple choice, and closer to 1.0 for creative and generative tasks. |
| Top K | The top K value to use for generating the response. Only sample from the top K options for each subsequent token. Recommended for advanced use cases only. You usually only need to use temperature. |
| Top P | The top P value to use for generating the response. Top P is for nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by top\_p. Recommended for advanced use cases only. You usually only need to use temperature. |
| User Message | The user message to send to Vertex. FlowFile attributes may be referenced via Expression Language, and the contents of the FlowFile may be referenced via the flowfile\_content variable. E.g., ${flowfile\_content}. The user message is added first, unless an image is present. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If unable to obtain a valid response from Vertex, the original FlowFile will be routed to this relationship |
| success | The response from Vertex is routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| vertex.usage.inputTokens | The number of input tokens read in the request. |
| vertex.usage.outputTokens | The number of output tokens generated in the response. |
| vertex.chat.completion.id | A unique id assigned to the conversation |
| mime.type | The mime type of the response. |
| filename | An updated filename for the response. |

Expand

Show lessSee more
