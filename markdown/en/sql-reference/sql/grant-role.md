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
GRANT ROLE <name> TO { ROLE <parent_role_name> | USER <user_name> }
```

## Parameters

`name`
:   Specifies the identifier for the role to grant. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`ROLE parent_role_name`
:   Grants the role to the specified role.

`USER user_name`
:   Grants the role to the specified user.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Role | Role that is granted to a user or another role. |

Expand

Show lessSee more

Alternatively, use a role with the global MANAGE GRANTS privilege. Only the SECURITYADMIN role, or a higher role, has this privilege by default. The privilege can be granted to additional roles as needed.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The system-defined roles, including PUBLIC, do not need to be granted to other roles because the role hierarchy for these roles is
  defined and maintained by Snowflake.

## Examples

Copy code

```
GRANT ROLE analyst TO ROLE SYSADMIN;
```

Copy code

```
GRANT ROLE analyst TO USER user1;
```
