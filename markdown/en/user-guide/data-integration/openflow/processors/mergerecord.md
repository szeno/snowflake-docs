# MergeRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

This Processor merges together multiple record-oriented FlowFiles into a single FlowFile that contains all of the Records of the input FlowFiles. This Processor works by creating ‘bins’ and then adding FlowFiles to these bins until they are full. Once a bin is full, all of the FlowFiles will be combined into a single output FlowFile, and that FlowFile will be routed to the ‘merged’ Relationship. A bin will consist of potentially many ‘like FlowFiles’. In order for two FlowFiles to be considered ‘like FlowFiles’, they must have the same Schema (as identified by the Record Reader) and, if the <Correlation Attribute Name> property is set, the same value for the specified attribute. See Processor Usage and Additional Details for more information. NOTE: this processor should NOT be configured with Cron Driven for the Scheduling Strategy.

## Tags

content, correlation, event, merge, record, stream

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Attribute Strategy | Determines which FlowFile attributes should be added to the bundle. If ‘Keep All Unique Attributes’ is selected, any attribute on any FlowFile that gets bundled will be kept unless its value conflicts with the value from another FlowFile. If ‘Keep Only Common Attributes’ is selected, only the attributes that exist on all FlowFiles in the bundle, with the same value, will be preserved. |
| correlation-attribute-name | If specified, two FlowFiles will be binned together only if they have the same value for this Attribute. If not specified, FlowFiles are bundled by the order in which they are pulled from the queue. |
| max-bin-age | The maximum age of a Bin that will trigger a Bin to be complete. Expected format is <duration> <time unit> where <duration> is a positive integer and time unit is one of seconds, minutes, hours |
| max-bin-size | The maximum size for the bundle. If not specified, there is no maximum. This is a ‘soft limit’ in that if a FlowFile is added to a bin, all records in that FlowFile will be added, so this limit may be exceeded by up to the number of bytes in last input FlowFile. |
| max-records | The maximum number of Records to include in a bin. This is a ‘soft limit’ in that if a FlowFIle is added to a bin, all records in that FlowFile will be added, so this limit may be exceeded by up to the number of records in the last input FlowFile. |
| max.bin.count | Specifies the maximum number of bins that can be held in memory at any one time. This number should not be smaller than the maximum number of concurrent threads for this Processor, or the bins that are created will often consist only of a single incoming FlowFile. |
| merge-strategy | Specifies the algorithm used to merge records. The ‘Defragment’ algorithm combines fragments that are associated by attributes back into a single cohesive FlowFile. The ‘Bin-Packing Algorithm’ generates a FlowFile populated by arbitrarily chosen FlowFiles |
| min-bin-size | The minimum size of for the bin |
| min-records | The minimum number of records to include in a bin |
| record-reader | Specifies the Controller Service to use for reading incoming data |
| record-writer | Specifies the Controller Service to use for writing out the records |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If the bundle cannot be created, all FlowFiles that would have been used to created the bundle will be transferred to failure |
| merged | The FlowFile containing the merged records |
| original | The FlowFiles that were used to create the bundle |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| record.count | The merged FlowFile will have a ‘record.count’ attribute indicating the number of records that were written to the FlowFile. |
| mime.type | The MIME Type indicated by the Record Writer |
| merge.count | The number of FlowFiles that were merged into this bundle |
| merge.bin.age | The age of the bin, in milliseconds, when it was merged and output. Effectively this is the greatest amount of time that any FlowFile in this bundle remained waiting in this processor before it was output |
| merge.uuid | UUID of the merged FlowFile that will be added to the original FlowFiles attributes |
| merge.completion.reason | This processor allows for several thresholds to be configured for merging FlowFiles. This attribute indicates which of the Thresholds resulted in the FlowFiles being merged. For an explanation of each of the possible values and their meanings, see the Processor’s Usage / documentation and see the ‘Additional Details’ page. |
| <Attributes from Record Writer> | Any Attribute that the configured Record Writer returns will be added to the FlowFile. |

Expand

Show lessSee more

## Use cases

| Combine together many arbitrary Records in order to create a single, larger file |
| --- |

Expand

Show lessSee more

## Use Cases Involving Other Components

| Combine together many Records that have the same value for a particular field in the data, in order to create a single, larger file |
| --- |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.MergeContent](/user-guide/data-integration/openflow/processors/mergecontent)
- [org.apache.nifi.processors.standard.PartitionRecord](/user-guide/data-integration/openflow/processors/partitionrecord)
- [org.apache.nifi.processors.standard.SplitRecord](/user-guide/data-integration/openflow/processors/splitrecord)
