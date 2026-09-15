# SplitText 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Splits a text file into multiple smaller text files on line boundaries limited by maximum number of lines or total size of fragment. Each output split file will contain no more than the configured number of lines or bytes. If both Line Split Count and Maximum Fragment Size are specified, the split occurs at whichever limit is reached first. If the first line of a fragment exceeds the Maximum Fragment Size, that line will be output in a single split file which exceeds the configured maximum size limit. This component also allows one to specify that each split should include a header lines. Header lines can be computed by either specifying the amount of lines that should constitute a header or by using header marker to match against the read lines. If such match happens then the corresponding line will be treated as header. Keep in mind that upon the first failure of header marker match, no more matches will be performed and the rest of the data will be parsed as regular lines for a given split. If after computation of the header there are no more data, the resulting split will consists of only header lines.

## Tags

split, text

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Header Line Count | The number of lines that should be considered part of the header; the header lines will be duplicated to all split files |
| Header Line Marker Characters | The first character(s) on the line of the datafile which signifies a header line. This value is ignored when Header Line Count is non-zero. The first line not containing the Header Line Marker Characters and all subsequent lines are considered non-header |
| Line Split Count | The number of lines that will be added to each split file, excluding header lines. A value of zero requires Maximum Fragment Size to be set, and line count will not be considered in determining splits. |
| Maximum Fragment Size | The maximum size of each split file, including header lines. NOTE: in the case where a single line exceeds this property (including headers, if applicable), that line will be output in a split of its own which exceeds this Maximum Fragment Size setting. |
| Remove Trailing Newlines | Whether to remove newlines at the end of each split file. This should be false if you intend to merge the split files later. If this is set to ‘true’ and a FlowFile is generated that contains only ‘empty lines’ (i.e., consists only of r and n characters), the FlowFile will not be emitted. Note, however, that if header lines are specified, the resultant FlowFile will never be empty as it will consist of the header lines, so a FlowFile may be emitted that contains only the header lines. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If a file cannot be split for some reason, the original file will be routed to this destination and nothing will be routed elsewhere |
| original | The original input file will be routed to this destination when it has been successfully split into 1 or more files |
| splits | The split files will be routed to this destination when an input file is successfully split into 1 or more split files |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| text.line.count | The number of lines of text from the original FlowFile that were copied to this FlowFile |
| fragment.size | The number of bytes from the original FlowFile that were copied to this FlowFile, including header, if applicable, which is duplicated in each split FlowFile |
| fragment.identifier | All split FlowFiles produced from the same parent FlowFile will have the same randomly generated UUID added for this attribute |
| fragment.index | A one-up number that indicates the ordering of the split FlowFiles that were created from a single parent FlowFile |
| fragment.count | The number of split FlowFiles generated from the parent FlowFile |
| segment.original.filename | The filename of the parent FlowFile |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.MergeContent](/user-guide/data-integration/openflow/processors/mergecontent)
