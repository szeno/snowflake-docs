# GRANT ROLE

Assigns a role to a user or another role:

- Granting a role to another role creates a “parent-child” relationship between the roles (also referred to as a *role hierarchy*).
- Granting a role to a user enables the user to perform all operations allowed by the role (through the access privileges granted to the role).

For more details, see [Overview of Access Control](/user-guide/security-access-control-overview).

See also:
:   [REVOKE ROLE](/sql-reference/sql/revoke-role)

    [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role) , [REVOKE DATABASE ROLE](/sql-reference/sql/revoke-database-role)

    [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege)

## Syntax

Copy code

```
GRANT ROLE <name> TO ROLE <parent_role_name> [ WITH GRANT OPTION ]

GRANT ROLE <name> TO USER <user_name>
```

## Parameters

`name`
:   Specifies the identifier for the role to grant. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`ROLE parent_role_name`
:   Grants the role to the specified role.

`USER user_name`
:   Grants the role to the specified user.

`WITH GRANT OPTION`
:   If specified, allows the recipient role to grant the role to other roles. The recipient can include
    `WITH GRANT OPTION` on those grants.

    Default: No value, which means the recipient role can’t grant the role to other roles. The recipient
    still inherits the privileges of the granted role.

    Note

    `WITH GRANT OPTION` is valid on a grant to a role.
    `GRANT ROLE ... TO USER ... WITH GRANT OPTION` isn’t supported.

    The same clause is supported for database roles. See [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role).

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
