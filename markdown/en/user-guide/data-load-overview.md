# Overview of data loading

This topic provides an overview of the main options available to load data into Snowflake.

To easily and accurately measure the ingestion latency of your data pipelines, use row timestamps. For more information, see [Use row timestamps to measure latency in your pipelines](/user-guide/data-engineering/row-timestamps).

## Supported file locations

Snowflake refers to the location of data files in cloud storage as a *stage*.
The [COPY INTO <table>](/sql-reference/sql/copy-into-table) command used for both bulk and continuous data loads (Snowpipe) supports
cloud storage accounts managed by your business entity (*external stages*) as well as cloud storage contained in your Snowflake account
(*internal stages*).

### External stages

Loading data from any of the following cloud storage services is supported regardless of the [cloud platform](/user-guide/intro-cloud-platforms) that hosts your Snowflake account:

- Amazon S3
- Google Cloud Storage
- Microsoft Azure

You cannot access data held in archival cloud storage classes that requires restoration before it can be retrieved. These archival storage classes include, for example, the Amazon S3 Glacier Flexible Retrieval or Glacier Deep Archive storage class, or Microsoft Azure Archive Storage.

Upload (i.e. *stage*) files to your cloud storage account using the tools provided by the cloud storage service.

A named external stage is a database object created in a schema. This object stores the URL to files in cloud storage, the settings used to access the cloud storage account, and convenience settings such as the options that describe the format of staged files. Create stages using the [CREATE STAGE](/sql-reference/sql/create-stage) command.

With Business Critical Edition (or higher) and account replication, pipelines that bulk load with `COPY INTO <table>` or load continuously with Snowpipe auto-ingest can fail over to a storage location in another region or on another cloud provider, so that your pipelines keep loading after a region-wide cloud provider outage. Snowpipe Streaming and Openflow don’t support this capability. For more information, see [Multi-Location Resilience for Data Pipelines](/user-guide/multi-location-resilience-data-pipelines).

Note

Some data transfer billing charges may apply when loading data from files in a cloud storage service in a different region or cloud platform from your Snowflake account. For more information, see [Understanding data transfer cost](/user-guide/cost-understanding-data-transfer).

### Internal stages

Snowflake maintains the following stage types in your account:

User:
:   A user stage is allocated to each user for storing files. This stage type is designed to store files that are staged and managed by a single user but can be loaded into multiple tables. User stages cannot be altered or dropped.

Table:
:   A table stage is available for each table created in Snowflake. This stage type is designed to store files that are staged and managed by one or more users but only loaded into a single table. Table stages cannot be altered or dropped.

    Note that a table stage is not a separate database object; rather, it is an implicit stage tied to the table itself. A table stage has no grantable privileges of its own. To stage files to a table stage, list the files, query them on the stage, or drop them, you must be the table owner (have the role with the OWNERSHIP privilege on the table).

Named:
:   A named internal stage is a database object created in a schema. This stage type can store files that are staged and managed by one or more users and loaded into one or more tables. Because named stages are database objects, the ability to create, modify, use, or drop them can be controlled using security access control privileges. Create stages using the [CREATE STAGE](/sql-reference/sql/create-stage) command.

Upload files to any of the internal stage types from your local file system using the [PUT](/sql-reference/sql/put) command.

## Bulk vs continuous loading

Snowflake provides the following main solutions for data loading. The best solution may depend upon the volume of data to load and the frequency of loading.

### Bulk loading using the COPY command

This option enables loading batches of data from files already available in cloud storage, or copying (i.e. *staging*) data files from a local machine to an internal (i.e. Snowflake) cloud storage location before loading the data into tables using the COPY command.

To have [CoCo](/user-guide/cortex-code/cortex-code) run a bulk load for you from a stage, a cloud storage path, or your computer (in CoCo CLI or CoCo Desktop), see [Bulk load files with CoCo](/user-guide/data-load-bulk-coco). CoCo creates or reuses a file format and table that match your files, and runs the COPY command. CoCo waits for your approval before each statement that creates or changes objects or loads data, in every approval mode.

