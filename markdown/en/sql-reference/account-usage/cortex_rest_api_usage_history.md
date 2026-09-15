Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# CORTEX\_REST\_API\_USAGE\_HISTORY view

Query the CORTEX\_REST\_API\_USAGE\_HISTORY view to see the history of Cortex REST API calls.

The information in the view includes the number of tokens processed and credits consumed for each REST API request. The view also includes
relevant metadata, such as the request ID, model name, user ID, and inference region. For more information on Cortex billing, see
[Snowflake Cortex AI functions incur compute cost based on the number of tokens…](/user-guide/snowflake-cortex/aisql-cost#label-cortex-llm-cost-considerations).

Tip

In [Cortex Code](/user-guide/cortex-code/cortex-code), including the [CLI](/user-guide/cortex-code/cortex-code-cli), [Desktop](/user-guide/cortex-code/cortex-code-desktop), and [Snowsight](/user-guide/cortex-code/cortex-code-snowsight) interfaces, you can use the [`cost-intelligence`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-cost-intelligence) bundled skill to answer questions about the usage data in this view. Invoke the skill with `/cost-intelligence`, or describe your question in plain language and Cortex Code selects the skill automatically.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The beginning of the time range for the usage history. |
| END\_TIME | TIMESTAMP\_LTZ | The end of the time range for the usage history. |
| REQUEST\_ID | TEXT | The unique identifier for the REST API request. |
| MODEL\_NAME | TEXT | Name of the model used in the REST API call. |
| TOKENS | NUMBER | Number of tokens processed for the REST API request. |
| TOKENS\_GRANULAR | OBJECT | A SQL object that provides a breakdown of tokens processed by token type (input or output) for the REST API request. |
| USER\_ID | TEXT | The internal ID of the user who invoked the REST API.  For more information about authenticating, see [Authenticating to the server](/developer-guide/sql-api/authenticating). |
| INFERENCE\_REGION | TEXT | The region in which the inference was performed. |

Expand

Show lessSee more

## Usage notes

- The view provides up-to-date usage information for an account within the last 365 days (1 year).
- Credit usage is based on the number of tokens processed, as outlined in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
