# REVOKE APPLICATION ROLE

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Revokes an application role from an account role or another application role.

See also:
:   [ALTER APPLICATION ROLE](/sql-reference/sql/alter-application-role), [CREATE APPLICATION ROLE](/sql-reference/sql/create-application-role), [GRANT APPLICATION ROLE](/sql-reference/sql/grant-application-role),
    [SHOW APPLICATION ROLES](/sql-reference/sql/show-application-roles)

## Syntax

Copy code

```
REVOKE APPLICATION ROLE <name> FROM { ROLE <parent_role_name> | APPLICATION ROLE <application_role> | APPLICATION <application> }
```

## Parameters

`name`
:   Specifies the identifier for the application role to revoke. If the identifier contains spaces or special
    characters, the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`FROM ROLE parent_role_name`
:   Revokes the application role from the specified account role.

`APPLICATION ROLE application_role`
:   Revokes the role from the specified application role.

`APPLICATION ROLE application`
:   Revokes the role from the specified application.

## Usage notes

An application role may only be revoked from another application role within the context of
the installed application, for example within the application setup script.

## Examples

Copy code

```
REVOKE APPLICATION ROLE app_role FROM APPLICATION ROLE other_role;
```
