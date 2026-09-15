# ANOMALY\_INSIGHTS!GET\_ORG\_NOTIFICATION\_EMAILS

Returns the email addresses where notifications are sent when there is an [organization-level cost anomaly](/user-guide/cost-anomalies#label-cost-anomaly-level).
An organization-level anomaly occurs when the aggregate consumption for all accounts falls outside an expected range.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_ORG_NOTIFICATION_EMAILS()
```

## Arguments

None.

## Output

Returns a table with the following column:

| Column name | Data type | Description |
| --- | --- | --- |
| EMAIL\_LIST | VARCHAR | Comma-delimited list of email addresses where notifications are sent when there is an organization-level cost anomaly. |

Expand

Show lessSee more

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.ORGANIZATION\_BILLING\_VIEWER application role in the organization account
- SNOWFLAKE.APP\_ORGANIZATION\_BILLING\_VIEWER application role in an ORGADMIN-enabled account

## Example

The following example returns the list of email addresses that are notified when there is an organization-level cost anomaly.

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_ORG_NOTIFICATION_EMAILS();
```
