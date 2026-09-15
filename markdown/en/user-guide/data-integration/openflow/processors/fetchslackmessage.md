# FetchSlackMessage 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-slack-processors-nar

## Description

Fetches data about a single Slack message

## Tags

conversation, conversation.history, slack, social media, team, text, unstructured

## Input Requirement

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Access Token | OAuth Access Token used for authenticating/authorizing the Slack request sent by NiFi. This may be either a User Token or a Bot Token. It must be granted the channels:history, groups:history, im:history, or mpim:history scope, depending on the type of conversation being used. |
| Channel | The Slack Channel ID to Retrieve a message from. |
| Include Message Blocks | Specifies whether or not the output JSON should include the value of the ‘blocks’ field for each Slack Message. This field includes information such as individual parts of a message that are formatted using rich text. This may be useful, for instance, for parsing. However, it often accounts for a significant portion of the data and as such may be set to null when it is not useful to you. |
| Include Null Fields | Specifies whether or not fields that have null values should be included in the output JSON. If true, any field in a Slack Message that has a null value will be included in the JSON with a value of null. If false, the key omitted from the output JSON entirely. Omitting null values results in smaller messages that are generally more efficient to process, but including the values may provide a better understanding of the format, especially for schema inference. |
| Message Timestamp | The timestamp of the message which is also its ID within a channel. |
| Rate Limiter Service | Slack Rate Limiter Service to coordinate rate limiting across processors |
| Resolve Usernames | Specifies whether or not User IDs should be resolved to usernames. By default, Slack Messages provide the ID of the user that sends a message, such as U0123456789, but not the username, such as NiFiUser. The username may be resolved, but it may require additional calls to the Slack API and requires that the Token used be granted the users:read scope. If set to true, usernames will be resolved with a best-effort policy: if a username cannot be obtained, it will be skipped over. Also, note that when a username is obtained, the Message’s <username> field is populated, and the <text> field is updated such that any mention will be output such as “Hi @user” instead of “Hi <@U1234567>”. |
| Thread Timestamp | The timestamp of the thread the message belongs to. This can be null or empty unless the message is a reply to another message. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Slack messages that fail to be received will be routed to this relationship |
| not found | Slack messages that were not found on the Slack server will be routed to this relationship |
| success | Slack messages that are successfully received will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | Set to application/json, as the output will always be in JSON format |

Expand

Show lessSee more
