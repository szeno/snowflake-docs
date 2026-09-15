Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# CORTEX\_FUNCTIONS\_QUERY\_USAGE\_HISTORY view

Important

This view is no longer updated. Use the [CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_ai_functions_usage_history) view instead.

The CORTEX\_FUNCTIONS\_QUERY\_USAGE\_HISTORY view can be used to view the usage history of each [Cortex Functions](/user-guide/snowflake-cortex/aisql) query in a Snowflake account. For more information, see [Snowflake Cortex AI functions incur compute cost based on the number of tokens…](/user-guide/snowflake-cortex/aisql-cost#label-cortex-llm-cost-considerations).

The information in the view includes the number of tokens and credits consumed for each query.

The view also includes relevant metadata, such as the model name and the ID of the warehouse running the queries.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| FUNCTION\_NAME | VARCHAR | Function name for the model. |
| MODEL\_NAME | VARCHAR | Model name used in the query. A query can have more than one model. For queries with multiple models, the usage history includes a row for each model. |
| QUERY\_ID | VARCHAR | Query ID |
| TOKENS | NUMBER | Number of tokens used for the (`QUERY_ID`, `MODEL_NAME`, `WAREHOUSE_ID`) combination. |
| TOKEN\_CREDITS | NUMBER | Tokens converted to credits for the (`QUERY_ID`, `MODEL_NAME`, `WAREHOUSE_ID`) combination. |
| WAREHOUSE\_ID | VARCHAR | ID of the warehouse used to run the query. |

Expand

Show lessSee more

## Usage notes

- The view provides up-to-date credit usage for an account within the last 365 days (1 year).
- Query usage data might take a few hours to appear in the CORTEX\_FUNCTIONS\_QUERY\_USAGE\_HISTORY view.
- Credit rate usage is based on the number of messages processed, as outlined in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
