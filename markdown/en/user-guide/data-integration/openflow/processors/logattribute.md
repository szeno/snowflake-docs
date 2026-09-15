# LogAttribute 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Emits attributes of the FlowFile at the specified log level

## Tags

attributes, logging

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Attributes to Ignore | A comma-separated list of Attributes to ignore. If not specified, no attributes will be ignored unless *Attributes to Ignore by Regular Expression* is modified. There’s an OR relationship between the two properties. |
| Attributes to Log | A comma-separated list of Attributes to Log. If not specified, all attributes will be logged unless *Attributes to Log by Regular Expression* is modified. There’s an AND relationship between the two properties. |
| Log FlowFile Properties | Specifies whether or not to log FlowFile “properties”, such as Entry Date, Lineage Start Date, and content size |
| Log Level | The Log Level to use when logging the Attributes |
| Log Payload | If true, the FlowFile’s payload will be logged, in addition to its attributes; otherwise, just the Attributes will be logged. |
| Log prefix | Log prefix appended to the log lines. It helps to distinguish the output of multiple LogAttribute processors. |
| Output Format | Specifies the format to use for logging FlowFile attributes |
| attributes-to-ignore-regex | A regular expression indicating the Attributes to Ignore. If not specified, no attributes will be ignored unless *Attributes to Ignore* is modified. There’s an OR relationship between the two properties. |
| attributes-to-log-regex | A regular expression indicating the Attributes to Log. If not specified, all attributes will be logged unless *Attributes to Log* is modified. There’s an AND relationship between the two properties. |
| character-set | The name of the CharacterSet to use |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| success | All FlowFiles are routed to this relationship |

Expand

Show lessSee more
