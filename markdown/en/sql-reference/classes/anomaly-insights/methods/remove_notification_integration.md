# ANOMALY\_INSIGHTS!REMOVE\_NOTIFICATION\_INTEGRATION

Removes a [notification integration](/sql-reference/sql/create-notification-integration) that was previously registered to receive
[cost anomaly](/user-guide/cost-anomalies) notifications for the specified anomaly scope.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!REMOVE_NOTIFICATION_INTEGRATION(
  '<integration_name>',
  '<anomaly_scope>' )
```

## Arguments

`'integration_name'`
:   Name of the registered notification integration to remove.

`'anomaly_scope'`
:   Specifies the anomaly level that the notification integration is removed from. The value is case-insensitive and must be one of
    the following:

    - `ACCOUNT`: Removes the integration from [account-level cost anomaly](/user-guide/cost-anomalies#label-cost-anomaly-level) notifications.
    - `ORG`: Removes the integration from [organization-level cost anomaly](/user-guide/cost-anomalies#label-cost-anomaly-level) notifications.

## Output

Returns a VARCHAR status message:

- `Integration removed successfully` if the integration was removed.
- `No matching integration found for anomaly scope <anomaly_scope>` if no matching registration exists for the specified anomaly
  scope (for example, `No matching integration found for anomaly scope ACCOUNT`).

## Access control requirements

To remove an integration for an account-level cost anomaly (`ACCOUNT` scope), users with any of the following roles can call this
method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role

To remove an integration for an organization-level cost anomaly (`ORG` scope), users with any of the following roles can call this
method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.ORGANIZATION\_BILLING\_VIEWER application role in the organization account
- SNOWFLAKE.APP\_ORGANIZATION\_BILLING\_VIEWER application role in an ORGADMIN-enabled account

## Usage notes

- Anomaly Insights notification integrations must be enabled for the account. If the feature isn’t enabled, this method raises an
  exception.
- If no matching registration exists for the specified anomaly scope, the call returns a descriptive message and no error is raised.
- The integration name doesn’t need to refer to a notification integration object that still exists.
- If removing the integration leaves no active notification channels or integrations, the daily anomaly notification task is
  suspended.
- This method raises an exception if the anomaly scope is invalid or if the caller’s role isn’t permitted to modify integrations
  for the requested anomaly scope.

## Example

Remove the notification integration named `my_slack_integration` from account-level cost anomaly notifications:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!REMOVE_NOTIFICATION_INTEGRATION(
  'my_slack_integration',
  'ACCOUNT');
```
