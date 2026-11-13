# Block users at a per-user quota limit

Quotas can automatically block a user from issuing new AI requests once their spend reaches their
per-user limit. Blocking is built in: you enable it with a single setting, and Snowflake handles
the blocking, the cycle reset, and the safety logic when multiple quotas cover the same user. No
stored procedures, privilege grants, or scheduling are required.

Enforcement runs in a Snowflake-managed pipeline that evaluates breaches within minutes of a spend
event.

## Enable block enforcement

To enable block enforcement and email users when they’re blocked:

Copy code

```
CALL my_quota!SET_BLOCK_ENFORCEMENT_ENABLED(TRUE, TRUE);
```

The first argument turns enforcement on or off. When you pass `FALSE`, users that this quota has
blocked are automatically unblocked within approximately 5 to 10 minutes.

The second argument determines whether users receive an email when they’re blocked. To block users
without emailing them, pass `FALSE`.

## Enforceable domains

Block enforcement supports the following AI domains: AI functions, Cortex Agents, Snowflake CoWork,
Snowflake CoCo, and the AI Gateway. Warehouse spend can be tracked in a separate quota, but block
enforcement doesn’t apply to warehouses.

If a user breaches their limit through non-enforceable spend (such as warehouse usage),
enforcement still applies to the supported AI domains, but the non-enforceable spend continues.

Note

`SET_BLOCK_ENFORCEMENT_ENABLED` turns enforcement on or off without validating the quota’s scope.
It doesn’t reject quotas that contain non-enforceable domains.

## How blocking works

When enforcement is enabled, Snowflake runs a continuous loop for each user in scope:

1. **Usage**: The user issues AI requests. Usage data flows through the metering pipeline into the
   per-user attribution data within minutes.
2. **Evaluation**: The enforcement pipeline compares each user’s spend against their per-user
   limit. If spend meets or exceeds the limit, the pipeline records a block.
3. **Notification**: If the quota is configured to email blocked users, Snowflake emails the user.
   The email explains that their quota is exhausted and that new AI requests are denied until an
   administrator raises the limit or the cycle resets. The quota admin is notified separately when
   the quota measurement task next runs.
4. **Deny**: The next time the user issues an AI request, the service returns a domain-appropriate
   error that identifies the cause (quota exhausted) rather than a generic authorization failure.
   For AI functions, in-progress calls are terminated when the block takes effect, not just new
   requests. For the AI Gateway, the block applies only to new requests. Requests already in progress
   run to completion and are billed, so usage can slightly exceed the limit.
5. **Cycle reset**: Blocks expire automatically at the cycle boundary (UTC midnight for a daily
   limit, Monday at 00:00 UTC for a weekly limit, the first of the month for a monthly limit). No
   separate clearing step is required, and the user can spend again once the cycle rolls over.
   Blocks are also released when you raise the per-user limit above the user’s current spend or
   remove the quota.

## Limitations of block enforcement

- Because enforcement is evaluated within minutes of a spend event rather than at request time, a
  user might briefly continue past their limit until the block lands. The overshoot is bounded by what
  they spend in that short window, which is usually small for interactive use. For example, with a
  100-credit limit, a user who reaches 100 and spends 30 more before the block takes effect ends at
  130. A large single request, such as an AI function over a big table, can overshoot more. Account
  for this overshoot when you set the per-user limit.
- Daily and monthly cycles reset at UTC midnight, and the weekly cycle resets Monday at 00:00 UTC. A user
  who starts spending near a cycle boundary can consume up to one full limit before the reset and a fresh
  limit after it.
- Limit and scope changes aren’t immediate. Changes to a quota’s configuration, including its limits
  and scope, take approximately 5 to 10 minutes to propagate before enforcement acts on them.

## Check enforcement status

Review which users are currently blocked:

Copy code

```
CALL my_quota!GET_ACTIVE_BLOCKS_V2();
```

The method returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| `USER_ID` | `NUMBER` | Internal identifier of the blocked user. |
| `USER_NAME` | `VARCHAR` | Name of the blocked user. |
| `CYCLE` | `VARCHAR` | Limit cycle of the block: `DAILY`, `WEEKLY`, or `MONTHLY`. A user blocked in more than one cycle has one row for each cycle. |
| `BLOCKED_UNTIL` | `TIMESTAMP_LTZ` | Time when the block lifts, which is the start of the next cycle. If the user has more than one block for the cycle, this is the latest time. |

