# Daily credit usage limits for CoCo

Account administrators can set daily estimated credit usage limits for CoCo on a per-user basis. These
limits help organizations control CoCo consumption by blocking access when a user’s estimated credit usage
in a rolling 24-hour window exceeds the configured threshold.

For other CoCo spend controls, including budgets and per-user quotas, see
[Cost controls for CoCo](/user-guide/cortex-code/cost-controls).

Credit limits are a separate, complementary mechanism to database role grants. A user needs both a qualifying
database role (SNOWFLAKE.CORTEX\_USER or SNOWFLAKE.CORTEX\_AGENT\_USER) and a non-zero credit limit to access
a surface. By default, SNOWFLAKE.CORTEX\_USER is granted to the PUBLIC role, so all users have access; to
restrict access, revoke it from PUBLIC or set the account-level credit limit to `0`.

There are separate parameters for each CoCo surface:

| Parameter | Controls |
| --- | --- |
| `CORTEX_CODE_CLI_DAILY_EST_CREDIT_LIMIT_PER_USER` | CoCo CLI usage |
| `CORTEX_CODE_DESKTOP_DAILY_EST_CREDIT_LIMIT_PER_USER` | CoCo Desktop usage |
| `CORTEX_CODE_SNOWSIGHT_DAILY_EST_CREDIT_LIMIT_PER_USER` | CoCo in Snowsight usage |

Expand

Show lessSee more

## How credit limits work

Each parameter tracks the corresponding user’s estimated credit usage over a rolling 24-hour window. When
a user’s estimated usage reaches the configured limit for a given surface, access is blocked for that surface
until usage drops below the threshold.

All three parameters share the same behavior:

| Value | Behavior |
| --- | --- |
| `-1` (default) | No limit. The user has unlimited access. |
| `0` | Access is blocked entirely for the user. |
| Positive number | Access is blocked when the user’s estimated credit usage in the past 24 hours exceeds this value. |

Expand

Show lessSee more

Using credit limits to control access

Setting the account-level parameter to `0` blocks CoCo access for all users for that surface. You
can then selectively allow access for individual users by assigning them a positive value at the user level.
This pattern is useful when you want to limit a surface to a specific set of users:

Copy code

```
-- Block Cortex Code Desktop for all users in the account
ALTER ACCOUNT SET CORTEX_CODE_DESKTOP_DAILY_EST_CREDIT_LIMIT_PER_USER = 0;

-- Allow a specific user up to 20 credits per day
ALTER USER power_user SET CORTEX_CODE_DESKTOP_DAILY_EST_CREDIT_LIMIT_PER_USER = 20;
```

Each parameter can be set at the account level (applies to all users) or at the user level (applies to a
specific user). A user-level setting overrides the account-level setting for that user.

Note

Only users with the `ACCOUNTADMIN` role (or a role with sufficient privileges to modify the account or user object)
can set these parameters.

## CoCo CLI limits

The `CORTEX_CODE_CLI_DAILY_EST_CREDIT_LIMIT_PER_USER` parameter controls the daily credit limit for
CoCo CLI usage.

### Account level

To set a daily credit limit for all users in the account:

Copy code

```
-- Set the daily credit usage limit to 20 credits for all users in the account
ALTER ACCOUNT SET CORTEX_CODE_CLI_DAILY_EST_CREDIT_LIMIT_PER_USER = 20;
```

To remove the account-level limit and restore the default (unlimited):

Copy code

```
-- Remove the account-level limit (restores default unlimited usage)
ALTER ACCOUNT UNSET CORTEX_CODE_CLI_DAILY_EST_CREDIT_LIMIT_PER_USER;
```

### User level

To set a daily credit limit for a specific user, overriding the account-level setting:

Copy code

```
-- Set a per-user CLI limit that overrides the account-level setting
ALTER USER jsmith SET CORTEX_CODE_CLI_DAILY_EST_CREDIT_LIMIT_PER_USER = 10;
```

To remove the user-level limit, so the account-level setting applies instead:

Copy code

```
-- Remove the user-level override (account-level setting applies instead)
ALTER USER jsmith UNSET CORTEX_CODE_CLI_DAILY_EST_CREDIT_LIMIT_PER_USER;
```

## CoCo Desktop limits

The `CORTEX_CODE_DESKTOP_DAILY_EST_CREDIT_LIMIT_PER_USER` parameter controls the daily credit limit for
CoCo Desktop usage.

### Account level

To set a daily credit limit for all users in the account:

Copy code

```
-- Set the daily Desktop credit usage limit to 20 credits for all users in the account
ALTER ACCOUNT SET CORTEX_CODE_DESKTOP_DAILY_EST_CREDIT_LIMIT_PER_USER = 20;
```

To remove the account-level limit and restore the default (unlimited):

Copy code

```
-- Remove the account-level Desktop limit (restores default unlimited usage)
ALTER ACCOUNT UNSET CORTEX_CODE_DESKTOP_DAILY_EST_CREDIT_LIMIT_PER_USER;
```

### User level

To set a daily credit limit for a specific user, overriding the account-level setting:

Copy code

```
-- Set a per-user Desktop limit that overrides the account-level setting
ALTER USER jsmith SET CORTEX_CODE_DESKTOP_DAILY_EST_CREDIT_LIMIT_PER_USER = 10;
```

