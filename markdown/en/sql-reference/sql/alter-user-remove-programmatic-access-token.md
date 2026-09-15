# ALTER USER … REMOVE PROGRAMMATIC ACCESS TOKEN (PAT)

Revokes a [programmatic access token](/user-guide/programmatic-access-tokens) for a user.

Note

You cannot revoke a programmatic access token in a session where you used a programmatic access token for authentication.

See also:
:   [ALTER USER … ADD PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-add-programmatic-access-token) ,
    [ALTER USER … MODIFY PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-modify-programmatic-access-token) ,
    [ALTER USER … ROTATE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-rotate-programmatic-access-token) ,
    [SHOW USER PROGRAMMATIC ACCESS TOKENS](/sql-reference/sql/show-user-programmatic-access-tokens)

## Syntax

Copy code

```
ALTER USER [ IF EXISTS ] [ <username> ] REMOVE { PROGRAMMATIC ACCESS TOKEN | PAT } [ IF EXISTS ] <token_name>
```

## Parameters

`username`
:   The name of the user that the token is associated with.

    If you omit this parameter, the command revokes the token for the user who is currently logged in (the active user in the
    current session).

`REMOVE { PROGRAMMATIC ACCESS TOKEN | PAT } token_name`
:   Revokes a programmatic access token with the specified name.

    You can use the keyword PAT as a shorter way of specifying the keywords PROGRAMMATIC ACCESS TOKEN.

`IF EXISTS`
:   Revokes the programmatic access token only if a token with the specified name exists for the user. If no token with that
    name exists, the command does nothing and completes successfully instead of returning an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MODIFY PROGRAMMATIC AUTHENTICATION METHODS | User | Required only when revoking a programmatic access token for a human user other than yourself or a service user. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You cannot use revoked programmatic access tokens for authentication.
- You cannot recover programmatic access tokens. You must generate a new programmatic access token instead.
- You cannot revoke a programmatic access token in a session where you used a programmatic access token for authentication.

## Examples

Revoke a programmatic access token named `example_token` from the user `example_user`:

Copy code

```
ALTER USER IF EXISTS example_user REMOVE PROGRAMMATIC ACCESS TOKEN example_token;
```
