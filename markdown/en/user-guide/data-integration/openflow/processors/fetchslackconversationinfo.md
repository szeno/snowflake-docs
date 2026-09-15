# FetchSlackConversationInfo 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-slack-processors-nar

## Description

Fetches Slack conversation info and member emails

## Tags

conversation, conversation.members, slack, social media, team

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Access Token | OAuth Access Token used for authenticating/authorizing the Slack request sent by NiFi. This may be either a User Token or a Bot Token. It must be granted the channels:history, groups:history, im:history, or mpim:history scope, depending on the type of conversation being used. |
| Cache Expiration | User emails are cached to reduce network lookups. A longer expiration reduces network overhead but can cause data to be out of sync. |
| Cache Size | User emails are cached to reduce network lookups. A larger cache consumes memory but reduces network overhead. |
| Channel | The Slack Channel ID to retrieve info from. Leave blank to iterate over every available Conversation. |
| Rate Limiter Service | Slack Rate Limiter Service to coordinate rate limiting across processors |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| conversations | Each configured Slack Conversation info and members will be routed to this relationship in separate FlowFiles |
| failure | If Slack Conversation metadata is unable to be received the input FlowFile will be routed to this relationship |
| original | Original input FlowFile that has been successfully processed. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| conversation.members.count | Set to the number of members of the conversation |
| conversation.id | Set to the number of members of the conversation |
| channel.name | Set to the name of the channel if the conversation is a channel |
| mime.type | Set to application/json, as the output will always be in JSON format |

Expand

Show lessSee more
