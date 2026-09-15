Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

# CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

This Organization Usage view can be used to query the usage history of [Cortex AI Functions](/user-guide/snowflake-cortex/aisql) across all the accounts in your organization.

The view includes the number of tokens and credits consumed each time a Cortex Function is called, aggregated in one-hour
windows. The view also includes relevant metadata, such as the warehouse ID, start and end times of the function
execution, and the name of the function and the model, if specified. Each row represents the usage for a single function
call.

See also:
:   [CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_ai_functions_usage_history) (Account Usage)

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

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the usage aggregation window. The window resolution is 1 hour. For example, if a query began at 05:30 and completed at 08:30, four records appear in the usage view, one each for the 5:00, 6:00, 7:00, and 8:00 aggregation windows. |
| END\_TIME | TIMESTAMP\_LTZ | End of the usage aggregation window. |
| FUNCTION\_NAME | VARCHAR | Name of the Cortex AI Function called. Usage history contains a row for each function called in a query. |
| MODEL\_NAME | VARCHAR | Model name. Empty for Cortex AI Functions where a model is not specified as an argument. Usage history contains a row for each model used in a query. |
| QUERY\_ID | VARCHAR | The ID of the query in which the function was called. |
| WAREHOUSE\_ID | NUMBER | System-generated identifier for the warehouse used by the query calling the Cortex AI Function. |
| ROLE\_NAMES | ARRAY | Roles associated with the query. The primary role is the first element of the array. |
| QUERY\_TAG | VARCHAR | The tag, if any, associated with the query in which the function was called. |
| USER\_ID | VARCHAR | System-generated identifier for the user that executed the query calling the Cortex AI Function. |
| METRICS | ARRAY | A breakdown of usage metrics for the specified function and model for the combination of QUERY\_ID, MODEL\_NAME, and WAREHOUSE\_ID. See [Metrics column](#metrics-column) below for more details. |
| CREDITS | NUMBER | Number of credits billed for Cortex AI Function usage based on metrics for the specified function and model for the combination of QUERY\_ID, MODEL\_NAME, and WAREHOUSE\_ID. Does not include warehouse usage credits. |
| IS\_COMPLETED | BOOLEAN | Whether the query was completed in this aggregation window. |

Expand

Show lessSee more

## Metrics column

The metrics column contains a breakdown of usage metrics for the specified function and model for the combination of
QUERY\_ID, MODEL\_NAME, and WAREHOUSE\_ID. Each element contains a `key` object (with `metric` type and `unit`
fields) and a `value`. The structure varies by metering method, as follows:

- **Token-based metering** (most AI Functions): Bills by token count, either as separate input and output token counts or as total token count, depending on the function.

  Example: `[{"key":{"metric":"input","unit":"tokens"},"value":17},{"key":{"metric":"output","unit":"tokens"},"value":65}]`  
  `[{"key":{"metric":"total","unit":"tokens"},"value":527}]`
- **Page-based metering** (AI\_PARSE\_DOCUMENT): Bills by page.

  Example: `[{"key":{"metric":"total","unit":"pages"},"value":3}]`

## Usage notes

- Latency for the view may be up to 24 hours.
- This view includes only usage that occurred on or after January 5, 2026.
- User ID attribution, Query tag, and Roles fields are available for data acquired after February 16, 2026.
- The view tracks both function calls that have completed and calls that are still in progress.
- Running queries are updated every 30 minutes (best effort) with an SLA of one hour.
- The credit rate usage is determined based on the function called, model used and the tokens processed as outlined in the
  [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
