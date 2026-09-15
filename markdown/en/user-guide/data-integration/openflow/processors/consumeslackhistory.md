# ConsumeSlackHistory 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

com.snowflake.openflow.runtime | runtime-slack-processors-nar

## Description

Fetches historical messages from all Slack channels available to the App. This processor queries Slack’s conversations.history and conversations.replies to retrieve older messages and outputs the result as records. The processor tracks the earliest retrieved message timestamp in the cluster state to allow it to continue the historical load on subsequent executions. Channels are discovered automatically, no channel ID or name needs to be configured.

## Tags

consume, conversation, history, slack

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Access Token | OAuth Access Token used for authenticating the Slack request. It must be granted the channels:history (and, if resolving usernames, users:read) scope. |
| Batch Size | The maximum number of messages to retrieve in a single request to Slack. |
| Channel Refresh Frequency | The frequency at which the processor refreshes the list of Slack channels accessible to the App. This helps detect newly available channels or remove channels that are no longer available. |
| Include Message Blocks | Specifies whether the output JSON should include the value of the ‘blocks’ field for each Slack Message. |
| Include Null Fields | Specifies whether fields that have null values should be included in the output JSON. If true, any field with a null value will be output as null; if false, it will be omitted. |
| Rate Limiter Service | Slack Rate Limiter Service to coordinate rate limiting across processors |
| Resolve Usernames | Specifies whether User IDs should be resolved to usernames. If true, usernames will be resolved with a best-effort policy; if a username cannot be obtained, it will be skipped. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | Maintains a mapping of Slack Channel IDs to the earliest message timestamp that has been retrieved. When no more messages are available, a flag is set indicating that the historical load is complete for that channel. This state is stored in the cluster so that if the Primary Node changes, the new node will pick up where the previous node left off. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | FlowFiles containing the JSON-encoded Slack conversation history are routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| slack.channel.id | The ID of the Slack Channel from which the messages were retrieved |
| slack.channel.name | The name of the Slack Channel from which the messages were retrieved |
| slack.message.count | The number of Slack messages that are included in the FlowFile |
| mime.type | Set to application/json, the output will always be in JSON format |

Expand

Show lessSee more
