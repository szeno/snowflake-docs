# RedisDistributedMapCacheClientService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

An implementation of DistributedMapCacheClient that uses Redis as the backing cache. This service relies on the WATCH, MULTI, and EXEC commands in Redis, which are not fully supported when Redis is clustered. As a result, this service can only be used with a Redis Connection Pool that is configured for standalone or sentinel mode. Sentinel mode can be used to provide high-availability configurations.

## Tags

cache, distributed, map, redis

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| TTL \* | redis-cache-ttl | 0 secs |  | Indicates how long the data should exist in Redis. Setting ’0 secs’ would mean the data would exist forever |
| Redis Connection Pool \* | redis-connection-pool |  |  |  |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
