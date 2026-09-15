# RouteOnContent 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Applies Regular Expressions to the content of a FlowFile and routes a copy of the FlowFile to each destination whose Regular Expression matches. Regular Expressions are added as User-Defined Properties where the name of the property is the name of the relationship and the value is a Regular Expression to match against the FlowFile content. User-Defined properties do support the Attribute Expression Language, but the results are interpreted as literal values, not Regular Expressions

## Tags

content, detect, filter, find, regex, regexp, regular expression, route, search, string, text

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Character Set | The Character Set in which the file is encoded |
| Content Buffer Size | Specifies the maximum amount of data to buffer in order to apply the regular expressions. If the size of the FlowFile exceeds this value, any amount of this value will be ignored |
| Match Requirement | Specifies whether the entire content of the file must match the regular expression exactly, or if any part of the file (up to Content Buffer Size) can contain the regular expression in order to be considered a match |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| unmatched | FlowFiles that do not match any of the user-supplied regular expressions will be routed to this relationship |

Expand

Show lessSee more