Expand

Show lessSee more

Review the blocking and unblocking history for the quota over a date range. Both the start and end
dates are required:

Copy code

```
CALL my_quota!GET_ENFORCEMENT_HISTORY('2026-06-01', '2026-06-30');
```

The method returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| `ACTION_AT` | `TIMESTAMP_LTZ` | Time when the action was taken. |
| `ACTION` | `VARCHAR` | `BLOCKED` or `UNBLOCKED`. |
| `USER_ID` | `NUMBER` | Internal identifier of the user. |
| `USER_NAME` | `VARCHAR` | Name of the user. |
| `CYCLE` | `VARCHAR` | Limit cycle that the action applies to: `DAILY`, `WEEKLY`, or `MONTHLY`. |
| `PER_USER_LIMIT` | `NUMBER(38,9)` | Per-user credit limit for the cycle at the time of the action. |
| `CREDITS` | `NUMBER(38,9)` | Credits the user had consumed in the cycle when the block was applied. `NULL` for `UNBLOCKED` rows. |
| `BLOCKED_UNTIL` | `TIMESTAMP_LTZ` | Time when the block lifts. For `UNBLOCKED` rows, the time when the released block would have lifted. |

Expand

Show lessSee more

You can also review enforcement in Snowsight using the **Enforcement breakdown** chart and the
**Enforcement status** column of the quota deep-dive view. For more information, see
[Monitor quotas in Snowsight](/user-guide/budgets/per-user-quotas-monitor#label-per-user-quota-monitor-snowsight).

To list blocked users across all quotas, query the
`SNOWFLAKE.ACCOUNT_USAGE.QUOTA_ACCESS_BLOCK_HISTORY` view.

Individual users can check whether they’re currently blocked by calling
[MY\_BUDGET\_SUMMARY (SNOWFLAKE.LOCAL)](/sql-reference/functions/my_budget_summary-snowflake-local). For more information, see
[Check your quota usage](/user-guide/budgets/per-user-quotas-monitor#label-per-user-quota-check-quota-usage).

Note

`GET_CONFIG` includes the `BLOCK_ENFORCEMENT_ENABLED`, `PER_USER_LIMIT_WEEKLY`, and
`PER_USER_LIMIT_DAILY` values alongside the existing configuration, such as `PER_USER_LIMIT`.

## Respond to escalations

A quota is a policy: one limit applies to all users in the quota, and there’s no per-user override
within a single quota. When a blocked user needs more headroom, you have two options.

**Raise the limit for everyone in the quota.** No separate unblock call is needed. After you raise
the limit and the change propagates (approximately 5 to 10 minutes), the pipeline automatically clears
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
CALL my_quota!SET_BLOCK_ENFORCEMENT_ENABLED(TRUE, TRUE);

-- Tag the user who needs more headroom.
ALTER USER alice SET TAG cost_mgmt_db.tags.usage_tier = 'high';

-- Higher-limit quota scoped to the intersection of both tags.
CALL high_tier_quota!SET_USER_TAGS(
  [
    [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.cost_center', 'SESSION', 'APPLYBUDGET')), 'analytics'],
    [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.usage_tier', 'SESSION', 'APPLYBUDGET')), 'high']
  ],
  'INTERSECTION'
);
CALL high_tier_quota!SET_PER_USER_LIMIT(5000);
CALL high_tier_quota!SET_BLOCK_ENFORCEMENT_ENABLED(TRUE, TRUE);
```

Note

Multiple quotas can block the same user. If a user is covered by more than one quota with
enforcement enabled, each quota independently evaluates and records its own blocks. Clearing blocks
from one quota doesn’t clear blocks from another. To see which user is blocked by which quota over
time, query the `SNOWFLAKE.ACCOUNT_USAGE.QUOTA_ACCESS_BLOCK_HISTORY` view.

## Related content

- [Per-user quotas](/user-guide/budgets/per-user-quotas)
- [Monitor per-user quota spending](/user-guide/budgets/per-user-quotas-monitor)
- [Per-user quota method reference](/user-guide/budgets/per-user-quotas-reference)
