# Costs for Snowpipe Streaming Classic

With Snowpipe Streaming’s serverless compute model, users can stream any data volume without managing a virtual warehouse. Instead, Snowflake provides and manages the compute resources, automatically growing or shrinking capacity based on the current Snowpipe Streaming load.

For Snowpipe Streaming Classic, accounts are charged based on the per-second time that serverless compute and active client streaming ingestion uses. Be aware of the following:

- File migration occurs asynchronously from streaming ingestion.
- File migration might be pre-empted by clustering or other DML operations.
- File migration might not always occur, and therefore compute costs might be reduced.
- For Snowflake-managed Apache Iceberg™ tables, file migration operates similarly to Iceberg table maintenance to create new compacted Parquet files, if necessary.

For more information, see the “Serverless Feature Credit Table” in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

## Estimating Snowpipe Streaming charges

Given the number of factors that can differentiate Snowpipe Streaming loads, it is very difficult for Snowflake to provide sample costs. Size of records, number of records, data types, etc. can affect the compute resource consumption for file migration. Client charges are dictated only by how many clients are actively writing data to Snowflake on a per-second basis.

We suggest that you experiment by performing a typical streaming ingestion load to estimate future charges.
To see a sample streaming ingestion experiment with estimated costs, see [this blog post](https://www.snowflake.com/blog/data-ingestion-best-practices-part-three/).

## Temporary file storage and billing

Although the Snowpipe Streaming API is designed to write rows directly to Snowflake tables without requiring users to explicitly stage files, in Snowpipe Streaming Classic, Snowflake’s internal processes use a transparent internal stage for temporary buffering of data. The Snowpipe Streaming with classic architecture SDK generates and uploads intermediate files to this internal stage before they are transformed into Snowflake’s native file format.

Snowflake bills you for the storage that is consumed by these temporary files in the internal stage. This storage cost is separate from the Snowpipe Streaming serverless compute cost and appears under the general “storage cost” on your Snowflake bill.

The retention period for these temporary files in the internal stage is directly associated with the data retention time for the target table (or the account-level retention if no specific table retention is set). Snowflake automatically deletes these files after they fall outside of the defined Time Travel window. Typically, this deletion occurs within one day of the data exiting the retention period. Users don’t have direct access to, or visibility into, these internal stage files.

## Cloning tables with Snowpipe Streaming

When users clone a table that is actively receiving data through Snowpipe Streaming with classic architecture, users might observe higher storage costs. This additional cost isn’t because of duplication of the underlying data files. Snowflake performs zero-copy cloning. Instead, it’s because data in flight – data that was processed by the Snowpipe Streaming with classic architecture SDK and is temporarily stored in the internal stage but not yet fully committed to the target table – requires a file migration for both the original table and the clone. This double processing of temporary files increases file migration consumption and leads to greater storage usage. This additional cost is typically very small, reflecting a maximum of about 5 minutes of temporary files, but could be larger with very high throughput if the system is experiencing delays in these migrations. This duplication contributes to increased storage consumption.

In contrast, Snowpipe Streaming with a high-performance architecture offers true zero-copy cloning for tables that actively receive streaming data. With the high-performance architecture, cloning operations behave like standard Snowflake table clones. This means that only new data written after the clone operation consumes additional storage. Data in flight at the time of cloning isn’t subject to this dual migration. As a result, you benefit from cost-efficient cloning for streaming tables.

## Viewing the data load history for your account

Account administrators (users with the ACCOUNTADMIN role) or users with a role granted the MONITOR USAGE global privilege can use SQL commands to view the credits billed to your Snowflake account within a specified date range. You can use the following views to query the history of data migrated into Snowflake tables, the amount of time spent loading data into Snowflake tables using Snowpipe Streaming, and the credits consumed.

To view the total Snowpipe Streaming costs, including both compute and client costs, query the metering history when the `SERVICE_TYPE` is set to `SNOWPIPE_STREAMING`.

> - [METERING\_HISTORY view](/sql-reference/account-usage/metering_history) (in [Account Usage](/sql-reference/account-usage)).

For more information about querying the total Snowpipe Streaming costs, see [a SQL example](/user-guide/cost-exploring-compute#label-cost-explore-query-snowpipe-streaming).

To see the detailed breakdowns of client ingestion and migration compute, you can query the following views:

> - [SNOWPIPE\_STREAMING\_CLIENT\_HISTORY view](/sql-reference/account-usage/snowpipe_streaming_client_history) (in [Account Usage](/sql-reference/account-usage)).
> - [SNOWPIPE\_STREAMING\_FILE\_MIGRATION\_HISTORY view](/sql-reference/account-usage/snowpipe_streaming_file_migration_history) (in [Account Usage](/sql-reference/account-usage)).
