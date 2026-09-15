# RestLookupService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Use a REST service to look up values.

## Tags

http, json, lookup, rest, xml

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Proxy Configuration Service | proxy-configuration-service |  |  | Specifies the Proxy Configuration Controller Service to proxy network requests. In case of SOCKS, it is not guaranteed that the selected SOCKS Version will be used by the processor. |
| Authentication Strategy \* | rest-lookup-authentication-strategy | NONE | - None - Basic - OAuth2 | Authentication strategy to use with REST service. |
| Basic Authentication Password | rest-lookup-basic-auth-password |  |  | The password to be used by the client to authenticate against the Remote URL. |
| Basic Authentication Username | rest-lookup-basic-auth-username |  |  | The username to be used by the client to authenticate against the Remote URL. Cannot include control characters (0-31), ‘:’, or DEL (127). |
| Connection Timeout \* | rest-lookup-connection-timeout | 5 secs |  | Max wait time for connection to remote service. |
| Use Digest Authentication | rest-lookup-digest-auth | false | - true - false | Whether to communicate with the website using Digest Authentication. ‘Basic Authentication Username’ and ‘Basic Authentication Password’ are used for authentication. |
| OAuth2 Access Token Provider \* | rest-lookup-oauth2-access-token-provider |  |  | Enables managed retrieval of OAuth2 Bearer Token applied to HTTP requests using the Authorization Header. |
| Read Timeout \* | rest-lookup-read-timeout | 15 secs |  | Max wait time for response from remote service. |
| Record Path | rest-lookup-record-path |  |  | An optional record path that can be used to define where in a record to get the real data to merge into the record set to be enriched. See documentation for examples of when this might be useful. |
| Record Reader \* | rest-lookup-record-reader |  |  | The record reader to use for loading the payload and handling it as a record set. |
| Response Handling Strategy \* | rest-lookup-response-handling-strategy | RETURNED | - Returned - Evaluated | Whether to return all responses or throw errors for unsuccessful HTTP status codes. |
| SSL Context Service | rest-lookup-ssl-context-service |  |  | The SSL Context Service used to provide client certificate information for TLS/SSL connections. |
| URL \* | rest-lookup-url |  |  | The URL for the REST endpoint. Expression language is evaluated against the lookup key/value pairs, not flowfile attributes. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
