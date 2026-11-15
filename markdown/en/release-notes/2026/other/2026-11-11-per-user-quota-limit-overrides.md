# Nov 11, 2026: Override per-user quota limits for specific users (*General availability*)

You can now set per-user, per-cycle credit limit overrides on a
[per-user quota](/user-guide/budgets/per-user-quotas) to give specific users a higher or lower limit
than the quota default without changing the quota’s user scope or creating a separate quota. You can
also set an optional expiration date so a temporary adjustment reverts automatically to the quota’s
default limit.

For example, the following call gives `ALICE` a monthly limit of 2,500 credits on `my_quota` until
December 1, 2026:

Copy code

```
CALL my_quota!SET_USER_QUOTA_OVERRIDE(
  ['ALICE'],
  2500,
  'MONTHLY',
  '2026-12-01'
);
```

You can also list overrides with `LIST_USER_QUOTA_OVERRIDES`, remove overrides with
`REMOVE_USER_QUOTA_OVERRIDE`, `REMOVE_USER_QUOTA_OVERRIDES_BY_USER`,
`REMOVE_USER_QUOTA_OVERRIDES_BY_CYCLE`, or `REMOVE_ALL_USER_QUOTA_OVERRIDES`, and manage overrides
in Snowsight from the quota deep-dive or user deep-dive view by selecting **Set override**.

For more information, see [Override limits for specific users in a per-user quota](/user-guide/budgets/per-user-quotas-overrides).
