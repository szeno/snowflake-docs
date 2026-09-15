# Wait 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Routes incoming FlowFiles to the ‘wait’ relationship until a matching release signal is stored in the distributed cache from a corresponding Notify processor. When a matching release signal is identified, a waiting FlowFile is routed to the ‘success’ relationship. The release signal entry is then removed from the cache. The attributes of the FlowFile that produced the release signal are copied to the waiting FlowFile if the Attribute Cache Regex property of the corresponding Notify processor is set properly. If there are multiple release signals in the cache identified by the Release Signal Identifier, and the Notify processor is configured to copy the FlowFile attributes to the cache, then the FlowFile passing the Wait processor receives the union of the attributes of the FlowFiles that produced the release signals in the cache (identified by Release Signal Identifier). Waiting FlowFiles will be routed to ‘expired’ if they exceed the Expiration Duration. If you need to wait for more than one signal, specify the desired number of signals via the ‘Target Signal Count’ property. This is particularly useful with processors that split a source FlowFile into multiple fragments, such as SplitText. In order to wait for all fragments to be processed, connect the ‘original’ relationship to a Wait processor, and the ‘splits’ relationship to a corresponding Notify processor. Configure the Notify and Wait processors to use the ‘${fragment.identifier}’ as the value of ‘Release Signal Identifier’, and specify ‘${fragment.count}’ as the value of ‘Target Signal Count’ in the Wait processor. It is recommended to use a prioritizer (for instance First In First Out) when using the ‘wait’ relationship as a loop.

## Tags

cache, distributed, hold, map, release, signal, wait

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| attribute-copy-mode | Specifies how to handle attributes copied from FlowFiles entering the Notify processor |
| distributed-cache-service | The Controller Service that is used to check for release signals from a corresponding Notify processor |
| expiration-duration | Indicates the duration after which waiting FlowFiles will be routed to the ‘expired’ relationship |
| releasable-flowfile-count | A value, or the results of an Attribute Expression Language statement, which will be evaluated against a FlowFile in order to determine the releasable FlowFile count. This specifies how many FlowFiles can be released when a target count reaches target signal count. Zero (0) has a special meaning, any number of FlowFiles can be released as long as signal count matches target. |
| release-signal-id | A value that specifies the key to a specific release signal cache. To decide whether the FlowFile that is being processed by the Wait processor should be sent to the ‘success’ or the ‘wait’ relationship, the processor checks the signals in the cache specified by this key. |
| signal-counter-name | Within the cache (specified by the Release Signal Identifier) the signals may belong to different counters. If this property is specified, the processor checks the number of signals in the cache that belong to this particular counter. If not specified, the processor checks the total number of signals in the cache. |
| target-signal-count | The number of signals that need to be in the cache (specified by the Release Signal Identifier) in order for the FlowFile processed by the Wait processor to be sent to the ‘success’ relationship. If the number of signals in the cache has reached this number, the FlowFile is routed to the ‘success’ relationship and the number of signals in the cache is decreased by this value. If Signal Counter Name is specified, this processor checks a particular counter, otherwise checks against the total number of signals in the cache. |
| wait-buffer-count | Specify the maximum number of incoming FlowFiles that can be buffered to check whether it can move forward. The more buffer can provide the better performance, as it reduces the number of interactions with cache service by grouping FlowFiles by signal identifier. Only a signal identifier can be processed at a processor execution. |
| wait-mode | Specifies how to handle a FlowFile waiting for a notify signal |
| wait-penalty-duration | If configured, after a signal identifier got processed but did not meet the release criteria, the signal identifier is penalized and FlowFiles having the signal identifier will not be processed again for the specified period of time, so that the signal identifier will not block others to be processed. This can be useful for use cases where a Wait processor is expected to process multiple signal identifiers, and each signal identifier has multiple FlowFiles, and also the order of releasing FlowFiles is important within a signal identifier. The FlowFile order can be configured with Prioritizers. IMPORTANT: There is a limitation of number of queued signals can be processed, and Wait processor may not be able to check all queued signal ids. See additional details for the best practice. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| expired | A FlowFile that has exceeded the configured Expiration Duration will be routed to this relationship |
| failure | When the cache cannot be reached, or if the Release Signal Identifier evaluates to null or empty, FlowFiles will be routed to this relationship |
| success | A FlowFile with a matching release signal in the cache will be routed to this relationship |
| wait | A FlowFile with no matching release signal in the cache will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| wait.start.timestamp | All FlowFiles will have an attribute ‘wait.start.timestamp’, which sets the initial epoch timestamp when the file first entered this processor. This is used to determine the expiration time of the FlowFile. This attribute is not written when the FlowFile is transferred to failure, expired or success |
| wait.counter.<counterName> | The name of each counter for which at least one signal has been present in the cache since the last time the cache was empty gets copied to the current FlowFile as an attribute. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.Notify](/user-guide/data-integration/openflow/processors/notify)
