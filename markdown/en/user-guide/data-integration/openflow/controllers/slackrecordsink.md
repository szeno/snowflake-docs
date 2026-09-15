# SlackRecordSink

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Format and send Records to a configured Channel using the Slack Post Message API. The service requires a Slack App with a Bot User configured for access to a Slack workspace. The Bot User OAuth Bearer Token is required for posting messages to Slack.

## Tags

record, sink, slack

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Access Token \* | access-token |  |  | Bot OAuth Token used for authenticating and authorizing the Slack request sent by NiFi. |
| API URL \* | api-url | <https://slack.com/api> |  | Slack Web API URL for posting text messages to channels. It only needs to be changed if Slack changes its API URL. |
| Channel ID \* | channel-id |  |  | Slack channel, private group, or IM channel to send the message to. Use Channel ID instead of the name. |
| Input Character Set \* | input-character-set | UTF-8 |  | Specifies the character set of the records used to generate the Slack message. |
| Record Writer \* | record-sink-record-writer |  |  | Specifies the Controller Service to use for writing out the records. |
| Web Service Client Provider \* | web-service-client-provider |  |  | Controller service to provide HTTP client for communicating with Slack API |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
