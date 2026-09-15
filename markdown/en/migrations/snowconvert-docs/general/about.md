# SnowConvert AI - About

SnowConvert AI is an AI-powered Snowflake utility that accurately converts source database code from other platforms to Snowflake.

It ingests scripts for the source database objects such as tables, views, stored procedures, and functions. These scripts are then converted into Snowflake SQL scripts to recreate the exact equivalent Snowflake database objects. After reviewing the converted code, you can deploy the Snowflake SQL scripts on an existing instance of Snowflake.

Database platforms differ in syntax, built-in and procedural language features, logical architecture, SQL extensions, data types, and the extent of user defined customizations.
SnowConvert AI intelligently detects these differences and flags them as errors, warnings, issues ([EWIs](technical-documentation/issues-and-troubleshooting/conversion-issues/README)), and functional difference messages ([FDMs](technical-documentation/issues-and-troubleshooting/functional-difference/README)). These can be resolved manually or by using the built AI Code Conversion feature.
The AI Code Conversion feature also creates test cases to verify that the functionality of the converted Snowflake SQL code is exactly the same as the source database code.

Users can deploy the converted and verified code in an existing Snowflake instance.

## SnowConvert AI capabilities

| Source Technology | Availability | Supported Code Conversion | Source DB Connection | Data Migration | Snowflake Deployment | AI Code Conversion |
| --- | --- | --- | --- | --- | --- | --- |
| Teradata | GA | Tables, views, stored procedures, functions, Basic Teradata Query (BTEQ), Teradata MultiLoad (MLOAD), Teradata Parallel Data Pump (TPUMP) | Extraction script | No | No | No |
| Oracle | GA | Tables, views, stored procedures, functions, packages | Extraction script | No | No | No |
| SQL Server | GA | Tables, views, stored procedures, functions | Extraction script, direct DB connection | Yes | Yes | Yes |
| Redshift | GA | Tables, views, stored procedures, functions | Extraction script, direct DB connection | Yes | Yes | Yes |
| Azure Synapse | GA | Tables, views, stored procedures, functions | Extraction script | No | No | No |
| Sybase IQ | GA | Tables, views, stored procedures, functions | Extraction script | No | No | No |
| Google BigQuery | GA | Tables, views | Extraction script | No | No | Yes |
| Greenplum | GA | Tables, views | No | No | No | No |
| Netezza | GA | Tables, views | No | No | No | No |
| PostgreSQL | GA | Tables, views | No | No | No | Yes |
| Spark SQL | GA | Tables, views | No | No | No | No |
| Databricks SQL | GA | Tables, views | No | No | No | No |
| Vertica | GA | Tables, views | No | No | No | No |
| Hive | GA | Tables, views | No | No | No | No |
| IBM DB2 | GA | Tables, views, stored procedures, functions | No | No | No | No |

Expand

Show lessSee more

For more information, contact [snowconvert-info@snowflake.com](mailto:snowconvert-info@snowflake.com).
