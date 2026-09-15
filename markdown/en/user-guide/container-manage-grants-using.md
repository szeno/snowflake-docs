# Using container-level MANAGE GRANTS

This topic describes how to grant, delegate, revoke, and audit
[container-level `MANAGE GRANTS`](/user-guide/container-manage-grants-intro).

## Get started

Container-level `MANAGE GRANTS` lets you delegate grant administration on a database or schema without granting
account-wide grant-management authority.

Before delegating `MANAGE GRANTS`, determine whether the role actually needs to make independent authorization
decisions. If the access requirement can be expressed directly (for example, a role needs `SELECT` on every current
and future table in a database), prefer an [inherited grant](/user-guide/inherited-grants-intro) instead. See
[When to use container-level MANAGE GRANTS](/user-guide/container-manage-grants-intro#label-container-manage-grants-intro-when)
for more guidance.

A typical workflow is as follows:

1. **Identify the administrative boundary and the delegated role.** Choose the narrowest database or schema that
   matches the intended trust boundary.
2. **Grant `MANAGE GRANTS` on that container.** Use `SECURITYADMIN` (or another role that already holds account-level
   `MANAGE GRANTS WITH GRANT OPTION`) to grant the privilege to the delegated role.
3. **Add `WITH GRANT OPTION` only if the administrator must delegate `MANAGE GRANTS` further.**
4. **Audit both the delegated administrative privilege and the grants created within the delegated scope.**
5. **Revoke grant-management authority when it’s no longer required, and separately review access previously
   established by the administrator.**

## Syntax

Copy code

```
GRANT  MANAGE GRANTS ON { ACCOUNT | DATABASE <name> | SCHEMA <name> }
  TO   { ROLE <role_name> | DATABASE ROLE <db_role_name> }
  [ WITH GRANT OPTION ]

REVOKE MANAGE GRANTS ON { ACCOUNT | DATABASE <name> | SCHEMA <name> }
  FROM { ROLE <role_name> | DATABASE ROLE <db_role_name> }
  [ RESTRICT | CASCADE ]
```

`RESTRICT` (default) fails the revocation if any dependent `MANAGE GRANTS` privileges exist. `CASCADE` also revokes
those dependent `MANAGE GRANTS` privileges.

## How to obtain MANAGE GRANTS on a container

A role obtains `MANAGE GRANTS` on a database or schema in one of two ways:

1. **From an account administrator** holding `MANAGE GRANTS ON ACCOUNT WITH GRANT OPTION`:

   Copy code

   ```
   USE ROLE SECURITYADMIN;

   GRANT MANAGE GRANTS ON DATABASE sales_db
     TO ROLE sales_admin;
   ```

   `WITH GRANT OPTION` is not required if `sales_admin` only administers grants within `sales_db` and does not need
   to delegate `MANAGE GRANTS` to another role.
2. **From an existing role that holds container-level `MANAGE GRANTS`** on the same or a higher container, with
   `WITH GRANT OPTION`. See [Allow further delegation](#label-container-manage-grants-using-delegate) for an
   end-to-end example.

## Allow further delegation

Add `WITH GRANT OPTION` only when the delegated administrator also needs to delegate `MANAGE GRANTS` to another role.

Grant `MANAGE GRANTS` `WITH GRANT OPTION` to the delegated role:

Copy code

```
USE ROLE SECURITYADMIN;

GRANT MANAGE GRANTS ON DATABASE sales_db
  TO ROLE sales_admin
  WITH GRANT OPTION;
```

The delegated role can then grant `MANAGE GRANTS` on that same container, or on a lower-level container:

Copy code

```
USE ROLE sales_admin;

GRANT MANAGE GRANTS ON SCHEMA sales_db.us_west
  TO ROLE us_west_lead;
```

`WITH GRANT OPTION` expands the administrator’s ability to create additional grant-management authorities. Don’t
include it when further delegation isn’t required.

Periodically review any lower-level `MANAGE GRANTS` privileges created through this delegation.

## Examples

### Delegate grant management for a database

Copy code

```
USE ROLE SECURITYADMIN;

GRANT MANAGE GRANTS ON DATABASE sales_db
  TO ROLE sales_admin;
```

**Outcome:** `sales_admin` can manage supported grants within `sales_db`, but cannot delegate `MANAGE GRANTS` further
unless separately authorized with `WITH GRANT OPTION`.

For an example that permits further delegation, see
[Allow further delegation](#label-container-manage-grants-using-delegate).

### Skip-level delegation

Copy code

```
USE ROLE SECURITYADMIN;
GRANT MANAGE GRANTS ON SCHEMA sales_db.us_west TO ROLE us_west_lead;
```

**Outcome:** `us_west_lead` becomes the role that holds `MANAGE GRANTS` for `sales_db.us_west`. No intermediate grant
on `sales_db` is required.

### Reduce delegated grant-management authority

A delegated administrator might no longer require `MANAGE GRANTS` if its recurring work can be represented directly
through inherited grants. For example, suppose `analyst` should always have `SELECT` on every current and future
table in `sales_db`, and `sales_admin` currently maintains that access manually.

To reduce delegated grant-management authority:

1. Migrate the administrator’s recurring, uniform grant patterns to inherited grants. See
   [Using inherited grants](/user-guide/inherited-grants-using#label-inherited-grants-using-migrate) for step-by-step
   migration guidance.
2. Determine whether the administrator still needs to make independent authorization decisions.
3. If not, revoke its container-level `MANAGE GRANTS`.

Don’t remove `MANAGE GRANTS` if the administrator must continue making independent authorization decisions, whether
through per-object grants, new inherited-grant patterns, or other privilege decisions.

Revoking `MANAGE GRANTS` does not remove the grants the administrator previously created. Review those grants
separately.

### Revoke MANAGE GRANTS from a role with cascade

Copy code

```
USE ROLE SECURITYADMIN;
REVOKE MANAGE GRANTS ON ACCOUNT FROM ROLE sales_admin CASCADE;
```

**Outcome:** Dependent `MANAGE GRANTS` granted by `sales_admin` (for example, `MANAGE GRANTS` on database `sales_db`
or on schemas inside `sales_db`) are revoked. Regular grants, and non-`MANAGE GRANTS` inherited grants created by
`sales_admin`, are preserved.

## Audit container-level MANAGE GRANTS

Snowflake supports the following approaches to facilitate container-level `MANAGE GRANTS` auditing.

- Use `SHOW GRANTS ON DATABASE <name>` and `SHOW GRANTS ON SCHEMA <name>` to enumerate every grant inside a delegated
  container, including grants made by the role that holds `MANAGE GRANTS`.
- Use the `GRANTS_TO_ROLES` view in `ACCOUNT_USAGE` to reconstruct the history of `MANAGE GRANTS` delegations,
  including revoked grants (which appear with a non-null `DELETED_ON` value).

**Find all roles that hold MANAGE GRANTS in the account:**

Copy code

```
SELECT grantee_name, granted_on, name AS container_name, granted_by, created_on
  FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_ROLES
  WHERE privilege = 'MANAGE GRANTS'
    AND granted_on IN ('DATABASE', 'SCHEMA')
    AND deleted_on IS NULL
  ORDER BY granted_on, name;
```

**Find all roles that hold MANAGE GRANTS for a specific database:**

Copy code

```
SHOW GRANTS ON DATABASE sales_db;
```

**Find all containers where a specific role holds MANAGE GRANTS:**

Copy code

```
SHOW GRANTS TO ROLE sales_admin;
```
