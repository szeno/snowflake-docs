# Manage database schemas

The Snowflake REST [Schema API](/developer-guide/snowflake-rest-api/reference/schema.html) provides the following endpoints to manage Snowflake schemas:

**Snowflake REST Schemas API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/databases/database/schemas` | Lists the available schemas. |
| `POST /api/v2/databases/database/schemas` | Creates a schema. |
| `POST /api/v2/databases/database/schemas/name:clone` | Clones a schema. |
| `POST /api/v2/databases/database/schemas/name:undrop` | Undrops a schema. |
| `GET /api/v2/databases/database/schemas/name` | Fetches a schema. |
| `PUT /api/v2/databases/database/schemas/name` | Creates a new or alters an existing schema. |
| `DELETE /api/v2/databases/database/schemas/name` | Deletes a schema. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Schema API reference](/developer-guide/snowflake-rest-api/reference/schema.html).
