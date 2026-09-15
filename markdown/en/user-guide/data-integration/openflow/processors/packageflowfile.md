# PackageFlowFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

This processor will package FlowFile attributes and content into an output FlowFile that can be exported from NiFi and imported back into NiFi, preserving the original attributes and content.

## Tags

attributes, flowfile, flowfile-stream, flowfile-stream-v3, package

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Maximum Batch Content Size | Maximum combined content size of FlowFiles to package into one output FlowFile. Note, that FlowFiles whose content exceeds this limit are packaged separately. |
| max-batch-size | Maximum number of FlowFiles to package into one output FlowFile. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| original | The FlowFiles that were used to create the package are sent to this relationship |
| success | The packaged FlowFile is sent to this relationship |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | The mime.type will be changed to application/flowfile-v3 |

Expand

Show lessSee more

## Use Cases Involving Other Components

| Send FlowFile content and attributes from one NiFi instance to another NiFi instance. |
| --- |
| Export FlowFile content and attributes from NiFi to external storage and reimport. |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.MergeContent](/user-guide/data-integration/openflow/processors/mergecontent)
- [org.apache.nifi.processors.standard.UnpackContent](/user-guide/data-integration/openflow/processors/unpackcontent)
