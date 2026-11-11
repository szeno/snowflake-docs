# GRANT ROLE

Assigns a role to a user or another role:

- Granting a role to another role creates a “parent-child” relationship between the roles (also referred to as a *role hierarchy*).
- Granting a role to a user enables the user to perform all operations allowed by the role (through the access privileges granted to the role).

For more details, see [Overview of Access Control](/user-guide/security-access-control-overview).

See also:
:   [REVOKE ROLE](/sql-reference/sql/revoke-role)

    [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role) , [REVOKE DATABASE ROLE](/sql-reference/sql/revoke-database-role)

    [GRANT APPLICATION ROLE](/sql-reference/sql/grant-application-role) , [REVOKE APPLICATION ROLE](/sql-reference/sql/revoke-application-role)

    [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege)

## Syntax

Copy code

```
GRANT ROLE <name> TO ROLE <parent_role_name> [ WITH GRANT OPTION ]

GRANT ROLE <name> TO USER <user_name>
  [ { FOR INTERVAL <interval> | UNTIL <timestamp> } [ RESET EXPIRATION ] ]
```

## Parameters

`name`
:   Specifies the identifier for the role to grant. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`ROLE parent_role_name`
:   Grants the role to the specified role.

`USER user_name`
:   Grants the role to the specified user.

[Preview Feature](/release-notes/preview-features) — Open

The `FOR INTERVAL`, `UNTIL`, and `RESET EXPIRATION` clauses are in preview, and are available to all accounts.

`FOR INTERVAL interval`
:   Specifies that the grant of the role to the user expires after the specified length of time.

    Specify *interval* as a quoted string in the form `'integer unit'`, where:

    - *integer* is a positive whole number.
    - *unit* is `MINUTE`, `HOUR`, or `DAY`, or the plural form (`MINUTES`, `HOURS`, or `DAYS`). The unit is case-insensitive.

    For example, `'30 MINUTES'`, `'24 HOURS'`, or `'7 DAYS'`. You can specify only one unit; for example, `'1 DAY 12 HOURS'` isn’t
    supported. To specify 36 hours, use `'36 HOURS'`.

`UNTIL timestamp`
:   Specifies that the grant of the role to the user expires at the specified timestamp. The timestamp must be in the future and must
    include an explicit time zone designator (`Z`) or a numeric offset (for example, `+00:00` or `-07:00`). Timestamps without an offset
    aren’t supported. The following formats are supported:

    - `YYYY-MM-DDTHH:MM:SSZ`
    - `YYYY-MM-DDTHH:MM:SS+00:00`
    - `YYYY-MM-DD HH:MM:SSZ`
    - `YYYY-MM-DD HH:MM:SS+00:00`

