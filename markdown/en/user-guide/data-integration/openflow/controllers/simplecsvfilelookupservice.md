# SimpleCsvFileLookupService

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

A reloadable CSV file-based lookup service. The first line of the csv file is considered as header.

## Tags

cache, csv, enrich, join, key, lookup, reloadable, value

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| CSV Format \* | CSV Format | default | - Custom Format - RFC 4180 - Microsoft Excel - Tab-Delimited - MySQL Format - Informix Unload - Informix Unload Escape Disabled - Default Format - RFC4180 | Specifies which “format” the CSV data is in, or specifies if custom formatting should be used. |
| Character Set \* | Character Set | UTF-8 |  | The Character Encoding that is used to decode the CSV file. |
| Comment Marker | Comment Marker |  |  | The character that is used to denote the start of a comment. Any line that begins with this comment will be ignored. |
| Escape Character \* | Escape Character |  |  | The character that is used to escape characters that would otherwise have a specific meaning to the CSV Parser. If the property has been specified via Expression Language but the expression gets evaluated to an invalid Escape Character at runtime, then it will be skipped and the default Escape Character will be used. Setting it to an empty string means no escape character should be used. |
| Quote Character \* | Quote Character | “ |  | The character that is used to quote values so that escape characters do not have to be used. If the property has been specified via Expression Language but the expression gets evaluated to an invalid Quote Character at runtime, then it will be skipped and the default Quote Character will be used. |
| Quote Mode \* | Quote Mode | MINIMAL | - Quote All Values - Quote Minimal - Quote Non-Numeric Values - Do Not Quote Values | Specifies how fields should be quoted when they are written |
| Trim Fields \* | Trim Fields | true | - true - false | Whether or not white space should be removed from the beginning and end of fields |
| Value Separator \* | Value Separator | , |  | The character that is used to separate values/fields in a CSV Record. If the property has been specified via Expression Language but the expression gets evaluated to an invalid Value Separator at runtime, then it will be skipped and the default Value Separator will be used. |
| CSV File \* | csv-file |  |  | Path to a CSV File in which the key value pairs can be looked up. |
| Ignore Duplicates \* | ignore-duplicates | true | - true - false | Ignore duplicate keys for records in the CSV file. |
| Lookup Key Column \* | lookup-key-column |  |  | The field in the CSV file that will serve as the lookup key. This is the field that will be matched against the property specified in the lookup processor. |
| Lookup Value Column \* | lookup-value-column |  |  | Lookup value column. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

## Restrictions

| Required Permission | Explanation |
| --- | --- |
| read filesystem | Provides operator the ability to read from any file that NiFi has access to. |

Expand

Show lessSee more

## System Resource Considerations

This component does not specify system resource considerations.
