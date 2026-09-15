# Manage tags

The Snowflake REST [Tag API](/developer-guide/snowflake-rest-api/reference/tag.html) provides the following endpoints to access, update, and perform certain actions on Tag resources in a Snowflake database:

**Snowflake REST Tag API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/databases/database/schemas/` `schema/tags` | List tags. |
| `POST /api/v2/databases/database/schemas/` `schema/tags` | Create a tag. |
| `GET /api/v2/databases/database/schemas/` `schema/tags/name` | Fetch a tag. |
| `DELETE /api/v2/databases/database/schemas/` `schema/tags/name` | Delete a tag. |
| `PUT /api/v2/databases/database/schemas/` `schema/tags/name` | Create or update a tag. |
| `POST /api/v2/databases/database/schemas/` `schema/tags/name:undrop` | Undrop a tag. |
| `POST /api/v2/databases/database/schemas/` `schema/tags/name:rename` | Rename a tag with a new identifier. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Tag API reference](/developer-guide/snowflake-rest-api/reference/tag.html).
