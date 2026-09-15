# Manage database roles

The Snowflake REST [Database Role API](/developer-guide/snowflake-rest-api/reference/database-role.html) provides the following endpoints to access, update, and perform certain actions on Database Role resources.

**Snowflake REST Database Role API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/databases/database/` `database-roles` | Lists available database roles. |
| `POST /api/v2/databases/database/` `database-roles` | Creates a database role. |
| `DELETE /api/v2/databases/database/` `database-roles/name` | Deletes a database role. |
| `POST /api/v2/databases/database/` `database-roles/name:clone` | Creates a new database role by cloning from the specified resource. |
| `GET /api/v2/databases/database/database-roles/name/grants` | Lists all grants to the role. |
| `POST /api/v2/databases/database/database-roles/name/grants` | Grants privileges to the specified role. |
| `POST /api/v2/databases/database/database-roles/name/grants:revoke` | Revokes grants from the specified role. |
| `GET /api/v2/databases/database/database-roles/name/future-grants` | Lists all future grants to the specified role. |
| `POST /api/v2/databases/database/database-roles/name/future-grants` | Grants future privileges to the specified role. |
| `POST /api/v2/databases/database/database-roles/name/future-grants:revoke` | Revokes future grants from the specified role |

Expand

Show lessSee more

For reference documentation, see [Snowflake Database Role API reference](/developer-guide/snowflake-rest-api/reference/database-role.html).
