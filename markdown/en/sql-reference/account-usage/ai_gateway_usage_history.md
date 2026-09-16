Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# AI\_GATEWAY\_USAGE\_HISTORY view

The AI\_GATEWAY\_USAGE\_HISTORY view can be used to query the usage history of
[Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway).

Each row in the view represents a single request sent through the gateway, and includes the user who made
it, the service that handled it, details of the operation, and the resulting credit consumption. Use this
view for showback, adoption reporting, and identifying which users and models drive spend.

Note

Requests sent directly to [Cortex Inference](/user-guide/snowflake-cortex/cortex-rest-api) rather than
through a gateway are recorded in
[CORTEX\_REST\_API\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_rest_api_usage_history) instead.

Tip

In [Cortex Code](/user-guide/cortex-code/cortex-code), including the [CLI](/user-guide/cortex-code/cortex-code-cli), [Desktop](/user-guide/cortex-code/cortex-code-desktop), and [Snowsight](/user-guide/cortex-code/cortex-code-snowsight) interfaces, you can use the [`cost-intelligence`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-cost-intelligence) bundled skill to answer questions about the usage data in this view. Invoke the skill with `/cost-intelligence`, or describe your question in plain language and Cortex Code selects the skill automatically.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| REQUEST\_ID | TEXT | Unique identifier for the request. Each HTTP request gets a unique ID. |
| GATEWAY\_NAME | TEXT | The gateway that served the request. A gateway name can change over time. |
| GATEWAY\_ID | TEXT | The identifier of the gateway that served the request. This is static over time. |
| USER\_ID | TEXT | The internal identifier of the authenticated user. |
| SERVICE\_TYPE | TEXT | The service that handled the request. Inference requests are recorded as `AI_INFERENCE`. |
| OPERATION\_DETAILS | OBJECT | Details of the operation, keyed by model. For inference, each model maps to its token counts, as in `{"claude-sonnet-5": {"input_tokens": 27, "output_tokens": 7427}}`. |
| CREDITS | NUMBER | Total credits consumed for the request. |
| CREDITS\_GRANULAR | OBJECT | Credits consumed for the request, keyed by model, as in `{"claude-sonnet-5": 0.037162}`. |
| METADATA | OBJECT | Additional metadata about the request. |

Expand

Show lessSee more

## Usage notes

- The view provides credit usage for an account within the last 365 days (1 year).
- Credit rate usage is as outlined in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
- This view reports credits. It isn’t intended for near-real-time activity monitoring, and it can’t be reconciled request-for-request against activity data.

## Examples

Retrieve all gateway usage history:

Copy code

```
SELECT *
  FROM SNOWFLAKE.ACCOUNT_USAGE.AI_GATEWAY_USAGE_HISTORY;
```

Retrieve total credits consumed per user:

Copy code

```
SELECT USER_ID,
       SUM(CREDITS) AS TOTAL_CREDITS
  FROM SNOWFLAKE.ACCOUNT_USAGE.AI_GATEWAY_USAGE_HISTORY
  GROUP BY USER_ID
  ORDER BY TOTAL_CREDITS DESC;
```

Inspect the per-request operation details and credit breakdown, which are objects whose contents depend
on the service that handled the request:

Copy code

```
SELECT REQUEST_ID,
       SERVICE_TYPE,
       OPERATION_DETAILS,
       CREDITS_GRANULAR,
       CREDITS
  FROM SNOWFLAKE.ACCOUNT_USAGE.AI_GATEWAY_USAGE_HISTORY
  ORDER BY CREDITS DESC
  LIMIT 100;
```
