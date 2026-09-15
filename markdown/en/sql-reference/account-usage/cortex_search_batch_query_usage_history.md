Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# CORTEX\_SEARCH\_BATCH\_QUERY\_USAGE\_HISTORY view

This Account Usage view can be used to query the usage history of [Cortex Search batch search queries](/user-guide/snowflake-cortex/cortex-search/batch-cortex-search).
Batch search queries incur three types of cost:

- **Serving cost**: Charged based on the search index data size and the duration of the batch search query.
- **Query embedding cost**: Charged based on the number of tokens embedded from the input workload. Standard embedding costs apply.
- **Virtual warehouse compute cost**: Charged for the virtual warehouse used to run the batch search query. This cost isn’t included in this view.

This view tracks serving cost and query embedding cost only. It includes the credits consumed, billable indexed data, billable duration,
and token usage for each batch search query submitted to a Cortex Search Service.
For more information, see [Cost considerations](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-cost-considerations).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_TZ | Start of the specified time range in which the Cortex Search batch search query usage took place. |
| END\_TIME | TIMESTAMP\_TZ | End of the specified time range in which the Cortex Search batch search query usage took place. |
| QUERY\_ID | VARCHAR | Internal/system-generated identifier for the SQL statement that invoked the batch search query. |
| DATABASE\_NAME | VARCHAR | Name of the database in which the Cortex Search Service resides. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database in which the Cortex Search Service resides. |
| SCHEMA\_NAME | VARCHAR | Name of the schema in which the Cortex Search Service resides. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema in which the Cortex Search Service resides. |
| SERVICE\_NAME | VARCHAR | Name of the Cortex Search Service. |
| SERVICE\_ID | NUMBER | Internal/system-generated identifier for the Cortex Search Service. |
| CONSUMPTION\_TYPE | VARCHAR | The category of consumption incurred for the batch search query. One of: “BATCH\_SERVING” (serving cost based on indexed data size and query duration) or “BATCH\_EMBED\_TEXT\_TOKENS” (query embedding cost based on input tokens). |
| CREDITS\_USED | NUMBER | Number of credits consumed for the batch search query for the specified CONSUMPTION\_TYPE. |
| BILLABLE\_INDEXED\_DATA\_BYTES | NUMBER | For CONSUMPTION\_TYPE = “BATCH\_SERVING”, the number of bytes of indexed data billed during the batch search query. NULL for other consumption types. |
| BILLABLE\_DURATION\_SECONDS | NUMBER | For CONSUMPTION\_TYPE = “BATCH\_SERVING”, the duration in seconds billed for the batch search query. NULL for other consumption types. |
| MODEL\_NAME | VARCHAR | For CONSUMPTION\_TYPE = “BATCH\_EMBED\_TEXT\_TOKENS”, the name of the embedding model used to generate vector embeddings for the batch search query input. NULL for other consumption types. |
| TOKENS | NUMBER | For CONSUMPTION\_TYPE = “BATCH\_EMBED\_TEXT\_TOKENS”, the number of input tokens consumed for query embedding. NULL for other consumption types. |

Expand

Show lessSee more

## Usage notes

- The view provides up-to-date credit usage for an account within the last 365 days (1 year).
- Each row represents a single batch search query identified by QUERY\_ID.
- Serving cost is incurred per gigabyte-hour of indexed data, metered by the billable duration of the batch search query.
- Query embedding cost is incurred per input token. Unlike interactive search, query embedding for batch search queries is a billable cost.
- For daily-level aggregated batch usage, you can also query the [CORTEX\_SEARCH\_DAILY\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_search_daily_usage_history) view
  with `CONSUMPTION_TYPE = 'BATCH'`.
