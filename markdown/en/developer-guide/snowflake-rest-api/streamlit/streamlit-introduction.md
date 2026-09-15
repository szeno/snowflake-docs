# Manage Streamlit

The Snowflake REST [Streamlit API](/developer-guide/snowflake-rest-api/reference/streamlit.html) provides the following endpoints to access, update, and perform certain actions on Streamlit resources.

**Snowflake REST Streamlit API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/databases/database/schemas/` `schema/streamlits` | List Streamlits in a schema. Supports filtering with pattern matching. |
| `POST /api/v2/databases/database/schemas/` `schema/streamlits` | Create a new Streamlit application, or replace an existing one. |
| `GET /api/v2/databases/database/schemas/` `schema/streamlits/name` | Fetch detailed information about a specific Streamlit by name. |
| `DELETE /api/v2/databases/database/schemas/` `schema/streamlits/name` | Delete a Streamlit. The Streamlit can be restored using undrop within the retention period. |
| `POST /api/v2/databases/database/schemas/` `schema/streamlits/name:undrop` | Restore a previously deleted Streamlit within the retention period. |
| `POST /api/v2/databases/database/schemas/` `schema/streamlits/name:rename` | Rename a Streamlit to a new name, optionally in a different database or schema. |
| `POST /api/v2/databases/database/schemas/` `schema/streamlits/name:add-live-version` | Add a live version to the Streamlit, making a specific version active for users. |
| `POST /api/v2/databases/database/schemas/` `schema/streamlits/name:commit` | Commit the LIVE version of the Streamlit to the Git repository. |
| `POST /api/v2/databases/database/schemas/` `schema/streamlits/name:add-version` | Add a new version to the Streamlit by copying files from a specified stage location. |
| `POST /api/v2/databases/database/schemas/` `schema/streamlits/name:add-version-from-git` | Add a new version to the Streamlit using a Git reference URI. |
| `POST /api/v2/databases/database/schemas/` `schema/streamlits/name:abort` | Abort the live version of the Streamlit, discarding uncommitted changes. |
| `POST /api/v2/databases/database/schemas/` `schema/streamlits/name:pull` | Pull the latest changes from the Git repository for a Streamlit with Git integration. |
| `POST /api/v2/databases/database/schemas/` `schema/streamlits/name:push` | Push committed changes from the Streamlit back to its connected Git repository. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Streamlit API reference](/developer-guide/snowflake-rest-api/reference/streamlit.html).
