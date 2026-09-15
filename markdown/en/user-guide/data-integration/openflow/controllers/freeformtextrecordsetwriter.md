# FreeFormTextRecordSetWriter

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Writes the contents of a RecordSet as free-form text. The configured text is able to make use of the Expression Language to reference each of the fields that are available in a Record, as well as the attributes in the FlowFile and variables. If there is a name collision, the field name/value is used before attributes or variables. Each record in the RecordSet will be separated by a single newline character.

## Tags

el, expression, freeform, language, record, recordset, resultset, serialize, text, writer

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Character Set \* | Character Set | UTF-8 |  | The Character set to use when writing the data to the FlowFile |
| Text \* | Text |  |  | The text to use when writing the results. This property will evaluate the Expression Language using any of the fields available in a Record. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
