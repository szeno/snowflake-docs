# StandardConfluenceClientService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides connection service to Confluence APIs

## Tags

Preview, atlassian, confluence

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| API Token \* | API Token |  |  | Token used for API authentication |
| Environment URL \* | Environment URL |  |  | URL to the Atlassian Confluence Environment ie. <https://domain.atlassian.net> |
| Request Rate Manager \* | Request Rate Manager |  |  | Controller service for keeping track of rate limits for Atlassian APIs |
| User Email \* | User Email |  |  | Confluence user email |
| Web Client Service \* | Web Client Service |  |  | The Web Client Service to use for communicating with Confluence |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
