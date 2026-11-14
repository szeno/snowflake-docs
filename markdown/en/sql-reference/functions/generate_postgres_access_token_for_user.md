# GENERATE\_POSTGRES\_ACCESS\_TOKEN\_FOR\_USER

Generates a short-lived access token to use as a password when logging into a Snowflake Postgres instance that has
the AUTHENTICATION\_AUTHORITY attribute set to POSTGRES\_OR\_SNOWFLAKE.

Short-lived access tokens generated with this function have a 15-minute lifetime. Once expired they can no longer be used to
establish new connections to the Snowflake Postgres instance.

For mapping and token steps, see [Configure authentication for Snowflake Postgres](/user-guide/snowflake-postgres/postgres-authentication).

## Syntax

Copy code

```
GENERATE_POSTGRES_ACCESS_TOKEN_FOR_USER('<snowflake_postgres_instance_name>', '<postgres_username>')
```

## Arguments

`snowflake_postgres_instance_name`
:   Specifies the Snowflake Postgres instance name to generate the short-lived access token for. If the given instance does not exist,
    or the caller doesn’t meet the [access control requirements](#label-generate-postgres-access-token-access-control), the function
    fails.

    This argument is case-insensitive. Use double-quotes if case-sensitivity is needed.

`postgres_username`
:   Specifies the Postgres username to generate the short-lived access token for. This argument is not validated, which allows for creating
    unusable tokens for Postgres users that do not exist or are not mapped to a Snowflake user. Valid tokens will be usable if a mapping is
    subsequently created.

    This argument is case-sensitive.

## Returns

Returns a short-lived access token that has a 15-minute lifetime.

## Access control requirements

The function checks the caller’s active role hierarchy in the following order and returns the first token that applies:

1. **Owner token** (*Preview*): the role has the OWNERSHIP privilege on the instance, or the MANAGE GRANTS privilege on the account. The token can log in as any Postgres user that uses password authentication, or any Postgres user that has an access role.
2. **Access role token** (*Preview*): the role holds the [access role](/user-guide/snowflake-postgres/postgres-authentication#label-sfpg-token-auth-access-roles)
   for `postgres_username`. The token can log in as that Postgres user.
3. **User token**: the role has the USAGE privilege on the instance. The token can log in as the Postgres user mapped to the
   calling Snowflake user.

If none apply, the function fails. You can’t call this function from an owner’s rights stored procedure unless the owner of the
procedure has the OWNERSHIP privilege on the instance, the MANAGE GRANTS privilege on the account, or holds the access role.

## Examples

Access roles are in preview. A role with the OWNERSHIP privilege on the instance, a role with the MANAGE GRANTS privilege on the account, or the SYSADMIN role can grant the access role. A role that holds `my_instance!app_user` can then generate a token to log in as `app_user`:

Copy code

```
GRANT POSTGRES ACCESS ROLE my_instance!app_user TO ROLE analyst;
USE ROLE analyst;
SELECT GENERATE_POSTGRES_ACCESS_TOKEN_FOR_USER('my_instance', 'app_user');
```

Snowflake user Casey can generate a short-lived access token to use when logging into the `reporting_server` with a Postgres user
named `reporting_user` with:

Copy code

```
SELECT GENERATE_POSTGRES_ACCESS_TOKEN_FOR_USER('reporting_server', 'reporting_user');
```

If the instance’s name was created case-sensitive as `Reporting_server` then double-quotes are needed for the instance name:

Copy code

```
SELECT GENERATE_POSTGRES_ACCESS_TOKEN_FOR_USER('"Reporting_server"', 'reporting_user');
```
