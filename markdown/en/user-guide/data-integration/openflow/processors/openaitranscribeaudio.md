# OpenAiTranscribeAudio 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-openai-nar

## Description

Transcribes audio into English text. The audio data must be in one of these formats: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm

## Tags

audio, flac, m4a, mp3, mp4, mpeg, mpga, ogg, openai, openflow, speech-to-text, text, transcribe, translate, wav, webm

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Model Name | The name of the OpenAI Model to use |
| OpenAI API Key | The API Key for interacting with OpenAI |
| Prompt | Text that can be used to guide the model’s style or continue a previous audio segment. The text must be in English. |
| Response Format | Specifies which format is desired for the output |
| Temperature | The sampling temperature to use. The value must be a floating-point number between 0.0 and 1.0. A higher value, such as 0.8 will result in more of an interpreted translation, whereas a value of 0.0 will result in a more literal translation. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that could not be transcribed are routed to this relationship. |
| success | FlowFiles that have been successfully transcribed will be transferred to this relationship. |

Expand

Show lessSee more

## Use Cases Involving Other Components

| Create embeddings for audio data and insert them into Pinecone so that the audio can be made available to a large language model (LLM) such as OpenAI’s GPT models. |
| --- |

Expand

Show lessSee more
