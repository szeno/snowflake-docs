# ExtractGrok 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Evaluates one or more Grok Expressions against the content of a FlowFile, adding the results as attributes or replacing the content of the FlowFile with a JSON notation of the matched content

## Tags

delimit, extract, grok, log, parse, text

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Character Set | The Character Set in which the file is encoded |
| Destination | Control if Grok output value is written as a new flowfile attributes, in this case each of the Grok identifier that is matched in the flowfile will be added as an attribute, prefixed with “grok.” or written in the flowfile content. Writing to flowfile content will overwrite any existing flowfile content. |
| Grok Expression | Grok expression. If other Grok expressions are referenced in this expression, they must be provided in the Grok Pattern File if set or exist in the default Grok patterns |
| Grok Pattern file | Custom Grok pattern definitions. These definitions will be loaded after the default Grok patterns. The Grok Parser will use the default Grok patterns when this property is not configured. |
| Keep Empty Captures | If true, then empty capture values will be included in the returned capture map. |
| Maximum Buffer Size | Specifies the maximum amount of data to buffer (per file) in order to apply the Grok expressions. Files larger than the specified maximum will not be fully evaluated. |
| Named captures only | Only store named captures from grok |

Expand

Show lessSee more

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| reference remote resources | Patterns can reference resources over HTTP |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| matched | FlowFiles are routed to this relationship when the Grok Expression is successfully evaluated and the FlowFile is modified as a result |
| unmatched | FlowFiles are routed to this relationship when no provided Grok Expression matches the content of the FlowFile |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| grok.XXX | When operating in flowfile-attribute mode, each of the Grok identifier that is matched in the flowfile will be added as an attribute, prefixed with “grok.” For example,if the grok identifier “timestamp” is matched, then the value will be added to an attribute named “grok.timestamp” |

Expand

Show lessSee more
