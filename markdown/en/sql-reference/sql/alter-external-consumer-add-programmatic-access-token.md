# ALTER EXTERNAL CONSUMER … ADD PROGRAMMATIC ACCESS TOKEN (PAT)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Creates a Programmatic Access Token (PAT) for an external consumer. The token is used by the external consumer
to authenticate with an Iceberg REST Catalog client when accessing shared data via [Open Data Sharing](/user-guide/open-data-sharing).

See also:
:   [ALTER EXTERNAL CONSUMER … REMOVE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-remove-programmatic-access-token) ,
    [ALTER EXTERNAL CONSUMER … ROTATE PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-rotate-programmatic-access-token) ,
    [ALTER EXTERNAL CONSUMER … MODIFY PROGRAMMATIC ACCESS TOKEN (PAT)](/sql-reference/sql/alter-external-consumer-modify-programmatic-access-token) ,
    [SHOW USER PROGRAMMATIC ACCESS TOKENS FOR EXTERNAL CONSUMER](/sql-reference/sql/show-external-consumer-programmatic-access-tokens)

## Syntax

Copy code

```
ALTER EXTERNAL CONSUMER <name>
  ADD { PROGRAMMATIC ACCESS TOKEN | PAT } [ IF NOT EXISTS ] <token_name>
  [ DAYS_TO_EXPIRY = <integer> ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   Specifies the identifier for the external consumer to add the token to.

`ADD { PROGRAMMATIC ACCESS TOKEN | PAT } token_name`
:   Creates a programmatic access token with the specified name. `PAT` is an alias for `PROGRAMMATIC ACCESS TOKEN`.

## Optional parameters

`IF NOT EXISTS`
:   Creates the token only if a token with the specified name does not already exist for the external consumer. If a token
    with the same name already exists, the command does nothing and completes successfully without creating a new token or
    returning a token secret.

`DAYS_TO_EXPIRY = integer`
:   The number of days that the token can be used for authentication.

    Default: `15`

`COMMENT = 'string_literal'`
:   Specifies a comment for the token.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | External Consumer | Required to add a PAT to the external consumer. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You must save the token secret when Snowflake returns it. You cannot retrieve the secret later.
- Provide the token secret and the catalog URI returned by [SYSTEM$GET\_LISTING\_URL\_FOR\_EXTERNAL\_CONSUMER](/sql-reference/functions/system_get_listing_url_for_external_consumer) to the external consumer.

## Examples

Add a PAT to an external consumer:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer ADD PAT acme_pat;
```

Add a PAT that expires after 30 days:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer ADD PAT acme_pat
  DAYS_TO_EXPIRY = 30
  COMMENT = 'PAT for Acme Corp data access';
```
