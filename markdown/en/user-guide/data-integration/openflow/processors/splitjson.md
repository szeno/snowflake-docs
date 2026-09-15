# SplitJson 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Splits a JSON File into multiple, separate FlowFiles for an array element specified by a JsonPath expression. Each generated FlowFile is comprised of an element of the specified array and transferred to relationship ‘split,’ with the original file transferred to the ‘original’ relationship. If the specified JsonPath is not found or does not evaluate to an array element, the original file is routed to ‘failure’ and no files are generated.

## Tags

json, jsonpath, split

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| JsonPath Expression | A JsonPath expression that indicates the array element to split into JSON/scalar fragments. |
| Max String Length | The maximum allowed length of a string value when parsing the JSON document |
| Null Value Representation | Indicates the desired representation of JSON Path expressions resulting in a null value. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | If a FlowFile fails processing for any reason (for example, the FlowFile is not valid JSON or the specified path does not exist), it will be routed to this relationship |
| original | The original FlowFile that was split into segments. If the FlowFile fails processing, nothing will be sent to this relationship |
| split | All segments of the original FlowFile will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| fragment.identifier | All split FlowFiles produced from the same parent FlowFile will have the same randomly generated UUID added for this attribute |
| fragment.index | A one-up number that indicates the ordering of the split FlowFiles that were created from a single parent FlowFile |
| fragment.count | The number of split FlowFiles generated from the parent FlowFile |
| segment.original.filename | The filename of the parent FlowFile |

Expand

Show lessSee more
