Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SECRETS view

This Account Usage view provides the [secrets](/sql-reference/sql/create-secret) in your account.

Each row in this view corresponds to a different secret.

## Columns

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

- Latency for the view may be up to 120 minutes (2 hours).
- Sensitive values that the secret stores, such as the values for username, password, and OAuth refresh token, are not reported in this
  view.
