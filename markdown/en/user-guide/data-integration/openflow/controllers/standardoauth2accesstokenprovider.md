# StandardOauth2AccessTokenProvider

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides OAuth 2.0 access tokens that can be used as Bearer authorization header in HTTP requests. Can use either Resource Owner Password Credentials Grant or Client Credentials Grant. Client authentication can be done with either HTTP Basic authentication or in the request body.

## Tags

access token, authorization, http, oauth2, provider

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Audience | Audience |  |  | Audience for the access token request defined in RFC 8693 Section 2.1 |
| Authorization Server URL \* | Authorization Server URL |  |  | The URL of the authorization server that issues access tokens. |
| Client Authentication Strategy \* | Client Authentication Strategy | REQUEST\_BODY | - REQUEST\_BODY - BASIC\_AUTHENTICATION | Strategy for authenticating the client against the OAuth2 token provider service. |
| Client ID | Client ID |  |  |  |
| Client secret \* | Client secret |  |  |  |
| Grant Type \* | Grant Type | password | - User Password - Client Credentials - Refresh Token | The OAuth2 Grant Type to be used when acquiring an access token. |
| HTTP Protocols \* | HTTP Protocols | H2\_HTTP\_1\_1 | - http/1.1 - h2 http/1.1 - h2 | HTTP Protocols supported for Application Layer Protocol Negotiation with TLS |
| Password \* | Password |  |  | Password for the username on the service that is being accessed. |
| Refresh Token \* | Refresh Token |  |  | Refresh Token supports retrieving a new Access Token when configured |
| Refresh Window \* | Refresh Window | 0 s |  | The service will attempt to refresh tokens expiring within the refresh window, subtracting the configured duration from the token expiration. |
| Resource | Resource |  |  | Resource URI for the access token request defined in RFC 8707 Section 2 |
| SSL Context Service | SSL Context Service |  |  |  |
| Scope | Scope |  |  | Space-delimited, case-sensitive list of scopes of the access request (as per the OAuth 2.0 specification) |
| Username \* | Username |  |  | Username on the service that is being accessed. |
| Proxy Configuration Service | proxy-configuration-service |  |  | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
