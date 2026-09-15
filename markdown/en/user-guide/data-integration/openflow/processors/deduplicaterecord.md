# DeduplicateRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

This processor de-duplicates individual records within a record set. It can operate on a per-file basis using an in-memory hashset or bloom filter. When configured with a distributed map cache, it de-duplicates records across multiple files.

## Tags

change, dedupe, distinct, dupe, duplicate, filter, hash, modify, record, replace, text, unique, update

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| bloom-filter-certainty | The desired false positive probability when using the BloomFilter type. Using a value of .05 for example, guarantees a five-percent probability that the result is a false positive. The closer to 1 this value is set, the more precise the result at the expense of more storage space utilization. |
| cache-identifier | An optional expression language field that overrides the record’s computed cache key. This field has an additional attribute available: ${record.hash.value}, which contains the cache key derived from dynamic properties (if set) or record fields. |
| deduplication-strategy | The strategy to use for detecting and routing duplicate records. The option for detecting duplicates across a single FlowFile operates in-memory, whereas detection spanning multiple FlowFiles utilises a distributed map cache. |
| distributed-map-cache | This property is required when the deduplication strategy is set to ‘multiple files.’ The map cache will for each record, atomically check whether the cache key exists and if not, set it. |
| filter-capacity-hint | An estimation of the total number of unique records to be processed. The more accurate this number is will lead to fewer false negatives on a BloomFilter. |
| filter-type | The filter used to determine whether a record has been seen before based on the matching RecordPath criteria. If hash set is selected, a Java HashSet object will be used to deduplicate all encountered records. If the bloom filter option is selected, a bloom filter will be used. The bloom filter option is less memory intensive, but has a chance of having false positives. |
| include-zero-record-flowfiles | If a FlowFile sent to either the duplicate or non-duplicate relationships contains no records, a value of *false* in this property causes the FlowFile to be dropped. Otherwise, the empty FlowFile is emitted. |
| put-cache-identifier | For each record, check whether the cache identifier exists in the distributed map cache. If it doesn’t exist and this property is true, put the identifier to the cache. |
| record-hashing-algorithm | The algorithm used to hash the cache key. |
| record-reader | Specifies the Controller Service to use for reading incoming data |
| record-writer | Specifies the Controller Service to use for writing out the records |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| duplicate | Records detected as duplicates are routed to this relationship. |
| failure | If unable to communicate with the cache, the FlowFile will be penalized and routed to this relationship |
| non-duplicate | Records not found in the cache are routed to this relationship. |
| original | The original input FlowFile is sent to this relationship unless a fatal error occurs. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| record.count | Number of records written to the destination FlowFile. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.DetectDuplicate](/user-guide/data-integration/openflow/processors/detectduplicate)
