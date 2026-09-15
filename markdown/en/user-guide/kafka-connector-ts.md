Important

- Advance notice: The classic Kafka connector (v3 and earlier) is fully supported today,
  but it is planned for future deprecation.
- Action: No immediate changes are required. Your current workloads are safe
  and continue to be fully supported.
- Timeline: Snowflake plans to issue a formal deprecation announcement in mid-2026.
  After the announcement, an 18-month migration window begins before end-of-life.
- Recommendation: Use the
  [Snowflake Connector for Kafka (v4)](/user-guide/kafka-connector/index)
  for all new implementations.

For migration guidance, see [Migrate from v3 to v4](/user-guide/kafka-connector/migrate-v3-to-v4).

# Troubleshooting the Kafka connector

This section describes how to troubleshoot issues encountered while ingesting data using the Kafka connector.

## Error notifications

Configure error notifications for Snowpipe. When Snowpipe encounters file errors during a load, the feature pushes a notification to a configured cloud messaging service, enabling analysis of your data files. For more information, see [Snowpipe error notifications](/user-guide/data-load-snowpipe-errors).

## General troubleshooting steps

Complete the following steps to troubleshoot issues with loads using the Kafka connector.

### Step 1: View the COPY history for the table

Query the load activity history for the target table. For information, see [COPY\_HISTORY view](/sql-reference/account-usage/copy_history). If the COPY\_HISTORY output does not include a set of expected files, query an earlier time period. If the files were duplicates of earlier files, the load history might have recorded the activity when the attempt to load the original files was made. The `STATUS` column indicates whether a particular set of files was loaded, partially loaded, or failed to load. The `FIRST_ERROR_MESSAGE` column provides a reason when an attempt partially loaded or failed.

The Kafka connector moves files it could not load to the stage associated with the target table. The syntax for referencing a table stage is `@[namespace.]%table_name`.

List all files located in the table stage using [LIST](/sql-reference/sql/list).

For example:

Copy code

```
LIST @mydb.public.%mytable;
```

File names are in one of the following formats. The conditions that produce each format are described in the table:

| File Type | Description |
| --- | --- |
| Raw bytes | These files match the following pattern:  `<connector_name>/<table_name>/<partition>/offset_(<key>/<value>_)<timestamp>.gz`  For these files, the Kafka records could not be converted from raw bytes to the source file format (Avro, JSON, or Protobuf).  A common cause for this issue is a network failure that resulted in a character getting dropped from the record. The Kafka connector could no longer parse the raw bytes, resulting in a broken record. |
| Source file format (Avro, JSON, or Protobuf) | These files match the following pattern:  `<connector_name>/<table_name>/<partition>/<start_offset>_<end_offset>_<timestamp>.<file_type>.gz`  For these files, after the Kafka connector converted the raw bytes back to the source file format, Snowpipe encountered an error and could not load the file. |

Expand

Show lessSee more

The following sections provide instructions for resolving issues with each of the file types:

#### Raw bytes

The filename `<connector_name>/<table_name>/<partition>/offset_(<key>/<value>_)<timestamp>.gz` includes the exact offset of the record that was not converted from raw bytes to the source file format. To resolve issues, resend the record to the Kafka connector as a new record.

#### Source file format (Avro, JSON, or protobuf)

If Snowpipe could not load data from files in the internal stage created for the Kafka topic, the Kafka connector moves the files to the stage for the target table in the source file format.

If a set of files has multiple issues, the `FIRST_ERROR_MESSAGE` column in the COPY\_HISTORY output only indicates the first error encountered. To view all errors in the files, it is necessary to retrieve the files from the table stage, upload them to a named stage, and then execute a [COPY INTO <table>](/sql-reference/sql/copy-into-table) statement with the VALIDATION\_MODE copy option set to `RETURN_ALL_ERRORS`. The VALIDATION\_MODE copy option instructs a COPY statement to validate the data to be loaded and return results based on the validation option specified. No data is loaded when this copy option is specified. In the statement, reference the set of files you had attempted to load using the Kafka connector.

When any issues with the data files are resolved, you can load the data manually using one or more COPY statements.

The following example references data files located in the table stage for the `mytable` table in the `mydb.public` database and schema.

To validate data files in the table stage and resolve errors:

1. List all files located in the table stage using [LIST](/sql-reference/sql/list).

   For example:

   Copy code

   ```
   LIST @mydb.public.%mytable;
   ```

   The examples in this section presume that JSON is the source format for the data files.
