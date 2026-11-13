Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# INTEGRATIONS view

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

This Account Usage view displays a row for each [integration](/sql-reference/sql/create-integration) in your account, including API,
catalog, external access, notification, security, and storage integrations.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ID | NUMBER | Internal, system-generated identifier for the integration. |
| NAME | VARCHAR | Name of the integration. |
| TYPE | VARCHAR | Type of the integration (for example, `EXTERNAL_API`, `EXTERNAL_ACCESS`, `EXTERNAL_STAGE`, `CATALOG`, `EMAIL`, `WEBHOOK`, `OAUTH - CUSTOM`, `SAML2`, `SCIM - OKTA`, or `API_AUTHENTICATION`). Matches the `type` column in the [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations) output. |
| CATEGORY | VARCHAR | Category of the integration (for example, `API`, `CATALOG`, `EXTERNAL_ACCESS`, `NOTIFICATION`, `SECURITY`, or `STORAGE`). Matches the `category` column in the [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations) output. |
| DETAILS | VARIANT | Additional configuration details for the integration. Depending on the integration type, this column contains an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the following key-value pairs, or NULL for other integration types:   - For [API integrations](/sql-reference/sql/create-api-integration) (`TYPE = 'EXTERNAL_API'`):    - `api_allowed_prefixes`: Array of HTTPS URL prefixes that the integration is allowed to access.   - `api_blocked_prefixes`: Array of HTTPS URL prefixes that the integration is blocked from accessing. For example:  Copy code  ```   {     "api_allowed_prefixes": ["https://github.com/"],     "api_blocked_prefixes": ["https://github.com/example/private/"]   }   ``` - For [external access integrations](/sql-reference/sql/create-external-access-integration) (`TYPE = 'EXTERNAL_ACCESS'`):    - `allowed_network_rules`: Array of fully qualified names of the egress [network rules](/sql-reference/sql/create-network-rule) that are     allowed for the integration.   - `allowed_network_rule_ids`: Array of internal identifiers for the allowed network rules. For example:  Copy code  ```   {     "allowed_network_rule_ids": [101],     "allowed_network_rules": ["MY_DB.PUBLIC.API_NETWORK_RULE"]   }   ``` - For [storage integrations](/sql-reference/sql/create-storage-integration) (`TYPE = 'EXTERNAL_STAGE'`):    - `storage_allowed_locations`: Array of cloud storage URLs (buckets, containers, or prefixes) that the integration is allowed to access.   - `storage_blocked_locations`: Array of cloud storage URLs that the integration is blocked from accessing. For example:  Copy code  ```   {     "storage_allowed_locations": ["s3://mybucket1/path1/"],     "storage_blocked_locations": ["s3://mybucket1/path1/sensitive/"]   }   ``` - For all other integration types, this column contains NULL. |
| ENABLED | BOOLEAN | `TRUE` if the integration is enabled and available for use; `FALSE` if the integration is disabled. |
| OWNER | VARCHAR | Name of the role that owns the integration. NULL if the integration has been dropped. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| COMMENT | VARCHAR | Comment for the integration, if any. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the integration was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the integration was last altered. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the integration was dropped. NULL if the integration has not been dropped. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 240 minutes (4 hours).
- Credentials, secrets, and other sensitive authentication properties configured on an integration are not returned in this view. For API,
  external access, and external stage storage integrations, the `DETAILS` column exposes only the configured network rules and location
  allowlists or blocklists.

## Examples

Retrieve all active integrations in the account:

Copy code

```
SELECT name, type, category, details, enabled, owner, created
  FROM SNOWFLAKE.ACCOUNT_USAGE.INTEGRATIONS
  WHERE deleted IS NULL
  ORDER BY category, name;
```

Retrieve all active external access integrations and their allowed network rules:

Copy code

```
SELECT name, details:allowed_network_rules AS allowed_network_rules, enabled, owner
  FROM SNOWFLAKE.ACCOUNT_USAGE.INTEGRATIONS
  WHERE category = 'EXTERNAL_ACCESS'
    AND deleted IS NULL
  ORDER BY name;
```
