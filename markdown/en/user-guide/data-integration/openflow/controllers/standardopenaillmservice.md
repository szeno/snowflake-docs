# StandardOpenAILLMService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

A Controller Service that provides integration with OpenAI’s Chat Completion API. Supports configurable parameters including model selection, temperature, top\_p, max tokens, and retry behavior. Handles API authentication, request retries with exponential backoff, and error handling.

## Tags

ai, chat completion, chatgpt, large language model, llm, openai, openflow

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Backoff Base Delay (ms) \* | Backoff Base Delay (ms) | 1000 |  | The base delay in milliseconds for exponential backoff between retries |
| Max Response Tokens | Max Response Tokens |  |  | The maximum number of tokens to generate in the response. |
| Max Retries \* | Max Retries | 3 |  | The maximum number of retry attempts for API calls |
| Model Name \* | Model Name | gpt-4o-mini |  | The name of the OpenAI model. |
| OpenAI API Key \* | OpenAI API Key |  |  | The API Key for authenticating to OpenAI. |
| Seed | Seed |  |  | The seed to use for generating the response |
| Temperature | Temperature |  |  | The temperature to use for generating the response. |
| Top P | Top P |  |  | The top\_p value for nucleus sampling. It controls the diversity of the generated responses. |
| User | User |  |  | Your end user, sent to OpenAI for monitoring and detection of abuse |
| Web Client Service \* | Web Client Service |  |  | The Web Client Service to use for communicating with the LLM provider. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
