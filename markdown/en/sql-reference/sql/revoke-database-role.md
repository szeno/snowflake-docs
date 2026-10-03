# REVOKE DATABASE ROLE

Revokes a database role from an [account role or another database role](/user-guide/security-access-control-overview#label-access-control-overview-role-types).

See also:
:   [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role) , [GRANT ROLE](/sql-reference/sql/grant-role) , [REVOKE ROLE](/sql-reference/sql/revoke-role) , [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege)

## Syntax

Copy code

```
REVOKE [ GRANT OPTION FOR ]
  DATABASE ROLE <name>
  FROM { ROLE | DATABASE ROLE } <parent_role_name>
  [ RESTRICT | CASCADE ]

REVOKE DATABASE ROLE <name> FROM APPLICATION <app_name>
```

## Parameters

`name`
:   Specifies the identifier for the database role to revoke. If the identifier contains spaces or special characters, the entire string must
    be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`DATABASE ROLE parent_role_name`
:   Revokes the database role from the specified database role.

`ROLE parent_role_name`
:   Revokes the database role from the specified account role.

`APPLICATION app_name`
:   Revokes the database role from the specified Snowflake Native App.

## Optional parameters

`GRANT OPTION FOR`
:   If specified, removes the ability for the recipient role to grant the database role to another role.
    The database role grant itself remains, so the recipient role still inherits the granted database
    role’s privileges.

    Default: No value, which revokes the database role grant.

`RESTRICT | CASCADE`
:   Determines whether the revoke operation succeeds when the database role has been re-granted to
    another role. These clauses apply to `REVOKE DATABASE ROLE ... FROM ROLE` and
    `REVOKE DATABASE ROLE ... FROM DATABASE ROLE`.

    - `RESTRICT`: If the database role being revoked has been re-granted to another role, the REVOKE
      command fails.
    - `CASCADE`: If the database role being revoked has been re-granted, the REVOKE command recursively
      revokes these dependent grants. `GRANT OPTION FOR ... CASCADE` revokes the dependent grants and
      leaves the database role grant in place without the grant option. `CASCADE` without
      `GRANT OPTION FOR` revokes the database role grant and the dependent grants.

    Default: `RESTRICT`

## Examples

Revokes the database role named `analyst` from the account role named `SYSADMIN`.

Copy code

```
REVOKE DATABASE ROLE analyst FROM ROLE SYSADMIN;
```

Revokes the database role named `dr1` from another database role named `dr2`.

Copy code

```
REVOKE DATABASE ROLE dr1 FROM DATABASE ROLE dr2;
```

Revokes the database role named `dr1` from the Snowflake Native App named `hello_snowflake_app`.

Copy code

```
REVOKE DATABASE ROLE dr1 FROM APPLICATION hello_snowflake_app;
```

Remove only the grant option from the `data_steward` role. `data_steward` keeps the database role:

Copy code

```
REVOKE GRANT OPTION FOR DATABASE ROLE mydb.analyst FROM ROLE data_steward;
```

Revoke the database role from `data_steward`, including grants of that database role that
`data_steward` made:

Copy code

```
REVOKE DATABASE ROLE mydb.analyst FROM ROLE data_steward CASCADE;
```
