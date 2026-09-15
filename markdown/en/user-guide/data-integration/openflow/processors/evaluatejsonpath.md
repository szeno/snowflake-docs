# EvaluateJsonPath 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Evaluates one or more JsonPath expressions against the content of a FlowFile. The results of those expressions are assigned to FlowFile Attributes or are written to the content of the FlowFile itself, depending on configuration of the Processor. JsonPaths are entered by adding user-defined properties; the name of the property maps to the Attribute Name into which the result will be placed (if the Destination is flowfile-attribute; otherwise, the property name is ignored). The value of the property must be a valid JsonPath expression. A Return Type of ‘auto-detect’ will make a determination based off the configured destination. When ‘Destination’ is set to ‘flowfile-attribute,’ a return type of ‘scalar’ will be used. When ‘Destination’ is set to ‘flowfile-content,’ a return type of ‘JSON’ will be used. If the JsonPath evaluates to a JSON array or JSON object and the Return Type is set to ‘scalar’ the FlowFile will be unmodified and will be routed to failure. A Return Type of JSON can return scalar values if the provided JsonPath evaluates to the specified value and will be routed as a match. If Destination is ‘flowfile-content’ and the JsonPath does not evaluate to a defined path, the FlowFile will be routed to ‘unmatched’ without having its contents modified. If Destination is ‘flowfile-attribute’ and the expression matches nothing, attributes will be created with empty strings as the value unless ‘Path Not Found Behaviour’ is set to ‘skip’, and the FlowFile will always be routed to ‘matched.’

## Tags

JSON, JsonPath, evaluate

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Destination | Indicates whether the results of the JsonPath evaluation are written to the FlowFile content or a FlowFile attribute; if using attribute, must specify the Attribute Name property. If set to flowfile-content, only one JsonPath may be specified, and the property name is ignored. |
| Max String Length | The maximum allowed length of a string value when parsing the JSON document |
| Null Value Representation | Indicates the desired representation of JSON Path expressions resulting in a null value. |
| Path Not Found Behavior | Indicates how to handle missing JSON path expressions when destination is set to ‘flowfile-attribute’. Selecting ‘warn’ will generate a warning when a JSON path expression is not found. Selecting ‘skip’ will omit attributes for any unmatched JSON path expressions. |
| Return Type | Indicates the desired return type of the JSON Path expressions. Selecting ‘auto-detect’ will set the return type to ‘json’ for a Destination of ‘flowfile-content’, and ‘scalar’ for a Destination of ‘flowfile-attribute’. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles are routed to this relationship when the JsonPath cannot be evaluated against the content of the FlowFile; for instance, if the FlowFile is not valid JSON |
| matched | FlowFiles are routed to this relationship when the JsonPath is successfully evaluated and the FlowFile is modified as a result |
| unmatched | FlowFiles are routed to this relationship when the JsonPath does not match the content of the FlowFile and the Destination is set to flowfile-content |

Expand

Show lessSee more
