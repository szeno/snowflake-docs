# GrokReader

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a mechanism for reading unstructured text data, such as log files, and structuring the data so that it can be processed. The service is configured using Grok patterns. The service reads from a stream of data and splits each message that it finds into a separate Record, each containing the fields that are configured. If a line in the input does not match the expected message pattern, the line of text is either considered to be part of the previous message or is skipped, depending on the configuration, with the exception of stack traces. A stack trace that is found at the end of a log message is considered to be part of the previous message but is added to the ‘stackTrace’ field of the Record. If a record has no stack trace, it will have a NULL value for the stackTrace field (assuming that the schema does in fact include a stackTrace field of type String). Assuming that the schema includes a ‘\_raw’ field of type String, the raw message will be included in the Record.

## Tags

grok, logfiles, logs, logstash, parse, pattern, reader, record, regex, text, unstructured

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Grok Expressions \* | Grok Expression |  |  | Specifies the format of a log line in Grok format. This allows the Record Reader to understand how to parse each log line. The property supports one or more Grok expressions. The Reader attempts to parse input lines according to the configured order of the expressions.If a line in the log file does not match any expressions, the line will be assumed to belong to the previous log message.If other Grok patterns are referenced by this expression, they need to be supplied in the Grok Pattern File property. |
| Grok Patterns | Grok Pattern File |  |  | Grok Patterns to use for parsing logs. If not specified, a built-in default Pattern file will be used. If specified, all patterns specified will override the default patterns. See the Controller Service’s Additional Details for a list of pre-defined patterns. |
| Schema Access Strategy \* | Schema Access Strategy | string-fields-from-grok-expression | - Use String Fields From Grok Expression - Use ‘Schema Name’ Property - Use ‘Schema Text’ Property - Schema Reference Reader | Specifies how to obtain the schema that is to be used for interpreting the data. |
| Schema Branch | Schema Branch |  |  | Specifies the name of the branch to use when looking up the schema in the Schema Registry property. If the chosen Schema Registry does not support branching, this value will be ignored. |
| Schema Name | Schema Name | ${schema.name} |  | Specifies the name of the schema to lookup in the Schema Registry property |
| Schema Reference Reader \* | Schema Reference Reader |  |  | Service implementation responsible for reading FlowFile attributes or content to determine the Schema Reference Identifier |
| Schema Registry | Schema Registry |  |  | Specifies the Controller Service to use for the Schema Registry |
| Schema Text | Schema Text | ${avro.schema} |  | The text of an Avro-formatted Schema |
| Schema Version | Schema Version |  |  | Specifies the version of the schema to lookup in the Schema Registry. If not specified then the latest version of the schema will be retrieved. |
| No Match Behavior \* | no-match-behavior | append-to-previous-message | - Append to Previous Message - Skip Line - Raw Line | If a line of text is encountered and it does not match the given Grok Expression, and it is not part of a stack trace, this property specifies how the text should be processed. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| reference remote resources | Patterns and Expressions can reference resources over HTTP |

Expand

Show lessSee more

## System Resource Considerations

This component does not specify system resource considerations.
