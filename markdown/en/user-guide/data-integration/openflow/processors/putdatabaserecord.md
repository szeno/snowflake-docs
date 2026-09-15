# PutDatabaseRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

The PutDatabaseRecord processor uses a specified RecordReader to input (possibly multiple) records from an incoming flow file. These records are translated to SQL statements and executed as a single transaction. If any errors occur, the flow file is routed to failure or retry, and if the records are transmitted successfully, the incoming flow file is routed to success. The type of statement executed by the processor is specified via the Statement Type property, which accepts some hard-coded values such as INSERT, UPDATE, and DELETE, as well as ‘Use statement.type Attribute’, which causes the processor to get the statement type from a flow file attribute. IMPORTANT: If the Statement Type is UPDATE, then the incoming records must not alter the value(s) of the primary keys (or user-specified Update Keys). If such records are encountered, the UPDATE statement issued to the database may do nothing (if no existing records with the new primary key values are found), or could inadvertently corrupt the existing data (by changing records for which the new values of the primary keys exist).

## Tags

database, delete, insert, jdbc, put, record, sql, update

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Column Name Translation Pattern | Column name will be normalized with this regular expression |
| Column Name Translation Strategy | The strategy used to normalize table column name. Column Name will be uppercased to do case-insensitive matching irrespective of strategy |
| Data Record Path | If specified, this property denotes a RecordPath that will be evaluated against each incoming Record and the Record that results from evaluating the RecordPath will be sent to the database instead of sending the entire incoming Record. If not specified, the entire incoming Record will be published to the database. |
| Database Dialect Service | Database Dialect Service for generating statements specific to a particular service or vendor. |
| Delete Keys | A comma-separated list of column names that uniquely identifies a row in the database for DELETE statements. If the Statement Type is DELETE and this property is not set, the table’s columns are used. This property is ignored if the Statement Type is not DELETE |
| Rollback On Failure | Specify how to handle error. By default (false), if an error occurs while processing a FlowFile, the FlowFile will be routed to ‘failure’ or ‘retry’ relationship based on error type, and processor can continue with next FlowFile. Instead, you may want to rollback currently processed FlowFiles and stop further processing immediately. In that case, you can do so by enabling this ‘Rollback On Failure’ property. If enabled, failed FlowFiles will stay in the input relationship without penalizing it and being processed repeatedly until it gets processed successfully or removed by other means. It is important to set adequate ‘Yield Duration’ to avoid retrying too frequently. |
| Statement Type Record Path | Specifies a RecordPath to evaluate against each Record in order to determine the Statement Type. The RecordPath should equate to either INSERT, UPDATE, UPSERT, or DELETE. (Debezium style operation types are also supported: “r” and “c” for INSERT, “u” for UPDATE, and “d” for DELETE) |
| database-session-autocommit | The autocommit mode to set on the database connection being used. If set to false, the operation(s) will be explicitly committed or rolled back (based on success or failure respectively). If set to true, the driver/database automatically handles the commit/rollback. |
| db-type | Database Type for generating statements specific to a particular service or vendor. The Generic Type supports most cases but selecting a specific type enables optimal processing or additional features. |
| put-db-record-allow-multiple-statements | If the Statement Type is ‘SQL’ (as set in the statement.type attribute), this field indicates whether to split the field value by a semicolon and execute each statement separately. If any statement causes an error, the entire set of statements will be rolled back. If the Statement Type is not ‘SQL’, this field is ignored. |
| put-db-record-binary-format | The format to be applied when decoding string values to binary. |
| put-db-record-catalog-name | The name of the database (or the name of the catalog, depending on the destination system) that the statement should update. This may not apply for the database that you are updating. In this case, leave the field empty. Note that if the property is set and the database is case-sensitive, the catalog name must match the database’s catalog name exactly. |
| put-db-record-dcbp-service | The Controller Service that is used to obtain a connection to the database for sending records. |
| put-db-record-field-containing-sql | If the Statement Type is ‘SQL’ (as set in the statement.type attribute), this field indicates which field in the record(s) contains the SQL statement to execute. The value of the field must be a single SQL statement. If the Statement Type is not ‘SQL’, this field is ignored. |
| put-db-record-max-batch-size | Specifies maximum number of sql statements to be included in each batch sent to the database. Zero means the batch size is not limited, and all statements are put into a single batch which can cause high memory usage issues for a very large number of statements. |
| put-db-record-query-timeout | The maximum amount of time allowed for a running SQL statement , zero means there is no limit. Max time less than 1 second will be equal to zero. |
| put-db-record-quoted-identifiers | Enabling this option will cause all column names to be quoted, allowing you to use reserved words as column names in your tables. |
| put-db-record-quoted-table-identifiers | Enabling this option will cause the table name to be quoted to support the use of special characters in the table name. |
| put-db-record-record-reader | Specifies the Controller Service to use for parsing incoming data and determining the data’s schema. |
| put-db-record-schema-name | The name of the schema that the table belongs to. This may not apply for the database that you are updating. In this case, leave the field empty. Note that if the property is set and the database is case-sensitive, the schema name must match the database’s schema name exactly. |
| put-db-record-statement-type | Specifies the type of SQL Statement to generate. Please refer to the database documentation for a description of the behavior of each operation. Please note that some Database Types may not support certain Statement Types. If ‘Use statement.type Attribute’ is chosen, then the value is taken from the statement.type attribute in the FlowFile. The ‘Use statement.type Attribute’ option is the only one that allows the ‘SQL’statement type. If ‘SQL’ is specified, the value of the field specified by the ‘Field Containing SQL’ property is expected to be a valid SQL statement on the target database, and will be executed as-is. |
| put-db-record-table-name | The name of the table that the statement should affect. Note that if the database is case-sensitive, the table name must match the database’s table name exactly. |
| put-db-record-translate-field-names | If true, the Processor will attempt to translate field names into the appropriate column names for the table specified. If false, the field names must match the column names exactly, or the column will not be updated |
| put-db-record-unmatched-column-behavior | If an incoming record does not have a field mapping for all of the database table’s columns, this property specifies how to handle the situation |
| put-db-record-unmatched-field-behavior | If an incoming record has a field that does not map to any of the database table’s columns, this property specifies how to handle the situation |
| put-db-record-update-keys | A comma-separated list of column names that uniquely identifies a row in the database for UPDATE statements. If the Statement Type is UPDATE and this property is not set, the table’s Primary Keys are used. In this case, if no Primary Key exists, the conversion to SQL will fail if Unmatched Column Behaviour is set to FAIL. This property is ignored if the Statement Type is INSERT |
| table-schema-cache-size | Specifies how many Table Schemas should be cached |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | A FlowFile is routed to this relationship if the database cannot be updated and retrying the operation will also fail, such as an invalid query or an integrity constraint violation |
| retry | A FlowFile is routed to this relationship if the database cannot be updated but attempting the operation again may succeed |
| success | Successfully created FlowFile from SQL query result set. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| putdatabaserecord.error | If an error occurs during processing, the flow file will be routed to failure or retry, and this attribute will be populated with the cause of the error. |

Expand

Show lessSee more

## Use cases

| Insert records into a database |
| --- |

Expand

Show lessSee more