To use an error table to record the rows that a `COPY INTO` statement rejects, see [Error logging for COPY INTO and Snowpipe](/user-guide/data-load-error-tables).

#### Compute resources

Bulk loading relies on user-provided virtual warehouses, which are specified in the COPY statement. Users are required to size the warehouse appropriately to accommodate expected loads.

#### Simple transformations during a load

Snowflake supports transforming data while loading it into a table using the COPY command. Options include:

- Column reordering
- Column omission
- Casts
- Truncating text strings that exceed the target column length

There is no requirement for your data files to have the same number and ordering of columns as your target table.

### Continuous loading using Snowpipe

Snowpipe loads files into standard tables or Apache Iceberg™ tables continuously as the files arrive in a stage, so new data is typically available for analysis within minutes. Use Snowpipe when files arrive throughout the day and you don’t want to schedule batch loads. For more information, see [Snowpipe](/user-guide/data-load-snowpipe-intro).

To set up Snowpipe auto-ingest with [CoCo](/user-guide/cortex-code/cortex-code) from a cloud storage path, see [Set up continuous file ingestion with CoCo](/user-guide/data-load-snowpipe-auto-coco). Depending on the setup option you choose, CoCo creates the stage, pipe, related objects, and cloud notifications for you, generates deployment files for your team, or does some of each.

To use an error table to record the rows that a pipe rejects or the files that it skips, see [Error logging for COPY INTO and Snowpipe](/user-guide/data-load-error-tables).

#### Snowpipe compute and billing

Snowpipe uses serverless compute that Snowflake provides and scales automatically, so you don’t size or manage a warehouse. Snowpipe charges a fixed number of credits per GB of data loaded. For more information, see [Snowpipe costs](/user-guide/data-load-snowpipe-billing).

#### Transformations in a pipe

The `COPY INTO` statement in a pipe definition supports the same transformation options as bulk loading. For more information, see [Transform data during a load](/user-guide/data-load-transform).

To transform the data after it loads, use [dynamic tables](/user-guide/dynamic-tables/overview) or [streams and tasks](/user-guide/streams-intro).

### Continuous loading using Snowpipe Streaming

The Snowpipe Streaming API writes rows of data directly to Snowflake tables without the requirement of staging files. This architecture results in lower load latencies with corresponding lower costs for loading any volume of data, which makes it a powerful tool for handling near real-time data streams.

Snowpipe Streaming is also available for the Snowflake Connector for Kafka, which offers an easy upgrade path to take advantage of the lower latency and lower cost loads.

For more information, refer to [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview).

## Loading data from Apache Kafka topics

