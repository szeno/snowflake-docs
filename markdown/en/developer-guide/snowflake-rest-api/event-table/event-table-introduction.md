# Manage event tables

The Snowflake REST [Event Table API](/developer-guide/snowflake-rest-api/reference/event-table.html) provides the following endpoints to access, update, and perform certain actions on Event Table resources.

**Snowflake REST Event Table API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/databases/database/schemas/` `schema/event-tables` | Lists available event tables. |
| `POST /api/v2/databases/database/schemas/` `schema/event-tables` | Creates an event table. |
| `GET /api/v2/databases/database/schemas/` `schema/event-tables/name` | Fetches an event table. |
| `DELETE /api/v2/databases/database/schemas/` `schema/event-tables/name` | Deletes an event table. |
| `POST /api/v2/databases/database/schemas/` `schema/event-tables/name:rename` | Renames an event table. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Event Table API reference](/developer-guide/snowflake-rest-api/reference/event-table.html).
