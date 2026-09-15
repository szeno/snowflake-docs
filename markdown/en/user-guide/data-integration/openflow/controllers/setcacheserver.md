# SetCacheServer

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a set (collection of unique values) cache that can be accessed over a socket. Interaction with this service is typically accomplished via a DistributedSetCacheClient service.

## Tags

cache, distinct, distributed, server, set

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Eviction Strategy \* | Eviction Strategy | Least Frequently Used | - Least Frequently Used - Least Recently Used - First In, First Out | Determines which strategy should be used to evict values from the cache to make room for new entries |
| Maximum Cache Entries \* | Maximum Cache Entries | 10000 |  | The maximum number of cache entries that the cache can hold |
| Persistence Directory | Persistence Directory |  |  | If specified, the cache will be persisted in the given directory; if not specified, the cache will be in-memory only |
| Port \* | Port | 4557 |  | The port to listen on for incoming connections |
| SSL Context Service | SSL Context Service |  |  | If specified, this service will be used to create an SSL Context that will be used to secure communications; if not specified, communications will not be secure |
| Maximum Read Size | maximum-read-size | 1 MB |  | The maximum number of network bytes to read for a single cache item |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
