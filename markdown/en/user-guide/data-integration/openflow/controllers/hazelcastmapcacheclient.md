# HazelcastMapCacheClient

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

An implementation of DistributedMapCacheClient that uses Hazelcast as the backing cache. This service relies on another controller service that manages the actual Hazelcast calls, set in the Hazelcast Cache Manager property.

## Tags

cache, hazelcast, map

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Hazelcast Cache Manager \* | hazelcast-cache-manager |  |  | A Hazelcast Cache Manager which manages connections to Hazelcast and provides cache instances. |
| Hazelcast Cache Name \* | hazelcast-cache-name |  |  | The name of a given cache. A Hazelcast cluster may handle multiple independent caches, each identified by a name. Clients using caches with the same name are working on the same data structure within Hazelcast. |
| Hazelcast Entry Lifetime \* | hazelcast-entry-ttl | 5 min |  | Indicates how long the written entries should exist in Hazelcast. Setting it to ’0 secs’ means that the data will exist until its deletion or until the Hazelcast server is shut down. Using *EmbeddedHazelcastCacheManager* as cache manager will not provide policies to limit the size of the cache. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
