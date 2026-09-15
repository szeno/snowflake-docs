# Manage password policies

The Snowflake REST [Password Policy API](/developer-guide/snowflake-rest-api/reference/password-policy.html) provides the following endpoints to access, update, and perform certain actions on Password Policy resources.

**Snowflake REST Password Policy API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/databases/database/schemas/` `schema/password-policies` | Lists available password policies. |
| `POST /api/v2/databases/database/schemas/` `schema/password-policies` | Creates a password policy. |
| `GET /api/v2/databases/database/schemas/` `schema/password-policies/name` | Fetches a password policy. |
| `DELETE /api/v2/databases/database/schemas/` `schema/password-policies/name` | Deletes a password policy. |
| `POST /api/v2/databases/database/schemas/` `schema/password-policies/name:rename` | Renames a password policy. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Password Policy API reference](/developer-guide/snowflake-rest-api/reference/password-policy.html).
