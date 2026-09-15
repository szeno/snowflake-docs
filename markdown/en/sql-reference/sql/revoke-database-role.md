# REVOKE DATABASE ROLE

Revokes a database role from an [account role or another database role](/user-guide/security-access-control-overview#label-access-control-overview-role-types).

See also:
:   [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role) , [GRANT ROLE](/sql-reference/sql/grant-role) , [REVOKE ROLE](/sql-reference/sql/revoke-role) , [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege)

## Syntax

Copy code

```
REVOKE DATABASE ROLE <name> FROM { ROLE | DATABASE ROLE } <parent_role_name>

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
