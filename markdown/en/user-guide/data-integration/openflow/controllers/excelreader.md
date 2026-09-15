# ExcelReader

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Parses a Microsoft Excel document returning each row in each sheet as a separate record. This reader allows for inferring a schema from all the required sheets or providing an explicit schema for interpreting the values. See Controller Service ‘s Usage for further documentation. This reader is capable of processing both password and non password protected .xlsx (XSSF 2007 OOXML file format) and older .xls (HSSF’97(-2007) file format) Excel documents.

## Tags

cell, excel, parse, reader, record, row, spreadsheet, values, xls, xlsx

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Date Format | Date Format |  |  | Specifies the format to use when reading/writing Date fields. If not specified, Date fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, MM/dd/yyyy for a two-digit month, followed by a two-digit day, followed by a four-digit year, all separated by ‘/’ characters, as in 01/01/2017). |
| Input File Type \* | Input File Type | XLSX | - XLS - XLSX | Specifies type of Excel input file. |
| Password \* | Password |  |  | The password for a password protected Excel spreadsheet |
| Protection Type \* | Protection Type | UNPROTECTED | - Unprotected - Password Protected | Specifies whether an Excel spreadsheet is protected by a password or not. |
| Required Sheets | Required Sheets |  |  | Comma-separated list of Excel document sheet names whose rows should be extracted from the excel document. If this property is left blank then all the rows from all the sheets will be extracted from the Excel document. The list of names is case sensitive. Any sheets not specified in this value will be ignored. An exception will be thrown if a specified sheet(s) are not found. |
| Row Evaluation Strategy \* | Row Evaluation Strategy | STANDARD | - Standard - All Rows | A strategy to select how many rows after the starting row to use for determining the schema. |
| Schema Access Strategy \* | Schema Access Strategy | Use Starting Row | - Use ‘Schema Name’ Property - Use ‘Schema Text’ Property - Schema Reference Reader - Use Starting Row - Infer Schema | Specifies how to obtain the schema that is to be used for interpreting the data. |
| Schema Branch | Schema Branch |  |  | Specifies the name of the branch to use when looking up the schema in the Schema Registry property. If the chosen Schema Registry does not support branching, this value will be ignored. |
| Schema Name | Schema Name | ${schema.name} |  | Specifies the name of the schema to lookup in the Schema Registry property |
| Schema Reference Reader \* | Schema Reference Reader |  |  | Service implementation responsible for reading FlowFile attributes or content to determine the Schema Reference Identifier |
| Schema Registry | Schema Registry |  |  | Specifies the Controller Service to use for the Schema Registry |
| Schema Text | Schema Text | ${avro.schema} |  | The text of an Avro-formatted Schema |
| Schema Version | Schema Version |  |  | Specifies the version of the schema to lookup in the Schema Registry. If not specified then the latest version of the schema will be retrieved. |
| Starting Row \* | Starting Row | 1 |  | The row number of the first row to start processing (One based). Use this to skip over rows of data at the top of a worksheet that are not part of the dataset. When using the ‘Use Starting Row’ strategy this should be the column header row. |
| Time Format | Time Format |  |  | Specifies the format to use when reading/writing Time fields. If not specified, Time fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, HH:mm:ss for a two-digit hour in 24-hour format, followed by a two-digit minute, followed by a two-digit second, all separated by ‘:’ characters, as in 18:04:15). |
| Timestamp Format | Timestamp Format |  |  | Specifies the format to use when reading/writing Timestamp fields. If not specified, Timestamp fields will be assumed to be number of milliseconds since epoch (Midnight, Jan 1, 1970 GMT). If specified, the value must match the Java java.time.format.DateTimeFormatter format (for example, MM/dd/yyyy HH:mm:ss for a two-digit month, followed by a two-digit day, followed by a four-digit year, all separated by ‘/’ characters; and then followed by a two-digit hour in 24-hour format, followed by a two-digit minute, followed by a two-digit second, all separated by ‘:’ characters, as in 01/01/2017 18:04:15). |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
