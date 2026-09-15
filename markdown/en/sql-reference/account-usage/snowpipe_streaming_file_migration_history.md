Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SNOWPIPE\_STREAMING\_FILE\_MIGRATION\_HISTORY view

This Account Usage view can be used to query the history of data migrated into Snowflake tables using [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview) within the last 365 days (1 year). The view displays the number of rows and bytes migrated and credits used for migration billed for your entire Snowflake account.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the time (in the local time zone) range in which data migration took place. |
| END\_TIME | TIMESTAMP\_LTZ | End of the time (in the local time zone) range in which data migration took place. |
| CREDITS\_USED | FLOAT | Number of credits billed for Snowpipe Streaming data migration during the START\_TIME and END\_TIME window. |
| NUM\_BYTES\_MIGRATED | NUMBER | Number of bytes migrated during the START\_TIME and END\_TIME window. |
| NUM\_ROWS\_MIGRATED | NUMBER | Number of rows migrated during the START\_TIME and END\_TIME window. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the target table that the Snowpipe Streaming client loads data into. |
| TABLE\_NAME | VARCHAR | The name of the target table that the Snowpipe Streaming client loads data into. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that the target table belongs to. |
| SCHEMA\_NAME | VARCHAR | The name of the schema that the target table belongs to. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that the target table belongs to. |
| DATABASE\_NAME | VARCHAR | The name of the database that the target table belongs to. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 12 hours.

- Note that file migration sometimes may be pre-empted by clustering or other DML operations. Migration may not always occur and therefore the migration history will be empty even after 12 hours.
- The NUM\_BYTES\_MIGRATED and NUM\_ROWS\_MIGRATED columns only show the number of bytes and rows processed during the migration process. These numbers may not equal the actual numbers of rows and bytes inserted by Snowpipe Streaming to the table because some rows and bytes are processed outside of the migration process due to clustering or other DML operations.

  For example, Snowpipe Streaming inserts 1M rows and the table has 1M rows, but the NUM\_ROWS\_MIGRATED column in the migration history view only shows 800K rows. This is because the other 200K rows are processed outside of the migration process.

## Examples

Query the history of data migrated into Snowflake tables using Snowpipe Streaming within the last 365 days.

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.SNOWPIPE_STREAMING_FILE_MIGRATION_HISTORY;
```

The query returns the following results.

> Copy code
>
> ```
> +-------------------------------+-------------------------------+--------------+--------------------+------------------+----------+-----------------+------------+--------------+---------------+--------------+
> | START_TIME                    | END_TIME                      | CREDITS_USED | NUM_BYTES_MIGRATED | NUM_ROWS_MIGRATED| TABLE_ID |      TABLE_NAME | SCHEMA_ID  |  SCHEMA_NAME |   DATABASE_ID | DATABASE_NAME|
> |-------------------------------+-------------------------------+--------------+--------------------+------------------+----------+----------------------------------------------------------------------------|
> |2023-02-08 19:00:00.000 +0000  |2023-02-08 20:00:00.000 +0000  | 0.0000325    |                 0  |                0 |  16849926| STREAMING_TABLE |   101351   |   SNOW       |  3166         |STREAMING     |
> |2023-02-07 19:00:00.000 +0000  |2023-02-07 20:00:00.000 +0000  | 0.000096761  |             7,850  |               39 |  16849926| STREAMING_TABLE |   101351   |   SNOW       |  3166         |STREAMING     |
> +-------------------------------+-------------------------------+--------------+--------------------+------------------+----------+-----------------+------------+--------------+---------------|--------------+
> ```
