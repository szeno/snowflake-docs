Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SERVERLESS\_ALERT\_HISTORY view

This Account Usage view can be used to query the [serverless alert](/user-guide/alerts#label-alerts-serverless-compute) usage history.
The information returned by the view includes the serverless alert name and credits consumed by serverless alert usage.

See also:
:   [SERVERLESS\_ALERT\_HISTORY function](/sql-reference/functions/serverless_alert_history)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range. |
| CREDITS\_USED | VARCHAR | Number of credits billed for serverless alert usage during the START\_TIME and END\_TIME window. |
| ALERT\_ID | NUMBER | Internal/system-generated identifier for the serverless alert. |
| ALERT\_NAME | VARCHAR | Name of the serverless alert. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the serverless alert. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the serverless alert. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database that contains the serverless alert. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the serverless alert. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

## Example

The following SQL statement queries for the credits used by the two most recent executions of serverless alerts:

Copy code

```
SELECT
    start_time,
    end_time,
    alert_id,
    alert_name,
    credits_used,
    schema_id,
    schema_name,
    database_id,
    database_name,
  FROM SNOWFLAKE.ACCOUNT_USAGE.SERVERLESS_ALERT_HISTORY
  LIMIT 2;
```

```
+---------------------------------+---------------------------------+----------+---------------------+--------------+-----------+-------------+-------------+---------------+
|           START_TIME            |            END_TIME             | ALERT_ID |     ALERT_NAME      | CREDITS_USED | SCHEMA_ID | SCHEMA_NAME | DATABASE_ID | DATABASE_NAME |
+---------------------------------+---------------------------------+----------+---------------------+--------------+-----------+-------------+-------------+---------------+
| Tue, 10 Sep 2024 17:57:00 -0700 | Tue, 10 Sep 2024 17:58:00 -0700 | 202      | MY_SERVERLESS_ALERT | 0.000869065  | 52        | SCTEST      | 30          | DBTEST        |
| Tue, 10 Sep 2024 18:57:00 -0700 | Tue, 10 Sep 2024 18:58:00 -0700 | 202      | MY_SERVERLESS_ALERT | 0.000841918  | 52        | SCTEST      | 30          | DBTEST        |
+---------------------------------+---------------------------------+----------+---------------------+--------------+-----------+-------------+-------------+---------------+
```
