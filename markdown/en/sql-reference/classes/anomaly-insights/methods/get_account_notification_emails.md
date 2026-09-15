# ANOMALY\_INSIGHTS!GET\_ACCOUNT\_NOTIFICATION\_EMAILS

Returns the email addresses where notifications are sent when there is an [account-level cost anomaly](/user-guide/cost-anomalies#label-cost-anomaly-level) in
the current account.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_ACCOUNT_NOTIFICATION_EMAILS()
```

## Arguments

None.

## Output

Returns a table with the following column:

| Column name | Data type | Description |
| --- | --- | --- |
| EMAIL\_LIST | VARCHAR | Comma-delimited list of email addresses where notifications are sent when there is a cost anomaly in the current account. |

Expand

Show lessSee more

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role

## Usage notes

This method retrieves the email notification list for the account in which it is called.

## Example

The following example returns the email addresses where notifications are sent.

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_ACCOUNT_NOTIFICATION_EMAILS();
```
