# REVOKE\_FROM\_PUBLIC\_APPLICATION\_ROLE

Revokes an administrator-revocable capability from the `SNOWFLAKE.PUBLIC` application role. The capability stays revoked across Snowflake
upgrades until you restore it with [GRANT\_TO\_PUBLIC\_APPLICATION\_ROLE](/sql-reference/stored-procedures/snowflake_local_grant_to_public_application_role).

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.REVOKE_FROM_PUBLIC_APPLICATION_ROLE(
  '<kind>',
  '<name>'
)
```

## Arguments

`'kind'`
:   The type of capability: `PRIVILEGE`, `APP_ROLE`, or `DB_ROLE`. In the output of `SHOW GRANTS TO APPLICATION ROLE SNOWFLAKE.PUBLIC`,
    these correspond to a `granted_on` value of `ACCOUNT`, `APPLICATION_ROLE`, or `DATABASE_ROLE`.

`'name'`
:   The name of the capability. For a privilege, replace spaces with underscores; for example, `USE_AI_FUNCTIONS`. For a role,
    omit the `SNOWFLAKE.` prefix; for example, `CORTEX-MODEL-ROLE-ALL`.

## Returns

Returns a `VARCHAR` value in the form `Revoked <name>`.

## Access control requirements

A role must be granted the `SNOWFLAKE.SNOWFLAKE_PUBLIC_GRANT_ADMIN` application role to call this stored procedure. By default, only
the `ACCOUNTADMIN` role is granted this application role. `ACCOUNTADMIN` can grant it to other roles:

Copy code

```
GRANT APPLICATION ROLE SNOWFLAKE.SNOWFLAKE_PUBLIC_GRANT_ADMIN TO ROLE my_role;
```

## Usage notes

- To list the capabilities granted to `SNOWFLAKE.PUBLIC`, run `SHOW GRANTS TO APPLICATION ROLE SNOWFLAKE.PUBLIC`.
- Users who receive the capability only through `SNOWFLAKE.PUBLIC` lose it. Before you revoke a capability, grant it directly to the roles
  that still need it.
- Use this stored procedure instead of a `REVOKE` statement. A `REVOKE` statement doesn’t remove the capability from `SNOWFLAKE.PUBLIC` or
  persist across Snowflake upgrades.
- The stored procedure returns an error if the capability isn’t administrator-revocable.
- Revoking a capability that is already revoked succeeds.

## Examples

Copy code

```
USE ROLE ACCOUNTADMIN;

CALL SNOWFLAKE.LOCAL.REVOKE_FROM_PUBLIC_APPLICATION_ROLE('PRIVILEGE', 'USE_AI_FUNCTIONS');
```
