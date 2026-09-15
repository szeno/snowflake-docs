# GRANT DATABASE ROLE

Assigns a database role to an [account role, another database role](/user-guide/security-access-control-overview#label-access-control-overview-role-types), or a user. A user with
OWNERSHIP privilege on a database role can grant that database role to either an account role, another database role, or a user in the same
database. Granting a database role to another role creates a “parent-child” relationship (also referred to as a *role hierarchy*) between
the database role and the other role. For specific limitations on database roles, see [Database roles and role hierarchies](/user-guide/security-access-control-overview#label-db-role-hierarchy-and-privilege-inheritance).

See also:
:   [REVOKE DATABASE ROLE](/sql-reference/sql/revoke-database-role) , [GRANT ROLE](/sql-reference/sql/grant-role) , [REVOKE ROLE](/sql-reference/sql/revoke-role) , [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege)

## Syntax

Copy code

```
GRANT DATABASE ROLE <name> TO { DATABASE ROLE <parent_role_name> | ROLE <parent_role_name> | USER <user_name> }

GRANT DATABASE ROLE <name> TO APPLICATION <app_name>
```

## Parameters

`name`
:   Specifies the identifier (name) for the database role; must be unique in the database in which the database role is created.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

    If the identifier is not fully qualified in the form of `db_name.database_role_name`, the command looks for the database role
    in the current database for the session.

`ROLE parent_role_name`
:   Grants the database role to the specified account role.

`DATABASE ROLE parent_role_name`
:   Grants the database role to the specified database role. If the parent role is a database role and the identifier is not fully qualified
    in the form of `db_name.database_role_name`, the command looks for the database role in the current database for the session.

`APPLICATION app_name`
:   Grants the database role to the specified Snowflake Native App.

`USER user_name`
:   Grants the database role to the specified user.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege or role | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Database role | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

## Examples

Grants the database role `analyst` to the SYSADMIN role:

Copy code

```
GRANT DATABASE ROLE analyst TO ROLE SYSADMIN;
```

Grants the database role `dr1` to the database role `dr2`:

Copy code

```
GRANT DATABASE ROLE dr1 TO DATABASE ROLE dr2;
```

Grants the database role `db1` to the Snowflake Native App named `hello_snowflake_app`:

Copy code

```
GRANT DATABASE ROLE db1 TO APPLICATION hello_snowflake_app;
```

Grants the database role `dr3` to the user `user1`:

Copy code

```
GRANT DATABASE ROLE dr3 TO USER user1;
```
