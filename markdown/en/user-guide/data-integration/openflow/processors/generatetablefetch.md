# GenerateTableFetch 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-standard-nar

## Description

Generates SQL select queries that fetch “pages” of rows from a table. The partition size property, along with the table ‘s row count, determine the size and number of pages and generated FlowFiles. In addition, incremental fetching can be achieved by setting Maximum-Value Columns, which causes the processor to track the columns’ maximum values, thus only fetching rows whose columns ‘values exceed the observed maximums. This processor is intended to be run on the Primary Node only. This processor can accept incoming connections; the behavior of the processor is different whether incoming connections are provided: - If no incoming connection(s) are specified, the processor will generate SQL queries on the specified processor schedule. Expression Language is supported for many fields, but no FlowFile attributes are available. However the properties will be evaluated using the Environment/System properties. - If incoming connection(s) are specified and no FlowFile is available to a processor task, no work will be performed. - If incoming connection(s) are specified and a FlowFile is available to a processor task, the FlowFile’s attributes may be used in Expression Language for such fields as Table Name and others. However, the Max-Value Columns and Columns to Return fields must be empty or refer to columns that are available in each specified table.

## Tags

database, fetch, generate, jdbc, query, select, sql

## Input Requirement

ALLOWED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| Columns to Return | A comma-separated list of column names to be used in the query. If your database requires special treatment of the names (quoting, e.g.), each name should include such treatment. If no column names are supplied, all columns in the specified table will be returned. NOTE: It is important to use consistent column names for a given table for incremental fetch to work properly. |
| Database Connection Pooling Service | The Controller Service that is used to obtain a connection to the database. |
| Database Dialect Service | Database Dialect Service for generating statements specific to a particular service or vendor. |
| Max Wait Time | The maximum amount of time allowed for a running SQL select query , zero means there is no limit. Max time less than 1 second will be equal to zero. |
| Maximum-value Columns | A comma-separated list of column names. The processor will keep track of the maximum value for each column that has been returned since the processor started running. Using multiple columns implies an order to the column list, and each column ‘s values are expected to increase more slowly than the previous columns’ values. Thus, using multiple columns implies a hierarchical structure of columns, which is usually used for partitioning tables. This processor can be used to retrieve only those rows that have been added/updated since the last retrieval. Note that some JDBC types such as bit/boolean are not conducive to maintaining maximum value, so columns of these types should not be listed in this property, and will result in error(s) during processing. If no columns are provided, all rows from the table will be considered, which could have a performance impact. NOTE: It is important to use consistent max-value column names for a given table for incremental fetch to work properly. |
| Table Name | The name of the database table to be queried. |
| db-fetch-db-type | Database Type for generating statements specific to a particular service or vendor. The Generic Type supports most cases but selecting a specific type enables optimal processing or additional features. |
| db-fetch-where-clause | A custom clause to be added in the WHERE condition when building SQL queries. |
| gen-table-column-for-val-partitioning | The name of a column whose values will be used for partitioning. The default behavior is to use row numbers on the result set for partitioning into ‘pages’ to be fetched from the database, using an offset/limit strategy. However for certain databases, it can be more efficient under the right circumstances to use the column values themselves to define the ‘pages’. This property should only be used when the default queries are not performing well, when there is no maximum-value column or a single maximum-value column whose type can be coerced to a long integer (i.e. not date or timestamp), and the column values are evenly distributed and not sparse, for best performance. |
| gen-table-custom-orderby-column | The name of a column to be used for ordering the results if Max-Value Columns are not provided and partitioning is enabled. This property is ignored if either Max-Value Columns is set or Partition Size = 0. NOTE: If neither Max-Value Columns nor Custom ORDER BY Column is set, then depending on the database/driver, the processor may report an error and/or the generated SQL may result in missing and/or duplicate rows. This is because without an explicit ordering, fetching each partition is done using an arbitrary ordering. |
| gen-table-fetch-partition-size | The number of result rows to be fetched by each generated SQL statement. The total number of rows in the table divided by the partition size gives the number of SQL statements (i.e. FlowFiles) generated. A value of zero indicates that a single FlowFile is to be generated whose SQL statement will fetch all rows in the table. |
| gen-table-output-flowfile-on-zero-results | Depending on the specified properties, an execution of this processor may not result in any SQL statements generated. When this property is true, an empty FlowFile will be generated (having the parent of the incoming FlowFile if present) and transferred to the ‘success’ relationship. When this property is false, no output FlowFiles will be generated. |

Expand

Show lessSee more

## State management

| Scopes | Description |
| --- | --- |
| CLUSTER | After performing a query on the specified table, the maximum values for the specified column(s) will be retained for use in future executions of the query. This allows the Processor to fetch only those records that have max values greater than the retained values. This can be used for incremental fetching, fetching of newly added rows, etc. To clear the maximum values, clear the state of the processor per the State Management documentation |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | This relationship is only used when SQL query execution (using an incoming FlowFile) failed. The incoming FlowFile will be penalized and routed to this relationship. If no incoming connection(s) are specified, this relationship is unused. |
| success | Successfully created FlowFile from SQL query result set. |

Expand

Show lessSee more

## Writes attributes

| Name | Description |
| --- | --- |
| generatetablefetch.sql.error | If the processor has incoming connections, and processing an incoming FlowFile causes a SQL Exception, the FlowFile is routed to failure and this attribute is set to the exception message. |
| generatetablefetch.tableName | The name of the database table to be queried. |
| generatetablefetch.columnNames | The comma-separated list of column names used in the query. |
| generatetablefetch.whereClause | Where clause used in the query to get the expected rows. |
| generatetablefetch.maxColumnNames | The comma-separated list of column names used to keep track of data that has been returned since the processor started running. |
| generatetablefetch.limit | The number of result rows to be fetched by the SQL statement. |
| generatetablefetch.offset | Offset to be used to retrieve the corresponding partition. |
| fragment.identifier | All FlowFiles generated from the same query result set will have the same value for the fragment.identifier attribute. This can then be used to correlate the results. |
| fragment.count | This is the total number of FlowFiles produced by a single ResultSet. This can be used in conjunction with the fragment.identifier attribute in order to know how many FlowFiles belonged to the same incoming ResultSet. |
| fragment.index | This is the position of this FlowFile in the list of outgoing FlowFiles that were all generated from the same execution. This can be used in conjunction with the fragment.identifier attribute to know which FlowFiles originated from the same execution and in what order FlowFiles were produced |

Expand

Show lessSee more

## See also

- [org.apache.nifi.processors.standard.ExecuteSQL](/user-guide/data-integration/openflow/processors/executesql)
- [org.apache.nifi.processors.standard.ListDatabaseTables](/user-guide/data-integration/openflow/processors/listdatabasetables)
- [org.apache.nifi.processors.standard.QueryDatabaseTable](/user-guide/data-integration/openflow/processors/querydatabasetable)
