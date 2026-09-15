# PublishSlack 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-slack-nar

## Description

Posts a message to the specified Slack channel. The content of the message can be either a user-defined message that makes use of Expression Language or the contents of the FlowFile can be sent as the message. If sending a user-defined message, the contents of the FlowFile may also be optionally uploaded as a file attachment.

## Tags

chat.postMessage, conversation, publish, send, slack, social media, team, text, unstructured, upload, write

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Access Token | OAuth Access Token used for authenticating/authorizing the Slack request sent by NiFi. This may be either a User Token or a Bot Token. The token must be granted the chat:write scope. Additionally, in order to upload FlowFile contents as an attachment, it must be granted files:write. |
| Channel | The name or identifier of the channel to send the message to. If using a channel name, it must be prefixed with the # character. For example, #general. This is valid only for public channels. Otherwise, the unique identifier of the channel to publish to must be provided. |
| Character Set | Specifies the name of the Character Set used to encode the FlowFile contents. |
| Include FlowFile Content as Attachment | Specifies whether or not the contents of the FlowFile should be uploaded as an attachment to the Slack message. |
| Max FlowFile Size | The maximum size of a FlowFile that can be sent to Slack. If any FlowFile exceeds this size, it will be routed to failure. This plays an important role because the entire contents of the file must be loaded into NiFi’s heap in order to send the data to Slack. |
| Message Text | The text of the message to send to Slack. |
| Methods Endpoint Url Prefix | Customization of the Slack Client. Set the methodsEndpointUrlPrefix. If you need to set a different URL prefix for Slack API Methods calls, you can set the one. Default value: <https://slack.com/api/> |
| Publish Strategy | Specifies how the Processor will send the message or file to Slack. |
| Thread Timestamp | The Timestamp identifier for the thread that this message is to be a part of. If not specified, the message will be a top-level message instead of being in a thread. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles are routed to ‘failure’ if unable to be sent to Slack for any other reason |
| rate limited | FlowFiles are routed to ‘rate limited’ if the Rate Limit has been exceeded |
| success | FlowFiles are routed to success after being successfully sent to Slack |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| slack.channel.id | The ID of the Slack Channel from which the messages were retrieved |
| slack.ts | The timestamp of the slack messages that was sent; this is used by Slack as a unique identifier |

Expand

Show lessSee more

## Use cases

| Send specific text as a message to Slack, optionally including the FlowFile’s contents as an attached file. |
| --- |
| Send the contents of the FlowFile as a message to Slack. |

Expand

Show lessSee more

## Use Cases Involving Other Components

| Respond to a Slack message in a thread. |
| --- |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.slack.ConsumeSlack](/user-guide/data-integration/openflow/processors/consumeslack)
- [org.apache.nifi.processors.slack.ListenSlack](/user-guide/data-integration/openflow/processors/listenslack)