2. Download the files created by Kafka connector to your local machine using [GET](/sql-reference/sql/get).

   For example, download the files to a directory named `data` on your local machine:

   Linux or macOS:
   :   Copy code

       ```
       GET @mydb.public.%mytable file:///data/;
       ```

   Microsoft Windows:
   :   Copy code

       ```
       GET @mydb.public.%mytable file://C:\data\;
       ```
3. Create a named internal stage using [CREATE STAGE](/sql-reference/sql/create-stage) that stores data files with the same format as your source Kafka files.

   For example, create an internal stage named `kafka_json` that stores JSON files:

   Copy code

   ```
   CREATE STAGE kafka_json FILE_FORMAT = (TYPE = JSON);
   ```
4. Upload the files you downloaded from the table stage using [PUT](/sql-reference/sql/put).

   For example, upload the files downloaded to the `data` directory on your local machine:

   Linux or macOS:
   :   Copy code

       ```
       PUT file:///data/ @mydb.public.kafka_json;
       ```

   Microsoft Windows:
   :   Copy code

       ```
       PUT file://C:\data\ @mydb.public.kafka_json;
       ```
5. Create a temporary table with two variant columns for testing purposes. The table is only used to validate staged data file. No data is loaded into the table. The table is dropped automatically when the current user session ends:

   Copy code

   ```
   CREATE TEMPORARY TABLE t1 (col1 variant);
   ```
6. Retrieve all errors encountered in the data file by executing a [COPY INTO table … VALIDATION\_MODE = ‘RETURN\_ALL\_ERRORS’](/sql-reference/sql/copy-into-table) statement. The statement validates the file in the specified stage. No data is loaded into the table:

   Copy code

   ```
   COPY INTO mydb.public.t1
     FROM @mydb.public.kafka_json
     FILE_FORMAT = (TYPE = JSON)
     VALIDATION_MODE = 'RETURN_ALL_ERRORS';
   ```
7. Fix all reported errors in the data files on your local machine.
8. Upload the fixed files to either the table stage or the named internal stage using [PUT](/sql-reference/sql/put).

   The following example uploads the files to the table stage, overwriting the existing files:

   Linux or macOS:
   :   Copy code

       ```
       PUT file:///tmp/myfile.csv @mydb.public.%mytable OVERWRITE = TRUE;
       ```

   Windows:
   :   Copy code

       ```
       PUT file://C:\temp\myfile.csv @mydb.public.%mytable OVERWRITE = TRUE;
       ```
9. Load the data into the target table using COPY INTO *table* without the VALIDATION\_MODE option.

   You can optionally use the PURGE = TRUE copy option to delete the data files from the stage once the data is loaded successfully, or manually delete the files from the table stage using [REMOVE](/sql-reference/sql/remove):

   Copy code

   ```
   COPY INTO mydb.public.mytable(RECORD_METADATA, RECORD_CONTENT)
     FROM (SELECT $1:meta, $1:content FROM @mydb.public.%mytable)
     FILE_FORMAT = (TYPE = 'JSON')
     PURGE = TRUE;
   ```

### Step 2: Analyze the Kafka connector log file

If the COPY\_HISTORY view has no record of the data load, then analyze the log file for the Kafka connector. The connector writes events to the log file. Note that the Snowflake Kafka connector shares the same log file with all Kafka connector plugins. The name and location of this log file should be in your Kafka Connect configuration file. For more information, see the documentation provided for your Apache Kafka software.

Search the Kafka connector log file for Snowflake-related error messages. Most messages will have the string `ERROR` and will contain the file name
`com.snowflake.kafka.connector...` to make these messages easier to find.

Possible errors that you might encounter include:

Configuration error:
:   Possible causes of the error:

    - The connector doesn’t have the proper information to subscribe to the topic.
    - The connector doesn’t have the proper information to write to the Snowflake table (e.g. the key pair for authentication might be wrong).

    Note that the Kafka connector validates its parameters. The connector throws an error for each incompatible configuration parameter. The error message is written
    to the Kafka Connect cluster’s log file. If you suspect a configuration problem, check the errors in that log file.

Read error:
:   The connector might not have been able to read from Kafka for the following reasons:

    - Kafka or Kafka Connect might not be running.
    - The message might not have been sent yet.
    - The message might have been deleted (expired).

Write error (stage):
:   Possible causes of the error:

    - Insufficient privileges on the stage.
    - Stage is out of space.
    - Stage was dropped.
    - Some other user or process wrote unexpected files to the stage.

Write error (table):
:   Possible causes of the error:

    - Insufficient privileges on the table.

