# MergeContent 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Merges a Group of FlowFiles together based on a user-defined strategy and packages them into a single FlowFile. It is recommended that the Processor be configured with only a single incoming connection, as Group of FlowFiles will not be created from FlowFiles in different connections. This processor updates the mime.type attribute as appropriate. NOTE: this processor should NOT be configured with Cron Driven for the Scheduling Strategy.

## Tags

archive, concatenation, content, correlation, flowfile-stream, flowfile-stream-v3, merge, stream, tar, zip

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Attribute Strategy | Determines which FlowFile attributes should be added to the bundle. If ‘Keep All Unique Attributes’ is selected, any attribute on any FlowFile that gets bundled will be kept unless its value conflicts with the value from another FlowFile. If ‘Keep Only Common Attributes’ is selected, only the attributes that exist on all FlowFiles in the bundle, with the same value, will be preserved. |
| Bin Termination Check | Specifies an Expression Language Expression that is to be evaluated against each FlowFile. If the result of the expression is ‘true’, the bin that the FlowFile corresponds to will be terminated, even if the bin has not met the minimum number of entries or minimum size. Note that if the FlowFile that triggers the termination of the bin is itself larger than the Maximum Bin Size, it will be placed into its own bin without triggering the termination of any other bin. When using this property, it is recommended to use Prioritizers in the flow’s connections to ensure that the ordering is as desired. |
| Compression Level | Specifies the compression level to use when using the Zip Merge Format; if not using the Zip Merge Format, this value is ignored |
| Correlation Attribute Name | If specified, like FlowFiles will be binned together, where ‘like FlowFiles’ means FlowFiles that have the same value for this Attribute. If not specified, FlowFiles are bundled by the order in which they are pulled from the queue. |
| Delimiter Strategy | Determines if Header, Footer, and Demarcator should point to files containing the respective content, or if the values of the properties should be used as the content. |
| Demarcator File | Filename or text specifying the demarcator to use. If not specified, no demarcator is supplied. |
| FlowFile Insertion Strategy | If a given FlowFile terminates the bin based on the <Bin Termination Check> property, specifies where the FlowFile should be included in the bin. |
| Footer File | Filename or text specifying the footer to use. If not specified, no footer is supplied. |
| Header File | Filename or text specifying the header to use. If not specified, no header is supplied. |
| Keep Path | If using the Zip or Tar Merge Format, specifies whether or not the FlowFiles’ paths should be included in their entry names. |
| Max Bin Age | The maximum age of a Bin that will trigger a Bin to be complete. Expected format is <duration> <time unit> where <duration> is a positive integer and time unit is one of seconds, minutes, hours |
| Maximum Group Size | The maximum size for the bundle. If not specified, there is no maximum. |
| Maximum Number of Entries | The maximum number of files to include in a bundle |
| Maximum number of Bins | Specifies the maximum number of bins that can be held in memory at any one time |
| Merge Format | Determines the format that will be used to merge the content. |
| Merge Strategy | Specifies the algorithm used to merge content. The ‘Defragment’ algorithm combines fragments that are associated by attributes back into a single cohesive FlowFile. The ‘Bin-Packing Algorithm’ generates a FlowFile populated by arbitrarily chosen FlowFiles |
| Minimum Group Size | The minimum size for the bundle |
| Minimum Number of Entries | The minimum number of files to include in a bundle |
| Tar Modified Time | If using the Tar Merge Format, specifies if the Tar entry should store the modified timestamp either by expression (e.g. ${file.lastModifiedTime} or static value, both of which must match the ISO8601 format ‘yyyy-MM-dd’T ‘HH:mm:ssZ’. |
| mergecontent-metadata-strategy | For FlowFiles whose input format supports metadata (Avro, e.g.), this property determines which metadata should be added to the bundle. If ‘Use First Metadata’ is selected, the metadata keys/values from the first FlowFile to be bundled will be used. If ‘Keep Only Common Metadata’ is selected, only the metadata that exists on all FlowFiles in the bundle, with the same value, will be preserved. If ‘Ignore Metadata’ is selected, no metadata is transferred to the outgoing bundled FlowFile. If ‘Do Not Merge Uncommon Metadata’ is selected, any FlowFile whose metadata values do not match those of the first bundled FlowFile will not be merged. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If the bundle cannot be created, all FlowFiles that would have been used to created the bundle will be transferred to failure |
| merged | The FlowFile containing the merged content |
| original | The FlowFiles that were used to create the bundle |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| filename | When more than 1 file is merged, the filename comes from the segment.original.filename attribute. If that attribute does not exist in the source FlowFiles, then the filename is set to the number of nanoseconds matching system time. Then a filename extension may be applied:if Merge Format is TAR, then the filename will be appended with .tar, if Merge Format is ZIP, then the filename will be appended with .zip, if Merge Format is FlowFileStream, then the filename will be appended with .pkg |
| merge.count | The number of FlowFiles that were merged into this bundle |
| merge.bin.age | The age of the bin, in milliseconds, when it was merged and output. Effectively this is the greatest amount of time that any FlowFile in this bundle remained waiting in this processor before it was output |
| merge.uuid | UUID of the merged flow file that will be added to the original flow files attributes. |
| merge.reason | This processor allows for several thresholds to be configured for merging FlowFiles. This attribute indicates which of the Thresholds resulted in the FlowFiles being merged. For an explanation of each of the possible values and their meanings, see the Processor’s Usage / documentation and see the ‘Additional Details’ page. |

Expand

Show lessSee more

## Use cases

| Concatenate FlowFiles with textual content together in order to create fewer, larger FlowFiles. |
| --- |
| Concatenate FlowFiles with binary content together in order to create fewer, larger FlowFiles. |
| Reassemble a FlowFile that was previously split apart into smaller FlowFiles by a processor such as SplitText, UnpackContext, SplitRecord, etc. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.MergeRecord](/user-guide/data-integration/openflow/processors/mergerecord)
- [org.apache.nifi.processors.standard.SegmentContent](/user-guide/data-integration/openflow/processors/segmentcontent)
