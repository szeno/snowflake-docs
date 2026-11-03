# GRANT\_TO\_PUBLIC\_APPLICATION\_ROLE

Restores an administrator-revocable capability on the `SNOWFLAKE.PUBLIC` application role after you revoke it with
[REVOKE\_FROM\_PUBLIC\_APPLICATION\_ROLE](/sql-reference/stored-procedures/snowflake_local_revoke_from_public_application_role).

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.GRANT_TO_PUBLIC_APPLICATION_ROLE(
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

Returns a `VARCHAR` value in the form `Granted <name>`.

## Access control requirements

A role must be granted the `SNOWFLAKE.SNOWFLAKE_PUBLIC_GRANT_ADMIN` application role to call this stored procedure. By default, only
the `ACCOUNTADMIN` role is granted this application role. `ACCOUNTADMIN` can grant it to other roles:

Copy code

```
GRANT APPLICATION ROLE SNOWFLAKE.SNOWFLAKE_PUBLIC_GRANT_ADMIN TO ROLE my_role;
```

## Usage notes

- The stored procedure returns an error if the capability isn’t administrator-revocable.
- Granting a capability that is already granted succeeds.

## Examples

Copy code

```
USE ROLE ACCOUNTADMIN;

CALL SNOWFLAKE.LOCAL.GRANT_TO_PUBLIC_APPLICATION_ROLE('PRIVILEGE', 'USE_AI_FUNCTIONS');
```
