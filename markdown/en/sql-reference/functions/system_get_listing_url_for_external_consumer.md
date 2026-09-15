Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$GET\_LISTING\_URL\_FOR\_EXTERNAL\_CONSUMER

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns the catalog URL and catalog URI for an external listing, enabling an external consumer to connect using an Iceberg REST Catalog client.

See also:
:   [Open Data Sharing](/user-guide/open-data-sharing)

## Syntax

Copy code

```
SYSTEM$GET_LISTING_URL_FOR_EXTERNAL_CONSUMER( '<listing_name>' )
```

## Arguments

**Required:**

`'listing_name'`
:   Name of the external listing. The name must be enclosed in single quotes.

## Returns

Returns a JSON object containing the following fields:

| Field | Description |
| --- | --- |
| `catalog` | The catalog name the external consumer uses to identify the shared data. |
| `catalog_uri` | The Iceberg REST Catalog endpoint URL the external consumer uses to connect. |
| `scope` | The OAuth scope required when requesting an access token for the Iceberg REST Catalog session. |
| `oauth_token_uri` | The OAuth token endpoint URL the external consumer uses to obtain an access token for the catalog. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP or USAGE | Listing | Required to retrieve the catalog URL for the listing. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The external consumer must authenticate using the Programmatic Access Token (PAT) generated for their external consumer identity.
- During Public Preview, the catalog URI returns data only from the region where the provider account is located.
- Provide both the `catalog_uri` value and the PAT to the external consumer so they can connect with an Iceberg REST Catalog client.

## Examples

Retrieve the catalog URL for an external listing named `TEST_LISTING`:

Copy code

```
CALL SYSTEM$GET_LISTING_URL_FOR_EXTERNAL_CONSUMER('TEST_LISTING');
```

Example output:

Copy code

```
{
  "catalog": "my-listing-GZ1Z23",
  "catalog_uri": "https://myorg-myalias.snowflakecomputing.com/polaris/open-sharing/api/catalog",
  "scope": "session:role:external",
  "oauth_token_uri": "https://myorg-myalias.snowflakecomputing.com/polaris/open-sharing/api/catalog/v1/oauth/tokens"
}
```
