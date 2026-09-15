# VolatileSchemaCache

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a Schema Cache that evicts elements based on a Least-Recently-Used algorithm. This cache is not persisted, so any restart of NiFi will result in the cache being cleared. Additionally, the cache will be cleared any time that the Controller Service is stopped and restarted.

## Tags

cache, record, schema

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Maximum Cache Size \* | max-cache-size | 100 |  | The maximum number of Schemas to cache. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