To remove the user-level limit, so the account-level setting applies instead:

Copy code

```
-- Remove the user-level Desktop override (account-level setting applies instead)
ALTER USER jsmith UNSET CORTEX_CODE_DESKTOP_DAILY_EST_CREDIT_LIMIT_PER_USER;
```

## CoCo in Snowsight limits

The `CORTEX_CODE_SNOWSIGHT_DAILY_EST_CREDIT_LIMIT_PER_USER` parameter controls the daily credit limit for
CoCo usage within the Snowsight web interface.

### Account level

To set a daily credit limit for all users in the account:

Copy code

```
-- Set the daily Snowsight credit usage limit to 20 credits for all users in the account
ALTER ACCOUNT SET CORTEX_CODE_SNOWSIGHT_DAILY_EST_CREDIT_LIMIT_PER_USER = 20;
```

To remove the account-level limit and restore the default (unlimited):

Copy code

```
-- Remove the account-level Snowsight limit (restores default unlimited usage)
ALTER ACCOUNT UNSET CORTEX_CODE_SNOWSIGHT_DAILY_EST_CREDIT_LIMIT_PER_USER;
```

### User level

To set a daily credit limit for a specific user, overriding the account-level setting:

Copy code

```
-- Set a per-user Snowsight limit that overrides the account-level setting
ALTER USER jsmith SET CORTEX_CODE_SNOWSIGHT_DAILY_EST_CREDIT_LIMIT_PER_USER = 10;
```

To remove the user-level limit, so the account-level setting applies instead:

Copy code

```
-- Remove the user-level Snowsight override (account-level setting applies instead)
ALTER USER jsmith UNSET CORTEX_CODE_SNOWSIGHT_DAILY_EST_CREDIT_LIMIT_PER_USER;
```

## When a limit is reached

When a user’s estimated credit usage exceeds the configured limit for a surface, that surface returns an error
indicating that the daily credit limit has been reached. The user cannot use that surface until sufficient time has
passed for the rolling 24-hour usage to drop below the limit. Other surfaces with separate limits are not affected.

For example, a CoCo CLI user who exceeds their limit sees an error like the following:

```
Error: Daily credit usage limit reached. Your estimated usage has exceeded the
configured limit for this surface. Please try again later or contact your
account administrator to adjust your limit.
```

In CoCo Desktop, a similar message appears in the chat interface. In Snowsight, the CoCo panel displays
the error inline.

Administrators can adjust or remove the limit at any time to restore access.

## Listing users with custom limits

The following SQL script lists all users who have a per-user credit limit override for the CLI parameter. This is
useful for administrators who want to audit which users have custom limits set at the user level.

Copy code

```
-- List all users who have a per-user CLI credit limit override
EXECUTE IMMEDIATE $$
DECLARE
  target_user STRING;
  rs_users RESULTSET;
  res      RESULTSET;
BEGIN
  CREATE OR REPLACE TEMPORARY TABLE _param_overrides (user_name STRING, param_value STRING);

  SHOW USERS;
  rs_users := (SELECT "name" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())));

  FOR record IN rs_users DO
    target_user := record."name";

    EXECUTE IMMEDIATE
      'SHOW PARAMETERS LIKE ''CORTEX_CODE_CLI_DAILY_EST_CREDIT_LIMIT_PER_USER'' IN USER "' || :target_user || '"';

    INSERT INTO _param_overrides (user_name, param_value)
      SELECT :target_user, "value"
      FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
      WHERE "level" = 'USER';
  END FOR;

  res := (SELECT * FROM _param_overrides);
  RETURN TABLE(res);
END;
$$;
```

This script iterates over all users in the account, checks whether a user-level override is set for
`CORTEX_CODE_CLI_DAILY_EST_CREDIT_LIMIT_PER_USER`, and returns a table of users with their override values.
You can modify the parameter name in the `SHOW PARAMETERS LIKE` clause to check the Snowsight parameter instead.

## Example: Configuring limits for your organization

The following example sets default limits for all users in the account across all three surfaces, then assigns a
higher limit to a power user for CLI usage:

Copy code

```
-- Set default daily limits for all users
ALTER ACCOUNT SET CORTEX_CODE_CLI_DAILY_EST_CREDIT_LIMIT_PER_USER = 20;
ALTER ACCOUNT SET CORTEX_CODE_DESKTOP_DAILY_EST_CREDIT_LIMIT_PER_USER = 20;
ALTER ACCOUNT SET CORTEX_CODE_SNOWSIGHT_DAILY_EST_CREDIT_LIMIT_PER_USER = 20;

-- Allow a specific user a higher CLI limit
ALTER USER power_user SET CORTEX_CODE_CLI_DAILY_EST_CREDIT_LIMIT_PER_USER = 50;

-- Block a specific user from Snowsight entirely
ALTER USER restricted_user SET CORTEX_CODE_SNOWSIGHT_DAILY_EST_CREDIT_LIMIT_PER_USER = 0;
```

Note

When both an account-level and a user-level value are set for the same parameter, the user-level value takes
precedence for that user. All other users in the account continue to use the account-level value.
