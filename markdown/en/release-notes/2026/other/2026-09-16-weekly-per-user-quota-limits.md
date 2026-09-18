# Sep 16, 2026: Weekly per-user quota limits (*General availability*)

[Per-user quotas](/user-guide/budgets/per-user-quotas) now support a weekly credit limit alongside the
existing monthly and daily limits. Pass `'WEEKLY'` as the cycle argument to `SET_PER_USER_LIMIT`:

Copy code

```
CALL my_quota!SET_PER_USER_LIMIT(500, 'WEEKLY');
```

The weekly cycle follows the ISO week and resets Monday at 00:00 UTC. Each cycle is evaluated
independently, so a user is blocked as soon as they reach any limit you set, and a user blocked by
their weekly limit is released the following Monday.

`GET_CONFIG` reports the configured value as `PER_USER_LIMIT_WEEKLY`, `UNSET_PER_USER_LIMIT('WEEKLY')`
removes it, and notification thresholds accept `'WEEKLY'` so users can be alerted against their weekly
limit.
