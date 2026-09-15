# Manage compute pools

Feature — Generally Available

Not available in government regions.

The Snowflake REST [Compute Pool API](/developer-guide/snowflake-rest-api/reference/compute-pool.html) provides the following endpoints to access, update, and perform certain actions on Compute Pool resources.

**Snowflake REST Compute Pool API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/compute-pools` | Lists available compute pools. |
| `POST /api/v2/compute-pools` | Creates a compute pool. |
| `GET /api/v2/compute-pools/name` | Fetches a compute pool. |
| `PUT /api/v2/compute-pools/name` | Creates a new, or alters an existing, compute pool. |
| `DELETE /api/v2/compute-pools/name` | Deletes a compute pool. |
| `POST /api/v2/compute-pools/name:resume` | Resumes a suspended compute pool. |
| `POST /api/v2/compute-pools/name:suspend` | Suspends an active compute pool. |
| `POST /api/v2/compute-pools/` `name:stopallservices` | \*Deprecated. Use the replacement endpoint below.\* |
| `POST /api/v2/compute-pools/` `name:stop-all-services` | Stops all active services on the compute pool. |
| `GET /api/v2/compute-pools/instance-families` | Lists available compute pool instance families. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Compute Pool API reference](/developer-guide/snowflake-rest-api/reference/compute-pool.html).
