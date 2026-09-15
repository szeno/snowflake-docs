# Manage databases

The Snowflake REST [Database API](/developer-guide/snowflake-rest-api/reference/database.html) provides the following endpoints to manage Snowflake databases:

**Snowflake REST Database API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/databases` | Lists accessible databases. |
| `POST /api/v2/databases` | Creates a database. |
| `POST /api/v2/databases:from-share` | Creates a database from a specified share. |
| `POST /api/v2/databases/name:clone` | Clones an existing database. |
| `GET /api/v2/databases/name` | Fetches a named database. |
| `PUT /api/v2/databases/name` | Creates a new, or alters an existing, database. |
| `DELETE /api/v2/databases/name` | Deletes a named database. |
| `POST /api/v2/databases/name:undrop` | Undrops a named database. |
| `POST /api/v2/databases/name/replication:enable` | Enables database replication. |
| `POST /api/v2/databases/name/replication:disable` | Disables replication for a named database. |
| `POST /api/v2/databases/name/replication:refresh` | Refreshes database replications. |
| `POST /api/v2/databases/name/failover:enable` | Enables failover for a named database. |
| `POST /api/v2/databases/name/failover:disable` | Disables failover for a named database. |
| `POST /api/v2/databases/name/failover:primary` | Sets a named database as the primary database. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Database API reference](/developer-guide/snowflake-rest-api/reference/database.html).
