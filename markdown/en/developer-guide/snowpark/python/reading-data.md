# Using Snowpark to read data

Whether your data sits in operational databases or arrives as files, Snowpark gives you a simple, Python-first way to pull it in, convert it to a DataFrame, and view it in Snowflake tables, so you can model, transform, and analyze without context switching.

## Reading data from external sources using Snowpark Python DB-API

Use standard Python DB-API 2.0 drivers to pull data from external databases (SQL Server, Oracle, PostgreSQL, MySQL, Databricks) directly into a Snowpark DataFrame. Snowpark Python DB-API can run from your client (*local* mode) or inside Snowflake using stored procedures or notebooks (with external access integration). The result behaves like any other DataFrame you can use to join, transform, and write to Snowflake tables. For more information, see [Using the Snowpark Python DB-API](/developer-guide/snowpark/python/reading-data-from-external-sources).

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

## Reading data from external sources using Snowpark Python JDBC

Use standard JDBC drivers provided by you to pull data from external databases directly into a Snowpark DataFrame. Snowpark Python JDBC can run from your client or inside Snowflake using stored procedures or notebooks. A UDTF is created to ingest your target data. The result behaves like any other DataFrame you can use to join, transform, and write to Snowflake tables. For more information, see [Using the Snowpark Python JDBC](/developer-guide/snowpark/python/snowpark-jdbc).

Note

To use this feature, upload the JDBC driver to a stage, configure an external access integration, and ensure Snowflake can reach the source endpoint.

## Reading data from XML files using Snowpark XML RowTag Reader

Use Snowpark XML to read large staged XML files efficiently: the reader splits the file on `rowTag`, loads each match as one row, and maps child elements into `VARIANT` columns (preserving the nested structure) for immediate querying with Snowpark or SQL. You can also validate each row against an XSD with `PERMISSIVE` (quarantine invalid rows in `_corrupt_record`) or `FAILFAST` behavior. The output is a standard DataFrame you can transform and save to tables. For more information, see [Using the Snowpark XML RowTag Reader](/developer-guide/snowpark/python/snowpark-xml-rowtag-reader).