### Step 3: Check Kafka Connect

If no error is reported in the Kafka connect log file, check Kafka Connect. For troubleshooting instructions, see the documentation provided by your Apache Kafka software vendor.

## Resolving specific issues

### Duplicate rows with the same topic partition and offset

When loading data using version 1.4 of the Kafka connector (or higher), duplicate rows in the target table with the same topic partition and offset can indicate that the load operation exceeded the default execution timeout of 300000 milliseconds (300 seconds). To verify the cause, check the Kafka Connect log file for the following error:

Copy code

```
org.apache.kafka.clients.consumer.CommitFailedException: Commit cannot be completed since the group has already rebalanced and assigned the partitions to another member.

This means that the time between subsequent calls to poll() was longer than the configured max.poll.interval.ms, which typically implies that the poll loop is spending too much time message processing. You can address this either by increasing max.poll.interval.ms or by reducing the maximum size of batches returned in poll() with max.poll.records.

at org.apache.kafka.clients.consumer.internals.ConsumerCoordinator.sendOffsetCommitRequest(ConsumerCoordinator.java:1061)
```

To resolve the error, in the Kafka configuration file (e.g. `<kafka_dir>/config/connect-distributed.properties`), change either of the following properties:

`consumer.max.poll.interval.ms`
:   Increase the execution timeout to `900000` (900 seconds).

`consumer.max.poll.records`
:   Decrease the number of records loaded with each operation to `50`.

### Failure in Streaming Channel Offset Migration Response Error Code: 5023

When upgrading to the v2.1.0 (or higher) connector version, there was a change introduced in Snowpipe Streaming Channel name format. As a result, the logic detecting information about previously committed offsets
will not find any information about previously committed ones.
This will manifest as the following exception:

Copy code

```
com.snowflake.kafka.connector.internal.SnowflakeKafkaConnectorException: [SF_KAFKA_CONNECTOR] Exception: Failure in Streaming Channel Offset Migration Response Error Code: 5023

Detail: Streaming Channel Offset Migration from Source to Destination Channel has no/invalid response, please contact Snowflake Support

Message: Snowflake experienced a transient exception, please retry the migration request.
```

To resolve this error, in the Kafka configuration file (for example, `<kafka_dir>/config/connect-distributed.properties`), add the following configuration property:

`enable.streaming.channel.offset.migration`
:   Disable automatic offset migration by setting it to `false`.

### Configuring connector to support multiple topics

We have encountered an issue with a single kafka connector instance supporting a large number of topics, each having multiple partitions. The connector’s configuration, even though seemed to be valid, resulted in endless re-balance cycle without possibility to ingest any data into the Snowflake.
The issue was specific to Snowpipe Streaming ingestion mode (`snowflake.ingestion.method=SNOWPIPE_STREAMING`), but guidelines are also applicable to Snowpipe ingestion mode (`snowflake.ingestion.method=SNOWPIPE`).
The issue manifests itself in the log file by repeatedly logging this log message:

`[Worker-xyz] [timestamp] INFO [my-connector|task-id] [SF_INGEST] Channel is marked as closed`

This can typically happen when you configure your connector to ingest topics via regex.
We recommend applying the following set of options to the Kafka configuration file (for example, `<kafka_dir>/config/connect-distributed.properties`):

