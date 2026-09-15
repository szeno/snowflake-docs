# Manage notebooks

The Snowflake REST [Notebook API](/developer-guide/snowflake-rest-api/reference/notebook.html) provides the following endpoints to access, update, and perform certain actions on Notebook resources.

**Snowflake REST Notebook API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/databases/database/schemas/` `schema/notebooks` | Lists available notebooks. |
| `POST /api/v2/databases/database/schemas/` `schema/notebooks` | Creates a notebook. |
| `GET /api/v2/databases/database/schemas/` `schema/notebooks/name` | Fetches a notebook. |
| `DELETE /api/v2/databases/database/schemas/` `schema/notebooks/name` | Deletes a notebook. |
| `POST /api/v2/databases/database/schemas/` `schema/notebooks/name:execute` | Execute a notebook. Note This endpoint only works with a session token. |
| `POST /api/v2/databases/database/schemas/` `schema/notebooks/name:rename` | Changes the name of a notebook. |
| `POST /api/v2/databases/database/schemas/` `schema/notebooks/name:add-live-version` | Adds a live version to the notebook |
| `POST /api/v2/databases/database/schemas/` `schema/notebooks/name:commit` | Commits the live version of the specified notebook to a Git repository. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Notebook API reference](/developer-guide/snowflake-rest-api/reference/notebook.html).
