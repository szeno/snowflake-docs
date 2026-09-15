# ALTER EXTERNAL CONSUMER … REMOVE PROGRAMMATIC ACCESS TOKEN (PAT)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Revokes a Programmatic Access Token (PAT) from an external consumer. Once removed, the token can no longer
be used to authenticate.

See also:
:   [ALTER EXTERNAL CONSUMER … ADD PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-add-programmatic-access-token) ,
    [ALTER EXTERNAL CONSUMER … ROTATE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-rotate-programmatic-access-token) ,
    [ALTER EXTERNAL CONSUMER … MODIFY PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-modify-programmatic-access-token) ,
    [SHOW USER PROGRAMMATIC ACCESS TOKENS FOR EXTERNAL CONSUMER](/sql-reference/sql/show-external-consumer-programmatic-access-tokens)

## Syntax

Copy code

```
ALTER EXTERNAL CONSUMER [ IF EXISTS ] <name>
  REMOVE { PROGRAMMATIC ACCESS TOKEN | PAT } [ IF EXISTS ] <token_name>
```

## Parameters

`IF EXISTS`
:   For the external consumer: applies the change only if the consumer exists.

    For the token: removes the token only if a token with the specified name exists. If no token with that name exists, the command
    does nothing and completes successfully instead of returning an error.

`name`
:   Specifies the identifier for the external consumer.

`REMOVE { PROGRAMMATIC ACCESS TOKEN | PAT } token_name`
:   Revokes the programmatic access token with the specified name. `PAT` is an alias for `PROGRAMMATIC ACCESS TOKEN`.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | External Consumer | Required to remove a PAT from the external consumer. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Revoked tokens cannot be recovered. You must generate a new token using [ALTER EXTERNAL CONSUMER … ADD PAT](/sql-reference/sql/alter-external-consumer-add-programmatic-access-token).
- Removing a token immediately revokes the external consumer’s ability to authenticate using that token.

## Examples

Remove a PAT from an external consumer:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer REMOVE PAT acme_pat;
```

Remove a PAT if it exists:

Copy code

```
ALTER EXTERNAL CONSUMER IF EXISTS acme_consumer REMOVE PAT IF EXISTS acme_pat;
```
