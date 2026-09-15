# Manage warehouses

The Snowflake REST [Warehouse API](/developer-guide/snowflake-rest-api/reference/warehouse.html) provides the following endpoints for managing Snowflake warehouses:

**Snowflake REST Warehouse API endpoints**

| Endpoint | Description |
| --- | --- |
| `POST /api/v2/warehouses` | Creates a new, or replaces an existing, warehouse. |
| `GET /api/v2/warehouses` | Returns a list of available warehouses. |
| `GET /api/v2/warehouses/name` | Describes a named warehouse. |
| `DELETE /api/v2/warehouses/name` | Deletes a named warehouse. |
| `PUT /api/v2/warehouses/name` | Updates the properties of a named warehouse. |
| `POST /api/v2/warehouses/name:resume` | Resumes a currently suspended warehouse. |
| `POST /api/v2/warehouses/name:suspend` | Suspends a named warehouse. |
| `POST /api/v2/warehouses/name:rename` | Renames a named warehouse. |
| `POST /api/v2/warehouses/name:abort` | Aborts all running or queued queries in a named warehouse. |
| `POST /api/v2/warehouses/name:enable` | Enables an Adaptive Warehouse. |
| `POST /api/v2/warehouses/name:disable` | Disables an Adaptive Warehouse. |
| `POST /api/v2/warehouses/name:use` | \*Deprecated.\* |

Expand

Show lessSee more

For reference documentation, see [Snowflake Warehouse API reference](/developer-guide/snowflake-rest-api/reference/warehouse.html).
