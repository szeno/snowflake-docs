# Manage functions

The Snowflake REST [Function API](/developer-guide/snowflake-rest-api/reference/function.html) provides the following Snowflake endpoints to manage Snowflake functions:

**Snowflake REST Function API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/databases/database/schemas/` `schema/functions` | Lists the user functions under the database and schema. |
| `POST /api/v2/databases/database/schemas/` `schema/functions` | Creates a function. |
| `GET /api/v2/databases/database/schemas/` `schema/functions/nameWithArgs` | Fetches a function using the DESCRIBE COMMAND output. |
| `DELETE /api/v2/databases/database/schemas/` `schema/functions/nameWithArgs` | Deletes a function with the given name and args. |
| `POST /api/v2/databases/database/schemas/` `schema/functions/name:execute` | Executes a function. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Function API reference](/developer-guide/snowflake-rest-api/reference/function.html).
