# DistributedMapCacheLookupService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Lets you choose a distributed map cache client to retrieve the value associated to a key. The coordinates that are passed to the lookup must contain the key ‘key’.

## Tags

cache, distributed, enrich, key, lookup, map, value

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Character Encoding \* | character-encoding | UTF-8 | - ISO-8859-1 - UTF-8 - UTF-16 - UTF-16LE - UTF-16BE - US-ASCII | Specifies a character encoding to use. |
| Distributed Cache Service \* | distributed-map-cache-service |  |  | The Controller Service that is used to get the cached values. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
