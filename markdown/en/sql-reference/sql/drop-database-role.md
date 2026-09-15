# DROP DATABASE ROLE

Removes the specified database role from the system.

See also:
:   [CREATE DATABASE ROLE](/sql-reference/sql/create-database-role) , [ALTER DATABASE ROLE](/sql-reference/sql/alter-database-role) , [SHOW DATABASE ROLES](/sql-reference/sql/show-database-roles)

## Syntax

Copy code

```
DROP DATABASE ROLE [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier (i.e. name) for the database role; must be unique in the database in which the role is created.

    The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    If the identifier is not fully qualified (in the form of `db_name.database_role_name`, the command looks for the database role
    in the current database for the session.

## Usage notes

- Dropped database roles cannot be recovered; they must be recreated.
- Ownership of any objects owned by the dropped database role is transferred to the role that executes the DROP DATABASE ROLE
  command. To transfer ownership of each of these objects to a different database role, use
  [GRANT OWNERSHIP … COPY CURRENT GRANTS](/sql-reference/sql/grant-ownership).
- If a database role has a future privilege as a grantor or grantee, the database role can only be dropped by a user with a role
  that has the MANAGE GRANTS privilege.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

- All current and future grants that name the database role as either the grantor or the grantee are removed when the database role is
  dropped.

  Query the [GRANTS\_TO\_ROLES](/sql-reference/account-usage/grants_to_roles) Account Usage view to retrieve the privilege grants
  that name a specified database role as the grantor or grantee:

  Copy code

  ```
  SELECT *
    FROM snowflake.account_usage.grants_to_roles
    WHERE grantee_name = upper('<database_name>.<db_role_name>') OR granted_by = upper('<database_name>.<db_role_name>');
  ```

  The following example retrieves the grants where `d1.dr1` is the grantor or grantee:

  Copy code

  ```
  SELECT *
    FROM snowflake.account_usage.grants_to_roles
    WHERE grantee_name = upper('d1.dr1') OR granted_by = upper('d1.dr1');
  ```

## Examples

> Copy code
>
> ```
> DROP DATABASE ROLE d1.dr1;
> ```
