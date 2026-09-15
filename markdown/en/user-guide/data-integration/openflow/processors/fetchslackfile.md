# FetchSlackFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-slack-processors-nar

## Description

Downloads a file shared on Slack. Writes the file content to the FlowFile content and FlowFile attributes from the file.

## Tags

download, file, slack

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Bot Token | The Bot Token that is registered to your Slack application |
| Channel ID | The Slack Channel ID where the file was shared. |
| File ID | The Slack File ID to download. |
| Rate Limiter Service | Slack Rate Limiter Service to coordinate rate limiting across processors |
| Web Client Service | The Web Client Service to use for downloading files from Slack |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles that could not be processed are routed to this relationship |
| success | FlowFiles containing successfully downloaded Slack files are routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | The MIME type of the downloaded file |
| filename | The name of the downloaded file |
| slack.file.name | The Slack File name |
| slack.file.mimetype | The Slack File MIME type |
| slack.file.size | The Slack File size in bytes |
| slack.conversation.id | The Slack Channel ID |
| slack.event.ts | The Slack event timestamp |

Expand

Show lessSee more

## See also

- [com.snowflake.openflow.runtime.processors.slack.FetchSlackConversationInfo](/user-guide/data-integration/openflow/processors/fetchslackconversationinfo)
- [com.snowflake.openflow.runtime.processors.slack.FetchSlackMessage](/user-guide/data-integration/openflow/processors/fetchslackmessage)