`RESET EXPIRATION`
:   Sets the expiration of your existing grant of this role to this user to exactly the expiration in this statement.

    Without this clause, granting the role again keeps the longer of the existing and new lifetimes, so the new expiration
    takes effect only if it’s later. For example, use `RESET EXPIRATION` to shorten a temporary grant or to make a
    permanent grant temporary. For details, see [Granting a role to a user again](#label-grant-role-regrant-to-user).

`WITH GRANT OPTION`
:   If specified, allows the recipient role to grant the role to other roles. The recipient can include
    `WITH GRANT OPTION` on those grants.

    Default: No value, which means the recipient role can’t grant the role to other roles. The recipient
    still inherits the privileges of the granted role.

    Note

    `WITH GRANT OPTION` is valid on a grant to a role.
    `GRANT ROLE ... TO USER ... WITH GRANT OPTION` isn’t supported.

    The same clause is supported for database roles and application roles. See
    [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role) and [GRANT APPLICATION ROLE](/sql-reference/sql/grant-application-role).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Role | Role that is granted to a user or another role. |

Expand

Show lessSee more

Alternatively, use a role with the global MANAGE GRANTS privilege. Only the SECURITYADMIN role, or a higher role, has this privilege by default. The privilege can be granted to additional roles as needed.

A role that was granted the role with `WITH GRANT OPTION` can also grant that role to other roles.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The system-defined roles, including PUBLIC, do not need to be granted to other roles because the role hierarchy for these roles is
  defined and maintained by Snowflake.
- Only a grant
  that includes `WITH GRANT OPTION` lets the recipient grant that role to other roles.
- To remove only the grant option, or to control grants that were made from it, see
  [REVOKE ROLE](/sql-reference/sql/revoke-role).
- [SHOW GRANTS](/sql-reference/sql/show-grants) `TO ROLE` lists a role grant as the `USAGE` privilege on the granted
  role. The `grant_option` column is `TRUE` when the role was granted with `WITH GRANT OPTION`.

### Temporary role grants to users

- The `FOR INTERVAL` and `UNTIL` clauses apply only to grants of account roles to users. If you use them to grant a role to
  another role, or to grant a [database role](/sql-reference/sql/grant-database-role) to a user or role, the statement fails
  with the following error:

  ```
  004903: SQL compilation error: Timed grants are only supported for user-role grants.
  ```

  Grants of [application roles](/sql-reference/sql/grant-application-role) and privileges granted directly to users don’t
  support these clauses.
- A grant of a role to a user without `FOR INTERVAL` or `UNTIL` is permanent.
- A temporary grant remains active until its expiration time. When the grant expires, the user immediately loses access through that
  grant for new statements.

  For queries on [hybrid tables](/user-guide/tables-hybrid) and queries that run on
  [interactive warehouses](/user-guide/interactive), it can take up to 60 seconds after the grant expires for access to be removed.
- What the user sees after a grant expires depends on how the role is used in the session:

  - If the role is the primary role of the session, the next statement fails with the following error:

    ```
    003048: Role '<role_name>', which was previously activated in this session, is no longer available to the executing user.  Login again to create a new session.
    ```
  - If the role is a [secondary role](/user-guide/security-access-control-overview#label-access-control-role-enforcement) of the
    session, the role is removed from the session’s secondary roles without an error.
- A role grant is evaluated when a session is activated or a job is created, and when the role is used. If the grant expires after a job
  is created, the job can continue using the role for the remainder of that job.
- If the same role is granted to a user by multiple grantors, each grant can have its own expiration. The user retains the role while at
  least one of those grants is active. Revoking one grant doesn’t revoke the others.
- Each grantor can have only one active grant for a given role and user.
- If a statement would make the only permanent grant of the ACCOUNTADMIN role in the account temporary, the statement fails with
  the following error. This prevents the account from losing its last administrator when the grant expires.

  ```
  004904: SQL compilation error: Role ACCOUNTADMIN cannot be granted with an expiration to user <user_name> since <user_name> is the only ACCOUNTADMIN; the account would have no administrator once the grant expires.
  ```
- When a grantor grants the same role to the same user again, the result depends on the existing grant. See
  [Granting a role to a user again](#label-grant-role-regrant-to-user).
- The output of [SHOW GRANTS](/sql-reference/sql/show-grants) `TO USER` and `OF ROLE` and the
  [GRANTS\_TO\_USERS view](/sql-reference/account-usage/grants_to_users) in the ACCOUNT\_USAGE schema include an `expires_on` column for
  role grants. The column is `NULL` for permanent grants.

### Granting a role to a user again

When a grantor grants a role to a user who already has a grant of that role from the same grantor, the existing grant is updated as
shown in the following table. Without `RESET EXPIRATION`, the grant keeps the longer of the existing and new lifetimes, and a permanent
grant counts as the longest. Grants from different grantors are tracked separately.

Keeping the longer lifetime lets independent processes grant the same role to the same user with different expirations without
conflicting. For example, if one workflow grants a role for 8 hours and another grants it for 24 hours, both statements succeed, the user
keeps the role for 24 hours, and the shorter grant doesn’t cut off the longer one. To deliberately shorten a grant, use
`RESET EXPIRATION`.

| Existing grant | New `GRANT ROLE ... TO USER` statement | Result |
| --- | --- | --- |
| None | No `FOR INTERVAL` or `UNTIL` | Permanent grant. |
| None | `FOR INTERVAL` or `UNTIL`, with or without `RESET EXPIRATION` | Temporary grant with the new expiration. |
| Permanent | No `FOR INTERVAL` or `UNTIL` | No change. The grant stays permanent. |
| Permanent | `FOR INTERVAL` or `UNTIL` | No change. The grant stays permanent. |
| Permanent | `FOR INTERVAL` or `UNTIL` with `RESET EXPIRATION` | The grant becomes temporary with the new expiration. |
| Temporary | No `FOR INTERVAL` or `UNTIL` | The grant becomes permanent. |
| Temporary | Later expiration | The expiration is extended to the new value. |
| Temporary | Earlier or same expiration | No change. |
| Temporary | `FOR INTERVAL` or `UNTIL` with `RESET EXPIRATION` | The expiration is set to the new value, earlier or later. |

Expand

Show lessSee more

In all cases, the statement returns the same success message and doesn’t report whether the expiration changed. If a script runs
`GRANT ROLE ... TO USER` without `FOR INTERVAL` or `UNTIL`, it makes existing temporary grants permanent. To check the result, query the
`expires_on` column in the output of SHOW GRANTS TO USER.

## Examples

Copy code

```
GRANT ROLE analyst TO ROLE SYSADMIN;
```

Copy code

```
GRANT ROLE analyst TO USER user1;
```

Grant the `analyst` role to the `data_steward` role and allow `data_steward` to grant `analyst` to
other roles:

Copy code

```
GRANT ROLE analyst TO ROLE data_steward WITH GRANT OPTION;
```

The `data_steward` role can then grant `analyst`:

Copy code

```
USE ROLE data_steward;

GRANT ROLE analyst TO ROLE analyst_west;
```

### Grant a role to a user temporarily

Grant the `oncall` role to the user `alice` for 24 hours:

Copy code

```
GRANT ROLE oncall TO USER alice FOR INTERVAL '24 HOURS';
```

Grant the `analyst` role to `alice` until the specified time. The timestamp must include an explicit time zone offset:

Copy code

```
GRANT ROLE analyst TO USER alice
  UNTIL '2027-08-01T17:00:00Z';

GRANT ROLE analyst TO USER alice
  UNTIL '2027-08-01T17:00:00-07:00';
```

Replace the expiration of the existing temporary grant of the `analyst` role to `alice`:

Copy code

```
GRANT ROLE analyst TO USER alice FOR INTERVAL '48 HOURS' RESET EXPIRATION;
```
