# ANOMALY\_INSIGHTS!ADD\_NOTIFICATION\_INTEGRATION

Registers a [notification integration](/sql-reference/sql/create-notification-integration) to receive notifications, such as
Slack messages or pager alerts, when there is a [cost anomaly](/user-guide/cost-anomalies). You can register an integration
for account-level anomalies, organization-level anomalies, or both.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!ADD_NOTIFICATION_INTEGRATION(
  '<integration_name>',
  '<anomaly_scope>' )
```

## Arguments

`'integration_name'`
:   Name of an existing [notification integration](/sql-reference/sql/create-notification-integration) in the account. The integration
    must be accessible to the role that calls this method.

`'anomaly_scope'`
:   Specifies the anomaly level that the notification integration is registered for. The value is case-insensitive and must be one of
    the following:

    - `ACCOUNT`: Sends a notification when there is an [account-level cost anomaly](/user-guide/cost-anomalies#label-cost-anomaly-level).
    - `ORG`: Sends a notification when there is an [organization-level cost anomaly](/user-guide/cost-anomalies#label-cost-anomaly-level).

## Output

Returns a VARCHAR status message:

- `Integration added successfully` if the integration is registered.
- `Integration already registered for anomaly scope <anomaly_scope>` if the integration is already registered for the specified
  anomaly scope (for example, `Integration already registered for anomaly scope ACCOUNT`).

## Access control requirements

To register an integration for an account-level cost anomaly (`ACCOUNT` scope), users with any of the following roles can call this
method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role

To register an integration for an organization-level cost anomaly (`ORG` scope), users with any of the following roles can call this
method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.ORGANIZATION\_BILLING\_VIEWER application role in the organization account
- SNOWFLAKE.APP\_ORGANIZATION\_BILLING\_VIEWER application role in an ORGADMIN-enabled account

In addition, you must grant the following privileges to the SNOWFLAKE application:

- The USAGE privilege on the notification integration.

If the notification integration is for a webhook that uses a secret object, you must also grant the following privileges to the
SNOWFLAKE application:

- The READ privilege on that secret.
- The USAGE privilege on the schema containing that secret.
- The USAGE privilege on the database containing that schema.

## Usage notes

- Anomaly Insights notification integrations must be enabled for the account. If the feature isn’t enabled, this method raises an
  exception.
- If the integration is already registered for the specified anomaly scope, the call is a no-op and no error is raised.
- A maximum of 20 notification integrations can be registered per account, counted across all anomaly scopes. If the maximum is
  reached, this method raises an exception.
- After a successful call, a confirmation test message is attempted to verify that the notification integration is configured
  correctly. Registration still succeeds even if the confirmation message can’t be delivered.
- This method raises an exception if the anomaly scope is invalid, if the notification integration doesn’t exist or isn’t
  accessible to the caller, or if the caller’s role isn’t permitted to register integrations for the requested anomaly scope.

## Example

Register a notification integration named `my_slack_integration` to receive notifications when there is an account-level cost
anomaly:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!ADD_NOTIFICATION_INTEGRATION(
  'my_slack_integration',
  'ACCOUNT');
```
