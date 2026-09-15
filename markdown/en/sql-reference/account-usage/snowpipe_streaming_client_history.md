Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SNOWPIPE\_STREAMING\_CLIENT\_HISTORY view

This Account Usage view can be used to query the amount of time spent loading data into Snowflake tables using [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview) within the last 365 days (1 year). The view displays the amount of data loaded and timestamp of the Snowpipe Streaming client calls for your entire Snowflake account.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| CLIENT\_NAME | VARCHAR | Name of the Snowpipe Streaming ingest client. |
| SNOWFLAKE\_PROVIDED\_ID | VARCHAR | Internal/system-generated identifier for the Snowpipe Streaming ingest client used for the data load. |
| EVENT\_TIMESTAMP | TIMESTAMP\_LTZ | Start of the time (in the local time zone) range in which data loading took place. |
| EVENT\_TYPE | VARCHAR | Type of the event. |
| BLOB\_SIZE\_BYTES | NUMBER | The blob size in bytes. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).

## Examples

Query the amount of time spent loading data into Snowflake tables using Snowpipe Streaming within the last 365 days.

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.SNOWPIPE_STREAMING_CLIENT_HISTORY;
```

The query returns the following results.

> Copy code
>
> ```
> +----------------+----------------------------+------------------------------+--------------+----------------+
> |    CLIENT_NAME |    SNOWFLAKE_PROVIDED_ID   |              EVENT_TIMESTAMP |   EVENT_TYPE | BLOB_SIZE_BYTES|
> |----------------+--------------------------- +------------------------------+--------------|----------------|
> |      MY_CLIENT |FE0B1xJrBAAL3bAAUz1M9876nMCd| 2023-02-04 02:07:34.000 +0000| BLOB_PERSIST |           1,648|
> |      MY_CLIENT |D1CIBBPGGFyprBanMvAA1234V3ss| 2023-02-04 02:15:54.000 +0000| BLOB_PERSIST |           3,120|
> +----------------+----------------------------+------------------------------+--------------+----------------+
> ```

Query the hourly credits consumed by each client loading data into Snowflake tables using Snowpipe Streaming within the last 365 days.

Copy code

```
SELECT COUNT(DISTINCT event_timestamp) AS client_seconds, date_trunc('hour',event_timestamp) AS event_hour, client_seconds*0.000002777777778 as credits, client_name, snowflake_provided_id
FROM SNOWFLAKE.ACCOUNT_USAGE.SNOWPIPE_STREAMING_CLIENT_HISTORY
GROUP BY event_hour, client_name, snowflake_provided_id;
```

Note that there can be multiple events per second. The credits are consumed only by the actual time spent, and not by the number of events.
