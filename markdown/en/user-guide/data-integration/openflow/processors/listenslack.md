# ListenSlack 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-slack-nar

## Description

Retrieves real-time messages or Slack commands from one or more Slack conversations. The messages are written out in JSON format. Note that this Processor should be used to obtain real-time messages and commands from Slack and does not provide a mechanism for obtaining historical messages. The ConsumeSlack Processor should be used for an initial load of messages from a channel. See Usage / Additional Details for more information about how to configure this Processor and enable it to retrieve messages and commands from Slack.

## Tags

command, event, listen, message, real-time, receive, slack, social media, team, text, unstructured

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| App Token | The Application Token that is registered to your Slack application |
| Bot Token | The Bot Token that is registered to your Slack application |
| Event Type to Receive | Specifies the type of Event that the Processor should respond to |
| Resolve User Details | Specifies whether the Processor should lookup details about the Slack User who sent the received message. If true, the output JSON will contain an additional field named ‘userDetails’. The ‘user’ field will still contain the ID of the user. In order to enable this capability, the Bot Token must be granted the ‘users:read’ and optionally the ‘users.profile:read’ Bot Token Scope. If the rate limit is exceeded when retrieving this information, the received message will be rejected and must be re-delivered. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | All FlowFiles that are created will be sent to this Relationship. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | Set to application/json, as the output will always be in JSON format |
| slack.event.type | Set to the type of Slack event that occurred |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.slack.ConsumeSlack](/user-guide/data-integration/openflow/processors/consumeslack)
