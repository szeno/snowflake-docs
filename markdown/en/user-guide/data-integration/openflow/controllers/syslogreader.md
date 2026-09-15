# SyslogReader

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Attempts to parses the contents of a Syslog message in accordance to RFC5424 and RFC3164. In the case of RFC5424 formatted messages, structured data is not supported, and will be returned as part of the message. Note: Be mindful that RFC3164 is informational and a wide range of different implementations are present in the wild.

## Tags

logfiles, logs, parse, reader, record, syslog, text

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Character Set \* | Character Set | UTF-8 |  | Specifies which character set of the Syslog messages |
| Raw message \* | syslog-5424-reader-raw-message | false | - true - false | If true, the record will have a \_raw field containing the raw message |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
