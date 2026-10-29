# Oct 28, 2026: Check the quotas that apply to you with MY\_BUDGET\_SUMMARY (*General availability*)

With this release, the [MY\_BUDGET\_SUMMARY (SNOWFLAKE.LOCAL)](/sql-reference/functions/my_budget_summary-snowflake-local) table function
is generally available. You can now use it to check your limits, usage, and block status for the
[per-user quotas](/user-guide/budgets/per-user-quotas) that apply to you:

Copy code

```
SELECT * FROM TABLE(SNOWFLAKE.LOCAL.MY_BUDGET_SUMMARY());
```

The function returns one row for each quota that applies to you and each cycle that has a per-user limit, with
your usage, the limit, the percentage consumed, and when the cycle resets. Any user can call the
function. It returns only the calling user’s information, so administrators don’t need to grant
additional privileges.

For more information, see [Check your quota usage](/user-guide/budgets/per-user-quotas#label-per-user-quota-check-quota-usage).
