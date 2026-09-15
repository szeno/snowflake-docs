# PromptAzureOpenAI 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-openai-nar

## Description

Sends a prompt to Azure’s OpenAI service, writing the response either as a FlowFile attribute or to the contents of the incoming FlowFile. The prompt may consist of pure text interaction or may include images. In the case of images, a URL may be provided, or the contents of the FlowFile may be used, depending on the provided configuration

## Tags

ai, azure, chat, image, openai, openflow, prompt, text

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| API Key | The API key for authenticating to the Azure OpenAI service |
| Deployment Name | The name of the OpenAI model deployment |
| Detail Level | The image detail level that OpenAI should use for processing the image. Low detail will be less expensive and lower latency, while a high level may provide better results. |
| Image MIME Type | The MIME type of the image |
| Image URL | The URL of the image to send to OpenAI. If not specified, the contents of the FlowFile will be used as the image. |
| Max File Size | The maximum size of a FlowFile that can be sent to OpenAI as an image. If the FlowFile is larger than this, it will be routed to ‘failure’. |
| Max Tokens | The maximum number of tokens to generate |
| OpenAI Service Name | The name of the OpenAI service to use |
| Prompt Type | The type of prompt to send to OpenAI |
| Response Format | The format of the response from OpenAI |
| Results Attribute | The name of the attribute to write the response to. If unset, the response will be written to the FlowFile content. |
| Seed | The seed to use for generating the response |
| System Message | The system message to send to OpenAI. FlowFile attributes may be referenced via Expression Language, and the contents of the FlowFile may be referenced via the flowfile\_content variable. E.g., ${flowfile\_content} |
| Temperature | The temperature to use for generating the response. |
| Top P | The top P value to use for generating the response |
| User | Your end user, sent to OpenAI for monitoring and detection of abuse |
| User Message | The user message to send to OpenAI. FlowFile attributes may be referenced via Expression Language, and the contents of the FlowFile may be referenced via the flowfile\_content variable. E.g., ${flowfile\_content} |
| Web Client Service | The Web Client Service to use for communicating with OpenAI |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If unable to obtain a valid response from Azure OpenAI, the original FlowFile will be routed to this relationship |
| success | The response from Azure OpenAI is routed to this relationship |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.openai.CreateAzureOpenAiEmbeddings](/user-guide/data-integration/openflow/processors/createazureopenaiembeddings)
- [com.snowflake.openflow.runtime.processors.openai.PromptOpenAI](/user-guide/data-integration/openflow/processors/promptopenai)
