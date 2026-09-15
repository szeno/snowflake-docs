# PutDistributedMapCache 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Gets the content of a FlowFile and puts it to a distributed map cache, using a cache key computed from FlowFile attributes. If the cache already contains the entry and the cache update strategy is ‘keep original’ the entry is not replaced.’

## Tags

cache, distributed, map, put

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Cache Entry Identifier | A FlowFile attribute, or the results of an Attribute Expression Language statement, which will be evaluated against a FlowFile in order to determine the cache key |
| Cache update strategy | Determines how the cache is updated if the cache already contains the entry |
| Distributed Cache Service | The Controller Service that is used to cache flow files |
| Max cache entry size | The maximum amount of data to put into cache |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | Any FlowFile that cannot be inserted into the cache will be routed to this relationship |
| success | Any FlowFile that is successfully inserted into cache will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| cached | All FlowFiles will have an attribute ‘cached’. The value of this attribute is true, is the FlowFile is cached, otherwise false. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.FetchDistributedMapCache](/user-guide/data-integration/openflow/processors/fetchdistributedmapcache)
