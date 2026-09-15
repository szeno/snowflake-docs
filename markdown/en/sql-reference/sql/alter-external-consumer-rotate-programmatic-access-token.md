# ALTER EXTERNAL CONSUMER … ROTATE PROGRAMMATIC ACCESS TOKEN (PAT)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Rotates a Programmatic Access Token (PAT) for an external consumer, generating a new token secret and expiring the existing one.
The new secret uses the same `DAYS_TO_EXPIRY` value set when the token was first created.

See also:
:   [ALTER EXTERNAL CONSUMER … ADD PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-add-programmatic-access-token) ,
    [ALTER EXTERNAL CONSUMER … REMOVE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-remove-programmatic-access-token) ,
    [ALTER EXTERNAL CONSUMER … MODIFY PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-modify-programmatic-access-token) ,
    [SHOW USER PROGRAMMATIC ACCESS TOKENS FOR EXTERNAL CONSUMER](/sql-reference/sql/show-external-consumer-programmatic-access-tokens)

## Syntax

Copy code

```
ALTER EXTERNAL CONSUMER <name>
  ROTATE { PROGRAMMATIC ACCESS TOKEN | PAT } [ IF EXISTS ] <token_name>
  [ EXPIRE_ROTATED_TOKEN_AFTER_HOURS = <integer> ]
```

## Required parameters

`name`
:   Specifies the identifier for the external consumer.

`ROTATE { PROGRAMMATIC ACCESS TOKEN | PAT } token_name`
:   Rotates the programmatic access token with the specified name. `PAT` is an alias for `PROGRAMMATIC ACCESS TOKEN`.

## Optional parameters

`IF EXISTS`
:   Rotates the token only if a token with the specified name exists. If no token with that name exists, the command does nothing
    and completes successfully instead of returning an error.

`EXPIRE_ROTATED_TOKEN_AFTER_HOURS = integer`
:   Sets the number of hours after which the prior token secret expires. Set to `0` to expire the prior secret immediately.

    Default: `24`

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | External Consumer | Required to rotate a PAT for the external consumer. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You must save the new token secret when Snowflake returns it. You cannot retrieve the secret later.
- Provide the new token secret to the external consumer to replace the prior secret before it expires.

## Examples

Rotate a PAT for an external consumer:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer ROTATE PAT acme_pat;
```

Rotate a PAT and expire the prior secret immediately:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer ROTATE PAT acme_pat
  EXPIRE_ROTATED_TOKEN_AFTER_HOURS = 0;
```
