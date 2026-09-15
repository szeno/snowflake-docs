# ExternalHazelcastCacheManager

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

A service that provides cache instances backed by Hazelcast running outside of NiFi.

## Tags

cache, hazelcast

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Hazelcast Cluster Name \* | hazelcast-cluster-name | nifi |  | Name of the Hazelcast cluster. |
| Hazelcast Connection Timeout \* | hazelcast-connection-timeout | 20 secs |  | The maximum amount of time the client tries to connect or reconnect before giving up. |
| Hazelcast Initial Backoff \* | hazelcast-retry-backoff-initial | 1 secs |  | The amount of time the client waits before it tries to reestablish connection for the first time. |
| Hazelcast Maximum Backoff \* | hazelcast-retry-backoff-maximum | 5 secs |  | The maximum amount of time the client waits before it tries to reestablish connection. |
| Hazelcast Backoff Multiplier \* | hazelcast-retry-backoff-multiplier | 1.5 |  | A multiplier by which the wait time is increased before each attempt to reestablish connection. |
| Hazelcast Server Address \* | hazelcast-server-address |  |  | Addresses of one or more the Hazelcast instances, using {host:port} format, separated by comma. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
