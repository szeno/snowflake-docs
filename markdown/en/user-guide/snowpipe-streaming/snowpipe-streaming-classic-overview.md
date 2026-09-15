# Snowpipe Streaming classic architecture

Important

- Advance notice: Snowpipe Streaming classic architecture is fully supported today, but it is planned for future deprecation.
- Action: No immediate changes are required. Your current workloads are safe and continue to be fully supported.
- Timeline: Snowflake plans to issue a formal deprecation announcement in mid-2026. This milestone refers to the announcement date only. After the deprecation announcement, an 18-month migration window begins before the end-of-life date.
- Recommendation: Use the high-performance architecture for all new implementations.

For full details, FAQs, and migration guidance, see [Notice of planned deprecation](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-deprecation).

Note

New to Snowpipe Streaming? See the [Snowpipe Streaming overview](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview) for current capabilities built on the high-performance architecture.

The Snowpipe Streaming classic architecture offers a proven and efficient method for continuous, low-latency, row-based data ingestion directly into Snowflake tables. This implementation, referred to as Snowpipe Streaming Classic in the documentation, remains a reliable choice for diverse streaming workloads such as application event data, Internet of things (IoT) sensor readings, and low-latency Change Data Capture (CDC).

Snowpipe Streaming Classic uses the `snowflake-ingest-java` SDK and operates without the explicit `PIPE` object concept for managing data flow that is central to the Snowpipe Streaming high-performance architecture. Instead, in Snowpipe Streaming Classic, channels are configured more directly against tables, offering a familiar and established approach to streaming data into Snowflake.

## Software requirements

- SDK: Use the [snowflake-ingest-sdk](https://mvnrepository.com/artifact/net.snowflake/snowflake-ingest-sdk) version 4.X or later.
- Java version: Requires Java 8 or later.
- Additional prerequisite: [Java Cryptography Extension (JCE) Unlimited Strength Jurisdiction Policy Files](/developer-guide/jdbc/java-install#label-jdbc-jce-policy-file-install) must be installed for your Java 8 environment.
- For documentation on the classes and interfaces for the classic architecture, see [Snowflake Ingest SDK API](https://javadoc.io/doc/net.snowflake/snowflake-ingest-sdk/latest/overview-summary.html).

For the differences between the classic and high-performance architectures, see [API differences](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-comparison).

### Custom client application

The API requires a custom Java application interface that can accept rows of data and handle errors that occur. You must ensure that the application runs continuously and can recover from failure. For a given batch of rows, the API supports the equivalent of `ON_ERROR = CONTINUE | SKIP_BATCH | ABORT`.

- `CONTINUE`: Continue to load the acceptable rows of data and return all errors.
- `SKIP_BATCH`: Skip loading and return all errors if any error is encountered in the entire batch of rows.
- `ABORT` (default setting): Abort the entire batch of rows and throw an exception when the first error is encountered.

For Snowpipe Streaming classic, the application does schema validations using the response from the `insertRow` (single row) or `insertRows` (set of rows) methods. For the error handling for the high-performance architecture, see [Error handling](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-error-handling).

## Loading data into Apache Iceberg™ tables

With Snowflake Ingest SDK versions 3.0.0 and later, Snowpipe Streaming can ingest data into Snowflake-managed [Apache Iceberg](/user-guide/tables-iceberg) tables. The Snowpipe Streaming Ingest Java SDK supports loading into both standard Snowflake tables (non-Iceberg) and Iceberg tables.

For more information, see [Snowpipe Streaming Classic with Apache Iceberg™ tables](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-iceberg).

## Migration to optimized files in the classic architecture

The API writes the rows from channels into blobs in cloud storage, which are then committed to the target table. Initially, the streamed data written to a target table is stored in a temporary intermediate file format. At this stage, the table is considered a “mixed table” because partitioned data is stored in a mixture of native and intermediary files. An automated background process migrates data from the active intermediate files to native files that are optimized for query and DML operations as needed.

## Replication in the classic architecture

Snowpipe streaming supports the [replication and failover](/user-guide/account-replication-intro) of Snowflake tables populated by Snowpipe Streaming and its associated channel offsets from a source account to a target account in different [regions](/user-guide/intro-regions) and across [cloud platforms](/user-guide/intro-cloud-platforms).

For more information, see [Replication and Snowpipe Streaming](/user-guide/account-replication-considerations#label-replication-snowpipe-streaming).
