# Manage Iceberg tables

Feature — Generally Available

Not available in government regions.

The Snowflake REST [Iceberg Table API](/developer-guide/snowflake-rest-api/reference/iceberg-table.html) provides the following Snowflake endpoints to access, update, and perform certain actions on Iceberg Table resource in Snowflake:

**Snowflake REST Iceberg Table API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/databases/database/schemas/` `schema/iceberg-tables` | Lists available iceberg tables. |
| `POST /api/v2/databases/database/schemas/` `schema/iceberg-tables` | Creates an iceberg table. |
| `POST /api/v2/databases/database/schemas/` `schema/iceberg-tables:as-select` | Creates an iceberg table using the result of the specified select query. |
| `POST /api/v2/databases/database/schemas/` `schema/iceberg-tables:from-aws-glue-catalog` | Creates an iceberg table from an AWS Glue catalog. |
| `POST /api/v2/databases/database/schemas/` `schema/iceberg-tables:from-delta` | Creates an iceberg table from a Delta catalog. |
| `POST /api/v2/databases/database/schemas/` `schema/iceberg-tables:from-iceberg-files` | Creates an iceberg table from Iceberg files in object storage (external cloud storage). |
| `POST /api/v2/databases/database/schemas/` `schema/iceberg-tables:from-iceberg-rest` | Creates an iceberg table from an Iceberg REST catalog. |
| `GET /api/v2/databases/database/schemas/` `schema/iceberg-tables/name` | Describes an iceberg table. |
| `DELETE /api/v2/databases/database/schemas/` `schema/iceberg-tables/name` | Drops an iceberg table. |
| `POST /api/v2/databases/database/schemas/` `schema/iceberg-tables/name:resume-recluster` | Resumes recluster for an iceberg table. |
| `POST /api/v2/databases/database/schemas/` `schema/iceberg-tables/name:suspend-recluster` | Suspends recluster for an iceberg table. |
| `POST /api/v2/databases/database/schemas/` `schema/iceberg-tables/name:refresh` | Refreshes the metadata of an iceberg table. |
| `POST /api/v2/databases/database/schemas/` `schema/iceberg-tables/name:convert-to-managed` | Converts an externally managed iceberg table to a managed table. |
| `POST /api/v2/databases/database/schemas/` `schema/iceberg-tables/name:undrop` | Restores a previously dropped iceberg table. |
| `POST /api/v2/databases/database/schemas/` `schema/iceberg-tables/name:clone` | Clones an Snowflake managed iceberg table. |
| `POST /api/v2/databases/database/schemas/` `schema/iceberg-tables/name:create-like` | Creates a new iceberg table like a specified one. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Iceberg Table API reference](/developer-guide/snowflake-rest-api/reference/iceberg-table.html).
