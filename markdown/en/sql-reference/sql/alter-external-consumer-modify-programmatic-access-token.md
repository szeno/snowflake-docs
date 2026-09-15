# ALTER EXTERNAL CONSUMER … MODIFY PROGRAMMATIC ACCESS TOKEN (PAT)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Modifies the properties of a Programmatic Access Token (PAT) for an external consumer.

See also:
:   [ALTER EXTERNAL CONSUMER … ADD PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-add-programmatic-access-token) ,
    [ALTER EXTERNAL CONSUMER … REMOVE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-remove-programmatic-access-token) ,
    [ALTER EXTERNAL CONSUMER … ROTATE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-rotate-programmatic-access-token) ,
    [SHOW USER PROGRAMMATIC ACCESS TOKENS FOR EXTERNAL CONSUMER](/sql-reference/sql/show-external-consumer-programmatic-access-tokens)

## Syntax

Copy code

```
ALTER EXTERNAL CONSUMER <name>
  MODIFY { PROGRAMMATIC ACCESS TOKEN | PAT } [ IF EXISTS ] <token_name>
  [ SET
    [ DAYS_TO_EXPIRY = <integer> ]
    [ COMMENT = '<string_literal>' ]
  ]
  [ UNSET
    [ COMMENT ]
  ]
```

## Required parameters

`name`
:   Specifies the identifier for the external consumer.

`MODIFY { PROGRAMMATIC ACCESS TOKEN | PAT } token_name`
:   Modifies the programmatic access token with the specified name. `PAT` is an alias for `PROGRAMMATIC ACCESS TOKEN`.

## Optional parameters

`IF EXISTS`
:   Applies the change only if a token with the specified name exists. If no token with that name exists, the command does nothing
    and completes successfully instead of returning an error.

`DAYS_TO_EXPIRY = integer`
:   Updates the number of days that the token can be used for authentication.

`COMMENT = 'string_literal'`
:   Updates the comment on the token.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | External Consumer | Required to modify a PAT for the external consumer. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

Update the comment on a PAT:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer MODIFY PAT acme_pat
  SET COMMENT = 'Renewed for Q3 access';
```

Update the expiry on a PAT:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer MODIFY PAT acme_pat
  SET DAYS_TO_EXPIRY = 30;
```
