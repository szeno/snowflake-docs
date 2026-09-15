Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SECRETS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view provides the [secrets](/sql-reference/sql/create-secret) in each account in your organization.

Each row in this view corresponds to a different secret.

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| `id` | NUMBER | Internal, system-generated identifier for the secret. |
| `name` | VARCHAR | Name of the secret. |
| `schema_id` | NUMBER | Internal, system-generated identifier for the schema of the secret. |
| `schema` | VARCHAR | Schema that the secret belongs to. |
| `database_id` | NUMBER | Internal, system-generated identifier for the database of the secret. |
| `database` | VARCHAR | Database that the secret belongs to. |
| `owner` | VARCHAR | Name of the role that owns the secret; NULL if it has been dropped. |
| `owner_role_type` | VARCHAR(13) | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| `secret_type` | VARCHAR | The type of secret (`GENERIC_STRING`, `OAUTH2`, `PASSWORD`, or `SYMMETRIC_KEY`). |
| `oauth_access_token_expiry_timestamp` | TIMESTAMP\_LTZ(6) | The expiry time of the OAuth access token stored in the secret. |
| `oauth_refresh_token_expiry_timestamp` | TIMESTAMP\_LTZ(6) | The expiry time of the OAuth refresh token stored in the secret. |
| `oauth_scopes` | VARCHAR | A comma-separated list of scopes to use when making a request from the OAuth server by a role with USAGE on the integration during the OAuth client credentials flow. |
| `api_authentication_integration_name` | VARCHAR | The name of the API Authentication Integration used by this secret for authentication. |
| `comment` | VARCHAR | Comment for the secret. |
| `created_on` | TIMESTAMP\_LTZ(6) | Date and time when the secret was created. |
| `last_altered_on` | TIMESTAMP\_LTZ(6) | Date and time when the secret was last altered. |
| `deleted_on` | TIMESTAMP\_LTZ(6) | Date and time when the secret was dropped. |
| `algorithm` | VARCHAR | Algorithm used to generate the key for a symmetric key secret. |
| `key_length` | VARCHAR | Length of the key used for a symmetric key secret. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
- Sensitive values that the secret stores, such as the values for username, password, and OAuth refresh token, are not reported in this
  view.
