# JWTBearerOAuth2AccessTokenProvider

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides OAuth 2.0 access tokens that can be used as Bearer authorization header in HTTP requests. This controller service is for implementing the OAuth 2.0 JWT Bearer Flow.

## Tags

access token, authorization, hjwt, oauth2, provider

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Assertion Parameter Name \* | Assertion Parameter Name | assertion |  | Name of the parameter to use for the JWT assertion in the request to the token endpoint. |
| Audience | Audience |  |  | The audience claim (aud) for the JWT. Space-separated list of audiences if multiple are expected. |
| Grant Type \* | Grant Type | <urn:ietf:params:oauth:grant-type:jwt-bearer> |  | Value to set for the grant\_type parameter in the request to the token endpoint. |
| Issuer | Issuer |  |  | The issuer claim (iss) for the JWT. |
| JWT Expiration Time \* | JWT Expiration Time | 1 hour |  | Expiration time used to set the corresponding claim of the JWT. In case the returned access token does not includean expiration time, this will be used with the refresh window to re-acquire a new access token. |
| JWT ID | JWT ID |  |  | The “jti” (JWT ID) claim provides a unique identifier for the JWT. The identifier value must be assigned in amanner that ensures that there’s a negligible probability that the same value will be accidentally assigned to adifferent data object; if the application uses multiple issuers, collisions MUST be prevented among values producedby different issuers as well. The “jti” value is a case-sensitive string. If set, it is recommended to set thisvalue to ${UUID()}. |
| Key ID | Key ID |  |  | The ID of the public key used to sign the JWT. It’ll be used as the kid header in the JWT. |
| Private Key Service \* | Private Key Service |  |  | The private key service to use for signing JWTs. |
| Refresh Window \* | Refresh Window | 5 minutes |  | The service will attempt to refresh tokens expiring within the refresh window, subtracting the configured duration from the token expiration. |
| SSL Context Service \* | SSL Context Service |  |  | An instance of SSLContextProvider configured with a certificate that will be used to set the x5t header. Must be using RSA algorithm. |
| Scope | Scope |  |  | The scope claim (scope) for the JWT. |
| Set JWT Header X.509 Cert Thumbprint \* | Set JWT Header X.509 Cert Thumbprint | false | - true - false | If true, will set the JWT header x5t field with the base64url-encoded SHA-256 thumbprint of the X.509 certificate’s DER encoding.If set to true, an instance of SSLContextProvider must be configured with a certificate using RSA algorithm. |
| Signing Algorithm \* | Signing Algorithm | PS256 | - RS256 - RS384 - RS512 - PS256 - PS384 - PS512 - ES256 - ES384 - ES512 - Ed25519 | The algorithm to use for signing the JWT. |
| Subject | Subject |  |  | The subject claim (sub) for the JWT. |
| Token Endpoint URL \* | Token Endpoint URL |  |  | The URL of the OAuth2 token endpoint. |
| Web Client Service \* | Web Client Service |  |  | The Web Client Service to use for calling the token endpoint. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
