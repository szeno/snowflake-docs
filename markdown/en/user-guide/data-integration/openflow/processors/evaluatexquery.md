# EvaluateXQuery 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Evaluates one or more XQueries against the content of a FlowFile. The results of those XQueries are assigned to FlowFile Attributes or are written to the content of the FlowFile itself, depending on configuration of the Processor. XQueries are entered by adding user-defined properties; the name of the property maps to the Attribute Name into which the result will be placed (if the Destination is ‘flowfile-attribute’; otherwise, the property name is ignored). The value of the property must be a valid XQuery. If the XQuery returns more than one result, new attributes or FlowFiles (for Destinations of ‘flowfile-attribute’ or ‘flowfile-content’ respectively) will be created for each result (attributes will have a ‘.n’ one-up number appended to the specified attribute name). If any provided XQuery returns a result, the FlowFile(s) will be routed to ‘matched’. If no provided XQuery returns a result, the FlowFile will be routed to ‘unmatched’. If the Destination is ‘flowfile-attribute’ and the XQueries matche nothing, no attributes will be applied to the FlowFile.

## Tags

XML, XPath, XQuery, evaluate

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Destination | Indicates whether the results of the XQuery evaluation are written to the FlowFile content or a FlowFile attribute. If set to <flowfile-content>, only one XQuery may be specified and the property name is ignored. If set to <flowfile-attribute> and the XQuery returns more than one result, multiple attributes will be added to theFlowFile, each named with a ‘.n’ one-up number appended to the specified attribute name |
| Output: Indent | Specifies whether the processor may add additional whitespace when outputting a result tree. |
| Output: Method | Identifies the overall method that should be used for outputting a result tree. |
| Output: Omit XML Declaration | Specifies whether the processor should output an XML declaration when transforming a result tree. |
| Validate DTD | Allow embedded Document Type Declaration in XML. This feature should be disabled to avoid XML entity expansion vulnerabilities. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles are routed to this relationship when the XQuery cannot be evaluated against the content of the FlowFile. |
| matched | FlowFiles are routed to this relationship when the XQuery is successfully evaluated and the FlowFile is modified as a result |
| unmatched | FlowFiles are routed to this relationship when the XQuery does not match the content of the FlowFile and the Destination is set to flowfile-content |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| user-defined | This processor adds user-defined attributes if the <Destination> property is set to flowfile-attribute . |

Expand

Show lessSee more
