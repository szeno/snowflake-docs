# DatabaseRecordSink

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Description

Provides a service to write records using a configured database connection.

## Tags

connection, database, db, jdbc, record

## Properties

In the list below required Properties are shown with an asterisk (\*).
Other properties are considered optional. The table also indicates any default values, and whether a property supports the NiFi Expression Language.

| Display Name | API Name | Default Value | Allowable Values | Description |
| --- | --- | --- | --- | --- |
| Catalog Name | db-record-sink-catalog-name |  |  | The name of the catalog that the statement should update. This may not apply for the database that you are updating. In this case, leave the field empty |
| Database Connection Pooling Service \* | db-record-sink-dcbp-service |  |  | The Controller Service that is used to obtain a connection to the database for sending records. |
| Max Wait Time \* | db-record-sink-query-timeout | 0 seconds |  | The maximum amount of time allowed for a running SQL statement , zero means there is no limit. Max time less than 1 second will be equal to zero. |
| Quote Column Identifiers | db-record-sink-quoted-identifiers | false | - true - false | Enabling this option will cause all column names to be quoted, allowing you to use reserved words as column names in your tables. |
| Quote Table Identifiers | db-record-sink-quoted-table-identifiers | false | - true - false | Enabling this option will cause the table name to be quoted to support the use of special characters in the table name. |
| Schema Name | db-record-sink-schema-name |  |  | The name of the schema that the table belongs to. This may not apply for the database that you are updating. In this case, leave the field empty |
| Table Name \* | db-record-sink-table-name |  |  | The name of the table that the statement should affect. |
| Translate Field Names | db-record-sink-translate-field-names | true | - true - false | If true, the Processor will attempt to translate field names into the appropriate column names for the table specified. If false, the field names must match the column names exactly, or the column will not be updated |
| Unmatched Column Behavior | db-record-sink-unmatched-column-behavior | Fail on Unmatched Columns | - Ignore Unmatched Columns - Warn on Unmatched Columns - Fail on Unmatched Columns | If an incoming record does not have a field mapping for all of the database table’s columns, this property specifies how to handle the situation |
| Unmatched Field Behavior | db-record-sink-unmatched-field-behavior | Ignore Unmatched Fields | - Ignore Unmatched Fields - Fail on Unmatched Fields | If an incoming record has a field that does not map to any of the database table’s columns, this property specifies how to handle the situation |

Expand

Show lessSee more

## State management

This component does not store state.

## Restricted

This component is not restricted.

## System Resource Considerations

This component does not specify system resource considerations.
