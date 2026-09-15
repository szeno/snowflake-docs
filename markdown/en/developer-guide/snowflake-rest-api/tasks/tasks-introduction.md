# Manage tasks

The Snowflake REST [Task API](/developer-guide/snowflake-rest-api/reference/task.html) provides the following endpoints to access, update, and perform certain actions on task resources in a Snowflake database:

**Snowflake REST Task API endpoints**

| Endpoint | Description |
| --- | --- |
| `GET /api/v2/databases/database/schemas/` `schema/tasks` | Lists tasks under the database and schema. |
| `POST /api/v2/databases/database/schemas/` `schema/tasks` | Creates a task, with standard create modifiers as query parameters. |
| `GET /api/v2/databases/database/schemas/` `schema/tasks/name` | Fetches a task. |
| `PUT /api/v2/databases/database/schemas/` `schema/tasks/name` | Creates (or alters an existing) task. |
| `DELETE /api/v2/databases/database/schemas/` `schema/tasks/name` | Deletes a task. |
| `POST /api/v2/databases/database/schemas/` `schema/tasks/name:execute` | Executes a task. |
| `POST /api/v2/databases/database/schemas/` `schema/tasks/name:resume` | Resumes a suspended task. |
| `POST /api/v2/databases/database/schemas/` `schema/tasks/name:suspend` | Suspends an active task. |
| `GET /api/v2/databases/database/schemas/` `schema/tasks/name/dependents` | Fetches the dependent tasks of a task. |
| `GET /api/v2/databases/database/schemas/` `schema/tasks/name/current_graphs` | \*Deprecated. Use the replacement endpoint below.\* |
| `GET /api/v2/databases/database/schemas/` `schema/tasks/name/current-graphs` | Gets the graph runs that are executing or scheduled for the task for the next 8 days. |
| `GET /api/v2/databases/database/schemas/` `schema/tasks/name/complete_graphs` | \*Deprecated. Use the replacement endpoint below.\* |
| `GET /api/v2/databases/database/schemas/` `schema/tasks/name/complete-graphs` | Gets the graph runs that are completed for the task. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Task API reference](/developer-guide/snowflake-rest-api/reference/task.html).
