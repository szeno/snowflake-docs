# Manage roles

The Snowflake REST [Role API](/developer-guide/snowflake-rest-api/reference/role.html) provides the following endpoints to manage Snowflake roles:

**Snowflake REST Role API endpoints**

| Endpoint | Description |
| --- | --- |
| `POST /api/v2/roles` | Creates a role according to the specified parameters. |
| `GET /api/v2/roles` | Lists the roles available to the user’s account. |
| `DELETE /api/v2/roles/name` | Deletes the specified role. |
| `GET /api/v2/roles/name/grants` | Lists all grants to the role. |
| `POST /api/v2/roles/name/grants` | Grants privileges to the specified role. |
| `POST /api/v2/roles/name/grants:revoke` | Revokes grants from the specified role. |
| `GET /api/v2/roles/name/grants-of` | Lists all grants of the specified role. |
| `GET /api/v2/roles/name/grants-on` | Lists all grants on the specified role. |
| `GET /api/v2/roles/name/future-grants` | Lists all future grants to the specified role. |
| `POST /api/v2/roles/name/future-grants` | Grants future privileges to the specified role. |
| `POST /api/v2/roles/name/future-grants:revoke` | Revokes future grants from the specified role |

Expand

Show lessSee more

For reference documentation, see [Snowflake Role API reference](/developer-guide/snowflake-rest-api/reference/role.html).
