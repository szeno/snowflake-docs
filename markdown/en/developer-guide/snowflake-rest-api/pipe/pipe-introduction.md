# Manage data pipes

The Snowflake REST [Pipe API](/developer-guide/snowflake-rest-api/reference/pipe.html) provides the following endpoints to access, update, and perform certain actions on Pipe resources.

**Snowflake REST Pipe API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/databases/database/schemas/schema/pipes` | Lists available pipes. |
| `POST /api/v2/databases/database/schemas/schema/pipes` | Creates a pipe. |
| `GET /api/v2/databases/database/schemas/schema/pipes/name` | Fetches a pipe. |
| `DELETE /api/v2/databases/database/schemas/schema/pipes/name` | Deletes a pipe. |
| `POST /api/v2/databases/database/schemas/schema/pipes/name:refresh` | Refreshes a pipe. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Pipe API reference](/developer-guide/snowflake-rest-api/reference/pipe.html).
