# GENERATE\_POSTGRES\_ACCESS\_TOKEN\_FOR\_USER

Generates a short-lived access token to use as a password when logging into a Snowflake Postgres instance that has
the `AUTHENTICATION_AUTHORITY` attribute set to `POSTGRES_OR_SNOWFLAKE`.

Short-lived access tokens generated with this function have a 15-minute lifetime. Once expired they can no longer be used to
establish new connections to the Snowflake Postgres instance. Expiry doesn’t close established connections.
A token is valid only for the instance it was generated for, including when connecting to a replica or fork.

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
:   Specifies the Postgres username to authenticate as. Snowflake resolves the corresponding
    access-role name case-insensitively. Individual user-token authentication compares the Postgres
    username case-sensitively.

    For access-role naming and incompatible mappings, see
    [Access-role requirements and names](/user-guide/snowflake-postgres/postgres-authentication#label-sfpg-token-auth-access-role-requirements).

## Returns

Returns a short-lived access token that has a 15-minute lifetime.

## Access control requirements

The function evaluates permissions from your primary role and active secondary roles, including
their inherited roles. It returns the first applicable token in the following order:

1. **Owner token**: The active role hierarchy has `OWNERSHIP` on the instance. The token can
   authenticate as any Postgres login role, except superusers, replication users, and protected
   system users. See the [owner-token login requirements](/user-guide/snowflake-postgres/postgres-authentication#label-sfpg-token-auth-token-types).
2. **Access role token**: The caller holds the
   [access role](/user-guide/snowflake-postgres/postgres-authentication#label-sfpg-token-auth-access-roles)
   for `postgres_username`. The token can
   authenticate as the corresponding enrolled Postgres user.
3. **User token**: The token represents the calling Snowflake user’s identity.

Attention

If you have neither `OWNERSHIP` on the instance nor the access role for the requested Postgres
user, the function returns a user token when your active role hierarchy has `USAGE` on the instance.
Generating a token doesn’t validate the Postgres user’s existence or mapping. When you connect with a
user token, Postgres checks that the requested Postgres login role is mapped to the Snowflake user who generated
the token. An unexpired user token can authenticate after the required mapping is created. For mapping
steps, see [Map a Postgres user to a Snowflake user](/user-guide/snowflake-postgres/postgres-authentication#label-sfpg-token-auth-user-mappings).

If no token type applies, the function fails. You can’t call this function from an owner’s rights stored procedure unless the owner of the
procedure has `OWNERSHIP` on the instance or holds the access role. The user-token fallback isn’t
available in an owner’s rights stored procedure.

`MANAGE GRANTS` authorizes access-role grants and revokes; it doesn’t by itself authorize an owner
token. For the effect of revocation, Postgres role changes, and expiry on new and existing connections,
see [When revoked access takes effect](/user-guide/snowflake-postgres/postgres-authentication#label-sfpg-token-auth-revocation).

## Examples

For Postgres access role creation and client connection steps, see
[Grant access with access roles](/user-guide/snowflake-postgres/postgres-authentication#label-sfpg-token-auth-access-roles).

After you enable `SNOWFLAKE_ACCESS_ROLE` for the Postgres user `app_user`, a Snowflake role with
`OWNERSHIP` on the instance or `MANAGE GRANTS` on the account grants the Postgres user’s access role
to the existing role `analyst`. In this example, `analyst` doesn’t hold `OWNERSHIP` on the instance.
A user assigned `analyst` activates it and generates a token for `app_user`:

Copy code

```
GRANT POSTGRES ACCESS ROLE my_instance!app_user TO ROLE analyst;
USE ROLE analyst;
SELECT GENERATE_POSTGRES_ACCESS_TOKEN_FOR_USER('my_instance', 'app_user');
```

Snowflake user Casey can generate a short-lived access token to use when logging into the `reporting_server` with a Postgres user
named `reporting_user`. For a user token, first create the individual mapping described in
[Map a Postgres user to a Snowflake user](/user-guide/snowflake-postgres/postgres-authentication#label-sfpg-token-auth-user-mappings):

Copy code

```
SELECT GENERATE_POSTGRES_ACCESS_TOKEN_FOR_USER('reporting_server', 'reporting_user');
```

If the instance’s name was created case-sensitive as `Reporting_server` then double-quotes are needed for the instance name:

Copy code

```
SELECT GENERATE_POSTGRES_ACCESS_TOKEN_FOR_USER('"Reporting_server"', 'reporting_user');
```
