# Manage stages

The Snowflake REST [Stage API](/developer-guide/snowflake-rest-api/reference/stage.html) provides the following endpoints to manage Snowflake stages:

**Snowflake REST Stage API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/databases/database/schemas/` `schema/stages` | Lists stages under the database and schema, with show options as query parameters. |
| `POST /api/v2/databases/database/schemas/` `schema/stages` | Creates a stage with standard create modifiers as query parameters. |
| `GET /api/v2/databases/database/schemas/` `schema/stages/name` | Fetches a stage using the describe command output. |
| `DELETE /api/v2/databases/database/schemas/` `schema/stages/name` | Deletes the stage with the specified name. |
| `GET /api/v2/databases/database/schemas/` `schema/stages/name/files` | Lists the files in the specified stage. |
| `POST /api/v2/databases/database/schemas/` `schema/stages/name/files/filePath:presigned-url` | Generates a pre-signed URL. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Stage API reference](/developer-guide/snowflake-rest-api/reference/stage.html).
