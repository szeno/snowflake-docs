# Manage dynamic tables

The [Dynamic Table API](/developer-guide/snowflake-rest-api/reference/dynamic-table.html) provides the following endpoints to manage Snowflake dynamic tables:

**Snowflake Dynamic Table API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/databases/database/schemas/` `schema/dynamic-tables` | Lists the dynamic tables under the database and schema. |
| `POST /api/v2/databases/database/schemas/` `schema/dynamic-tables` | Creates a dynamic table with standard create modifiers as query parameters. |
| `GET /api/v2/databases/database/schemas/` `schema/dynamic-tables/name` | Fetches a dynamic table. |
| `DELETE /api/v2/databases/database/schemas/` `schema/dynamic-tables/name` | Deletes a dynamic table with the given name. |
| `POST /api/v2/databases/database/schemas/` `schema/dynamic-tables/name:clone` | Creates a new dynamic table by cloning from the specified resource. |
| `POST /api/v2/databases/database/schemas/` `schema/dynamic-tables/name:undrop` | Undrops a dynamic table. |
| `POST /api/v2/databases/database/schemas/` `schema/dynamic-tables/name:suspend` | Suspends refreshes on the specified dynamic table. |
| `POST /api/v2/databases/database/schemas/` `schema/dynamic-tables/name:resume` | Resumes refreshes on the specified dynamic table. |
| `POST /api/v2/databases/database/schemas/` `schema/dynamic-tables/name:refresh` | Specifies that the specified dynamic table should be manually refreshed. |
| `POST /api/v2/databases/database/schemas/` `schema/dynamic-tables/` `name:suspend-recluster` | Suspends reclustering of the specified dynamic table. |
| `POST /api/v2/databases/database/schemas/` `schema/dynamic-tables/` `name:resume-recluster` | Resumes reclustering of the specified dynamic table. |
| `POST /api/v2/databases/database/schemas/` `schema/dynamic-tables/name:swap-with` | Swaps with another dynamic table. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Dynamic Table API reference](/developer-guide/snowflake-rest-api/reference/dynamic-table.html).
