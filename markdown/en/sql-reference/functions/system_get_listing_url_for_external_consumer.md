Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$GET\_LISTING\_URL\_FOR\_EXTERNAL\_CONSUMER

Returns the connection details that an external consumer uses to connect to an external listing: the catalog name, catalog URI,
OAuth scope, and OAuth token endpoint. The external consumer uses these values to connect with an Iceberg REST Catalog client.

See also:
:   [Share data with non-Snowflake consumers](/user-guide/open-data-sharing), [Connect to an open-sharing catalog](/user-guide/open-data-sharing-connect)

## Syntax

Copy code

```
SYSTEM$GET_LISTING_URL_FOR_EXTERNAL_CONSUMER( '<listing_name>' , '<external_consumer_name>' )
```

## Arguments

**Required:**

`'listing_name'`
:   Name of the external listing. The name must be enclosed in single quotes.

`'external_consumer_name'`
:   Name of the external consumer to return the connection details for. The external consumer must be a target of the listing. The
    name must be enclosed in single quotes.

    The connection details depend on the external consumer’s region, so a listing that targets consumers in different regions returns
    different values for each consumer.

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
| OWNERSHIP or USAGE | Listing | Required to retrieve the connection details for the listing. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The returned values depend on the external consumer’s region. Call the function separately for each external consumer.
- The external consumer authenticates with a programmatic access token (PAT) or workload identity federation (WIF), depending on how
  you configured the external consumer. For more information, see [Workload identity federation for external consumers](/user-guide/open-data-sharing-workload-identity).
- Provide the `catalog`, `catalog_uri`, `scope`, and `oauth_token_uri` values to the external consumer, along with their PAT or
  workload identity details. The consumer sends token requests to `oauth_token_uri` and catalog requests to `catalog_uri`. For
  instructions, see [Connect to an open-sharing catalog](/user-guide/open-data-sharing-connect).

## Examples

Retrieve the connection details for the external consumer `TEST_EXT_CONSUMER` on the listing `TEST_LISTING`:

Copy code

```
CALL SYSTEM$GET_LISTING_URL_FOR_EXTERNAL_CONSUMER('TEST_LISTING', 'TEST_EXT_CONSUMER');
```

Example output for an external consumer in the provider account’s region:

Copy code

```
{
  "catalog": "my-listing-GZ1Z23",
  "catalog_uri": "https://myorg-myaccount.snowflakecomputing.com/polaris/open-sharing/api/catalog",
  "scope": "session:role:external",
  "oauth_token_uri": "https://myorg-myaccount.snowflakecomputing.com/polaris/open-sharing/api/catalog/v1/oauth/tokens"
}
```

Example output for an external consumer in the `PUBLIC.AWS_EU_CENTRAL_1` region:

Copy code

```
{
  "catalog": "my-listing-GZ1Z23",
  "catalog_uri": "https://myaccount-sharing.myorg-open-sharing-t1.eu-central-1.aws.snowflake.com/polaris/open-sharing/api/catalog",
  "scope": "session:role:external",
  "oauth_token_uri": "https://myaccount-sharing.myorg-open-sharing-t1.eu-central-1.aws.snowflake.com/polaris/open-sharing/api/catalog/v1/oauth/tokens"
}
```
