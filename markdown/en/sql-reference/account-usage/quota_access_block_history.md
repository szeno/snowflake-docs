Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# QUOTA\_ACCESS\_BLOCK\_HISTORY view

This Account Usage view returns the history of block and unblock actions that
[per-user quotas](/user-guide/budgets/per-user-quotas) take on users in the account. It covers all
quotas in the account, so you can find which quota blocked a user without checking each quota
separately.

Each row represents one action: a quota blocked a user for a limit cycle, or released that block
before the cycle ended. Rows are recorded only for quotas with
[block enforcement](/user-guide/budgets/per-user-quotas-enforcement#label-per-user-quota-enforcement) enabled.

## Columns

The view has the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| ACTION\_AT | TIMESTAMP\_LTZ | Time when the action was recorded. |
| QUOTA\_ID | NUMBER | Internal identifier of the quota that took the action. |
| QUOTA\_NAME | VARCHAR | Name of the quota that took the action. `NULL` if the quota no longer exists. |
| USER\_ID | NUMBER | Internal identifier of the user that was blocked or unblocked. |
| USER\_NAME | VARCHAR | Name of the user that was blocked or unblocked. `NULL` if the user no longer exists. |
| CYCLE | VARCHAR | Limit cycle that the action applies to: `DAILY`, `WEEKLY`, or `MONTHLY`. A quota blocks a user separately for each cycle that has a per-user limit. |
| ACTION | VARCHAR | Action that the quota took: `BLOCKED` when the user’s credit usage in the cycle reached the per-user limit, or `UNBLOCKED` when the quota released the block before the cycle ended. See [Usage notes](#usage-notes). |
| PER\_USER\_LIMIT | NUMBER | Per-user credit limit for the cycle at the time of the action. For an `UNBLOCKED` row recorded because you raised the limit, this is the new limit. Can be `NULL` for an `UNBLOCKED` row if the quota was removed. |
| CREDITS | NUMBER | Credits the user had consumed in the cycle when the block was applied. For `UNBLOCKED` rows, the value is `NULL`. |
| BLOCKED\_UNTIL | TIMESTAMP\_LTZ | Time when the cycle resets and the block expires. For `UNBLOCKED` rows, this is the reset time of the block that was released. |

Expand

Show lessSee more

## Usage notes

- To query the view, use a role that is granted the `USAGE_VIEWER` database role. For more
  information, see [SNOWFLAKE database roles](/sql-reference/snowflake-db-roles).
- The view records actions, not current block status. A block that expires when its cycle resets
  doesn’t produce an `UNBLOCKED` row, so a user whose latest row is `BLOCKED` might no longer be
  blocked. To list the users that a quota currently blocks, call `GET_ACTIVE_BLOCKS_V2` on the
  quota. For more information, see [Check enforcement state](/user-guide/budgets/per-user-quotas-enforcement#label-per-user-quota-enforcement).
- Rows appear in the view as soon as a quota blocks or unblocks a user. A quota blocks a user
  approximately 2 to 3 minutes after the user’s credit usage reaches the per-user limit, so usage can
  exceed the limit during that time.
- An `UNBLOCKED` row is recorded when a block is released before the cycle resets: when you raise
  the per-user limit above the user’s usage, disable block enforcement, remove the user from the
  quota’s scope, or remove the quota.
- A user can have more than one `BLOCKED` row for the same quota and cycle. For example, the quota
  records a block again after you add or remove a monitored domain.
- Each quota records its own actions. If more than one quota with block enforcement enabled covers a
  user, each quota can block the user independently, and the view returns a separate row for each
  quota.
- Block enforcement applies only to AI domains, so warehouse usage never produces rows in this view.
  For more information, see [Block users at the limit](/user-guide/budgets/per-user-quotas-enforcement#label-per-user-quota-enforcement).
- Cycles use UTC boundaries. Values in `BLOCKED_UNTIL` are displayed in the session time zone.
- The view retains data for 1 year. Rows remain in the view after the quota is removed.

## Examples

Retrieve the number of blocks and blocked users for each quota in the last 30 days:

Copy code

```
SELECT quota_name,
       COUNT(*) AS block_count,
       COUNT(DISTINCT user_id) AS blocked_users
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUOTA_ACCESS_BLOCK_HISTORY
  WHERE action = 'BLOCKED'
    AND action_at >= DATEADD('day', -30, CURRENT_TIMESTAMP())
  GROUP BY quota_id, quota_name
  ORDER BY block_count DESC;
```

Retrieve the block and unblock history for one user across all quotas:

Copy code

```
SELECT action_at,
       quota_name,
       cycle,
       action,
       credits,
       per_user_limit,
       blocked_until
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUOTA_ACCESS_BLOCK_HISTORY
  WHERE user_name = 'ALICE'
  ORDER BY action_at;
```

Retrieve the users whose latest action in each quota and cycle is a block that hasn’t reached its
reset time. The view records actions rather than current status, so call `GET_ACTIVE_BLOCKS_V2` when
you need the current list for a quota:

Copy code

```
SELECT quota_name,
       user_name,
       cycle,
       action_at AS blocked_at,
       blocked_until
  FROM SNOWFLAKE.ACCOUNT_USAGE.QUOTA_ACCESS_BLOCK_HISTORY
  QUALIFY ROW_NUMBER() OVER (PARTITION BY quota_id, user_id, cycle ORDER BY action_at DESC) = 1
    AND action = 'BLOCKED'
    AND blocked_until > CURRENT_TIMESTAMP()
  ORDER BY quota_name, user_name;
```