The [Snowflake Connector for Kafka](/user-guide/kafka-connector/index) enables users to connect to an [Apache Kafka](https://kafka.apache.org/) server, read data from one or more topics, and load that data into Snowflake tables.

## Error logging

If you turn on error logging for a table, Snowflake records the rows that DML statements, `COPY INTO`, and Snowpipe
can’t write to the table. Snowflake records these rows in the table’s error table, where you can query the rows,
correct them, and write them again. For `COPY INTO` and Snowpipe, the `ON_ERROR` copy option still controls how a
load handles errors and determines which rejected rows are recorded. `COPY INTO` and Snowpipe also enforce CHECK
constraints on the target table and handle rows that violate them according to `ON_ERROR`. For more information, see
the following topics:

- [Introduction to error logging](/user-guide/data-engineering/error-logging): Which statements and loads record errors, how to turn on error
  logging, and how to find the tables that have it turned on.
- [Error logging for COPY INTO and Snowpipe](/user-guide/data-load-error-tables): How to record the rows that `COPY INTO` and Snowpipe reject from staged
  files. Start here if you load files with `COPY INTO` or Snowpipe.
  - [Query load errors](/user-guide/data-load-error-tables-query): How to query these rows.
  - [Correct and reload rejected rows](/user-guide/data-load-error-tables-reload): How to correct these rows and load them again.
- [Error logging for DML statements](/user-guide/data-engineering/error-logging-dml): How `INSERT`, `UPDATE`, `MERGE`, and `CREATE TABLE ... AS SELECT`
  statements record errors, how to detect these errors in a scheduled job and correct them, and how DML error logging
  compares with the Oracle `LOG ERRORS INTO` clause.
- [Error tables](/user-guide/data-engineering/error-tables): What an error table contains, how long it keeps errors, which
  privileges you need to query it, and how to process new errors with streams.

For error logging with the high-performance architecture of Snowpipe Streaming, see
[Error logging in Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables).

## Schema detection of column definitions from staged semi-structured data files

Semi-structured data can include thousands of columns. Snowflake provides robust solutions for handling this data. Options include
referencing the data directly in cloud storage using external tables, loading the data into a single column of type VARIANT, or
transforming and loading the data into separate columns in a standard relational table. All of these options require some knowledge of the
column definitions in the data.

A different solution involves automatically detecting the schema in a set of staged semi-structured data files and retrieving the column
definitions. The column definitions include the names, data types, and ordering of columns in the files. Generate syntax in a format
suitable for creating Snowflake standard tables, external tables, or views.

Note

This feature supports Apache Parquet, Apache Avro, ORC, JSON, and CSV files.

This support is implemented through the following SQL functions:

[INFER\_SCHEMA](/sql-reference/functions/infer_schema)
:   Detects the column definitions in a set of staged data files and retrieves the metadata in a format suitable for creating Snowflake objects.

[GENERATE\_COLUMN\_DESCRIPTION](/sql-reference/functions/generate_column_description)
:   Generates a list of columns from a set of staged files using the INFER\_SCHEMA function output.

These SQL functions support both internal and external stages.

Create tables or external tables with the column definitions derived from a set of staged files using the
[CREATE TABLE … USING TEMPLATE](/sql-reference/sql/create-table) or [CREATE EXTERNAL TABLE … USING TEMPLATE](/sql-reference/sql/create-external-table) syntax. The USING TEMPLATE clause accepts an expression that
calls the INFER\_SCHEMA SQL function to detect the column definitions in the files. After the table is created, you can then use a COPY statement with the `MATCH_BY_COLUMN_NAME` option to load files directly into the structured table.

Schema detection can also be used in conjunction with [table schema evolution](/user-guide/data-load-schema-evolution), where the structure of tables evolves automatically to support the structure of new data received from the data sources.

To create and evolve [structured](/sql-reference/data-types-structured) `OBJECT`, `ARRAY`, and `MAP` columns for nested data, set
`INFER_NESTED_TYPES` to `TRUE` in the `INFER_SCHEMA` call and in the `COPY INTO` statement. For more information, see
[Detect and evolve structured columns](/user-guide/data-load-schema-evolution#label-schema-evolution-structured-types).

## Alternatives to loading data

You can use the following option to query your data in cloud storage without loading it into Snowflake tables.

### External tables (data lake)

[External tables](/user-guide/tables-external-intro) enable querying existing data stored in external cloud storage for analysis without first loading it into Snowflake. The source of truth for the data remains in the external cloud storage. Data sets materialized in Snowflake via materialized views are read-only.

This solution is especially beneficial to accounts that have a large amount of data stored in external cloud storage and only want to query a portion of the data; for example, the most recent data. Users can create materialized views on subsets of this data for improved query performance.

### Working with Amazon S3-compatible storage

You can create external stages and tables in Snowflake to access storage in an application or device that is Amazon S3-compatible.
This feature lets you manage, govern, and analyze your data, regardless of where the data is stored.
For information, see [Work with Amazon S3-compatible storage](/user-guide/data-load-s3-compatible-storage).
