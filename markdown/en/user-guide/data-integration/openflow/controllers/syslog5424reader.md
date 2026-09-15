# Syslog5424Reader

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a mechanism for reading RFC 5424 compliant Syslog data, such as log files, and structuring the data so that it can be processed.

## Tags

logfiles, logs, parse, reader, record, syslog, syslog 5424, text

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
