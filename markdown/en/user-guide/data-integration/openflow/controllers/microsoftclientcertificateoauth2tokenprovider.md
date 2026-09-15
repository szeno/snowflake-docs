# MicrosoftClientCertificateOAuth2TokenProvider

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides OAuth2 access tokens for the Microsoft Graph API using client\_credentials with a client certificate.

## Tags

access token, authorization, graph, http, microsoft, oauth2, provider

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Client ID \* | Client ID |  |  | The Client ID for the Microsoft Graph API |
| Refresh Window \* | Refresh Window | 5 s |  | The service will attempt to refresh tokens expiring within the refresh window, subtracting the configured duration from the token expiration. |
| SSL Context Service \* | SSL Context Service |  |  | An instance of SSLContextProvider configured with a certificate and a private key which will be used to sign the JWT assertion. The keys must use RSA algorithm. |
| Tenant ID \* | Tenant ID |  |  | The Tenant ID for the Microsoft Graph API |
| Token Scope \* | Token Scope |  |  | The scope of the requested token.For Graph API should be: <https://graph.microsoft.com/.defaultFor> Sharepoint should in the following format: <https://organization.sharepoint.com/.default> |
| Web Client Service \* | Web Client Service |  |  | The Web Client Service to retrieve access tokens. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
