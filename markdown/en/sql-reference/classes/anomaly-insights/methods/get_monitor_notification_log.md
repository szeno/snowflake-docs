# ANOMALY\_INSIGHTS!GET\_MONITOR\_NOTIFICATION\_LOG

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns the notifications that were sent for an [anomaly monitor](/user-guide/cost-anomalies#label-cost-anomaly-monitors) during a specified time period.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_MONITOR_NOTIFICATION_LOG(
  '<alias>',
  '<start_date>',
  '<end_date>' )
```

## Arguments

`'alias'`
:   Name of the monitor. The name isn’t case-sensitive.

    Data type: VARCHAR

`'start_date'`
:   Specifies the beginning of the time period for which notification history is returned.

    Data type: DATE

`'end_date'`
:   Specifies the end of the time period for which notification history is returned.

    Data type: DATE

## Output

Returns a table with one row per notification, with the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| NOTIFICATION\_TYPE | VARCHAR | Type of notification that was sent. Monitors support `EMAIL` only. |
| LOG\_ID | VARCHAR | System-generated identifier for the notification. |
| ANOMALY\_DATE | DATE | Day of the cost anomaly that triggered the notification. |
| SENT\_AT | TIMESTAMP | Time when the notification was sent. |
| RECIPIENTS | VARCHAR | Email addresses that the notification was sent to. |

Expand

Show lessSee more

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role

## Usage notes

- Notification records are retained for 180 days. Older records are removed automatically.
- The notification history isn’t directly queryable. Use this method to retrieve it.

## Example

Return the notifications sent for the monitor `Eng-Platform` between January 1, 2026, and March 31, 2026:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_MONITOR_NOTIFICATION_LOG(
  'Eng-Platform', '2026-01-01', '2026-03-31');
```
