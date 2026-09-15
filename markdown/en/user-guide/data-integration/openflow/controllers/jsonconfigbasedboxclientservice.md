# JsonConfigBasedBoxClientService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides Box client objects through which Box API calls can be used.

## Tags

box, client, provider

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Account ID \* | Account ID |  |  | The ID of the Box account which the app will act on behalf of. |
| App Actor \* | App Actor | impersonated-user | - Service Account - Impersonated User | Specifies on behalf of whom Box API calls will be made. |
| App Config File | App Config File |  |  | Full path of an App config JSON file. See Additional Details for more information. |
| App Config JSON | App Config JSON |  |  | The raw JSON containing an App config. See Additional Details for more information. |
| Connect Timeout \* | Connect Timeout | 10 secs |  | Maximum amount of time to wait before failing during initial socket connection. |
| Read Timeout \* | Read Timeout | 30 secs |  | Maximum amount of time to wait before failing while reading socket responses. |
| Proxy Configuration Service | proxy-configuration-service |  |  | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
