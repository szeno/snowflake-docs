# CSVReader

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Parses CSV-formatted data, returning each row in the CSV file as a separate record. This reader allows for inferring a schema based on the first line of the CSV, if a ‘header line’ is present, or providing an explicit schema for interpreting the values. See Controller Service’s Usage for further documentation.

## Tags

comma, csv, delimited, parse, reader, record, row, separated, values

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Allow Duplicate Header Names | Allow Duplicate Header Names | true | - true - false | Whether duplicate header names are allowed. Header names are case-sensitive, for example “name” and “Name” are treated as separate fields.Handling of duplicate header names is CSV Parser specific (where applicable):\* Apache Commons CSV - duplicate headers will result in column data “shifting” right with new fields created for “unknown\_field\_index\_X” where “X” is the CSV column index number\* Jackson CSV - duplicate headers will be de-duplicated with the field value being that of the right-most duplicate CSV column\* FastCSV - duplicate headers will be de-duplicated with the field value being that of the left-most duplicate CSV column |
| CSV Format \* | CSV Format | custom | - Custom Format - RFC 4180 - Microsoft Excel - Tab-Delimited - MySQL Format - Informix Unload - Informix Unload Escape Disabled | Specifies which “format” the CSV data is in, or specifies if custom formatting should be used. |
| Character Set \* | Character Set | UTF-8 |  | The Character Encoding that is used to encode/decode the CSV file |
| Comment Marker | Comment Marker |  |  | The character that is used to denote the start of a comment. Any line that begins with this comment will be ignored. |
| Date Format | Date Format |  |  | Specifies the format to use when reading/writing Date fields. If not specified, Date fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, MM/dd/yyyy for a two-digit month, followed by a two-digit day, followed by a four-digit year, all separated by ‘/’ characters, as in 01/01/2017). |
| Escape Character \* | Escape Character |  |  | The character that is used to escape characters that would otherwise have a specific meaning to the CSV Parser. If the property has been specified via Expression Language but the expression gets evaluated to an invalid Escape Character at runtime, then it will be skipped and the default Escape Character will be used. Setting it to an empty string means no escape character should be used. |
| Ignore CSV Header Column Names | Ignore CSV Header Column Names | false | - true - false | If the first line of a CSV is a header, and the configured schema does not match the fields named in the header line, this controls how the Reader will interpret the fields. If this property is true, then the field names mapped to each column are driven only by the configured schema and any fields not in the schema will be ignored. If this property is false, then the field names found in the CSV Header will be used as the names of the fields. |
| Null String | Null String |  |  | Specifies a String that, if present as a value in the CSV, should be considered a null field instead of using the literal value. |
| Quote Character \* | Quote Character | “ |  | The character that is used to quote values so that escape characters do not have to be used. If the property has been specified via Expression Language but the expression gets evaluated to an invalid Quote Character at runtime, then it will be skipped and the default Quote Character will be used. |
| Record Separator \* | Record Separator | n |  | Specifies the characters to use in order to separate CSV Records |
| Schema Access Strategy \* | Schema Access Strategy | infer-schema | - Use ‘Schema Name’ Property - Use ‘Schema Text’ Property - Schema Reference Reader - Use String Fields From Header - Infer Schema | Specifies how to obtain the schema that is to be used for interpreting the data. |
| Schema Branch | Schema Branch |  |  | Specifies the name of the branch to use when looking up the schema in the Schema Registry property. If the chosen Schema Registry does not support branching, this value will be ignored. |
| Schema Name | Schema Name | ${schema.name} |  | Specifies the name of the schema to lookup in the Schema Registry property |
| Schema Reference Reader \* | Schema Reference Reader |  |  | Service implementation responsible for reading FlowFile attributes or content to determine the Schema Reference Identifier |
| Schema Registry | Schema Registry |  |  | Specifies the Controller Service to use for the Schema Registry |
| Schema Text | Schema Text | ${avro.schema} |  | The text of an Avro-formatted Schema |
| Schema Version | Schema Version |  |  | Specifies the version of the schema to lookup in the Schema Registry. If not specified then the latest version of the schema will be retrieved. |
| Time Format | Time Format |  |  | Specifies the format to use when reading/writing Time fields. If not specified, Time fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, HH:mm:ss for a two-digit hour in 24-hour format, followed by a two-digit minute, followed by a two-digit second, all separated by ‘:’ characters, as in 18:04:15). |
| Timestamp Format | Timestamp Format |  |  | Specifies the format to use when reading/writing Timestamp fields. If not specified, Timestamp fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, MM/dd/yyyy HH:mm:ss for a two-digit month, followed by a two-digit day, followed by a four-digit year, all separated by ‘/’ characters; and then followed by a two-digit hour in 24-hour format, followed by a two-digit minute, followed by a two-digit second, all separated by ‘:’ characters, as in 01/01/2017 18:04:15). |
| Treat First Line as Header \* | Treat First Line as Header | false | - true - false | Specifies whether or not the first line of CSV should be considered a Header or should be considered a record. If the Schema Access Strategy indicates that the columns must be defined in the header, then this property will be ignored, since the header must always be present and won’t be processed as a Record. Otherwise, if ‘true’, then the first line of CSV data will not be processed as a record and if ‘false’,then the first line will be interpreted as a record. |
| Trim Fields \* | Trim Fields | true | - true - false | Whether or not white space should be removed from the beginning and end of fields |
| Trim double quote \* | Trim double quote | true | - true - false | Whether or not to trim starting and ending double quotes. For example: with trim string ‘”test”’ would be parsed to ‘test’, without trim would be parsed to ‘”test”’.If set to ‘false’ it means full compliance with RFC-4180. Default value is true, with trim. |
| Value Separator \* | Value Separator | , |  | The character that is used to separate values/fields in a CSV Record. If the property has been specified via Expression Language but the expression gets evaluated to an invalid Value Separator at runtime, then it will be skipped and the default Value Separator will be used. |
| CSV Parser \* | csv-reader-csv-parser | commons-csv | - Apache Commons CSV - Jackson CSV - FastCSV | Specifies which parser to use to read CSV records. NOTE: Different parsers may support different subsets of functionality and may also exhibit different levels of performance. |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
