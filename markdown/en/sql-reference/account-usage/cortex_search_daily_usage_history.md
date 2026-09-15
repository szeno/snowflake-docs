Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# CORTEX\_SEARCH\_DAILY\_USAGE\_HISTORY view

This Account Usage view can be used to query the daily usage history of [Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview),
with consumption broken out by category. The information in this view includes the number of credits consumed per day for a Cortex Search Service
for serving, embedding text, and batch search queries, but not the other costs associated with a Cortex Search Service.
For more information, see [Cost considerations](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-cost-considerations).

Tip

In [Cortex Code](/user-guide/cortex-code/cortex-code), including the [CLI](/user-guide/cortex-code/cortex-code-cli), [Desktop](/user-guide/cortex-code/cortex-code-desktop), and [Snowsight](/user-guide/cortex-code/cortex-code-snowsight) interfaces, you can use the [`cost-intelligence`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-cost-intelligence) bundled skill to answer questions about the usage data in this view. Invoke the skill with `/cost-intelligence`, or describe your question in plain language and Cortex Code selects the skill automatically.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| USAGE\_DATE | TIMESTAMP\_LTZ | Start of the specified time range in which the Cortex Search serving usage took place. |
| DATABASE\_NAME | VARCHAR | Name of the database in which the Cortex Search Service resides. |
| SCHEMA\_NAME | VARCHAR | Name of the schema in which the Cortex Search Service resides. |
| SERVICE\_NAME | VARCHAR | Name of the Cortex Search Service. |
| SERVICE\_ID | NUMBER | ID of the Cortex Search Service. |
| CONSUMPTION\_TYPE | VARCHAR | The category of consumption incurred. One of “SERVING”, “EMBED\_TEXT\_TOKENS”, or “BATCH”. |
| CREDITS | NUMBER | Number of credits billed for Cortex Search usage on the USAGE\_DATE date for the specified CONSUMPTION\_TYPE. |
| MODEL\_NAME | VARCHAR | For CONSUMPTION\_TYPE = “EMBED\_TEXT\_TOKENS”, the name of the embedding model used to generate vector embeddings (nullable). |
| TOKENS | VARCHAR | For CONSUMPTION\_TYPE = “EMBED\_TEXT\_TOKENS”, the number of input tokens consumed (nullable). |

Expand

Show lessSee more

## Usage notes

- The view provides up-to-date credit usage for an account within the last 365 days (1 year).
- Serving costs are incurred per gigabyte-month of indexed data, metered at one-second resolution. You can get an estimate of
  the indexed data size for a given service using the credit rate defined in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
- EMBED\_TEXT\_TOKENS cost is incurred per input token.
- BATCH cost includes both serving and query embedding costs incurred by batch search queries. For per-query details, see the
  [CORTEX\_SEARCH\_BATCH\_QUERY\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_search_batch_query_usage_history) view.
