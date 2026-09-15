# Dynamic table reference

This page collects links to the SQL commands, monitoring views and functions, and developer APIs for dynamic tables.

## SQL commands

Use these commands to create, modify, inspect, and remove dynamic tables.

| Command | Description |
| --- | --- |
| [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table) | Create a dynamic table with a definition, target lag, and warehouse assignment. |
| [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table) | Change properties of a dynamic table, including target lag, warehouse, suspend, and resume. |
| [DROP DYNAMIC TABLE](/sql-reference/sql/drop-dynamic-table) | Remove a dynamic table from the system. |
| [UNDROP DYNAMIC TABLE](/sql-reference/sql/undrop-dynamic-table) | Restore a dynamic table that was dropped within the Time Travel retention period. |
| [SHOW DYNAMIC TABLES](/sql-reference/sql/show-dynamic-tables) | List dynamic tables and their properties, including resolved refresh mode and scheduling state. |
| [DESCRIBE DYNAMIC TABLE](/sql-reference/sql/desc-dynamic-table) | Describe the columns and data types of a dynamic table. |

Expand

Show lessSee more

## Information Schema functions

Call these table functions from the INFORMATION\_SCHEMA schema. DYNAMIC\_TABLE\_REFRESH\_HISTORY and DYNAMIC\_TABLES are scoped to the current database. DYNAMIC\_TABLE\_GRAPH\_HISTORY returns account-level data regardless of database context. They retain **7 days** of history.

| Function | Description |
| --- | --- |
| [DYNAMIC\_TABLES](/sql-reference/functions/dynamic_tables) | Return metadata for dynamic tables, including scheduling state and current lag. |
| [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history) | Return refresh history for dynamic tables, including refresh status, duration, and data timestamp. |
| [DYNAMIC\_TABLE\_GRAPH\_HISTORY](/sql-reference/functions/dynamic_table_graph_history) | Return the dependency graph and scheduling state history for dynamic tables in a pipeline. |

Expand

Show lessSee more

## Account Usage views

Account Usage views are available in the SNOWFLAKE shared database and retain **365 days** of history, compared to 7 days for the Information Schema functions.

| View | Description |
| --- | --- |
| [DYNAMIC\_TABLE\_REFRESH\_HISTORY view](/sql-reference/account-usage/dynamic_table_refresh_history) | Return refresh history across all dynamic tables in the account, with 365-day retention. |

Expand

Show lessSee more

## System functions

| Function | Description |
| --- | --- |
| [SYSTEM$SHOW\_DYNAMIC\_TABLES\_CREATED\_FOR\_RESHARING](/sql-reference/functions/system_show_dynamic_tables_created_for_resharing) | List hidden dynamic tables created for cross-region resharing of listings. |

Expand

Show lessSee more

## Developer APIs

Use these APIs to manage dynamic tables programmatically.

| API | Description |
| --- | --- |
| [Manage dynamic tables](/developer-guide/snowflake-rest-api/dynamic-tables/dynamic-tables-introduction) | Manage dynamic tables through the Snowflake REST API. |
| [Managing Snowflake dynamic tables with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-dynamic-tables) | Create, alter, and drop dynamic tables with the Snowflake Python API. |
| [Snowflake Python APIs: Managing Snowflake objects with Python](/developer-guide/snowflake-python-api/snowflake-python-overview) | Overview of the Snowflake Python API for managing Snowflake objects programmatically. |

Expand

Show lessSee more

## What’s next

- [Dynamic tables](/user-guide/dynamic-tables/overview)
- [Create a dynamic table](/user-guide/dynamic-tables/create)
- [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring)
