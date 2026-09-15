# StandardAnthropicLLMService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

A Controller Service that provides integration with Anthropic’s Claude AI models through their Messages API. Supports configurable parameters including model selection, response generation settings (temperature, top\_p, top\_k), token limits, and retry behavior.

## Tags

ai, anthropic, api, claude, language model, llm, openflow

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Anthropic API Key \* | Anthropic API Key |  |  | The API Key for authenticating to Anthropic |
| Backoff Base Delay (ms) \* | Backoff Base Delay (ms) | 1000 |  | The base delay in milliseconds for exponential backoff between retries |
| Max Response Tokens \* | Max Response Tokens | 1000 |  | The maximum number of tokens to generate in the response. |
| Max Retries \* | Max Retries | 3 |  | The maximum number of retry attempts for API calls |
| Model Name \* | Model Name | claude-3-5-sonnet-latest |  | The name of the Anthropic model |
| Temperature | Temperature |  |  | The temperature to use for generating the response. |
| Top K | Top K |  |  | The top K value to use for generating the response. Only sample from the top K options for each subsequent token. Recommended for advanced use cases only. You usually only need to use temperature. |
| Top P | Top P |  |  | The top\_p value for nucleus sampling. It controls the diversity of the generated responses. |
| User ID | User ID |  |  | The user id to set in the request metadata |
| Web Client Service \* | Web Client Service |  |  | The Web Client Service to use for communicating with the LLM provider. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
