# ANOMALY\_INSIGHTS!GET\_MONITOR\_NOTIFICATION\_EMAILS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns the list of email addresses that receive a notification when an [anomaly monitor](/user-guide/cost-anomalies#label-cost-anomaly-monitors) detects a
cost anomaly.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_MONITOR_NOTIFICATION_EMAILS(
  '<alias>' )
```

## Arguments

`'alias'`
:   Name of the monitor. The name isn’t case-sensitive.

    Data type: VARCHAR

## Output

Returns a VARCHAR that contains a comma-delimited list of the email addresses currently associated with the monitor.

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role

## Usage notes

- The method fails if no monitor with the specified name exists in the account.
- To change the list, use [ANOMALY\_INSIGHTS!SET\_MONITOR\_NOTIFICATION\_EMAILS](/sql-reference/classes/anomaly-insights/methods/set_monitor_notification_emails).

## Example

Return the notification list for the monitor named `Eng-Platform`:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_MONITOR_NOTIFICATION_EMAILS('Eng-Platform');
```
