# DROP ROLE

Removes the specified role from the system.

See also:
:   [CREATE ROLE](/sql-reference/sql/create-role) , [ALTER ROLE](/sql-reference/sql/alter-role) , [SHOW ROLES](/sql-reference/sql/show-roles)

## Syntax

Copy code

```
DROP ROLE [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the role to drop. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- Dropped roles cannot be recovered; they must be recreated.
- The current primary role cannot be dropped. An attempt to drop this role returns an error. For example:

  Copy code

  ```
  CREATE ROLE bobr_primary;

  GRANT ROLE bobr_primary to USER bobr;

  USE ROLE bobr_primary;

  DROP ROLE bobr_primary;
  ```

  ```
  SQL execution error: Cannot drop role BOBR_PRIMARY as it is the current primary role.
  ```

  For more information, see [Active roles](/user-guide/security-access-control-overview#label-access-control-overview-active-roles) and [Authorization through primary role and secondary roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement).
- A role cannot be dropped if it has the OWNERSHIP privilege on a shared database. Use the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to transfer the
  OWNERSHIP privilege on the shared database first, and then drop the role.
- Ownership of any objects owned by the dropped role is transferred to the role that executes the DROP ROLE command. To transfer
  ownership of each of these objects to a different role, use
  [GRANT OWNERSHIP … COPY CURRENT GRANTS](/sql-reference/sql/grant-ownership).
- All current and future grants that name the role as either the grantor or the grantee are revoked when the role is dropped.

  Query the [GRANTS\_TO\_ROLES](/sql-reference/account-usage/grants_to_roles) Account Usage view to retrieve the privilege grants
  that name a specified role as the grantor or grantee:

  Copy code

  ```
  SELECT *
    FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_ROLES
    WHERE grantee_name = UPPER('<role_name>') OR granted_by = UPPER('<role_name>');
  ```

  The following example retrieves the grants where `myrole` is the grantor or grantee:

  Copy code

  ```
  SELECT *
    FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_ROLES
    WHERE grantee_name = UPPER('myrole') OR granted_by = UPPER('myrole');
  ```
- If a role is a grantor of roles to users, dropping the role revokes these grants automatically.
- Revoking grants happens as the DROP ROLE command executes. If there are thousands or millions of grants to revoke, the DROP ROLE
  command might time out. It is safe to rerun the command to continue execution where the previous invocation stopped.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

- You can drop a role that’s in use by an object inside a [backup](/user-guide/backups). Doing so might take a long time
  if there are backups. That’s because Snowflake rewrites the metadata for grants associated with the objects
  inside backups when a role is dropped.

## Examples

Copy code

```
DROP ROLE myrole;
```
