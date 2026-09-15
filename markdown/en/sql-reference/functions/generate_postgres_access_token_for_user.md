# GENERATE\_POSTGRES\_ACCESS\_TOKEN\_FOR\_USER

Generates a short-lived access token for a Snowflake user to use as a password when logging into a Snowflake Postgres instance that has
the AUTHENTICATION\_AUTHORITY attribute set to POSTGRES\_OR\_SNOWFLAKE.

Short-lived access tokens generated with this function have a 15-minute lifetime. Once expired they can no longer be used to
establish new connections to the Snowflake Postgres instance.

See [Snowflake Token Authentication for Snowflake Postgres](/user-guide/snowflake-postgres/postgres-token-auth) for more details.

## Syntax

Copy code

```
GENERATE_POSTGRES_ACCESS_TOKEN_FOR_USER('<snowflake_postgres_instance_name>', '<postgres_username>')
```

## Arguments

`snowflake_postgres_instance_name`
:   Specifies the Snowflake Postgres instance name to generate the short-lived access token for. If the given instance does not exist
    or the executing user does not have ownership or the USAGE permission on the instance, the function execution will fail.

    This argument is case-insensitive. Use double-quotes if case-sensitivity is needed.

`postgres_username`
:   Specifies the Postgres username to generate the short-lived access token for. This argument is not validated, which allows for creating
    unusable tokens for Postgres users that do not exist or are not mapped to a Snowflake user. Valid tokens will be usable if a mapping is
    subsequently created.

    This argument is case-sensitive.

## Returns

Returns a short-lived access token that has a 15-minute lifetime.

## Access control requirements

Execution of this function for a given Snowflake Postgres instance can only be done by the instance’s owner or users granted the USAGE
permission for it.

## Examples

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
