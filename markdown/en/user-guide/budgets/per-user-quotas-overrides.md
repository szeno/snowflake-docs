# Override limits for specific users in a per-user quota

A per-user limit override replaces a quota’s default credit limit for specific users on a given
cycle (monthly, weekly, or daily), without changing the quota’s user scope or creating a separate
quota. You can set a higher limit to grant extra headroom, set a lower limit to constrain a heavy
spender, or set an expiration date so a temporary adjustment reverts automatically.

## How limit overrides work

An override applies inside a single quota for one user and one cycle. While an override is active,
the quota evaluates and enforces that user’s spending against the override value instead of the
quota’s default limit for that cycle.

The following table shows how Snowflake resolves a user’s effective limit for a cycle within a
quota:

| Active override for this user and cycle? | Quota default set for this cycle? | Effective limit |
| --- | --- | --- |
| No (or expired) | No | No limit |
| No (or expired) | Yes | Quota default |
| Yes | No | Override value |
| Yes | Yes | Override value (replaces the quota default) |

Expand

Show lessSee more

Key behaviors of limit overrides:

- **Independent of the quota default**: An override can be higher or lower than the quota’s default
  limit for that cycle, and you can set an override for a cycle even when the quota has no default
  limit configured for that cycle.
- **Same domains, notifications, and enforcement**: An override inherits the quota’s monitored
  domains, block enforcement setting, notification settings, and monthly custom actions. Notification
  and custom-action thresholds are percentages, so they automatically scale to the user’s override
  limit. Notification and block emails indicate when an override limit is active, and users calling
  [MY\_BUDGET\_SUMMARY (SNOWFLAKE.LOCAL)](/sql-reference/functions/my_budget_summary-snowflake-local) see their effective limit.
- **Automatic unblock when raised**: If a user is blocked by the quota, setting an override above
  their current spend for the blocked cycle automatically clears that quota’s block within
  approximately 5 to 10 minutes. No separate unblock call is needed.
- **Other quotas still apply**: An override changes the limit only on the quota where you set it. If
  the user is also in scope for another quota that monitors the same domain, that second quota
  continues to evaluate and enforce its own limit independently, and the lowest limit across
  overlapping quotas binds.
- **Up to 200 overrides per quota**: A quota can hold at most 200 overrides, where each
  user-and-cycle combination counts as one override. A call that would exceed 200 overrides returns
  an error. Updating an existing override for the same user and cycle replaces it without using an
  additional slot, and removing an override deletes the entry and frees capacity toward the 200
  limit.

## Set or update a limit override

To create or update a limit override for one or more users, call `SET_USER_QUOTA_OVERRIDE`. To
call the override methods, use a role granted the quota’s `ADMIN` instance role, with the `USAGE`
privilege on the quota’s database and schema.

Copy code

```
CALL <quota_name>!SET_USER_QUOTA_OVERRIDE(
  <user_names>,
  '<cycle>',
  <limit>
  [ , <expires_on> ]
);
```

The method accepts the following arguments:

- `user_names` (`ARRAY`): An array of one or more user names, such as `['ALICE', 'BOB']`. User names
  are case-sensitive and must match each user’s Snowflake identifier (for example, `'ALICE'` for an
  unquoted user created as `alice`). Resolution is all-or-nothing: if any user name in the array
  doesn’t resolve to an active user in the account, the entire call fails and no overrides in the
  batch are written.
- `cycle` (`VARCHAR`): The cycle to override: `'MONTHLY'`, `'WEEKLY'`, or `'DAILY'` (not
  case-sensitive). Weekly and daily overrides apply to quotas scoped to AI domains.
- `limit` (`FLOAT`): The per-user credit limit for the specified cycle. Must be a whole number from
  1 to 1,000,000,000. Zero, negative, `NULL`, and decimal values return an error.
- `expires_on` (`DATE`, optional): The date when the override stops applying, or `NULL` for an
  override that doesn’t expire. You can omit the argument instead of passing `NULL`. When you pass
  a date, it must be later than the current UTC date. The date is exclusive: the override remains
  active through the day before `expires_on` and expires at `00:00 UTC` on `expires_on`, when the
  user automatically reverts to the quota’s default limit for that cycle.

If an override already exists for a user and cycle in the call, `SET_USER_QUOTA_OVERRIDE`
replaces its limit and expiration date.

The method returns a `VARIANT` object that maps each requested user name (in call order) to its
resolved user ID. It doesn’t report whether another quota still caps the user:

Copy code

```
{
  "ALICE": {
    "user_id": 101
  },
  "BOB": {
    "user_id": 102
  }
}
```

**Example: Grant a temporary monthly increase for one user**

Give `ALICE` a monthly limit of 2,500 credits until December 1, 2026 (active through November 30,
2026 UTC, reverting to the quota default at `00:00 UTC` on December 1):

Copy code

```
CALL my_quota!SET_USER_QUOTA_OVERRIDE(
  ['ALICE'],
  'MONTHLY',
  2500,
  '2026-12-01'
);
```

**Example: Set a permanent daily override for multiple users**

Give `ALICE` and `BOB` a daily limit of 300 credits with no expiration date:

Copy code

