# Per-user quotas

Per-user quotas let you enforce spending limits at a per-user granularity, preventing individual
users from generating unwanted costs. Quotas are particularly useful when deploying services where
individual users can accumulate significant charges in a short period of time, such as running
complex AI functions over a large dataset.

With per-user quotas, you can:

- Define monthly and daily per-user credit limits that apply uniformly to all users in scope.
- Apply the quota to all users in your account, or select specific users using tags to represent teams, cost centers, or business units.
- Block users automatically when they reach their daily or monthly limit. Blocks are released automatically when the cycle resets or you raise the limit.
- Configure notifications, based on actual or projected spend against the monthly or daily limit, when users approach or exceed their limits.
- Automate custom enforcement actions with stored procedures triggered at configurable thresholds, and reset affected states at the start of each quota cycle.
- Monitor per-user spending, utilization, and enforcement status in Snowsight.

## How per-user quotas work

A per-user quota is a first-class Snowflake object that defines per-user spending controls
within a specified database and schema. After you create a quota, you configure it by specifying
which users are in scope, what their quota thresholds are, and what actions to take when
thresholds are crossed.

### Monthly cycle

Quotas operate on a monthly cycle aligned to the UTC calendar month. At the start of each new
calendar month, per-user usage counters reset automatically.

### Monthly and daily limits

A quota can define two per-user spending limits that apply uniformly to every user in scope:

- **Monthly limit**: The maximum credits a user can consume during the UTC calendar month. Monthly
  usage resets at the start of each month.
- **Daily limit** (optional): The maximum credits a user can consume during a single UTC day,
  evaluated within the monthly cycle. Daily usage resets at the start of each UTC day.

Daily and monthly limits are evaluated independently. A user can be enforced against the daily
limit while still being within their monthly limit, and the reverse is also true.

### Enforcement actions

When a user reaches a limit, the quota can take an enforcement action:

