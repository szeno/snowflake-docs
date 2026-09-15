# GenerateFlowFile 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

This processor creates FlowFiles with random data or custom content. GenerateFlowFile is useful for load testing, configuration, and simulation. Also see DuplicateFlowFile for additional load testing.

## Tags

generate, load, random, test

## Input Requirement

FORBIDDEN

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Batch Size | The number of FlowFiles to be transferred in each invocation |
| Data Format | Specifies whether the data should be Text or Binary |
| File Size | The size of the file that will be used |
| Unique FlowFiles | If true, each FlowFile that is generated will be unique. If false, a random value will be generated and all FlowFiles will get the same content but this offers much higher throughput |
| character-set | Specifies the character set to use when writing the bytes of Custom Text to a flow file. |
| generate-ff-custom-text | If Data Format is text and if Unique FlowFiles is false, then this custom text will be used as content of the generated FlowFiles and the File Size will be ignored. Finally, if Expression Language is used, evaluation will be performed only once per batch of generated FlowFiles |
| mime-type | Specifies the value to set for the “mime.type” attribute. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success |  |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| mime.type | Sets the MIME type of the output if the ‘Mime Type’ property is set |

Expand

Show lessSee more