```
CALL my_quota!SET_USER_QUOTA_OVERRIDE(
  ['ALICE', 'BOB'],
  'DAILY',
  300
);
```

**Example: Set a lower limit for a single user**

Constrain `CAROL` to 50 credits per month while keeping the rest of the quota at a higher default:

Copy code

```
CALL my_quota!SET_USER_QUOTA_OVERRIDE(
  ['CAROL'],
  'MONTHLY',
  50
);
```

## View configured overrides

To list all overrides stored on a quota, call `LIST_USER_QUOTA_OVERRIDES`:

Copy code

```
CALL my_quota!LIST_USER_QUOTA_OVERRIDES();
```

The method returns a table with the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| `USER_ID` | `NUMBER` | Internal ID of the user. |
| `USER_NAME` | `VARCHAR` | Name of the user. |
| `CYCLE` | `VARCHAR` | Overridden cycle: `MONTHLY`, `WEEKLY`, or `DAILY`. |
| `OVERRIDE_VALUE` | `NUMBER` | Per-user credit limit set by the override. |
| `EXPIRY_DATE` | `DATE` | Date (UTC) when the override expires, or `NULL` if it doesn’t expire. |

Expand

Show lessSee more

## Remove limit overrides

When you remove an override, the user reverts to the quota’s default limit for that cycle on the
next evaluation run, and the removed entry no longer counts toward the 200-override cap.

Use one of the following methods depending on what you want to remove:

| Method | What it removes |
| --- | --- |
| `REMOVE_USER_QUOTA_OVERRIDE('<user_name>', '<cycle>')` | The override for one user and one cycle (`'MONTHLY'`, `'WEEKLY'`, or `'DAILY'`). |
| `REMOVE_USER_QUOTA_OVERRIDES_BY_USER('<user_name>')` | All overrides for one user across every cycle on this quota. |
| `REMOVE_USER_QUOTA_OVERRIDES_BY_CYCLE('<cycle>')` | All overrides for the specified cycle across every user on this quota. |
| `REMOVE_ALL_USER_QUOTA_OVERRIDES()` | Every override on this quota. |

Expand

Show lessSee more

In all removal methods, `user_name` is case-sensitive and `cycle` isn’t case-sensitive. Each method
returns a `VARCHAR` confirmation message.

Copy code

```
-- Remove ALICE's monthly override.
CALL my_quota!REMOVE_USER_QUOTA_OVERRIDE('ALICE', 'MONTHLY');

-- Remove all overrides for ALICE on this quota.
CALL my_quota!REMOVE_USER_QUOTA_OVERRIDES_BY_USER('ALICE');

-- Remove all daily overrides on this quota.
CALL my_quota!REMOVE_USER_QUOTA_OVERRIDES_BY_CYCLE('DAILY');

-- Remove every override on this quota.
CALL my_quota!REMOVE_ALL_USER_QUOTA_OVERRIDES();
```

## Manage overrides in Snowsight

You can create, inspect, and reset limit overrides in Snowsight without writing SQL:

1. Sign in to Snowsight.
2. In the navigation menu, select **Admin** » **Cost management**, then select the **Budgets** tab.
3. Select the quota’s name to open the quota deep-dive view.
4. Select **Set override** on the quota deep-dive page, or select a user in the table to open the
   user deep-dive view and select **Set override**.
5. In the dialog, enter the per-user override limit for each cycle you want to override (monthly,
   weekly, or daily) and choose when the override expires. The dialog shows the quota’s default
   limit and the user’s current spend for each cycle.
6. If other quotas that you have access to also cover the user on overlapping domains and would
   still cap the user at a lower limit, the dialog lists those conflicting quotas so you can raise
   them at the same time.
7. Confirm the changes.

In the quota deep-dive user table, users with an active override display an **Override** badge, and
you can filter the list by **Has override** or **Expiring soon**. On the user deep-dive view, the
user’s override limit is shown alongside the quota default, and you can select **Reset to default**
to remove the override.

## Lifecycle and considerations

- **Users who leave and re-enter scope**: An override takes effect only while the user is in the
  quota’s scope. If a user leaves the quota’s scope (for example, after a tag change), the override
  stays stored on the quota while inactive and applies again if the user re-enters the quota’s scope
  before it expires.
- **Dropped or renamed users**: Overrides are stored against the user’s internal ID. If you drop a
  user and recreate a user with the same name, the new user has a different ID and isn’t covered by
  the old override. Dropping a user doesn’t automatically delete their stored override, so it
  continues to count toward the 200-override cap until you remove it.
- **Unsetting a quota default limit**: Calling `UNSET_PER_USER_LIMIT` removes the quota’s default
  limit for that cycle, but leaves any per-user overrides for that cycle in place.
- **Dropping a quota**: Dropping a quota deletes all of its overrides.

## Related content

- [Per-user quotas](/user-guide/budgets/per-user-quotas)
- [Create and configure a per-user quota](/user-guide/budgets/per-user-quotas-create)
- [Block users at a per-user quota limit](/user-guide/budgets/per-user-quotas-enforcement)
- [Per-user quota method reference](/user-guide/budgets/per-user-quotas-reference)
