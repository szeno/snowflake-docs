# UpdateDatabaseTable 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

This processor uses a JDBC connection and incoming records to generate any database table changes needed to support the incoming records. It expects a ‘flat’ record layout, meaning none of the top-level record fields has nested fields that are intended to become columns themselves.

## Tags

alter, database, jdbc, metadata, table, update

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Column Name Translation Pattern | Column name will be normalized with this regular expression |
| Column Name Translation Strategy | The strategy used to normalize table column name. Column Name will be uppercased to do case-insensitive matching irrespective of strategy |
| Database Dialect Service | Database Dialect Service for generating statements specific to a particular service or vendor. |
| db-type | Database Type for generating statements specific to a particular service or vendor. The Generic Type supports most cases but selecting a specific type enables optimal processing or additional features. |
| record-reader | The service for reading incoming flow files. The reader is only used to determine the schema of the records, the actual records will not be processed. |
| updatedatabasetable-catalog-name | The name of the catalog that the statement should update. This may not apply for the database that you are updating. In this case, leave the field empty. Note that if the property is set and the database is case-sensitive, the catalog name must match the database’s catalog name exactly. |
| updatedatabasetable-create-table | Specifies how to process the target table when it does not exist (create it, fail, e.g.). |
| updatedatabasetable-dbcp-service | The Controller Service that is used to obtain connection(s) to the database |
| updatedatabasetable-primary-keys | A comma-separated list of record field names that uniquely identifies a row in the database. This property is only used if the specified table needs to be created, in which case the Primary Key Fields will be used to specify the primary keys of the newly-created table. IMPORTANT: Primary Key Fields must match the record field names exactly unless ‘Quote Column Identifiers’ is false and the database allows for case-insensitive column names. In practice it is best to specify Primary Key Fields that exactly match the record field names, and those will become the column names in the created table. |
| updatedatabasetable-query-timeout | Sets the number of seconds the driver will wait for a query to execute. A value of 0 means no timeout. NOTE: Non-zero values may not be supported by the driver. |
| updatedatabasetable-quoted-column-identifiers | Enabling this option will cause all column names to be quoted, allowing you to use reserved words as column names in your tables and/or forcing the record field names to match the column names exactly. |
| updatedatabasetable-quoted-table-identifiers | Enabling this option will cause the table name to be quoted to support the use of special characters in the table name and/or forcing the value of the Table Name property to match the target table name exactly. |
| updatedatabasetable-record-writer | Specifies the Controller Service to use for writing results to a FlowFile. The Record Writer should use Inherit Schema to emulate the inferred schema behavior, i.e. an explicit schema need not be defined in the writer, and will be supplied by the same logic used to infer the schema from the column types. If Create Table Strategy is set ‘Create If Not Exists’, the Record Writer ‘s output format must match the Record Reader’s format in order for the data to be placed in the created table location. Note that this property is only used if ‘Update Field Names’ is set to true and the field names do not all match the column names exactly. If no update is needed for any field names (or ‘Update Field Names’ is false), the Record Writer is not used and instead the input FlowFile is routed to success or failure without modification. |
| updatedatabasetable-schema-name | The name of the database schema that the table belongs to. This may not apply for the database that you are updating. In this case, leave the field empty. Note that if the property is set and the database is case-sensitive, the schema name must match the database’s schema name exactly. |
| updatedatabasetable-table-name | The name of the database table to update. If the table does not exist, then it will either be created or an error thrown, depending on the value of the Create Table property. |
| updatedatabasetable-translate-field-names | If true, the Processor will attempt to translate field names into the corresponding column names for the table specified, for the purposes of determining whether the field name exists as a column in the target table. NOTE: If the target table does not exist and is to be created, this property is ignored and the field names will be used as-is. If false, the field names must match the column names exactly, or the column may not be found and instead an error my be reported that the column already exists. |
| updatedatabasetable-update-field-names | This property indicates whether to update the output schema such that the field names are set to the exact column names from the specified table. This should be used if the incoming record field names may not match the table ‘s column names in terms of upper- and lower-case. For example, this property should be set to true if the output FlowFile is destined for Oracle e.g., which expects the field names to match the column names exactly. NOTE: The value of the’Translate Field Names’ property is ignored when updating field names; instead they are updated to match the column name as returned by the database. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | A FlowFile containing records routed to this relationship if the record could not be transmitted to the database. |
| success | A FlowFile containing records routed to this relationship after the record has been successfully transmitted to the database. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| output.table | This attribute is written on the flow files routed to the ‘success’ and ‘failure’ relationships, and contains the target table name. |
| output.path | This attribute is written on the flow files routed to the ‘success’ and ‘failure’ relationships, and contains the path on the file system to the table (or partition location if the table is partitioned). |
| mime.type | Sets the mime.type attribute to the MIME Type specified by the Record Writer, only if a Record Writer is specified and Update Field Names is ‘true’. |
| record.count | Sets the number of records in the FlowFile, only if a Record Writer is specified and Update Field Names is ‘true’. |

Expand

Show lessSee more
