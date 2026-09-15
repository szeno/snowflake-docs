# SalesforceDataCloudOAuthTokenProvider

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Retrieves an OAuth2 access token from Salesforce using the configured OAuth2 Access Token Provider and exchanges the token for a Data Cloud API token. The token is then used to authenticate with Salesforce Data Cloud APIs.

## Tags

preview, salesforce

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| OAuth2 Access Token Provider \* | OAuth2 Access Token Provider |  |  | JWT Token Provider to use in order to retrieve an access token from Salesforce that will be exchanged for a Data Cloud API token. |
| Refresh Window \* | Refresh Window | 0 s |  | The service will attempt to refresh tokens expiring within the refresh window, subtracting the configured duration from the token expiration. |
| Salesforce Instance \* | Salesforce Instance |  |  | The hostname of the Salesforce instance including the domain such as MyDomainName.my.salesforce.com |
| Web Client Service \* | Web Client Service |  |  | The Web Client Service to use for communicating with Salesforce |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
