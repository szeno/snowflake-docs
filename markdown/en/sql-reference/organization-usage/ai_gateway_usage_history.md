Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

# AI\_GATEWAY\_USAGE\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

The AI\_GATEWAY\_USAGE\_HISTORY view in the ORGANIZATION\_USAGE schema can be used to query the usage
history of [Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway) across all the accounts
in your organization.

Each row in the view represents a single request sent through a gateway, and includes the user who made
it, the service that handled it, details of the operation, and the resulting credit consumption. Use this
view for organization-wide showback, adoption reporting, and identifying which accounts, users, and
models drive spend.

Note

Requests sent directly to [Cortex Inference](/user-guide/snowflake-cortex/cortex-rest-api) rather than
through a gateway are recorded in
[CORTEX\_REST\_API\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_rest_api_usage_history) instead.

See also:
:   [AI\_GATEWAY\_USAGE\_HISTORY view](/sql-reference/account-usage/ai_gateway_usage_history) (Account Usage)

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

- Credit rate usage is as outlined in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
- This view reports credits. It isn’t intended for near-real-time activity monitoring, and it can’t be reconciled request-for-request against activity data.

## Examples

Retrieve gateway usage history across the organization:

Copy code

```
SELECT *
  FROM SNOWFLAKE.ORGANIZATION_USAGE.AI_GATEWAY_USAGE_HISTORY;
```

Retrieve total credits consumed per account:

Copy code

```
SELECT ACCOUNT_NAME,
       SUM(CREDITS) AS TOTAL_CREDITS
  FROM SNOWFLAKE.ORGANIZATION_USAGE.AI_GATEWAY_USAGE_HISTORY
  GROUP BY ACCOUNT_NAME
  ORDER BY TOTAL_CREDITS DESC;
```