- **Block** (built-in): Snowflake automatically blocks the user from issuing new AI requests once
  their spend reaches the limit, with no customer-authored code. Enforcement is evaluated within
  minutes of a spend event, applies per period (daily or monthly), and is
  released automatically when the period resets. For more information, see
  [Block users at the limit](#label-per-user-quota-enforcement).
- **Custom action**: A stored procedure that you provide runs when a threshold is crossed, letting
  you implement custom enforcement such as revoking access based on a role, sending customized notifications, or writing an
  audit record. For more information, see [Configure custom actions](#label-per-user-quota-custom-actions).

### User selection

A quota can apply to all users in your account, or to a specific set of users selected by tag.
When you select all users, the quota automatically includes any user added to the account later,
with no reconfiguration. You can also keep all users in scope while excluding a certain group of
users by tag.

When you scope by tag, quota scope is determined by the specific tags applied to user objects. In
Snowflake, tags function as key-value pairs where each key supports a single value per user. When
multiple tag keys are used for scoping, an operator is required to define the logic for user
resolution:

- `UNION` (default): This creates a union of users, including any individual who matches at
  least one defined tag.
- `INTERSECTION`: This creates an intersection, requiring a user to match every specified tag
  to be governed.

User resolution occurs dynamically at evaluation time, so changes to tag assignments are
automatically reflected in the quota without any reconfiguration.

Tip

If you want to automate user tagging, you can provision users through a SCIM identity provider
and use the `snowflakeTags` attribute to apply tags automatically when users are created or
updated. For more information, see [Automating user tags with SCIM](/user-guide/cost-attributing#label-cost-attribute-scim).
For provider-specific setup steps, see:

- [SCIM with Microsoft Entra ID](/user-guide/scim-azure)
- [SCIM with Okta](/user-guide/scim-okta)
- [SCIM with a custom identity provider](/user-guide/scim-custom)

### Threshold types

Thresholds determine when notifications or custom actions are triggered for a user. They are
expressed as a percentage of the monthly per-user quota and can be evaluated using one of two
methods:

- **Actual spend**: Triggers when a user’s accumulated spend within the current UTC calendar
  month exceeds the configured percentage of their monthly per-user quota. This is typically
  used for hard enforcement.
- **Projected spend** (default): Triggers when the user’s current spending rate, extrapolated
  to the end of the UTC calendar month or UTC calendar day, indicates they are likely to exceed the threshold. This
  is proactive and used for early warning and prevention.

**Example: Actual spend**

Per-user quota: 300 credits. Threshold: 90% (Actual). The notification or action triggers when
the user has consumed 270 credits of actual usage within the month.

**Example: Projected spend**

Per-user quota: 300 credits. Threshold: 90% (Projected). On day 1 of a 30-day month, the
threshold triggers if the user has spent 9 credits (because 9 × 30 = 270, which equals 90% of
the quota). This enables early intervention before limits are actually breached.

## Supported domains

Per-user quotas monitor the following supported domains that emit per-user usage data. The per-user
spending limit applies to usage against one or more of the selected domains.

A single quota monitors either warehouse compute or AI domains, but not a mix of the two. The units
of measurement differ (platform credits for warehouse compute versus AI credits for AI domains), so warehouse
and AI domains can’t be combined in the same quota.

| Domain | Monitored costs |
| --- | --- |
| WAREHOUSE | Compute resources for query execution in warehouses, includes warehouse metering and query acceleration costs. |
| AI FUNCTION | Credit usage for AI functions operations attributed to the user. |
| SNOWFLAKE INTELLIGENCE | Credit usage for Snowflake CoWork (formerly Snowflake Intelligence) operations attributed to the user. |
| CORTEX AGENT | Credit usage for Cortex Agents operations attributed to the user. |
| CORTEX CODE | Credit usage for Snowflake CoCo (formerly Cortex Code) operations attributed to the user. Includes spend from Snowflake CoCo CLI, Snowflake CoCo in Snowsight, and Snowflake CoCo Desktop. |

Expand

Show lessSee more

You can specify one or more of the selected domains that you want to track with your quota. This can be done during quota creation from the Snowsight UI or via SQL. Domain selection can also be modified after quota creation.

Example: Add all AI functions to your quota

Copy code

```
CALL my_quota!ADD_SHARED_RESOURCE('AI FUNCTION');
```

Example: Add the AI Classify function to your quota

Copy code

```
CALL my_quota!ADD_SHARED_RESOURCE('AI FUNCTION', 'AI_CLASSIFY');
```

Note

If you specify the whole AI Function domain, you do not need to selectively add specific functions like AI Classify separately.

Example: Add a specific Cortex Agent to the quota

Copy code

```
CALL my_quota!ADD_SHARED_RESOURCE(
  'CORTEX AGENT',
  (SELECT SYSTEM$REFERENCE('CORTEX AGENT', 'myagent'))
);
```

Example: Add the Snowflake CoWork domain to the quota

Copy code

```
CALL my_quota!ADD_SHARED_RESOURCE('SNOWFLAKE INTELLIGENCE');
```

Example: Add a specific warehouse resource to the quota

Copy code

```
CALL my_quota!ADD_SHARED_RESOURCE(
  'WAREHOUSE',
  (SELECT SYSTEM$REFERENCE('WAREHOUSE', 'SNOWADHOC'))
);
```

## Limitations and considerations

- Quotas operate on a monthly cycle aligned to the UTC calendar month. Custom quota cycles, such as weekly
  or custom start dates, are not supported.
- By default, a new quota monitors all users in the account. You can narrow the scope with tags,
  or exclude specific users.
- No enforcement occurs until a per-user spending limit is set.
- You cannot set different limits for different users within the same quota. All users share
  the same per-user limit.
- Collective spending limits across all users in a quota are not supported. Each user’s limit
  is evaluated independently.
- Quota evaluation is not real time but occurs within minutes. A slight lag might occur between a user being blocked and the data appearing in Snowsight.
- Notifications are sent at most once per threshold per user within a 24-hour period for
  projected spend thresholds. Actual spend thresholds trigger at most once per cycle.
- Each email address used for notifications must be verified. If a user’s email is not available,
  an informational event is logged in the event table. By default events are logged in
  `snowflake.telemetry.events`, but you can configure your own event table. You can verify a whole email domain using [SYSTEM$VERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_verify_dns_domain).

The following limitations apply to [block enforcement](#label-per-user-quota-enforcement):

- Block enforcement supports only the AI domains: AI functions, Cortex Agents, Snowflake CoWork, and Snowflake CoCo.
  Warehouse spend can be tracked in a separate quota, but block enforcement doesn’t apply to
  warehouses.
- Because enforcement is evaluated within minutes of a spend event rather than at request time, a
  user may briefly continue past their limit until the block lands. The overshoot is bounded by what
  they spend in that short window, which is usually small for interactive use. For example, with a
  100-credit limit, a user who reaches 100 and spends 30 more before the block takes effect ends at
  130. A large single request, such as an AI function over a big table, can overshoot more. This should be considered when defining the quota limit.
- Daily and monthly cycles reset at UTC midnight. A user who starts spending near a cycle boundary
  can consume up to one full limit before the reset and a fresh limit after it.
- Limit and scope changes aren’t immediate. Quota configuration can take up to approximately 5-10 minutes to
  propagate before enforcement acts on them, including changes to limits and scope.

## Create a per-user quota

You can create a per-user quota by executing SQL statements, as described in this section, or in
Snowsight. For the Snowsight workflow, see [Using Snowsight](#label-per-user-quota-snowsight).

### Create a custom role to create quotas

You can use a custom role to create quotas in your account or create quotas as an account admin.
The following example creates a role named `quota_owner` and grants the required role and
privileges to create quotas in the schema `cost_mgmt_db.quota_schema`. The example must be
executed using the `ACCOUNTADMIN` role:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE quota_owner;

GRANT USAGE ON DATABASE cost_mgmt_db TO ROLE quota_owner;
GRANT USAGE ON SCHEMA cost_mgmt_db.quota_schema TO ROLE quota_owner;
GRANT DATABASE ROLE SNOWFLAKE.QUOTA_CREATOR TO ROLE quota_owner;
GRANT CREATE SNOWFLAKE.CORE.QUOTA ON SCHEMA cost_mgmt_db.quota_schema TO ROLE quota_owner;
```

### Use SQL to create a per-user quota

Create a per-user quota, then configure the user scope, spending limit, and notifications.
To create a per-user quota, you must use a role with the required privileges to create a quota.

Create a quota named `my_quota` in `cost_mgmt_db.quota_schema`:

Copy code

```
USE SCHEMA cost_mgmt_db.quota_schema;

CREATE SNOWFLAKE.CORE.QUOTA my_quota();
```

After creating the quota, configure it by following the steps in the sections below.

## Specify users in scope

By default, a new quota monitors all users in the account, so no scope configuration is required.
You can narrow the scope to a subset of users with tags, or keep all users in scope while excluding
a specific subset.

To scope the quota to a subset of users, use the `SET_USER_TAGS` method to specify which users are
in scope. Pass the tags by reference and specify the operator (`UNION` or `INTERSECTION`). The
`SET_USER_TAGS` call is atomic and idempotent: any existing tags are overwritten.

Copy code

```
CALL my_quota!SET_USER_TAGS(
    [
        [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.cost_center', 'SESSION', 'APPLYBUDGET')), 'finance'],
        [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.dept', 'SESSION', 'APPLYBUDGET')), 'analytics']
    ],
    'UNION'
);
```

Note

The role used to set user tags on a quota must have the `APPLYBUDGET` privilege on each tag.

To keep all users in scope but exclude a subset, use `EXCLUDE_USERS` with the tags that identify
the users to exclude. In the following example, the quota keeps all users in scope except any user
tagged with a `usage_tier` tag whose value is `high`:

Copy code

```
CALL my_quota!EXCLUDE_USERS('TAG', [
    [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.usage_tier', 'SESSION', 'APPLYBUDGET')), 'high']
]);
```

To verify the current user scope:

Copy code

```
CALL my_quota!GET_QUOTA_SCOPE();
```

Returns a JSON object showing the configured tags and operator:

Copy code

```
{
  "user_tags": {
    "operator": "UNION",
    "tags": [
      {
        "type": "tag",
        "tag_database": "cost_mgmt_db",
        "tag_schema": "tags",
        "tag_key": "COST_CENTER",
        "tag_values": ["FINANCE"]
      },
      {
        "type": "tag",
        "tag_database": "cost_mgmt_db",
        "tag_schema": "tags",
        "tag_key": "DEPT",
        "tag_values": ["ANALYTICS"]
      }
    ]
  }
}
```

To list the users currently resolved into the quota’s scope:

Copy code

```
CALL my_quota!GET_USERS();
```

Note

User resolution relies on [TAG\_REFERENCES](/sql-reference/account-usage/tag_references), which can
lag by up to approximately 2 hours. Recent tag changes might not appear in `GET_USERS` immediately.

## Set per-user spending limits

The quota admin sets a monthly per-user credit limit. Each user in scope is assigned the same
per-user limit, and limits are enforced independently per user. There is no aggregation or
collective cap across users.

Set the spending limit per user to 120 credits:

Copy code

```
CALL my_quota!SET_PER_USER_LIMIT(120);
```

Retrieve the current configuration, including the monthly and daily per-user limits:

Copy code

```
CALL my_quota!GET_CONFIG();
```

### Set a daily per-user limit

In addition to the monthly limit, you can set a daily per-user limit by passing the optional cycle
argument to `SET_PER_USER_LIMIT`. The default cycle is monthly.

Copy code

```
-- Monthly limit (default, existing behavior).
CALL my_quota!SET_PER_USER_LIMIT(1000);

-- Daily limit.
CALL my_quota!SET_PER_USER_LIMIT(120, 'DAILY');
```

The daily limit resets at the start of each UTC day and is evaluated independently of the monthly
limit.

To remove a limit, pass the cycle to unset. For example, remove the daily limit:

Copy code

```
CALL my_quota!UNSET_PER_USER_LIMIT('DAILY');
```

## Block users at the limit

Quotas can automatically block a user from issuing new AI requests once their spend reaches their
per-user limit. Blocking is built in: you enable it with a single setting, and Snowflake handles
the blocking, the cycle reset, and the safety logic when multiple quotas cover the same user. No
stored procedures, privilege grants, or scheduling are required.

Enforcement runs in a Snowflake-managed pipeline that evaluates breaches within minutes of a spend
event.

To enable block enforcement:

Copy code

```
CALL my_quota!SET_BLOCK_ENFORCEMENT_ENABLED(TRUE, TRUE);
```

To disable it, pass `FALSE` in the first argument. When you disable enforcement, users that this quota has blocked are
automatically unblocked within approximately 5-10 minutes.

The second argument determines whether end users should receive notifications once they’re blocked. To disable end user notifications when they’re blocked, set it to `FALSE`.

### Enforceable domains

Block enforcement supports the following AI domains: AI functions, Cortex Agents, Snowflake CoWork, and Snowflake CoCo.
Warehouse spend can be tracked in a separate quota, but block enforcement doesn’t apply to
warehouses.

If a user breaches their limit through non-enforceable spend (such as warehouse usage),
enforcement still applies to the supported AI domains, but the non-enforceable spend continues.

Note

`SET_BLOCK_ENFORCEMENT_ENABLED` currently turns enforcement on or off without validating the
quota’s scope. Scope validation that rejects quotas containing non-enforceable domains is planned
but isn’t available yet.

### How enforcement works

When enforcement is enabled, Snowflake runs a continuous loop for each user in scope:

1. **Usage**: The user issues AI requests. Usage data flows through the metering pipeline into the
   per-user attribution data within minutes.
2. **Evaluation**: The enforcement pipeline compares each user’s spend against their per-user
   limit. If spend meets or exceeds the limit, the pipeline records a block.
3. **Notification**: When quota block enforcement is active and configured to notify end users upon being blocked, an email is sent to the affected user. This notification explains that their quota has been exhausted, resulting in the denial of subsequent AI requests until the limit is increased by an administrator or the cycle resets. The
   admin is notified separately through the regular quota measurement task soon thereafter.
4. **Deny**: The next time the user issues an AI request, the service returns a domain-appropriate
   error that identifies the cause (quota exhausted) rather than a generic authorization failure.
   For AI functions, in-progress calls are terminated when the block takes effect, not just new
   requests.
5. **Cycle reset**: Blocks expire automatically at the cycle boundary (UTC midnight for a daily
   limit, the first of the month for a monthly limit). No separate clearing step is required, and
   the user can spend again once the cycle rolls over. Blocks are also released when you raise the
   per-user limit above the user’s current spend or remove the quota.

### Check enforcement state

Review which users are currently blocked:

Copy code

```
CALL my_quota!GET_ACTIVE_BLOCKS_V2();
```

Review the blocking and unblocking history for the quota over a date range. Both the start and end
dates are required:

Copy code

```
CALL my_quota!GET_ENFORCEMENT_HISTORY('2026-06-01', '2026-06-30');
```

You can also review enforcement in Snowsight using the **Enforcement breakdown** chart and the
**Enforcement status** column of the quota deep-dive view. For more information, see
[Monitor per-user quotas in Snowsight](#label-per-user-quota-monitor-snowsight).

You can also view a list of all blocked users across quotas from the ACCOUNT\_USAGE.QUOTA\_ACCESS\_BLOCK\_HISTORY view.

Note

`GET_CONFIG` includes the `BLOCK_ENFORCEMENT_ENABLED` and `PER_USER_LIMIT_DAILY` values alongside
the existing configuration, such as `PER_USER_LIMIT`.

### Respond to escalations

A quota is a policy: one limit applies to all users in the quota, and there’s no per-user override
within a single quota. When a blocked user needs more headroom, you have two options.

**Raise the limit for everyone in the quota.** No separate unblock call is needed. After you raise
the limit and the change propagates (approximately 5-10 minutes), the pipeline automatically clears
blocks for users who are now under the new limit and keeps blocks for those still over it.

Copy code

```
CALL my_quota!SET_PER_USER_LIMIT(2000);
```

**Move one user to a quota with a higher limit.** Use `INTERSECTION` mode on both quotas with
different `usage_tier` tag values so their user sets don’t overlap. Changing the user’s
`usage_tier` tag moves them out of the first quota’s scope and into the higher-limit quota’s scope.
The pipeline clears the user’s blocks from the first quota and evaluates them against the new
limit, with no double-blocking and no manual unblock.

Copy code

```
-- Default quota: cost_center = analytics AND usage_tier = standard.
CALL my_quota!SET_USER_TAGS(
  [
    [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.cost_center', 'SESSION', 'APPLYBUDGET')), 'analytics'],
    [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.usage_tier', 'SESSION', 'APPLYBUDGET')), 'standard']
  ],
  'INTERSECTION'
);
CALL my_quota!SET_PER_USER_LIMIT(1000);
CALL my_quota!SET_BLOCK_ENFORCEMENT_ENABLED(TRUE,TRUE);

-- Tag the user who needs more headroom.
ALTER USER alice SET TAG usage_tier = 'high';

-- Higher-limit quota scoped to the intersection of both tags.
CALL high_tier_quota!SET_USER_TAGS(
  [
    [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.cost_center', 'SESSION', 'APPLYBUDGET')), 'analytics'],
    [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.usage_tier', 'SESSION', 'APPLYBUDGET')), 'high']
  ],
  'INTERSECTION'
);
CALL high_tier_quota!SET_PER_USER_LIMIT(5000);
CALL high_tier_quota!SET_BLOCK_ENFORCEMENT_ENABLED(TRUE);
```

Note

Multiple quotas can block the same user. If a user is covered by more than one quota with
enforcement enabled, each quota independently evaluates and records its own blocks. Clearing blocks
from one quota doesn’t clear blocks from another. To see which user is blocked by which quota over
time, query the `snowflake.account_usage.quota_access_block_history` view.

## Configure notifications

Quotas support two types of notifications: individual user notifications that alert users when
they approach or exceed thresholds, and admin summary notifications that provide aggregated
reports to administrators.

### Individual user notifications

You can configure notifications that are sent to individual users when they cross specified
thresholds of their per-user quota. For each threshold, you specify:

- The threshold percentage (for example, `80` for 80% of the quota).
- The threshold type: `PROJECTED` (default) or `ACTUAL`.
- Whether to notify the user directly (`TRUE` or `FALSE`).
- Whether the notification should be based on monthly or daily (‘MONTHLY’ or ‘DAILY’) limit.

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

Returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| `THRESHOLD` | NUMBER | Threshold percentage at which the notification is triggered. |
| `SPEND_STRATEGY` | VARCHAR | Type of threshold: `PROJECTED` or `ACTUAL`. |
| `NOTIFY_USER` | BOOLEAN | Indicates whether the user is notified when they cross the threshold. |
| `ADDED_TIMESTAMP` | TIMESTAMP\_TZ(9) | Indicates when the notification was added. |

Expand

Show lessSee more

Note

Notifications for projected spend thresholds are sent at most once per threshold within a
24-hour period. However, notifications on projected spend will continue to be sent if one or more users are projected to hit their quota on a recurring basis (once every 24-hour period).

Notifications for actual spend thresholds are sent at most once per quota cycle when users actually hit the spend threshold.

### Admin summary notifications

Quota admins can configure admin summary notifications to receive aggregated reports of users
who breach per-user quota thresholds. A summary is sent after a quota evaluation when new
threshold breaches are detected.

Each summary includes:

- User name
- Threshold breached
- Threshold type (Actual or Projected)
- User credit usage at evaluation time

Notifications can be delivered via a notification integration and/or a list of email recipients.
If both are null, summary notifications are suppressed.

Configure a notification integration for admin summaries:

Copy code

```
CALL my_quota!ADD_NOTIFICATION_INTEGRATION('my_notification_integration');
```

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

## Configure custom actions

Quota admins can configure custom actions that are executed when a user breaches a per-user
quota threshold. Custom actions are implemented as stored procedures. When a threshold is
breached, the stored procedure is invoked for each user who has exceeded the threshold.

The quota evaluation process passes the list of user IDs who have exceeded their quota
thresholds during the current quota run as the first argument to the stored procedure. Every
quota run covers the aggregated usage from the beginning of the current month to the quota run
time. Any additional configured parameters are passed after the list of user IDs.

Note

Stored procedures used as custom actions must use `EXECUTE AS OWNER` and must be granted
`USAGE` to the `SNOWFLAKE` application before they can be registered.

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
CALL my_quota!REMOVE_CUSTOM_ACTIONS(100, 'cost_mgmt_db.actions.disable_user_proc(varchar)');
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

Returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| `ACTION_ID` | VARCHAR | Internal ID to distinguish the various actions. |
| `PROCEDURE_FQN` | VARCHAR | Fully qualified name of the stored procedure. |
| `PROCEDURE_ARGS` | ARRAY | JSON array of additional parameters passed to the stored procedure. |
| `SPEND_STRATEGY` | VARCHAR | Spend strategy: `PROJECTED` or `ACTUAL`. |
| `THRESHOLD` | NUMBER | Threshold percentage at which the custom action is triggered. |
| `LAST_TRIGGER_ATTEMPT_TIME` | TIMESTAMP\_TZ(9) | Specifies the time when the custom action was last triggered. |
| `ADDED_TIMESTAMP` | TIMESTAMP\_TZ(9) | Specifies the time when the custom action was added to the quota. |

Expand

Show lessSee more

Note

For projected spend thresholds, the custom action is triggered at most once per user within
a 24-hour period. For actual spend thresholds, the action is triggered once per user per
quota cycle.

**Example: Disabling user access at 100% of quota**

The following example creates a stored procedure that disables users who have exceeded their
quota, then configures it as a custom action at 100% actual spend:

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
  user_id    VARCHAR;
  user_name  VARCHAR;
  sql_stmt   VARCHAR;
  disabled   INT     := 0;
  skipped    INT     := 0;
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
          sql_stmt := 'ALTER USER ' || :user_name || ' SET DISABLED = TRUE';
          EXECUTE IMMEDIATE :sql_stmt;
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

## Configure a cycle-start (reset) action

Quota admins can optionally configure a cycle-start action that is executed automatically at
the start of each quota cycle (the beginning of each UTC calendar month). The reset action is
implemented as a stored procedure and is intended to restore states affected by quota
enforcement, such as re-enabling users or restoring access to resources.

Only one reset action may be configured per quota. The reset action:

- Runs once at the beginning of each quota cycle.
- Executes independently of user-level threshold evaluations.
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

**Example: Re-enabling users at the start of a new cycle**

Copy code

```
-- Create a stored procedure that re-enables all previously disabled users.
CREATE OR REPLACE PROCEDURE cost_mgmt_db.actions.reset_users_proc()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS OWNER
AS
$$
BEGIN
  -- Your reset logic here, for example re-enabling users.
  RETURN 'Users re-enabled for new cycle';
END;
$$;

-- Grant the SNOWFLAKE application access to invoke the reset procedure.
GRANT USAGE ON PROCEDURE cost_mgmt_db.actions.RESET_USERS_PROC() TO APPLICATION SNOWFLAKE;

-- Configure the reset action.
CALL my_quota!SET_CYCLE_START_ACTION(
    SYSTEM$REFERENCE('PROCEDURE', 'cost_mgmt_db.actions.reset_users_proc()'),
    []
);
```

## View user spending

Quota admins can retrieve spending data for users included in a quota using
`GET_SPENDING_DETAILS_BY_USERS` for finalized usage data.

### GET\_SPENDING\_DETAILS\_BY\_USERS

Returns finalized granular usage records by user and resource within a specified date range:

Copy code

```
CALL my_quota!GET_SPENDING_DETAILS_BY_USERS('2026-04-01', '2026-04-30');
```

Returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| `USER_ID` | NUMBER | User ID. |
| `USER_NAME` | VARCHAR | Name of the user. |
| `SERVICE_TYPE` | VARCHAR | Resource type (for example, `WAREHOUSE_METERING` or `CORTEX_AGENTS`). |
| `ENTITY_TYPE` | VARCHAR | Type of the entity. |
| `ENTITY_NAME` | VARCHAR | Name of the entity, such as the warehouse name or AI function name. |
| `CREDITS_SPEND` | FLOAT | Credits consumed. |
| `USAGE_TIMESTAMP` | TIMESTAMP\_TZ(9) | Usage hour of the underlying spend. |

Expand

Show lessSee more

Note

The date range must fall in either the current month or the prior calendar month for data to
be returned. Dates before the prior month do not return any results.

## Monitor quota events

Quota-related operational events are recorded in the Snowflake Event Table, providing
visibility into whether notifications and custom actions were successfully executed.
Events include:

- `INFO`: Successful per-user notification delivery, and successful execution of custom
  actions and cycle-start actions.
- `ERROR`: Failures of custom actions or cycle-start actions, invalid or inaccessible
  admin notification integrations, and unverified admin email recipients.

Only users with the appropriate admin role for a quota have access to the events for that quota.

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

## Quota method reference

The following tables list the methods available on a quota object. Call each method using the
syntax `<quota_name>!<METHOD>(...)`. For detailed descriptions, parameters, and examples, see the
linked sections.

### Create a quota

| Command | Description |
| --- | --- |
| `CREATE SNOWFLAKE.CORE.QUOTA <name>()` | Create a per-user quota object. See [Use SQL to create a per-user quota](#label-per-user-quota-create). |

Expand

Show lessSee more

### Monitored domains

| Method | Description |
| --- | --- |
| `ADD_SHARED_RESOURCE('<domain>'[, '<resource>'])` | Add a monitored domain, or a specific resource within a domain, to the quota. See [Supported domains](#label-per-user-quota-supported-resources). |

Expand

Show lessSee more

### User scope

| Method | Description |
| --- | --- |
| `SET_USER_TAGS([[<tag_ref>, '<value>'], ...], '<operator>')` | Set the user tags and operator (`UNION` or `INTERSECTION`) that define which users are in scope. See [Specify users in scope](#label-per-user-quota-user-scope). |
| `EXCLUDE_USERS('TAG', [[<tag_ref>, '<value>'], ...])` | Keep all users in scope but exclude those matching the given tags. |
| `GET_QUOTA_SCOPE()` | Return the configured user tags and operator. |
| `GET_USERS()` | Return the users currently resolved into the quota’s scope. |

Expand

Show lessSee more

### Spending limits

| Method | Description |
| --- | --- |
| `SET_PER_USER_LIMIT(<credits>[, '<cycle>'])` | Set the per-user credit limit. The optional cycle argument accepts `'DAILY'`; the default is monthly. See [Set per-user spending limits](#label-per-user-quota-spending-limit). |
| `UNSET_PER_USER_LIMIT('<cycle>')` | Remove the per-user limit for a cycle (`'DAILY'` or monthly). |
| `GET_CONFIG()` | Return the quota configuration, including `PER_USER_LIMIT`, `PER_USER_LIMIT_DAILY`, `BLOCK_ENFORCEMENT_ENABLED`. |

Expand

Show lessSee more

### Enforcement

| Method | Description |
| --- | --- |
| `SET_BLOCK_ENFORCEMENT_ENABLED(<block_enforcement_boolean>,<email_notification_boolean>)` | Turn built-in block enforcement on or off. The first argument is a boolean that determines whether the block enforcement should be enabled or not. The second argument is a boolean that specifies whether emails should be sent to end users when they are blocked. See [Block users at the limit](#label-per-user-quota-enforcement). |
| `GET_ACTIVE_BLOCKS_V2()` | Return the users currently blocked by this quota. |
| `GET_ENFORCEMENT_HISTORY('<start>', '<end>')` | Return the blocking and unblocking history for this quota over a date range. |

Expand

Show lessSee more

### Notifications

| Method | Description |
| --- | --- |
| `ADD_NOTIFICATION_THRESHOLD(<threshold>, '<strategy>', <notify_user>, '<DAILY or MONTHLY limit>')` | Add an individual-user notification threshold. See [Configure notifications](#label-per-user-quota-notifications). |
| `REMOVE_NOTIFICATION_THRESHOLD(<threshold>, '<strategy>')` | Remove a notification threshold. |
| `GET_NOTIFICATION_THRESHOLDS()` | List configured notification thresholds. |
| `ADD_NOTIFICATION_INTEGRATION('<name>')` | Add a notification integration for admin summaries. |
| `REMOVE_NOTIFICATION_INTEGRATION('<name>')` | Remove a notification integration. |
| `GET_NOTIFICATION_INTEGRATIONS()` | List configured notification integrations. |
| `SET_ADMIN_EMAILS('<email>, ...')` | Set admin summary email recipients. |

Expand

Show lessSee more

### Custom actions

| Method | Description |
| --- | --- |
| `ADD_CUSTOM_ACTION(<sproc_ref>, <args>, '<strategy>', <threshold>)` | Register a stored procedure to run when a threshold is crossed. See [Configure custom actions](#label-per-user-quota-custom-actions). |
| `REMOVE_CUSTOM_ACTIONS([<threshold>[, '<sproc_fqn>']])` | Remove all custom actions, those at a threshold, or a specific procedure at a threshold. |
| `GET_CUSTOM_ACTIONS()` | List configured custom actions. |
| `CONFIRM_CUSTOM_ACTIONS_ACCESS()` | Verify the quota’s owner role can invoke the configured procedures. |

Expand

Show lessSee more

### Cycle-start action

| Method | Description |
| --- | --- |
| `SET_CYCLE_START_ACTION(<sproc_ref>, <args>)` | Set the procedure to run at the start of each quota cycle. See [Configure a cycle-start (reset) action](#label-per-user-quota-cycle-start). |
| `GET_CYCLE_START_ACTION()` | Return the configured cycle-start action. |
| `REMOVE_CYCLE_START_ACTION()` | Remove the cycle-start action. |

Expand

Show lessSee more

### View spending

| Method | Description |
| --- | --- |
| `GET_SPENDING_DETAILS_BY_USERS('<start>', '<end>')` | Return finalized per-user usage for a date range. See [View user spending](#label-per-user-quota-view-spending). |

Expand

Show lessSee more

## Using Snowsight

In Snowsight, you can create and monitor per-user quotas without writing SQL. Quotas are managed
alongside budgets on the **Budgets** tab. To get started, sign in to Snowsight and navigate via the
left menu to **Admin** » **Cost management**, then select the **Budgets** tab.

### Create a quota in Snowsight

Before you begin, make sure you’re using a role with privileges to create quota objects in your
target database and schema. If you plan to scope the quota by tag, make sure the relevant users
are tagged.

To start, select **+ Budget** in the upper right, then select **Quota**. This opens a four-step
wizard that tracks your progress in the left rail.

#### Quota scope

The **Quota scope** page determines which users and resources the quota monitors.

- **Specify which users to monitor**: Choose **All users in the account**, or **A group of users
  (through tags)** to scope by user tag. When you monitor all users, you can optionally exclude
  users that carry specific tags.
- **Specify which resources to track**: Choose **AI-related features** to monitor AI functions,
  Snowflake CoCo, Cortex Agents, and Snowflake CoWork (select all of them or specific resources
  within each), or **Warehouses** to monitor warehouse compute.

#### Basic information

The **Basic information** page sets the quota’s name, location, and limits.

- **Name**: A descriptive name for the quota. This is the name shown in the Budgets list.
- **Location**: The database and schema that own the quota object.
- **Monthly credit limit**: The monthly credit ceiling for each user in scope. Usage resets on the
  first of each month.
- **Daily credit limit**: The daily credit ceiling for each user in scope, in credits per user per
  day. Usage resets daily at 00:00 UTC. This field appears when you’re monitoring AI features. For
  AI features, set at least one of the daily or monthly credit limit.

Note

The available limit fields depend on the resource scope you chose on the **Quota scope** page. For
AI-related features, both **Monthly credit limit** and **Daily credit limit** appear, and at least
one is required. For warehouses, only **Monthly credit limit** appears, and it’s required.

#### Alert notifications

The **Alert notifications** page configures who is notified when spend reaches a threshold. You can
add multiple alerts, and each one is evaluated independently. Alert notifications are available when
you set a monthly limit.

- **Alert based on**: Use **Actual spend** to alert on accumulated usage, or **Projected spend** to
  alert on the user’s current spending trend.
- **Alert at**: The percentage of the limit that triggers the alert.
- **Notify affected user**: Email the user in scope. Leave it cleared to notify only the summary
  recipients.
- **Summary emails**: Email addresses that receive a summary when one or more of the alerts are
  triggered.

#### Enforcement and actions

The **Enforcement and actions** page configures how limits are enforced and adds custom automated
actions.

- **Enable enforcement**: When enabled, the monthly and daily credit limits are enforced for the
  quota by blocking users who reach their limit. Admins can configure whether the end user receives emails when they are blocked. For more information, see
  [Block users at the limit](#label-per-user-quota-enforcement).
- **Custom actions**: Trigger stored procedures when monthly spend reaches a threshold. Custom
  actions are evaluated against the monthly credit limit and are independent of alert
  notifications. For more information, see [Configure custom actions](#label-per-user-quota-custom-actions).

Note

The options on this page depend on the resource scope you chose. AI-related scopes show
**Enable enforcement**; warehouse scopes show **Custom actions** only, because block enforcement
doesn’t apply to warehouses.

When you’re done, select **Create**. Snowflake provisions the quota and begins evaluating
consumption for all users in scope.

### Monitor quotas in Snowsight

Snowsight provides three levels of monitoring: a list of all quotas in your account, a deep dive
into a single quota, and a deep dive into an individual user’s spending.

#### Quotas list

The **Budgets** tab lists every quota and budget in your account. Quotas are tracked alongside
budgets so that you can govern all spend controls from one place.
This view includes:

- **Summary cards**: At-a-glance counts of spend controls that are tracking spend, that are over
  or at risk, and that have no limit set. Each card shows the split between custom budgets and
  quotas.
- **Filter tabs**: Switch between **All budgets**, **Custom budgets**, and **Quotas**, and filter
  the list by **Type** and **Status**.
- **List columns**: For each quota, the list shows the **Name**, **Status**, **Monthly per-user
  limit**, **Daily per-user limit**, **Monthly avg utilization**, **Daily budget utilization**,
  **Users monitored**, and **Users blocked**.

Select a quota’s name to open the quota deep-dive view.

#### Quota deep-dive

The quota deep-dive view summarizes spending and enforcement across all users in scope for a
single quota.
This view includes:

- **Avg utilization**: Average utilization across in-scope users, measured against the per-user
  limit.
- **User status**: A breakdown of how many users are on track versus over budget.
- **Enforcement breakdown**: A breakdown of users with an enforcement action applied, such as the
  number of users blocked against the daily or monthly limit.
- **Top user spend over time**: A graph of the highest-spending users over the current cycle,
  plotted against the per-user limit.
- **Quota details**: The quota’s configuration, including:
  - **Per-user limit**: The monthly limit and, if configured, the daily limit (for example,
    `1 credit / month` and `1 credit / day`).
  - **Avg user spend** and **Highest spend** across in-scope users.
  - **Quota scope**: The users in scope (all users in the account, or the tag-based filters
    applied) and the monitored domains, such as AI functions, Snowflake CoCo, Cortex Agents, and Snowflake CoWork.
  - **Notifications**: The configured notification thresholds.
- **User table**: A searchable, filterable list of every user in scope. For each user, the table
  shows **Utilization**, **Status**, **Spend**, **Enforcement status** (such as Blocked), and
  **Monitored tags**.

Select a user in the table to open the user deep-dive view.

#### User deep-dive

The user deep-dive view shows spending detail for a single user within a quota.
This view includes:

- **Monthly utilization**: The user’s spend against their monthly limit.
- **Daily utilization**: The user’s spend against their daily limit.
- **Spend by type**: A breakdown of the user’s spend by monitored domain, such as AI functions.
- **User details**: The per-user monthly and daily limits, the user’s current spend, and their
  average daily spend.
- **Spend by day**: A graph and table of the user’s daily and aggregated spend across the cycle,
  including each day’s spend as a percentage of the monthly limit. Switch between **Daily spend**
  and **Aggregated spend** to change how the graph is plotted.

## Using Snowflake CoCo

You can also work with per-user quotas through the **Cost Intelligence** skill in Snowflake CoCo,
using natural language instead of writing SQL or stepping through the Snowsight wizard. The Cost
Intelligence skill is available in both the Snowflake CoCo UI and the Snowflake CoCo CLI.

Use the skill to create and configure quotas, review per-user spending and utilization, and check
enforcement status by describing what you want in plain language. The skill translates your request
into the underlying quota operations described in this topic.

For more information about the Cost Intelligence skill, see
[Cost Intelligence](/user-guide/cortex-code/bundled-skills#cost-intelligence).

## Related content

- [Monitor credit usage with budgets](/user-guide/budgets/monitor)
- [Custom budgets](/user-guide/budgets/custom-budget)
- [Notifications for budgets](/user-guide/budgets/notifications)
- [Custom actions for budgets](/user-guide/budgets/custom-actions)
- [Cycle-start actions for budgets](/user-guide/budgets/cycle-start-actions)
- [Budgets roles and privileges](/user-guide/cost-access-control)
