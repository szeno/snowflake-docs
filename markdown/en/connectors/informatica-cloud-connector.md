# *Deprecated* — Snowflake Connector 1.x for Informatica Cloud

Deprecated Feature

This version of the Snowflake Connector has been deprecated. Use the latest version of the connector (provided by Informatica) instead.

For more details, see the [Snowflake Partner Network](https://www.snowflake.com/en/why-snowflake/partners/all-partners/).

This topic contains information about how to set up and use version 1.x of the Snowflake Connector. It explains how Informatica Cloud organization administrators and business users can use the Snowflake
Connector to publish data to Snowflake.

The connector implements the Informatica Cloud Connector SDK. It can be deployed on both Informatica Cloud and Informatica PowerCenter 9.6.1. For assistance deploying the connector on PowerCenter, please
contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Note

Snowflake also provides an ODBC library that can be used for data integration with Informatica’s products; currently, this library only supports read functionality.

## Introduction to Snowflake Connector

### Snowflake Connector Overview

Snowflake provides programmatic APIs for querying and modifying data in the form of industry-standard ODBC and JDBC libraries. The ODBC library can be used with Informatica products using standard ODBC
connectors. See the Informatica documentation for configuring the ODBC connector. The ODBC library can be downloaded from your Snowflake account. However, writing or updating large volumes of data into
Snowflake using ODBC is often not the most efficient or effective way to perform these operations.

The Snowflake Connector is designed to improve throughput of bulk insertion, modification, and deletion of large numbers of rows in Snowflake. It works by caching row-by-row data it receives through
Informatica, uploading it asynchronously to cloud storage in the form of compressed character-delimited files, and importing data from the files using the Snowflake COPY command.

### Snowflake Connector Implementation

Data submitted for processing is staged within the internal stage for the configured connection user (identified by the `~` character).

Subdirectories are created in the stage for each job. Multiple batches can be processed, with a corresponding subdirectory within the user stage for each batch. Each subdirectory
includes the following information:

- Name of the target table.
- Name of the operation (INSERT, DELETE, UPSERT, MODIFY).
- Timestamp and a unique identifier (consecutive number).

In the **Query History** page in Snowsight, the following commands are displayed for the user configured to run the process:

> - SQL statements configured to be run before a job.
> - Sequence of PUT commands to upload data files to the stage.
> - Creation of a temporary table to stage data.
> - COPY command to import data into the staging table, optionally in validation mode to first identify/retrieve data conversion errors.
> - DELETE, MERGE or INSERT command to process the data.
> - RM command to clean up staged files from the stage.

This sequence may be modified by the connector to optimize performance.

Data errors are reported to Informatica to be written to the error file session log, and may terminate the job if it is so configured. On its own, the Snowflake loading process skips all data conversion
errors.

## Snowflake Connections

### Snowflake Connection Overview

The Snowflake Connector uses the Snowflake JDBC driver to connect. The driver library is included in the connector distribution.

### Snowflake Connection Properties

The Snowflake Connector uses the following properties for connecting to Snowflake:

- [USER and PASSWORD](#user-and-password)
- [Snowflake URL](#snowflake-url)
- [Start transaction for jobs](#start-transaction-for-jobs)
- [Abort on data errors](#abort-on-data-errors)
- [Propagate data stream](#propagate-data-stream)

#### USER and PASSWORD

User name and password for the account that will be used for the loading process. Snowflake recommends using a dedicated user with the appropriate write privileges for the table where data will be loaded.

#### Snowflake URL

JDBC URL for connecting to the Snowflake database and schema in your account. For example:

> `jdbc:snowflake://xy12345.snowflakecomputing.com/?db=load&schema=etl`

Where:

- `xy12345` is the name of your account (provided by Snowflake).
- If your account is located in a region other than US West, the JDBC connection string must also include the [region ID](/user-guide/intro-regions#label-region-ids) after your account name in the form of
  `<account_id>.<region_id>.snowflakecomputing.com`.
- `load` is the name of the default database to use for loading data.
- `etl` is the name of the schema (in the `load` database) containing the tables to be loaded.

Note

During design time, metadata browsing is limited to the Snowflake schema and database specified in the connection or in the search path of the user.

Tip

If you run a job that includes a large set of data and very complex transformations, it may take a long time to complete. If the job takes over 4 hours, the Snowflake connection token may expire. To
avoid this situation, you can specify the `client_session_keep_alive` parameter in the JDBC connection string, which prevents the connection token from expiring. For example:

> `jdbc:snowflake://xy12345.snowflakecomputing.com/?...&client_session_keep_alive=true`

#### Start transaction for jobs

If set, the connector will initiate a transaction before the start of every job, and commit or rollback upon the completion or failure of the job.

Note

Informatica does not support operation rollback or disconnect in the connector API. Terminating a job may leave hanging table locks and an uncommitted transaction
that may be needed to be released manually from the Snowflake command line.

#### Abort on data errors

When this property is selected, every job will stop processing if any data conversion errors are encountered during data import. To rollback partial changes when errors
are encountered, also set **Start transaction for jobs**.

Note

Because data is loaded asynchronously, some data may already be committed if this property is used and more than one batch of data was generated.

#### Propagate data stream

The connector implements midstream write interface that allows chaining of data processing. If this property is selected, the connector will pass data for further
processing.

For better performance, do not select this property.

## Snowflake Data Synchronization Tasks

The connector provides advanced target properties for specifying Snowflake-specific actions and properties to use when a data synchronization task is performed.

### Snowflake Advanced Target Properties

The following table describes the advanced target properties that can be specified for a data synchronization task:

| Advanced Target Property | Description |
| --- | --- |
| **Update key columns** | Semicolon separated list of column names in the target table that should be used as a composite key for DELETE or MODIFY operations. |
| **Execute before** | SQL statement that will be executed prior to start of a job. |
| **Truncate table** | Delete all data from the target table prior to execution of the job. This statement is completed after execution of the **Execute before** statement. |
| **Execute after** | SQL statement that will be executed after completion of a job. |
| **Process data in one batch** | When this property is checked, the connector will upload all data from the job prior to processing it. |
| **Preserve stage file on Error** | Preserve staged data file when an error occurs in loading data. This property is valid only if Abort on data error is enabled. |
| **Use Local Timezone** | Use agent local timezone to convert TIMESTAMP/datetime data. By default, UTC is used in conversions. |
| **Success File Directory** | Not currently used. |
| **Error File Directory** | Not currently used. |
| **Database Override** | Name of the database to update; overrides the target database defined for the data synchronization task. Do not specify values for database override, schema override, or table override in a Data Synchronization task. You can specify the values in a PowerCenter session. |
| **Schema Override** | Name of the schema to update; overrides the target schema defined for the data synchronization task. Do not specify values for database override, schema override, or table override in a Data Synchronization task. You can specify the values in a PowerCenter session. |
| **Table Override** | Name of the table to update; overrides the target table defined for the data synchronization task. Do not specify values for database override, schema override, or table override in a Data Synchronization task. You can specify the values in a PowerCenter session. |

Expand

Show lessSee more

**Usage Notes:**

- Snowflake does not enforce primary or foreign key constraints, and does not preserve metadata for keys. You must specify the **Update key columns**
  property even if corresponding columns are marked as key in the Informatica environment.
- The **Process data in one batch** property may delay completion of the job, but guarantees that no data will be persisted in case of a failure,
  and without the overall transaction. Processing maximum amount of data at a time also maximizes utilization of Snowflake warehouse parallelism.
- The **Database Override**, **Schema Override**, and **Table Override** attributes are used by PowerCenter to provide values at runtime that
  override the target database, schema, and/or table for the data synchronization task. This enables using the same data synchronization task
  to update tables in multiple databases and schemas. The fields are blank by default and should be left blank because the values for the attributes
  are provided at runtime.
