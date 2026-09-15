# Manage procedures

The Snowflake REST [Procedure API](/developer-guide/snowflake-rest-api/reference/procedure.html) provides the following endpoints to access, update, and perform certain actions on Procedure resources.

**Snowflake REST Procedure API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/databases/database/schemas/` `schema/procedures` | Lists available procedures. |
| `POST /api/v2/databases/database/schemas/` `schema/procedures` | Creates a procedure. |
| `GET /api/v2/databases/database/schemas/` `schema/procedures/nameWithArgs` | Fetches a procedure. |
| `DELETE /api/v2/databases/database/schemas/` `schema/procedures/nameWithArgs` | Deletes a procedure. |
| `POST /api/v2/databases/database/schemas/` `schema/procedures/nameWithArgs:call` | Calls a procedure. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Procedure API reference](/developer-guide/snowflake-rest-api/reference/procedure.html).
