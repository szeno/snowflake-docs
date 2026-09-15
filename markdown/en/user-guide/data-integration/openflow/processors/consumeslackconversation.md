# ConsumeSlackConversation 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-slack-processors-nar

## Description

Retrieves messages from Slack conversations available to the App. New conversations are fetched based on the ‘Reply Monitor Frequency’. Ingested messages are written out in JSON format. See Usage / Additional Details for more information about how to configure this Processor and enable it to retrieve messages from Slack.

## Tags

conversation, conversation.history, slack, social media, team, text, unstructured

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Access Token | OAuth Access Token used for authenticating/authorizing the Slack request sent by NiFi. This may be either a User Token or a Bot Token. It must be granted the channels:history, groups:history, im:history, or mpim:history scope, depending on the type of conversation being used. |
| Batch Size | The maximum number of messages to retrieve in a single request to Slack. The entire response will be parsed into memory, so it is important that this be kept in mind when setting this value. |
| Rate Limiter Service | Slack Rate Limiter Service to coordinate rate limiting across processors |
| Reply Monitor Frequency | After consuming all messages in a given channel, this Processor will periodically poll all “threaded messages”, aka Replies, whose timestamp falls between now and the amount of time specified by the <Reply Monitor Window> property. This property determines how frequently those messages are polled. Setting the value to a shorter duration may result in replies to messages being captured more quickly, providing a lower latency. However, it will also result in additional resource use and could trigger Rate Limiting to occur. This also determines how frequently newly added channels are checked. |
| Reply Monitor Window | After consuming all messages in a given channel, this Processor will periodically poll all “threaded messages”, aka Replies, whose timestamp is between now and this amount of time in the past in order to check for any new replies. Setting this value to a larger value may result in additional resource use and may result in Rate Limiting. However, if a user replies to an old thread that was started outside of this window, the reply may not be captured. |
| Resolve Usernames | Specifies whether or not User IDs should be resolved to usernames. By default, Slack Messages provide the ID of the user that sends a message, such as U0123456789, but not the username, such as NiFiUser. The username may be resolved, but it may require additional calls to the Slack API and requires that the Token used be granted the users:read scope. If set to true, usernames will be resolved with a best-effort policy: if a username cannot be obtained, it will be skipped over. Also, note that when a username is obtained, the Message’s <username> field is populated, and the <text> field is updated such that any mention will be output such as “Hi @user” instead of “Hi <@U1234567>”. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | Maintains a mapping of Slack Channel IDs to the timestamp of the last message that was retrieved for that channel. This allows the processor to only retrieve messages that have been posted since the last time the processor was run. This state is stored in the cluster so that if the Primary Node changes, the new node will pick up where the previous node left off. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | Slack messages that are successfully received will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| slack.channel.id | The ID of the Slack Channel from which the messages were retrieved |
| slack.message.count | The number of slack messages that are included in the FlowFile |
| mime.type | Set to application/json, as the output will always be in JSON format |

Expand

Show lessSee more
