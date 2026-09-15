# Troubleshooting the Snowflake Connector for Google Analytics Raw Data

This topic provides guidelines for troubleshooting issues with the Snowflake Connector for Google Analytics Raw Data.

## Verifying a connection to the Google Cloud Platform (GCP) instance

To verify that the Snowflake Connector for Google Analytics Raw Data can access the Google Cloud Platform (GCP) instance, call the
`CONNECTION_STATUS` stored procedure, which is defined in the PUBLIC schema of the connector installation database:

Copy code

```
CALL CONNECTION_STATUS();
```

To check the connection status in Snowsight, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Select the Snowflake Connector for Google Analytics Raw Data.

The color of the icon in the Authenticate Google Cloud Platform section shows if the connection to GCP was successful. If the icon is red,
the attempt to connect to GCP failed. To try reconnecting, select **Reauthenticate**.

If the icon is green, the connector is ready to ingest data.

## Checking connector status

To examine connector status use the `GET_CONNECTOR_STATUS` stored procedure, as shown:

Copy code

```
CALL PUBLIC.GET_CONNECTOR_STATUS()
```

## Checking current ingestion status

If you’re missing data from a particular day, you can query the `CONNECTOR_STATS` view to see whether there have been any errors when trying to ingest that day’s table from BigQuery:

Copy code

```
SELECT * FROM CONNECTOR_STATS WHERE PROPERTY_ID = '<property_name>' AND BIG_QUERY_TABLE = 'events_<date>' ORDER BY RUN_START_TIME DESC;
```

The result will show all attempts to download a particular table from BigQuery’s dataset for a particular property, with the latest one at the top. The `STATUS` column will show the outcome, and for any failed attempt, the `ERROR_MESSAGES` column will detail what happened.

## Downloading connector logs

If you encounter problems with the connector, you can call the
`GET_TROUBLESHOOTING_DATA` stored procedure, which is defined in the PUBLIC schema of the connector installation database:

Copy code

```
CALL GET_TROUBLESHOOTING_DATA(7);
```

The parameter defines how many days in the past since now should be included in the logs. Please use 7 as a default unless support asks you to use a different value.

As a result, you get the full connector logs. You can download the logs, filter, and share the logs with the application provider.

## Sharing connector logs from an event table with an application provider

It is possible to share connector logs stored in the event table with the application provider. This could be used by the provider to investigate encountered problems with the connector. Click this link to read more about [consumer enable logging](https://other-docs.snowflake.com/en/native-apps/consumer-enable-logging/).

Note

This feature would not work without [enabling event tables](/developer-guide/logging-tracing/event-table-setting-up) on the account.

To enable sharing application events from the event table run:

Copy code

```
ALTER APPLICATION <GARD APPLICATION NAME> SET SHARE_EVENTS_WITH_PROVIDER = TRUE;
```

To stop sharing run:

Copy code

```
ALTER APPLICATION <GARD APPLICATION NAME> SET SHARE_EVENTS_WITH_PROVIDER = FALSE;
```

Current status could be checked by running:

Copy code

```
DESC APPLICATION <GARD APPLICATION NAME>;
```

## Comparing row counts in Google Cloud Platform (GCP) and Snowflake

To check if the ingestion was correct, you can compare the row counts in Snowflake and Google Cloud Platform (GCP).

To check the row count in Snowflake, run the following query:

Copy code

```
SELECT COUNT(*) FROM analytics_<property_name> WHERE source_table_date = '<date>' WHERE INGESTION_COMPLETE = true;
```

To check the row count in GCP, run the following query:

Copy code

```
SELECT COUNT(*) FROM '<project_id>.analytics_<property_name>.events_<date>';
```
