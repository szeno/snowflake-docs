Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# CORTEX\_AISQL\_USAGE\_HISTORY view

The CORTEX\_AISQL\_USAGE\_HISTORY view can be used to query the usage history of [Cortex AI Functions](/user-guide/snowflake-cortex/aisql).

The information in the view includes the number of credits consumed each time an AI function is called, aggregated in
one-hour increment, based on the time each query completed. The view also includes relevant metadata, such as the user
ID, query ID, function, and model. Each row in the view represents the usage for a specific combination of function, model, query, and
warehouse. For more information on Cortex billing, see [Snowflake Cortex AI functions incur compute cost based on the number of tokens…](/user-guide/snowflake-cortex/aisql-cost#label-cortex-llm-cost-considerations).

Important

Use [CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_ai_functions_usage_history) to view all functions including AI\_PARSE\_DOCUMENT.

Tip

In [Cortex Code](/user-guide/cortex-code/cortex-code), including the [CLI](/user-guide/cortex-code/cortex-code-cli), [Desktop](/user-guide/cortex-code/cortex-code-desktop), and [Snowsight](/user-guide/cortex-code/cortex-code-snowsight) interfaces, you can use the [`cost-intelligence`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-cost-intelligence) bundled skill to answer questions about the usage data in this view. Invoke the skill with `/cost-intelligence`, or describe your question in plain language and Cortex Code selects the skill automatically.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| USAGE\_TIME | TIMESTAMP\_LTZ | The date and the beginning of the hour (in the local time zone) in which this usage record was billed. Usage is not recorded until the query completes, so this timestamp represents the hour in which the query completed. For example, if a query begins at 05:30 and completes at 08:30, the record is aggregated in the 08:00-09:00 hour. |
| MODEL\_NAME | TEXT | Name of the model used in the query. A query can use more than one model; in this case, usage history includes a row for each model. |
| FUNCTION\_NAME | TEXT | The name of the Cortex AI Function called. A query can use more than one function; in this case, usage history includes a row for each function. |
| TOKEN\_CREDITS | NUMBER | Number of credits billed for Cortex AI Function usage based on tokens processed for the specified function and model for the combination of QUERY\_ID, MODEL\_NAME, and WAREHOUSE\_ID. Does not include warehouse usage credits. |
| TOKENS | NUMBER | Number of tokens processed for the specified function and model for the combination of QUERY\_ID, MODEL\_NAME, and WAREHOUSE\_ID. |
| TOKEN\_CREDITS\_GRANULAR | OBJECT | A SQL object that provides a breakdown of credits billed by token type (input or output) for the specified function and model for the combination of QUERY\_ID, MODEL\_NAME, and WAREHOUSE\_ID. |
| TOKENS\_GRANULAR | OBJECT | A SQL object that provides a breakdown of tokens processed by token type (input or output) for the specified function and model for the combination of QUERY\_ID, MODEL\_NAME, and WAREHOUSE\_ID. |
| QUERY\_ID | TEXT | The ID of the query in which the function was called. |
| QUERY\_TAG | TEXT | The tag, if any, associated with the query in which the function was called. |
| USER\_ID | TEXT | The internal ID of the user who invoked the function.  For more information about authenticating, see [Authenticating to the server](/developer-guide/sql-api/authenticating). |
| WAREHOUSE\_ID | TEXT | The ID of the virtual warehouse that processed the query in which the function was called. |

Expand

Show lessSee more

## Usage notes

- This view includes only usage that occurred on or after November 17, 2025.
- Billing is reported only after the query completes, and the timestamp is the hour in which the query completed.
- Credit usage is based on the number of tokens processed, as outlined in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
