Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# EVENT\_USAGE\_HISTORY view

Deprecated Feature

> The EVENT\_USAGE\_HISTORY view has been deprecated. Use the [METERING\_DAILY\_HISTORY view](/sql-reference/account-usage/metering_daily_history) and
> [METERING\_HISTORY view](/sql-reference/account-usage/metering_history) views instead.

This view can be used to query the history of data loaded into Snowflake event tables within the last 365 days (1 year).

The view displays the history of data loaded and credits billed for your entire Snowflake account.

For more information about event tables, refer to [Event table overview](/developer-guide/logging-tracing/event-table-setting-up).

For more information about logging and tracing, refer to [Logging, tracing, and metrics](/developer-guide/logging-tracing/logging-tracing-overview).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the time range (in the UTC time zone) in which data loading took place. |
| END\_TIME | TIMESTAMP\_LTZ | End of the time range (in the UTC time zone) in which data loading took place. |
| CREDITS\_USED | NUMBER | Number of credits billed for loading data into the event table during the START\_TIME and END\_TIME window. |
| BYTES\_INGESTED | NUMBER | Number of bytes of data loaded during the START\_TIME and END\_TIME window. |

Expand

Show lessSee more

## Usage notes

Latency for the view may be up to 180 minutes (3 hours).
