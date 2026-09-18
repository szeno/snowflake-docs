# Sep 16, 2026: Include and exclude per-user quota users by name (*General availability*)

[Per-user quotas](/user-guide/budgets/per-user-quotas) now accept individual user names, so you can add
or remove specific users alongside the quota’s tag scope. `INCLUDE_USERS` is new and takes user names
directly, and `EXCLUDE_USERS` accepts a `'USER'` argument alongside its existing `'TAG'` form:

Copy code

```
CALL my_quota!INCLUDE_USERS(['ALICE', 'BOB']);
CALL my_quota!EXCLUDE_USERS('USER', ['CAROL']);
```

Naming a user takes precedence over the quota’s tag scope. An included user is monitored whether or not
they match the tags, and an excluded user stays out even while they still match. A user who gains a
matching tag later joins the scope, but a user you excluded by name stays excluded.
