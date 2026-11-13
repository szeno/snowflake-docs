# Notifications and actions for per-user quotas

A per-user quota can notify users and administrators as spending approaches or exceeds a threshold,
and it can run stored procedures as custom actions. This topic covers notifications, custom actions,
cycle-start actions, and the events Snowflake records for them. Thresholds are a percentage of the
per-user limit, evaluated on actual or projected spend. For more information, see
[Threshold types](/user-guide/budgets/per-user-quotas#label-per-user-quota-threshold-types).

## Configure notifications

Quotas support two types of notifications: individual user notifications that alert users when
they approach or exceed thresholds, and admin summary notifications that provide aggregated
reports to administrators.

### Notify individual users

You can configure notifications that are sent to individual users when they cross specified
thresholds of their per-user quota. For each threshold, you specify the following:

- The threshold percentage (for example, `80` for 80% of the quota).
- The threshold type: `PROJECTED` (default) or `ACTUAL`.
- Whether to notify the user directly (`TRUE` or `FALSE`).
- Which limit the notification is based on (`'MONTHLY'`, `'WEEKLY'`, or `'DAILY'`).

Add a notification threshold:

Copy code

```
CALL my_quota!ADD_NOTIFICATION_THRESHOLD(80, 'PROJECTED', TRUE, 'MONTHLY');
```

Remove a notification threshold:

Copy code

```
CALL my_quota!REMOVE_NOTIFICATION_THRESHOLD(80, 'PROJECTED');
```

View all configured notification thresholds:

Copy code

```
CALL my_quota!GET_NOTIFICATION_THRESHOLDS();
```

The method returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| `THRESHOLD` | `NUMBER` | Threshold percentage at which the notification is triggered. |
| `SPEND_STRATEGY` | `VARCHAR` | Type of threshold: `PROJECTED` or `ACTUAL`. |
| `NOTIFY_USER` | `BOOLEAN` | Indicates whether the user is notified when they cross the threshold. |
| `ADDED_TIMESTAMP` | `TIMESTAMP_TZ(9)` | Indicates when the notification was added. |

Expand

Show lessSee more

Note

- Notifications for projected spend thresholds are sent at most once per threshold within a
  24-hour period. If a user stays projected to cross the threshold, Snowflake sends the notification
  again once every 24 hours.
- Notifications for actual spend thresholds are sent at most once per quota cycle, when the user’s
  spend crosses the threshold.

### Send admin summaries

Quota admins can configure admin summary notifications to receive aggregated reports of users
who breach per-user quota thresholds. A summary is sent after a quota evaluation when new
threshold breaches are detected.

Each summary includes the following information:

- User name
- Threshold breached
- Threshold type (Actual or Projected)
- User credit usage at evaluation time

Snowflake delivers summaries through a notification integration, a list of email recipients, or
both. If neither is configured, summary notifications are suppressed.

Configure a notification integration for admin summaries:

Copy code

```
CALL my_quota!ADD_NOTIFICATION_INTEGRATION('my_notification_integration');
```

`ADD_NOTIFICATION_INTEGRATION` accepts only webhook and queue notification integrations, including Amazon SNS, Azure Event Grid, and Google Cloud Pub/Sub queue integrations. Email integrations (`TYPE = EMAIL`) aren’t accepted. To send admin summaries by email, use `SET_ADMIN_EMAILS`.

Remove the notification integration:

Copy code

```
CALL my_quota!REMOVE_NOTIFICATION_INTEGRATION('my_notification_integration');
```

View configured notification integrations:

Copy code

```
CALL my_quota!GET_NOTIFICATION_INTEGRATIONS();
```

Configure email recipients for admin summaries:

Copy code

```
CALL my_quota!SET_ADMIN_EMAILS('admin1@example.com, admin2@example.com');
```

### Verify notification email addresses

Each email address used for notifications, for users and for admin summaries, must be verified. If
a user’s email address isn’t available, an informational event is logged in the event table. By
default, events are logged in `SNOWFLAKE.TELEMETRY.EVENTS`, but you can configure your own event
table. To verify a whole email domain, use
[SYSTEM$VERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_verify_dns_domain).

## Configure custom actions

Quota admins can configure custom actions that run when a user breaches a per-user quota threshold.
Custom actions are implemented as stored procedures. When a threshold is breached, the stored
procedure is invoked for each user who has exceeded the threshold.

Custom actions are evaluated against the monthly per-user limit only. You can configure them with SQL
for any resource scope, but Snowsight offers them only for quotas scoped to warehouses.

For quotas scoped to warehouses, a custom action runs only after Snowflake attributes the warehouse usage
to the quota, which can happen several hours after the query finishes. Users can keep running queries during
that delay, so set thresholds with some buffer for that additional usage.

The quota evaluation process passes the list of user IDs who have exceeded their quota
thresholds during the current quota run as the first argument to the stored procedure. Every
quota run covers the aggregated usage from the beginning of the current month to the quota run
time. Any additional configured parameters are passed after the list of user IDs.

Note

Stored procedures used as custom actions must use `EXECUTE AS OWNER`. Before you can register a stored
procedure, the `SNOWFLAKE` application must be granted the `USAGE` privilege on the stored procedure and on the
database and schema that contain it. For example, for `cost_mgmt_db.actions.disable_user_proc(VARCHAR)`:

Copy code

```
GRANT USAGE ON DATABASE cost_mgmt_db TO APPLICATION SNOWFLAKE;
GRANT USAGE ON SCHEMA cost_mgmt_db.actions TO APPLICATION SNOWFLAKE;
GRANT USAGE ON PROCEDURE cost_mgmt_db.actions.disable_user_proc(VARCHAR) TO APPLICATION SNOWFLAKE;
```

Add a custom action at a specified threshold:

Copy code

```
CALL my_quota!ADD_CUSTOM_ACTION(
    SYSTEM$REFERENCE('PROCEDURE',
        'cost_mgmt_db.actions.disable_user_proc(VARCHAR)'),  -- stored procedure
    [],                                                    -- additional arguments
    'ACTUAL',                                              -- spend strategy
    100                                                    -- threshold percentage
);
```

Remove custom actions:

Copy code

```
-- Remove all custom actions configured on the quota:
CALL my_quota!REMOVE_CUSTOM_ACTIONS();

-- Remove all custom actions at a specific threshold (both ACTUAL and PROJECTED):
CALL my_quota!REMOVE_CUSTOM_ACTIONS(100);

-- Remove a specific stored procedure at a specific threshold:
CALL my_quota!REMOVE_CUSTOM_ACTIONS(100, 'COST_MGMT_DB.ACTIONS.DISABLE_USER_PROC(VARCHAR)');
```

Note

The stored procedure name must include the argument signature. Copy the value from the
`PROCEDURE_FQN` column of `GET_CUSTOM_ACTIONS()`. If the remove call finds no match,
it returns a success message with “0 custom actions removed”.

View all configured custom actions:

Copy code

```
CALL my_quota!GET_CUSTOM_ACTIONS();
```

The method returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| `ACTION_ID` | `VARCHAR` | Internal ID to distinguish the various actions. |
| `PROCEDURE_FQN` | `VARCHAR` | Fully qualified name of the stored procedure. |
| `PROCEDURE_ARGS` | `ARRAY` | JSON array of additional parameters passed to the stored procedure. |
| `SPEND_STRATEGY` | `VARCHAR` | Spend strategy: `PROJECTED` or `ACTUAL`. |
| `THRESHOLD` | `NUMBER` | Threshold percentage at which the custom action is triggered. |
| `LAST_TRIGGER_ATTEMPT_TIME` | `TIMESTAMP_TZ(9)` | Specifies the time when the custom action was last triggered. |
| `ADDED_TIMESTAMP` | `TIMESTAMP_TZ(9)` | Specifies the time when the custom action was added to the quota. |

Expand

Show lessSee more

Note

For projected spend thresholds, the custom action is triggered at most once per user within
a 24-hour period. For actual spend thresholds, the action is triggered once per user per
quota cycle.

### Example: Disable users at 100% of their quota

The following example creates a stored procedure that disables users who have exceeded their
quota, then configures it as a custom action at 100% actual spend. Because the procedure runs with
owner’s rights, its owner role must be able to alter the affected users: only the role with the
`OWNERSHIP` privilege on a user, or a higher role, can change most user properties. For more
information, see [ALTER USER](/sql-reference/sql/alter-user). The owner role also needs access to the
`SNOWFLAKE.ACCOUNT_USAGE.USERS` view, which can lag behind recent user changes, so a user created
shortly before the threshold is crossed might be skipped:

Copy code

```
-- Create a stored procedure that disables users.
-- The first argument is automatically populated by the quota's custom-action
-- executor with a JSON-encoded array of the user IDs that breached the
-- threshold (for example, '[101,102,103]'). The procedure must use
-- EXECUTE AS OWNER, otherwise registration is rejected.
CREATE OR REPLACE PROCEDURE cost_mgmt_db.actions.disable_users_by_id(user_ids VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS OWNER
AS
$$
DECLARE
  arr        VARIANT := PARSE_JSON(:user_ids);
  i          INT     := 0;
  cnt        INT     := ARRAY_SIZE(:arr);
  user_id      VARCHAR;
  user_name    VARCHAR;
  quoted_name  VARCHAR;
  disabled     INT     := 0;
  skipped      INT     := 0;
BEGIN
  WHILE (i < cnt) DO
      user_id := :arr[:i]::VARCHAR;
      -- Resolve user_id to user name.
      user_name := NULL;
      SELECT name INTO :user_name
      FROM   snowflake.account_usage.users
      WHERE  user_id    = :user_id
        AND  deleted_on IS NULL
      LIMIT 1;
      IF (user_name IS NOT NULL) THEN
          -- Quote the name so users with lowercase or special characters resolve exactly.
          quoted_name := '"' || REPLACE(:user_name, '"', '""') || '"';
          ALTER USER IDENTIFIER(:quoted_name) SET DISABLED = TRUE;
          disabled := disabled + 1;
      ELSE
          skipped := skipped + 1;
      END IF;
      i := i + 1;
  END WHILE;
  RETURN 'Disabled: ' || :disabled
      || ', Skipped (not found): ' || :skipped
      || ', Total: ' || :cnt;
END;
$$;

-- Grant USAGE on the procedure to the SNOWFLAKE application.
GRANT USAGE ON PROCEDURE cost_mgmt_db.actions.disable_users_by_id(VARCHAR)
  TO APPLICATION SNOWFLAKE;

CALL my_quota!ADD_CUSTOM_ACTION(
    SYSTEM$REFERENCE(
        'PROCEDURE',
        'cost_mgmt_db.actions.disable_users_by_id(VARCHAR)'
    ),                       -- SPROC_REF
    ARRAY_CONSTRUCT(),       -- SPROC_ARGS: no extra arguments
    'ACTUAL',                -- SPEND_STRATEGY
    100                      -- THRESHOLD percentage
);

-- Verify the action is registered.
CALL my_quota!GET_CUSTOM_ACTIONS();

-- Confirm the quota's owner role can invoke the procedure.
CALL my_quota!CONFIRM_CUSTOM_ACTIONS_ACCESS();

-- Remove the action when no longer needed.
CALL my_quota!REMOVE_CUSTOM_ACTIONS(
    100,
    'COST_MGMT_DB.ACTIONS.DISABLE_USERS_BY_ID(VARCHAR)'
);
```

## Configure a cycle-start action

Quota admins can optionally configure a cycle-start (reset) action that runs automatically at
the beginning of each UTC calendar month. The reset action is implemented as a stored procedure
and is intended to restore states affected by quota enforcement, such as re-enabling users or
restoring access to resources.

Cycle-start actions run on the monthly cycle only. You can configure them with SQL for any resource
scope, but Snowsight offers them only for quotas scoped to warehouses.

You can configure only one reset action per quota. The reset action:

- Runs once at the beginning of each UTC calendar month.
- Runs independently of user-level threshold evaluations.
- Receives any configured parameters defined by the admin.

Set the cycle-start action:

Copy code

```
CALL my_quota!SET_CYCLE_START_ACTION(
    SYSTEM$REFERENCE('PROCEDURE', 'cost_mgmt_db.actions.reset_users_proc()'),
    []
);
```

View the current cycle-start action:

Copy code

```
CALL my_quota!GET_CYCLE_START_ACTION();
```

Remove the cycle-start action:

Copy code

```
CALL my_quota!REMOVE_CYCLE_START_ACTION();
```

### Example: Cycle-start action skeleton

The following example shows the structure of a cycle-start action: the procedure, the grant, and
the configuration call. Replace the placeholder logic with your own. To re-enable users that a
custom action disabled, the procedure needs to know which users those are, for example by having
the custom action record each disabled user in a table that the cycle-start action reads and then
clears.

Copy code

```
-- Create a stored procedure to run at the start of each monthly cycle.
CREATE OR REPLACE PROCEDURE cost_mgmt_db.actions.reset_users_proc()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS OWNER
AS
$$
BEGIN
  -- Placeholder: add your reset logic here, such as re-enabling users
  -- that a custom action disabled during the previous cycle.
  RETURN 'Cycle-start action completed';
END;
$$;

-- Grant the SNOWFLAKE application access to invoke the reset procedure.
GRANT USAGE ON PROCEDURE cost_mgmt_db.actions.reset_users_proc() TO APPLICATION SNOWFLAKE;

-- Configure the reset action.
CALL my_quota!SET_CYCLE_START_ACTION(
    SYSTEM$REFERENCE('PROCEDURE', 'cost_mgmt_db.actions.reset_users_proc()'),
    []
);
```

## Monitor quota events

Quota-related operational events are recorded in the Snowflake event table, providing
visibility into whether notifications and custom actions ran successfully.
Events include the following:

- `INFO`: Successful per-user notification delivery, and successful execution of custom
  actions and cycle-start actions.
- `ERROR`: Failures of custom actions or cycle-start actions, invalid or inaccessible
  admin notification integrations, and unverified admin email recipients.

To query quota events, use a role that is granted the `SNOWFLAKE.EVENTS_ADMIN` application role. For
more information, see [Roles for access to the default event table and EVENTS\_VIEW](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-default-roles).

To query quota events from the event table:

Copy code

```
SELECT
    RECORD:name::STRING   AS event_name,
    VALUE:message::STRING AS message,
    RESOURCE_ATTRIBUTES,
    *
FROM snowflake.telemetry.events
WHERE SCOPE['name'] = 'snow.cost.quota'
  AND TIMESTAMP > DATEADD('day', -1, CURRENT_TIMESTAMP())
ORDER BY TIMESTAMP DESC;
```

## Related content

- [Per-user quotas](/user-guide/budgets/per-user-quotas)
- [Block users at a per-user quota limit](/user-guide/budgets/per-user-quotas-enforcement)
- [Per-user quota method reference](/user-guide/budgets/per-user-quotas-reference)
