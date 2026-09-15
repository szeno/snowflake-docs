# MicrosoftGraphAuthenticationProvider

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides authentication for the Microsoft Graph API, which can be used for interacting with Microsoft 365 services.

## Tags

graph, microsoft, openflow

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Authentication Mechanism \* | Authentication Mechanism | Client Secret | - Client Secret - Username / Password | The mechanism to use for authenticating with the Microsoft Graph API |
| Client ID \* | Client ID |  |  | The Client ID for the Microsoft Graph API |
| Client Secret \* | Client Secret |  |  | The Client Secret for the Microsoft Graph API |
| Password \* | Password |  |  | The password to use for authentication |
| Tenant ID \* | Tenant ID |  |  | The Tenant ID for the Microsoft Graph API |
| Username \* | Username |  |  | The username to use for authentication |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
