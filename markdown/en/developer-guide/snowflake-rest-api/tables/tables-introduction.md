# Manage Tables

The Snowflake REST [Table API](/developer-guide/snowflake-rest-api/reference/table.html) provides the following endpoints to manage Snowflake tables:

**Snowflake REST Table API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/databases/database/schemas/` `schema/tables` | Lists the tables under the database and schema. |
| `POST /api/v2/databases/database/schemas/` `schema/tables` | Creates a table. |
| `POST /api/v2/databases/database/schemas/` `schema/tables/name:as_select` | \*Deprecated. Use the replacement endpoint below.\* |
| `POST /api/v2/databases/database/schemas/` `schema/tables:as-select` | Creates a table using the result of the specified select query. |
| `POST /api/v2/databases/database/schemas/` `schema/tables/name:using_template` | \*Deprecated. Use the replacement endpoint below.\* |
| `POST /api/v2/databases/database/schemas/` `schema/tables:using-template` | Creates a table using the templates specified in staged files. |
| `GET /api/v2/databases/database/schemas/` `schema/tables/name` | Fetches a table. |
| `PUT /api/v2/databases/database/schemas/` `schema/tables/name` | Creates a new or alters an existing table. |
| `DELETE /api/v2/databases/database/schemas/` `schema/tables/name` | Deletes a table. |
| `POST /api/v2/databases/database/schemas/` `schema/tables/name:clone` | Creates a new table by cloning from the specified resource. |
| `POST /api/v2/databases/database/schemas/` `schema/tables/name:create_like` | \*Deprecated. Use the replacement endpoint below.\* |
| `POST /api/v2/databases/database/schemas/` `schema/tables/name:create-like` | Creates a table like a specified one. |
| `POST /api/v2/databases/database/schemas/` `schema/tables/name:undrop` | Undrops a table. |
| `POST /api/v2/databases/database/schemas/` `schema/tables/name:suspend_recluster` | \*Deprecated. Use the replacement endpoint below.\* |
| `POST /api/v2/databases/database/schemas/` `schema/tables/name:suspend-recluster` | Suspends a table reclustering action. |
| `POST /api/v2/databases/database/schemas/` `schema/tables/name:resume_recluster` | \*Deprecated. Use the replacement endpoint below.\* |
| `POST /api/v2/databases/database/schemas/` `schema/tables/name:resume-recluster` | Resumes a suspended table reclustering action. |
| `POST /api/v2/databases/database/schemas/` `schema/tables/name:swapwith` | \*Deprecated. Use the replacement endpoint below.\* |
| `POST /api/v2/databases/database/schemas/` `schema/tables/name:swap-with` | Swaps one table with another. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Table API reference](/developer-guide/snowflake-rest-api/reference/table.html).
