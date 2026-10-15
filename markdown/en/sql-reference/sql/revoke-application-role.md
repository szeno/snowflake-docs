# REVOKE APPLICATION ROLE

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Revokes an application role from an account role, another application role, an application, or a user.

See also:
:   [ALTER APPLICATION ROLE](/sql-reference/sql/alter-application-role), [CREATE APPLICATION ROLE](/sql-reference/sql/create-application-role), [GRANT APPLICATION ROLE](/sql-reference/sql/grant-application-role),
    [SHOW APPLICATION ROLES](/sql-reference/sql/show-application-roles)

    [REVOKE ROLE](/sql-reference/sql/revoke-role), [REVOKE DATABASE ROLE](/sql-reference/sql/revoke-database-role)

## Syntax

Copy code

```
REVOKE [ GRANT OPTION FOR ]
  APPLICATION ROLE <name>
  FROM ROLE <parent_role_name>
  [ RESTRICT | CASCADE ]

REVOKE APPLICATION ROLE <name> FROM { APPLICATION ROLE <application_role> | APPLICATION <application> | USER <user_name> }
```

## Parameters

`name`
:   Specifies the identifier for the application role to revoke. If the identifier contains spaces or special
    characters, the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`FROM ROLE parent_role_name`
:   Revokes the application role from the specified account role.

`APPLICATION ROLE application_role`
:   Revokes the role from the specified application role.

`APPLICATION application`
:   Revokes the role from the specified application.

`USER user_name`
:   Revokes the application role from the specified user.

## Optional parameters

`GRANT OPTION FOR`
:   If specified, removes the ability for the recipient account role to grant the application role further.
    The application role grant itself remains, so the recipient role still inherits the application role’s
    privileges.

    Default: No value, which revokes the application role grant.

`RESTRICT | CASCADE`
:   Determines whether the revoke operation succeeds when the recipient role has granted the application role
    further. These clauses apply to `REVOKE APPLICATION ROLE ... FROM ROLE`.

    - `RESTRICT`: If the recipient role has granted the application role further, the REVOKE command fails.
    - `CASCADE`: If the recipient role has granted the application role further, the REVOKE command
      recursively revokes these dependent grants. `GRANT OPTION FOR ... CASCADE` revokes the dependent grants
      and leaves the application role grant in place without the grant option. `CASCADE` without
      `GRANT OPTION FOR` revokes the application role grant and the dependent grants.

    Default: `RESTRICT`

## Usage notes

An application role may only be revoked from another application role within the context of
the installed application, for example, in the application’s setup script.

## Examples

Revokes the application role `app_role` from the application role `other_role`:

Copy code

```
REVOKE APPLICATION ROLE app_role FROM APPLICATION ROLE other_role;
```

Revokes the application role `app_role` in the application `my_app` from the user `user1`:

Copy code

```
REVOKE APPLICATION ROLE my_app.app_role FROM USER user1;
```

Removes only the grant option on `my_app.app_role` from the account role `analyst`. The `analyst` role
keeps the application role:

Copy code

```
REVOKE GRANT OPTION FOR APPLICATION ROLE my_app.app_role FROM ROLE analyst;
```

Revokes `my_app.app_role` from the account role `analyst`, including grants of `my_app.app_role` that
`analyst` made:

Copy code

```
REVOKE APPLICATION ROLE my_app.app_role FROM ROLE analyst CASCADE;
```
