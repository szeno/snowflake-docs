# EnforceOrder 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Enforces expected ordering of FlowFiles that belong to the same data group within a single node. Although PriorityAttributePrioritizer can be used on a connection to ensure that flow files going through that connection are in priority order, depending on error-handling, branching, and other flow designs, it is possible for FlowFiles to get out-of-order. EnforceOrder can be used to enforce original ordering for those FlowFiles. [IMPORTANT] In order to take effect of EnforceOrder, FirstInFirstOutPrioritizer should be used at EVERY downstream relationship UNTIL the order of FlowFiles physically get FIXED by operation such as MergeContent or being stored to the final destination.

## Tags

order, sort

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| batch-count | The maximum number of FlowFiles that EnforceOrder can process at an execution. |
| group-id | EnforceOrder is capable of multiple ordering groups. ‘Group Identifier’ is used to determine which group a FlowFile belongs to. This property will be evaluated with each incoming FlowFile. If evaluated result is empty, the FlowFile will be routed to failure. |
| inactive-timeout | Indicates the duration after which state for an inactive group will be cleared from managed state. Group is determined as inactive if any new incoming FlowFile has not seen for a group for specified duration. Inactive Timeout must be longer than Wait Timeout. If a FlowFile arrives late after its group is already cleared, it will be treated as a brand new group, but will never match the order since expected preceding FlowFiles are already gone. The FlowFile will eventually timeout for waiting and routed to ‘overtook’. To avoid this, group states should be kept long enough, however, shorter duration would be helpful for reusing the same group identifier again. |
| initial-order | When the first FlowFile of a group arrives, initial target order will be computed and stored in the managed state. After that, target order will start being tracked by EnforceOrder and stored in the state management store. If Expression Language is used but evaluated result was not an integer, then the FlowFile will be routed to failure, and initial order will be left unknown until consecutive FlowFiles provide a valid initial order. |
| maximum-order | If specified, any FlowFiles that have larger order will be routed to failure. This property is computed only once for a given group. After a maximum order is computed, it will be persisted in the state management store and used for other FlowFiles belonging to the same group. If Expression Language is used but evaluated result was not an integer, then the FlowFile will be routed to failure, and maximum order will be left unknown until consecutive FlowFiles provide a valid maximum order. |
| order-attribute | A name of FlowFile attribute whose value will be used to enforce order of FlowFiles within a group. If a FlowFile does not have this attribute, or its value is not an integer, the FlowFile will be routed to failure. |
| wait-timeout | Indicates the duration after which waiting FlowFiles will be routed to the ‘overtook’ relationship. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| LOCAL | EnforceOrder uses following states per ordering group: ‘<groupId>.target’ is a order number which is being waited to arrive next. When a FlowFile with a matching order arrives, or a FlowFile overtakes the FlowFile being waited for because of wait timeout, target order will be updated to (FlowFile.order + 1). ‘<groupId>.max is the maximum order number for a group. ‘<groupId>.updatedAt’ is a timestamp when the order of a group was updated last time. These managed states will be removed automatically once a group is determined as inactive, see ‘Inactive Timeout’ for detail. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | A FlowFiles which does not have required attributes, or fails to compute those will be routed to this relationship |
| overtook | A FlowFile that waited for preceding FlowFiles longer than Wait Timeout and overtook those FlowFiles, will be routed to this relationship. |
| skipped | A FlowFile that has an order younger than current, which means arrived too late and skipped, will be routed to this relationship. |
| success | A FlowFile with a matching order number will be routed to this relationship. |
| wait | A FlowFile with non matching order will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| EnforceOrder.startedAt | All FlowFiles going through this processor will have this attribute. This value is used to determine wait timeout. |
| EnforceOrder.result | All FlowFiles going through this processor will have this attribute denoting which relationship it was routed to. |
| EnforceOrder.detail | FlowFiles routed to ‘failure’ or ‘skipped’ relationship will have this attribute describing details. |
| EnforceOrder.expectedOrder | FlowFiles routed to ‘wait’ or ‘skipped’ relationship will have this attribute denoting expected order when the FlowFile was processed. |

Expand

Show lessSee more
