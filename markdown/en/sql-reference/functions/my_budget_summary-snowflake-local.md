Categories:
:   [Table functions](/sql-reference/functions-table) (Budgets)

# MY\_BUDGET\_SUMMARY (SNOWFLAKE.LOCAL)

Returns the calling user’s limits, usage, and current block status for each
[per-user quota](/user-guide/budgets/per-user-quotas) that applies to them in the current account.

Any user can call this function. It returns only the calling user’s information, so users can check
how much of their per-user limit they’ve used without asking an administrator and without privileges on the
quota or on the `ACCOUNT_USAGE` schema.

See also:
:   [Per-user quotas](/user-guide/budgets/per-user-quotas) , [LOCAL schema](/sql-reference/local)

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.MY_BUDGET_SUMMARY()
```

## Arguments

None.

## Returns

The function returns one row for each quota that applies to the calling user and each cycle that has a
per-user limit. For example, a quota with daily, weekly, and monthly limits returns three rows. Cycles
without a limit don’t return a row.

| Column | Data type | Description |
| --- | --- | --- |
| ID | NUMBER | Identifier of the quota. |
| NAME | VARCHAR | Name of the quota. |
| DOMAINS | ARRAY | Array of the domains that the quota monitors, for example `["AI FUNCTION", "AI GATEWAY"]`. See [Usage notes](#label-my-budget-summary-usage-notes). |
| CYCLE | VARCHAR | Cycle that the row describes: `DAILY`, `WEEKLY`, or `MONTHLY`. |
| START\_TIME | TIMESTAMP\_LTZ | Start of the current cycle. |
| END\_TIME | TIMESTAMP\_LTZ | End of the current cycle, when usage for the cycle resets. |
| PER\_USER\_LIMIT | FLOAT | Per-user limit for the cycle, in the unit shown in `USAGE_UNIT`. |
| USAGE | FLOAT | Calling user’s usage that counts toward the quota in the current cycle, in the unit shown in `USAGE_UNIT`. |
| USAGE\_UNIT | VARCHAR | Unit for `USAGE` and `PER_USER_LIMIT`, for example `CREDITS` or `AI_CREDITS`. |
| PERCENT\_CONSUMED | FLOAT | Percentage of the per-user limit consumed in the current cycle (`USAGE / PER_USER_LIMIT * 100`), rounded to two decimal places. |
| BLOCK\_ENFORCEMENT\_ENABLED | BOOLEAN | Whether the quota blocks users who reach the limit. If `FALSE`, usage still counts toward the limit, but the user isn’t blocked. |
| STATUS | VARCHAR | `BLOCKED` if the calling user is currently blocked by this quota for this cycle. Otherwise, `NULL`. |

Expand

Show lessSee more

If no quota applies to the calling user, the function returns no rows.

## Access control requirements

No privileges are required. Any user can call this function, and it returns only the calling user’s information.

## Usage notes

- Call the function in the `FROM` clause with the `TABLE` keyword: `SELECT * FROM TABLE(SNOWFLAKE.LOCAL.MY_BUDGET_SUMMARY());`.
- Cycles start and end on UTC boundaries. `START_TIME` and `END_TIME` are displayed in the session’s time
  zone.
- `DOMAINS` lists only domains, even if the quota monitors selected resources within a domain. `USAGE`
  includes only usage on the resources that the quota monitors.
- Usage can count toward more than one quota. If quotas monitor overlapping domains, don’t add `USAGE`
  across those quotas to calculate total usage, because the overlapping usage would be double-counted.
- Usage data is refreshed periodically, typically within minutes. Recent activity might not appear yet in
  `USAGE` or `PERCENT_CONSUMED`.
- Because `STATUS` is updated with usage data, it can briefly lag behind enforcement. The calling user might already be
  blocked before `STATUS` shows `BLOCKED`.
- The function returns information only for the current account.

## Examples

Return the calling user’s limits and usage for each quota:

Copy code

```
SELECT * FROM TABLE(SNOWFLAKE.LOCAL.MY_BUDGET_SUMMARY());
```

Copy code

```
+------+-------------------+-----------------+---------+-------------------------------+-------------------------------+----------------+-------------+------------+------------------+---------------------------+--------+
| ID   | NAME              | DOMAINS         | CYCLE   | START_TIME                    | END_TIME                      | PER_USER_LIMIT | USAGE       | USAGE_UNIT | PERCENT_CONSUMED | BLOCK_ENFORCEMENT_ENABLED | STATUS |
|------+-------------------+-----------------+---------+-------------------------------+-------------------------------+----------------+-------------+------------+------------------+---------------------------+--------|
| 4002 | ALL_USER_QUOTA    | ["AI FUNCTION"] | DAILY   | 2026-10-27 00:00:00.000 +0000 | 2026-10-28 00:00:00.000 +0000 |             30 | 0           | AI_CREDITS |                0 | FALSE                     | NULL   |
| 4002 | ALL_USER_QUOTA    | ["AI FUNCTION"] | MONTHLY | 2026-10-01 00:00:00.000 +0000 | 2026-11-01 00:00:00.000 +0000 |            100 | 5.817098865 | AI_CREDITS |             5.82 | FALSE                     | NULL   |
| 4053 | WAREHOUSE_QUOTA   | ["WAREHOUSE"]   | MONTHLY | 2026-10-01 00:00:00.000 +0000 | 2026-11-01 00:00:00.000 +0000 |            100 | 4.568169411 | CREDITS    |             4.57 | FALSE                     | NULL   |
+------+-------------------+-----------------+---------+-------------------------------+-------------------------------+----------------+-------------+------------+------------------+---------------------------+--------+
```

Return only the cycles in which the calling user has used more than 80% of the per-user limit:

Copy code

```
SELECT name, cycle, usage, per_user_limit, percent_consumed, end_time
  FROM TABLE(SNOWFLAKE.LOCAL.MY_BUDGET_SUMMARY())
  WHERE percent_consumed > 80;
```
