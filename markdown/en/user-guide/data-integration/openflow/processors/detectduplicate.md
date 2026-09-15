# DetectDuplicate 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Caches a value, computed from FlowFile attributes, for each incoming FlowFile and determines if the cached value has already been seen. If so, routes the FlowFile to ‘duplicate’ with an attribute named ‘original.identifier’ that specifies the original FlowFile ‘s “description”, which is specified in the <FlowFile Description> property. If the FlowFile is not determined to be a duplicate, the Processor routes the FlowFile to’ non-duplicate’

## Tags

dedupe, dupe, duplicate, hash

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Age Off Duration | Time interval to age off cached FlowFiles |
| Cache Entry Identifier | A FlowFile attribute, or the results of an Attribute Expression Language statement, which will be evaluated against a FlowFile in order to determine the value used to identify duplicates; it is this value that is cached |
| Cache The Entry Identifier | When true this cause the processor to check for duplicates and cache the Entry Identifier. When false, the processor would only check for duplicates and not cache the Entry Identifier, requiring another processor to add identifiers to the distributed cache. |
| Distributed Cache Service | The Controller Service that is used to cache unique identifiers, used to determine duplicates |
| FlowFile Description | When a FlowFile is added to the cache, this value is stored along with it so that if a duplicate is found, this description of the original FlowFile will be added to the duplicate’s “original.flowfile.description” attribute |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| duplicate | If a FlowFile has been detected to be a duplicate, it will be routed to this relationship |
| failure | If unable to communicate with the cache, the FlowFile will be penalized and routed to this relationship |
| non-duplicate | If a FlowFile’s Cache Entry Identifier was not found in the cache, it will be routed to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| original.flowfile.description | All FlowFiles routed to the duplicate relationship will have an attribute added named original.flowfile.description. The value of this attribute is determined by the attributes of the original copy of the data and by the FlowFile Description property. |

Expand

Show lessSee more

## See also
