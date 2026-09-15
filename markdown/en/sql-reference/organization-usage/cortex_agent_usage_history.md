Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

# CORTEX\_AGENT\_USAGE\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

The CORTEX\_AGENT\_USAGE\_HISTORY view in the ORGANIZATION\_USAGE schema can be used to query the usage
history of Cortex Agents across all the accounts in your organization.

Note

This view does not include requests originating from Snowflake CoWork. Requests originating from Snowflake CoWork are recorded in the [SNOWFLAKE\_COWORK\_USAGE\_HISTORY](/sql-reference/organization-usage/snowflake_cowork_usage_history) view.

The information in the view includes the number of credits consumed each time a user interacts
with Cortex Agents. A request results in one or more calls to underlying tools, for example, Cortex Analyst and Cortex Search. Each row in the view represents a call to the agent and provides detail about
the aggregated tokens and credits in the call as well as granular detail. The view also includes
relevant metadata, such as the user ID, request ID, and the agent ID.
For more information about Cortex billing, see [Cost considerations](/user-guide/snowflake-cortex/cortex-agents#label-cortex-agent-cost-considerations).

See also:
:   [CORTEX\_AGENT\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_agent_usage_history) (Account Usage)

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column name | Data type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start time when the Cortex Agent message request was received. |
| END\_TIME | TIMESTAMP\_LTZ | End time when the Cortex Agent message response was sent. |
| USER\_ID | NUMBER | The unique identifier of the user who made the request. |
| USER\_NAME | VARCHAR | The name of the user who made the request. |
| USER\_TAGS | ARRAY | Tags associated with the user. Each object in the array contains the following value pairs:   - `level`: The level at which the tag is applied (for example, “ACCOUNT” or “USER”). - `tag_database`: The database where the tag is defined. - `tag_schema`: The schema where the tag is defined. - `tag_name`: The name of the tag. - `tag_value`: The value of the tag. |
| REQUEST\_ID | VARCHAR | The unique identifier for the request. |
| PARENT\_REQUEST\_ID | VARCHAR | The identifier of the parent request, if applicable. |
| AGENT\_DATABASE\_ID | NUMBER | The unique identifier of the agent database. |
| AGENT\_DATABASE\_NAME | VARCHAR | The name of the agent database. |
| AGENT\_SCHEMA\_ID | NUMBER | The unique identifier of the agent schema. |
| AGENT\_SCHEMA\_NAME | VARCHAR | The name of the agent schema. |
| AGENT\_ID | NUMBER | The unique identifier of the agent. |
| AGENT\_NAME | VARCHAR | The name of the agent. |
| AGENT\_TAGS | ARRAY | Tags associated with the agent. Each object in the array contains the following value pairs:   - `level`: The level at which the tag is applied (for example, “DATABASE” or “CORTEX\_AGENT”). - `tag_database`: The database where the tag is defined. - `tag_schema`: The schema where the tag is defined. - `tag_name`: The name of the tag. - `tag_value`: The value of the tag. |
| TOKEN\_CREDITS | NUMBER | The number of token credits used for the request. Used for user-level budgeting. |
| TOKENS | NUMBER | Sum of the tokens used by the Cortex Agent. |
| TOKENS\_GRANULAR | ARRAY | Granular breakdown of token usage by request, service type (cortex\_agents, cortex\_analyst), and model. Includes input, cache\_read\_input, cache\_write\_input, and output token counts per model. The “unknown” model name is used when a model is not present in the pricing data. Each object in the array contains the following value pairs:   - `request_id`: The unique identifier for the request. - `service_type`: The service type, such as “cortex\_agents” or “cortex\_analyst”. - `model`: The model name used for the request. - `input`: Number of input tokens. - `cache_read_input`: Number of cache read input tokens. - `cache_write_input`: Number of cache write input tokens. - `output`: Number of output tokens. - `start_time`: The start time of the request. |
| CREDITS\_GRANULAR | ARRAY | Granular breakdown of credit usage by request, service type (cortex\_agents, cortex\_analyst), and model. Includes input, cache\_read\_input, cache\_write\_input, and output credit values per model. The “unknown” model name is used when a model is not present in the pricing data. Each object in the array contains the following value pairs:   - `request_id`: The unique identifier for the request. - `service_type`: The service type, such as “cortex\_agents” or “cortex\_analyst”. - `model`: The model name used for the request. - `input`: Credit value for input tokens. - `cache_read_input`: Credit value for cache read input tokens. - `cache_write_input`: Credit value for cache write input tokens. - `output`: Credit value for output tokens. - `start_time`: The start time of the request. |
| METADATA | OBJECT | Additional metadata, including:   - `role_id`: ID of the primary role used for the request. - `role_name`: Name of the primary role used for the request. - `interaction_interface`: The interface through which the Cortex Agent was accessed (for example, `agent_admin_ui`, `sql_function`, `microsoft_teams`, or `external`). Contains NULL if the interface is unknown or the record predates the introduction of this field. - `ai_functions_credits`: Credits consumed by [AI functions](/user-guide/snowflake-cortex/aisql#label-cortex-llm-ai-function) invoked during the request. Contains NULL if no AI functions were used. - `sql_query_credits`: Warehouse compute credits consumed by SQL queries that the request ran, for example, queries run by a Cortex Analyst tool call. Doesn’t include credits for queries run on [Adaptive Warehouses](/user-guide/warehouses-adaptive). Contains NULL if the request didn’t run any SQL queries, or until SQL cost attribution is available for the request. - `sql_query_warehouses`: The names of the warehouses that ran the SQL queries counted in `sql_query_credits`. Contains NULL if the request didn’t run any SQL queries, or until SQL cost attribution is available for the request. - `inference_region`: The [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) routing used for the request. Possible values are `global` (any Snowflake-supported region across any cloud provider) or `regional` (requests restricted to specific geographic boundaries). Contains NULL if the record predates the introduction of this field. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
- The `sql_query_credits` and `sql_query_warehouses` fields in `METADATA` depend on a separate SQL cost-attribution pipeline and can lag the rest of the row by up to 32 hours. These fields contain NULL until that pipeline catches up with the request.
- The `sql_query_credits` and `sql_query_warehouses` fields don’t include credits for queries run on [Adaptive Warehouses](/user-guide/warehouses-adaptive).

## Examples

Retrieve Cortex Agent usage history:

Copy code

```
SELECT *
  FROM SNOWFLAKE.ORGANIZATION_USAGE.CORTEX_AGENT_USAGE_HISTORY;
```

```
+-------------------+-----------------+--------------+-------------------------------+-------------------------------+---------+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+-------------------+-------------------+---------------------+-----------------+-------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+--------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------+
| ORGANIZATION_NAME | ACCOUNT_LOCATOR | ACCOUNT_NAME | START_TIME                    | END_TIME                      | USER_ID | USER_NAME | USER_TAGS                                                                                                                                                                                                                                                | REQUEST_ID                           | PARENT_REQUEST_ID | AGENT_DATABASE_ID | AGENT_DATABASE_NAME | AGENT_SCHEMA_ID | AGENT_SCHEMA_NAME | AGENT_ID | AGENT_NAME | AGENT_TAGS                                                                                                                                                                                                                                                | TOKEN_CREDITS | TOKENS | TOKENS_GRANULAR                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | CREDITS_GRANULAR                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | METADATA                                                                                                          |
+-------------------+-----------------+--------------+-------------------------------+-------------------------------+---------+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+-------------------+-------------------+---------------------+-----------------+-------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+--------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------+
| MY_ORG            | AB12345         | MY_ACCOUNT   | 2026-02-06 10:11:51.642 +0000 | 2026-02-06 10:11:55.932 +0000 | 42563   | JKOWAL    | [{"level": "ACCOUNT", "tag_database": "SI", "tag_schema": "AGENTS", "tag_name": "cost-center", "tag_value": "engineering"}, {"level": "USER", "tag_database": "FINANCE", "tag_schema": "AGENTS", "tag_name": "cost-center", "tag_value": "engineering"}] | 5caf3de3-86b2-4896-b706-9f2d7629d337 | NULL              | 234               | finance             | 4231            | analytics         | 9234     | agent1     | [{"level": "DATABASE", "tag_database": "SI", "tag_schema": "AGENTS", "tag_name": "cost-center", "tag_value": "finance"}, {"level": "CORTEX_AGENT", "tag_database": "FINANCE", "tag_schema": "AGENTS", "tag_name": "cost-center", "tag_value": "finance"}] | 20.000000000  | 1900   | [{"5caf3de3-86b2-4896-b706-9f2d7629d337": {"cortex_agents": {"modelX": {"input": 100, "cache_read_input": 300, "cache_write_input": 400, "output": 200}}, "start_time": "2026-02-06 10:11:51.642 +0000"}}, {"a98b2946-4a7d-4028-9b19-1dab89fbf6c7": {"cortex_analyst": {"modelY": {"input": 100, "output": 200}, "modelZ": {"input": 100, "output": 200}}, "start_time": "2026-02-06 10:11:52.313 +0000"}}, {"996abb8b-678a-440d-9061-d186b6acc91b": {"cortex_analyst": {"unknown": {"input": 100, "output": 200}}, "start_time": "2026-02-06 10:11:53.112 +0000"}}] | [{"5caf3de3-86b2-4896-b706-9f2d7629d337": {"cortex_agents": {"modelX": {"input": 1, "cache_read_input": 2, "cache_write_input": 3, "output": 4}}, "start_time": "2026-02-06 10:11:51.642 +0000"}}, {"a98b2946-4a7d-4028-9b19-1dab89fbf6c7": {"cortex_analyst": {"modelY": {"input": 1, "output": 4}, "modelZ": {"input": 1, "output": 4}}, "start_time": "2026-02-06 10:11:52.313 +0000"}}, {"996abb8b-678a-440d-9061-d186b6acc91b": {"cortex_analyst": {"unknown": {"input": 0, "output": 0}}, "start_time": "2026-02-06 10:11:53.112 +0000"}}] | {"role_id": 12720, "role_name": "ENGINEER", "interaction_interface": "sql_function", "ai_functions_credits": 0.5, "sql_query_credits": 2.750000000, "sql_query_warehouses": ["COMPUTE_WH"], "inference_region": "global"} |
+-------------------+-----------------+--------------+-------------------------------+-------------------------------+---------+-----------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+-------------------+-------------------+---------------------+-----------------+-------------------+----------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+--------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------+
```
