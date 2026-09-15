# ExecuteSQLRecord 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Executes provided SQL select query. Query result will be converted to the format specified by a Record Writer. Streaming is used so arbitrarily large result sets are supported. This processor can be scheduled to run on a timer, or cron expression, using the standard scheduling methods, or it can be triggered by an incoming FlowFile. If it is triggered by an incoming FlowFile, then attributes of that FlowFile will be available when evaluating the select query, and the query may use the ? to escape parameters. In this case, the parameters to use must exist as FlowFile attributes with the naming convention sql.args. N.type and sql.args. N.value, where N is a positive integer. The sql.args. N.type is expected to be a number indicating the JDBC Type. The content of the FlowFile is expected to be in UTF-8 format. FlowFile attribute ‘executesql.row.count’ indicates how many rows were selected.

## Tags

database, jdbc, query, record, select, sql

## Input Requirement

ALLOWED

## Supports Sensitive Dynamic Properties

true

## Properties

| Property | Description |
| --- | --- |
| Database Connection Pooling Service | The Controller Service that is used to obtain connection to database |
| Default Decimal Precision | When a DECIMAL/NUMBER value is written as a ‘decimal’ Avro logical type, a specific ‘precision’ denoting number of available digits is required. Generally, precision is defined by column data type definition or database engines default. However undefined precision (0) can be returned from some database engines. ‘Default Decimal Precision’ is used when writing those undefined precision numbers. |
| Default Decimal Scale | When a DECIMAL/NUMBER value is written as a ‘decimal’ Avro logical type, a specific ‘scale’ denoting number of available decimal digits is required. Generally, scale is defined by column data type definition or database engines default. However when undefined precision (0) is returned, scale can also be uncertain with some database engines. ‘Default Decimal Scale’ is used when writing those undefined numbers. If a value has more decimals than specified scale, then the value will be rounded-up, e.g. 1.53 becomes 2 with scale 0, and 1.5 with scale 1. |
| Max Wait Time | The maximum amount of time allowed for a running SQL select query , zero means there is no limit. Max time less than 1 second will be equal to zero. |
| SQL Query | The SQL query to execute. The query can be empty, a constant value, or built from attributes using Expression Language. If this property is specified, it will be used regardless of the content of incoming flowfiles. If this property is empty, the content of the incoming flow file is expected to contain a valid SQL select query, to be issued by the processor to the database. Note that Expression Language is not evaluated for flow file contents. |
| Use Avro Logical Types | Whether to use Avro Logical Types for DECIMAL/NUMBER, DATE, TIME and TIMESTAMP columns. If disabled, written as string. If enabled, Logical types are used and written as its underlying type, specifically, DECIMAL/NUMBER as logical ‘decimal’: written as bytes with additional precision and scale meta data, DATE as logical ‘date-millis’: written as int denoting days since Unix epoch (1970-01-01), TIME as logical ‘time-millis’: written as int denoting milliseconds since Unix epoch, and TIMESTAMP as logical ‘timestamp-millis’: written as long denoting milliseconds since Unix epoch. If a reader of written Avro records also knows these logical types, then these values can be deserialized with more context depending on reader implementation. |
| esql-auto-commit | Enables or disables the auto commit functionality of the DB connection. Default value is ‘true’. The default value can be used with most of the JDBC drivers and this functionality doesn’t have any impact in most of the cases since this processor is used to read data. However, for some JDBC drivers such as PostgreSQL driver, it is required to disable the auto committing functionality to limit the number of result rows fetching at a time. When auto commit is enabled, postgreSQL driver loads whole result set to memory at once. This could lead for a large amount of memory usage when executing queries which fetch large data sets. More Details of this behaviour in PostgreSQL driver can be found in <https://jdbc.postgresql.org//documentation/head/query.html>. |
| esql-fetch-size | The number of result rows to be fetched from the result set at a time. This is a hint to the database driver and may not be honored and/or exact. If the value specified is zero, then the hint is ignored. |
| esql-max-rows | The maximum number of result rows that will be included in a single FlowFile. This will allow you to break up very large result sets into multiple FlowFiles. If the value specified is zero, then all rows are returned in a single FlowFile. |
| esql-output-batch-size | The number of output FlowFiles to queue before committing the process session. When set to zero, the session will be committed when all result set rows have been processed and the output FlowFiles are ready for transfer to the downstream relationship. For large result sets, this can cause a large burst of FlowFiles to be transferred at the end of processor execution. If this property is set, then when the specified number of FlowFiles are ready for transfer, then the session will be committed, thus releasing the FlowFiles to the downstream relationship. NOTE: The fragment.count attribute will not be set on FlowFiles when this property is set. |
| esqlrecord-normalize | Whether to change characters in column names. For example, colons and periods will be changed to underscores. |
| esqlrecord-record-writer | Specifies the Controller Service to use for writing results to a FlowFile. The Record Writer may use Inherit Schema to emulate the inferred schema behavior, i.e. an explicit schema need not be defined in the writer, and will be supplied by the same logic used to infer the schema from the column types. |
| sql-post-query | A semicolon-delimited list of queries executed after the main SQL query is executed. Example like setting session properties after main query. It ‘s possible to include semicolons in the statements themselves by escaping them with a backslash (‘;’). Results/outputs from these queries will be suppressed if there are no errors. |
| sql-pre-query | A semicolon-delimited list of queries executed before the main SQL query is executed. For example, set session properties before main query. It ‘s possible to include semicolons in the statements themselves by escaping them with a backslash (‘;’). Results/outputs from these queries will be suppressed if there are no errors. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | SQL query execution failed. Incoming FlowFile will be penalized and routed to this relationship |
| success | Successfully created FlowFile from SQL query result set. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| executesql.row.count | Contains the number of rows returned in the select query |
| executesql.query.duration | Combined duration of the query execution time and fetch time in milliseconds |
| executesql.query.executiontime | Duration of the query execution time in milliseconds |
| executesql.query.fetchtime | Duration of the result set fetch time in milliseconds |
| executesql.resultset.index | Assuming multiple result sets are returned, the zero based index of this result set. |
| executesql.error.message | If processing an incoming flow file causes an Exception, the Flow File is routed to failure and this attribute is set to the exception message. |
| fragment.identifier | If ‘Max Rows Per Flow File’ is set then all FlowFiles from the same query result set will have the same value for the fragment.identifier attribute. This can then be used to correlate the results. |
| fragment.count | If ‘Max Rows Per Flow File’ is set then this is the total number of FlowFiles produced by a single ResultSet. This can be used in conjunction with the fragment.identifier attribute in order to know how many FlowFiles belonged to the same incoming ResultSet. If Output Batch Size is set, then this attribute will not be populated. |
| fragment.index | If ‘Max Rows Per Flow File’ is set then the position of this FlowFile in the list of outgoing FlowFiles that were all derived from the same result set FlowFile. This can be used in conjunction with the fragment.identifier attribute to know which FlowFiles originated from the same query result set and in what order FlowFiles were produced |
| input.flowfile.uuid | If the processor has an incoming connection, outgoing FlowFiles will have this attribute set to the value of the input FlowFile’s UUID. If there is no incoming connection, the attribute will not be added. |
| mime.type | Sets the mime.type attribute to the MIME Type specified by the Record Writer. |
| record.count | The number of records output by the Record Writer. |

Expand

Show lessSee more
