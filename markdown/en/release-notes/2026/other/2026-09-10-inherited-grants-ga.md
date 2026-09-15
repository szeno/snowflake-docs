# Sep 10, 2026: Inherited grants and container-level MANAGE GRANTS (*General availability*)

Inherited grants and container-level `MANAGE GRANTS` are now generally available.

Use a single `GRANT INHERITED` statement on an `ACCOUNT`, `DATABASE`, or `SCHEMA` to apply a
privilege to every current and future object of a specified type in that container. Use
container-level `MANAGE GRANTS` to delegate grant administration for a database or schema to a
role, without granting that role account-wide access.

Both features remain opt-in. Enable them per account by setting:

Copy code

```
ALTER ACCOUNT SET FEATURE_RBAC_INHERITED_GRANTS = 'ENABLED';
```

For more information, see [Managing access with inherited grants](/user-guide/inherited-grants-intro) and
[Delegating grant management with container-level MANAGE GRANTS](/user-guide/container-manage-grants-intro).
