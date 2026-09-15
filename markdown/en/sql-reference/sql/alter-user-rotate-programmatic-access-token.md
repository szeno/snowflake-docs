# ALTER USER … ROTATE PROGRAMMATIC ACCESS TOKEN (PAT)

Rotates a [programmatic access token](/user-guide/programmatic-access-tokens), generating a new token secret with an
extended expiration time, and expiring the existing token secret. The new secret is generated using the same DAYS\_TO\_EXPIRY
property set when the token was first created.

Note

You cannot rotate a programmatic access token in a session where you used a programmatic access token for the same user for
authentication.

See also:
:   [ALTER USER … ADD PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-add-programmatic-access-token),
    [ALTER USER … MODIFY PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-modify-programmatic-access-token),
    [ALTER USER … REMOVE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-user-remove-programmatic-access-token),
    [SHOW USER PROGRAMMATIC ACCESS TOKENS](/sql-reference/sql/show-user-programmatic-access-tokens)

## Syntax

Copy code

```
ALTER USER [ IF EXISTS ] [ <username> ] ROTATE { PROGRAMMATIC ACCESS TOKEN | PAT } [ IF EXISTS ] <token_name>
  [ EXPIRE_ROTATED_TOKEN_AFTER_HOURS = <integer> ]
```

## Parameters

`username`
:   The name of the user that the token is associated with.

    If you omit this parameter, the command rotates the token for the user who is currently logged in (the active user in the
    current session).

`ROTATE { PROGRAMMATIC ACCESS TOKEN | PAT } token_name`
:   Rotates a programmatic access token with the specified name.

    You can use the keyword PAT as a shorter way of specifying the keywords PROGRAMMATIC ACCESS TOKEN.

`IF EXISTS`
:   Rotates the programmatic access token only if a token with the specified name exists for the user. If no token with that
    name exists, the command does nothing and completes successfully instead of returning an error.

`EXPIRE_ROTATED_TOKEN_AFTER_HOURS = integer`
:   Sets the expiration time of the existing token secret to expire after the specified number of hours.

    You can set this to a value of `0` to expire the current token secret immediately.

    You can set this to a value in the range of `0` to the number of hours remaining before the current secret expires.

    Default: `24`

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MODIFY PROGRAMMATIC AUTHENTICATION METHODS | User | Required only when rotating a programmatic access token for a human user other than yourself or a service user. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Output

The command output provides information about the rotated programmatic access token in the following columns:

| Column | Description |
| --- | --- |
| `token_name` | Name of the rotated token. |
| `token_secret` | The token itself. Use this to authenticate to an endpoint.  Note  The token only appears in the output of the ALTER USER … ROTATE PROGRAMMATIC ACCESS TOKEN command. No other SQL command or function prints out or returns the token.  If you need to access this token programmatically, you can use [Snowflake Scripting](/developer-guide/snowflake-scripting/index) to execute this command and retrieve the token from the [RESULTSET](/developer-guide/snowflake-scripting/resultsets). |
| `rotated_token_name` | Name of the token that represents the prior secret.  You can use this token object to determine how long the prior secret remains valid. You can also expire the token, if needed. You can’t make any other types of changes to this token.  Note that this token object counts against the maximum number of tokens allowed per user. |

Expand

Show lessSee more

## Usage notes

- When you rotate a programmatic access token:

  - Snowflake does not verify that the [network policy](/user-guide/programmatic-access-tokens#label-pat-prerequisites-network) and
    [authentication policy](/user-guide/programmatic-access-tokens#label-pat-prerequisites-authentication) requirements are met.
  - If the programmatic access token is restricted to a role, Snowflake does not verify that the user associated with the token
    has been granted that role.

## Examples

Rotate a programmatic access token associated with the user `example_user`:

Copy code

```
ALTER USER IF EXISTS example_user ROTATE PROGRAMMATIC ACCESS TOKEN token_name;
```

Rotate a programmatic access token associated with the user `example_user` and expire the existing token secret
immediately:

Copy code

```
ALTER USER IF EXISTS example_user ROTATE PROGRAMMATIC ACCESS TOKEN token_name
  EXPIRE_ROTATED_TOKEN_AFTER_HOURS=0;
```
