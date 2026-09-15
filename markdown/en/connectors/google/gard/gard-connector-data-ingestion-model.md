# Data ingestion model for the Snowflake Connector for Google Analytics Raw Data

This topic provides information on the data ingestion models supported by the Snowflake Connector for Google Analytics Raw Data.

## Google Analytics to BigQuery export

Google Analytics supports three types of BigQuery exports:
:   - Daily: Google Analytics exports data to tables named in the `events_XXXXXX` format. Tables are created once daily, after the end of the day, when all the events for the given day are collected.
    - Fresh Daily: Google Analytics exports data to tables named in the `events_fresh_XXXXXX` format. Tables are created and refreshed according to the scheduler, with a maximum frequency of once per hour. This feature is available only for the Google Analytics 360 customers.
    - Streaming: Google Analytics continuously exports data throughout the day, and stores it in a table named in the `events_intraday_XXXXXX` format.
    - Users: Google Analytics export containing user data related to the collected events. Tables are stored in BigQuery and named in the `users_XXXXXX` and `pseudonymous_users_XXXXXX` formats.

The connector supports these three types of exports and automatically downloads all the tables it finds in BigQuery, without requiring any additional configuration.

## Sink tables

For each property, the connector saves the events into property-specific tables, which are created in a database and a schema provided during connector configuration.

For each of the properties, there might be up to four sink tables created, depending on which export types were enabled. The tables are named as follows:

> - `ANALYTICS_<propertyId>`
> - `ANALYTICS_INTRADAY_<propertyId>`
> - `USERS_<propertyId>`
> - `PSEUDONYMOUS_USERS_<propertyId>`

## Daily table ingestion

The connector downloads the entire table in a single run when it recognizes the table is present in BigQuery. Google cautions the daily tables can be updated up to 72 hours after the table was created.
To ensure data consistency, the connector reloads tables after 72 hours, (Note that the exact reload time is dependent on the connector ingestion schedule).
Updates in BigQuery made after 72 hours since table creation, won’t be reflected in Snowflake. Such tables can be reloaded manually, using one of the [RELOAD\_PROPERTY](/connectors/google/gard/gard-connector-setting-up-data#label-reloading-property-procedures) procedures.

## Fresh Daily table ingestion

After every successful ingestion run of the connector, reloads are continuously created to reload the table for up to 96 hours, 24 hours on the day the
table is created and 72 hours when data updates can occur). Reloads will follow each successful ingestion run, triggered after every dispatcher run,
with a maximum frequency of once per hour. The last reload date is calculated based on the table name and the allocated 96-hour period.

If a fresh daily ingestion needs to catch up, for instance due to a connector pause, the connector will ingest all the tables sequentially.
Reloads will not be created if they are unnecessary, that is, if more than 96 hours have passed since the table was created.

This feature is available only for the Google Analytics 360 customers. Fresh daily exports can be enabled manually by using the `ENABLE_PROPERTIES` or `UPDATE_INGESTION_OPTIONS` procedures.

## Intraday ingestion

The connector supports downloading historical intraday tables (if they are present in BigQuery) and ongoing ingestion of intraday tables still receiving updates.

For past days, the connector downloads intraday tables the same way it foes daily ones – each table is downloaded in whole, one table at a time, until the process reaches the present day’s data.

When the connector recognizes that an intraday table is the last one in BigQuery, it starts processing the table incrementally. This means it downloads incoming batches of data from the table throughout the day, at a constant interval, which is 8 hours by default.

When any of the following conditions are met:

> - A next-day table appeared in the BigQuery dataset
> - 24 hours passed since the first load for the given table

the connector does a final ingestion for the given intraday table and switches to the next one.

Note

A small number of events may not be ingested if events are delayed more than 10 minutes. Immediately after the incremental load of a intraday table is finished, the connector verifies whether there are any lost events, and if so schedules a table reload to ensure data consistency between Snowflake and BigQuery.

## User data tables ingestion

User data table ingestion is based on the same mechanism as daily tables ingestion.

## Scheduling

Connector checks whether new tables exist in BigQuery and then schedules ingestions of them (or its parts in case of incremental intraday ingestions) into Snowflake when:

> - Task is triggered according to configured schedule
>   :   - By default it is every 8 hours
>       - Using [CONFIGURE\_INGESTION\_INTERVAL](/connectors/google/gard/gard-connector-managing#label-configure-ingestion-interval) you can change the default interval value if you need more/less frequent updates.
> - Connector finished ingestion of last scheduled table
>   :   - In consequence, this means that schedules are more frequent than it stems from the configuration, since there should be at least one ingestion per day, which means at least one extra check.
>       - In particular, when there is initial load ongoing, and there are a lot of tables to ingest, after ingesting each of the tables, the scheduling mechanism is triggered.
