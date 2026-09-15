# ANOMALY\_INSIGHTS!GET\_NOTIFICATION\_INTEGRATIONS

Returns the [notification integrations](/sql-reference/sql/create-notification-integration) that are registered to receive
[cost anomaly](/user-guide/cost-anomalies) notifications for the specified anomaly scope.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_NOTIFICATION_INTEGRATIONS(
  '<anomaly_scope>' )
```

## Arguments

`'anomaly_scope'`
:   Specifies the anomaly level to return registered notification integrations for. The value is case-insensitive and must be one of
    the following:

    - `ACCOUNT`: Returns the integrations registered for [account-level cost anomalies](/user-guide/cost-anomalies#label-cost-anomaly-level).
    - `ORG`: Returns the integrations registered for [organization-level cost anomalies](/user-guide/cost-anomalies#label-cost-anomaly-level).

## Output

Returns a table with the following columns, ordered by registration time in descending order. If no integrations are registered for
the specified anomaly scope, the table is empty.

| Column name | Data type | Description |
| --- | --- | --- |
| INTEGRATION\_NAME | VARCHAR | Name of the registered notification integration. |
| LAST\_SUCCESSFUL\_NOTIFICATION | TIMESTAMP\_TZ | Timestamp of the most recent successful notification sent to the integration. The value is NULL if no notification has been sent. |
| ADDED\_TIMESTAMP | TIMESTAMP\_TZ | Timestamp when the notification integration was registered. |

Expand

Show lessSee more

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role
- SNOWFLAKE.APP\_USAGE\_VIEWER application role
- SNOWFLAKE.ORGANIZATION\_BILLING\_VIEWER application role in the organization account
- SNOWFLAKE.APP\_ORGANIZATION\_BILLING\_VIEWER application role in an ORGADMIN-enabled account

## Usage notes

- Anomaly Insights notification integrations must be enabled for the account. If the feature isn’t enabled, this method raises an
  exception.
- This method raises an exception if the anomaly scope is invalid.
- This method doesn’t validate whether the underlying notification integration objects still exist in the account.

## Example

Return the notification integrations registered for account-level cost anomalies:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_NOTIFICATION_INTEGRATIONS('ACCOUNT');
```
