# SetCacheClientService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides the ability to communicate with a SetCacheServer. This can be used in order to share a Set between nodes in a NiFi cluster

## Tags

cache, cluster, distributed, set, state

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Communications Timeout \* | Communications Timeout | 30 secs |  | Specifies how long to wait when communicating with the remote server before determining that there is a communications failure if data cannot be sent or received |
| SSL Context Service | SSL Context Service |  |  | If specified, indicates the SSL Context Service that is used to communicate with the remote server. If not specified, communications will not be encrypted |
| Server Hostname \* | Server Hostname |  |  | The name of the server that is running the DistributedSetCacheServer service |
| Server Port \* | Server Port | 4557 |  | The port on the remote server that is to be used when communicating with the DistributedSetCacheServer service |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
