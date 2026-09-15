# Notify 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Caches a release signal identifier in the distributed cache, optionally along with the FlowFile’s attributes. Any flow files held at a corresponding Wait processor will be released once this signal in the cache is discovered.

## Tags

cache, distributed, map, notify, release, signal

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| attribute-cache-regex | Any attributes whose names match this regex will be stored in the distributed cache to be copied to any FlowFiles released from a corresponding Wait processor. Note that the uuid attribute will not be cached regardless of this value. If blank, no attributes will be cached. |
| distributed-cache-service | The Controller Service that is used to cache release signals in order to release files queued at a corresponding Wait processor |
| release-signal-id | A value, or the results of an Attribute Expression Language statement, which will be evaluated against a FlowFile in order to determine the release signal cache key |
| signal-buffer-count | Specify the maximum number of incoming flow files that can be buffered until signals are notified to cache service. The more buffer can provide the better performance, as it reduces the number of interactions with cache service by grouping signals by signal identifier when multiple incoming flow files share the same signal identifier. |
| signal-counter-delta | A value, or the results of an Attribute Expression Language statement, which will be evaluated against a FlowFile in order to determine the signal counter delta. Specify how much the counter should increase. For example, if multiple signal events are processed at upstream flow in batch oriented way, the number of events processed can be notified with this property at once. Zero (0) has a special meaning, it clears target count back to 0, which is especially useful when used with Wait Releasable FlowFile Count = Zero (0) mode, to provide ‘open-close-gate’ type of flow control. One (1) can open a corresponding Wait processor, and Zero (0) can negate it as if closing a gate. |
| signal-counter-name | A value, or the results of an Attribute Expression Language statement, which will be evaluated against a FlowFile in order to determine the signal counter name. Signal counter name is useful when a corresponding Wait processor needs to know the number of occurrences of different types of events, such as success or failure, or destination data source names, etc. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | When the cache cannot be reached, or if the Release Signal Identifier evaluates to null or empty, FlowFiles will be routed to this relationship |
| success | All FlowFiles where the release signal has been successfully entered in the cache will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| notified | All FlowFiles will have an attribute ‘notified’. The value of this attribute is true, is the FlowFile is notified, otherwise false. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.Wait](/user-guide/data-integration/openflow/processors/wait)
