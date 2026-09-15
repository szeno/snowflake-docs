# Use the Cortex Search Service

Feature — Generally Available

Not available in government regions.

The SNOWFLAKE REST [Cortex Search Service API](/developer-guide/snowflake-rest-api/reference/cortex-search-service.html) provides the following endpoints:

**Snowflake Cortex Search Service API endpoints**

| Endpoint | Description |
| --- | --- |
| `POST /api/v2/databases/database/schemas/schema/` `cortex-search-services/service_name:query` | Queries a Cortex Search Service to get search results. |
| `GET /api/v2/databases/database/schemas/` `schema/cortex-search-services` | Lists the Cortex Search Services under the database and schema. |
| `POST /api/v2/databases/database/schemas/schema/` `cortex-search-services` | Creates a Cortex Search Service, with standard create modifiers as query parameters. |
| `GET /api/v2/databases/database/schemas/` `schema/cortex-search-services/name` | Fetches a Cortex Search Service. |
| `DELETE /api/v2/databases/database/schemas/schema/` `cortex-search-services/name` | Deletes a Cortex Search Service with the given name. |
| `POST /api/v2/databases/database/schemas/schema/` `cortex-search-services/service_name:suggest` | Suggests from a Cortex Search Service to get auto-complete or contextual suggestions. |
| `POST /api/v2/databases/database/schemas/schema/` `cortex-search-services/name:suspend` | Suspends one or both of the indexing or serving targets of a Cortex Search Service. |
| `POST /api/v2/databases/database/schemas/schema/` `cortex-search-services/name:resume` | Resumes the Cortex Search Service. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Cortex Search Service API reference](/developer-guide/snowflake-rest-api/reference/cortex-search-service.html).