`consumer.override.partition.assignment.strategy`
:   Configure partition assignment strategy to tasks as `org.apache.kafka.clients.consumer.CooperativeStickyAssignor` - this will cause even distribution of ingested channels to available tasks, reducing the risk of re-balancing. Note that `CooperativeStickyAssignor` requires Kafka Connect version 3.0.1 or later because of [this known issue](https://issues.apache.org/jira/browse/KAFKA-12487).

`tasks.max`
:   The number of instantiated tasks per connector shouldn’t exceed number of available CPU’s - the underlying driver implements throttling mechanism based on the available CPU’s. Increasing number of concurrent requests will increase memory pressure on your system, but also will result in longer insert processing times, directly leading to missing connector’s heartbeats.

When speaking about connector’s timeout values, there is a set of configuration properties directly affecting these:

`consumer.override.heartbeat.interval.ms`
:   Defines how often the monitor thread (there is one associated with each task) will send heartbeat to Kafka. Default is `3000` ms, but in case of higher system load - you can experiment with increasing it to `5000` ms.

`consumer.override.session.timeout.ms`
:   Defines how long the broker will wait before assuming the consumer is in an invalid state and attempting re-balance. This setting should be typically 3 times higher than heartbeat interval, so if you configured heartbeat to `5000` ms, set this one to `15000` ms.

`consumer.override.max.poll.interval.ms`
:   Defines the maximum interval between call to `poll()` from underlying Kafka. The time spent between the polls basically maps to the connector processing batch of data (including upload to Snowflake and committing). In scenarios when you have multiple tasks processing data, underlying Snowflake Connection may start throttling requests, resulting in longer processing times. Depending on your scenario, you can increase this value to even 20 minutes (`1200000` ms) - especially when you start the connector with a large initial record count to be ingested.

`consumer.override.rebalance.timeout.ms`
:   When re-balance happens, in a scenario with large number of channels per task, there is a lot of underlying logic per channel to figure out where to resume processing. This code is executed sequentially, so the more channels per task, the longer initial setup will last. Configure this property to value large enough, to give each channel to complete its initialization. Value of 3 minutes (`180000` ms) is a good starting point.

It is also important to be aware of available heap memory for the connector. This is especially important in scenarios, where there are multiple connectors running simultaneously or you have one connector ingesting data from multiple topics. Each topic’s partition maps to a single channel and as such, requires memory.

Make sure you adjust your Kafka connect process memory settings via Xmx setting. One way of doing that is to define the
`KAFKA_OPTS` environment variable and set it accordingly (that is, `KAFKA_OPTS=-Xmx4G`).

### File cleaner purging files unexpectedly

When using the Kafka connector with SNOWPIPE, you might encounter an issue where you ingest data into a single table from multiple topics.
If your configuration doesn’t have the `snowflake.topic2table.map` entry or there is a 1:1 mapping between the topic and the table, this issue doesn’t apply.

The Kafka connector is generating files with records to be uploaded to a stage. These files are formatted according to the following pattern:
`snowflake_kafka_connector_<connector-name>_stage_<table-name>/<connector-name>/<table-name>/<partition-id>/<low-watermark>_<high-watermark>_<timestamp>.json.gz`. The issue is located in the `<partition-id>`: if multiple topics load data into a single table, duplicates are likely on the `partition-id` value. This is not a problem in a normal connector operation. However, if the connector restarts or rebalances, the cleaner process might inaccurately associate files loaded to stage (but not yet ingested) with the wrong partition and decide to delete them, which might result in a loss-of-data event.

The connector with version 2.5.0 fixes this issue by including the source topic’s hashcode in the `partition-id` to ensure unique file names that exactly match a single topic’s partition.
This fix is enabled by default - `snowflake.snowpipe.stageFileNameExtensionEnabled` - and affects only configurations where a target table is listed more than once in `snowflake.topic2table.map`.

If your configuration is affected by this functionality, you might end up having stale files uploaded to your stage. When the connector starts, it will check if your stage contains such files. You need to look for the log entries starting with `NOTE: For table`, followed by the list of detected files.

You can also check if there are some files affected at the stage manually:

1. Find the affected stage:

   Copy code

   ```
   show stages like 'snowflake_kafka_connector%<your table name>';
   ```
2. List the stage files:

   Copy code

   ```
   list @<your stage name> pattern = '.+/<your-table-name>/[0-9]{1,4}/[0-9]+_[0-9]+_[0-9]+\.json\.gz$';
   ```

The command above lists all files matching your table’s stage and having partition IDs in the range 0-9999.
These files won’t be ingested anymore, so you can download or delete them.

## Reporting issues

When contacting [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) for assistance, please have the following files available:

- Configuration file for your Kafka connector.

  Important

  Remove the private key before providing the file to Snowflake.
- Copy of the Kafka Connector log. Ensure that the file does not contain confidential or sensitive information.
- JDBC log file.

  To generate the log file, set the `JDBC_TRACE = true` environment variable on your Kafka Connect cluster before you run the Kafka
  connector.

  For more information about the JDBC log file, see
  [this article](https://community.snowflake.com/s/article/How-to-generate-log-file-on-Snowflake-connectors) in the Snowflake Community.
- Connect log file.

  To produce the log file, edit the `etc/kafka/connect-log4j.properties` file. Set the
  `log4j.appender.stdout.layout.ConversionPattern` property as follows:

  `log4j.appender.stdout.layout.ConversionPattern=[%d] %p %X{connector.context}%m (%c:%L)%n`

  Connector contexts are available in Kafka version 2.3 and higher.

  For more information, see the [Logging Improvements](https://www.confluent.io/blog/kafka-connect-improvements-in-apache-kafka-2-3/)
  information on the Confluent website.
