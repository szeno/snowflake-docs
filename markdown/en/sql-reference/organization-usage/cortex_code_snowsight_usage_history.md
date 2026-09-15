Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

# CORTEX\_CODE\_SNOWSIGHT\_USAGE\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

The CORTEX\_CODE\_SNOWSIGHT\_USAGE\_HISTORY view in the ORGANIZATION\_USAGE schema can be used to query the usage history of [Cortex Code in Snowsight](/user-guide/cortex-code/cortex-code-snowsight) across all the accounts in your organization.

The information in the view includes the number of credits consumed each time a user interacts
with Cortex Code in Snowsight. Each row in the view represents a single request and provides detail about
the aggregated tokens and credits as well as a granular breakdown by model. The view also includes
relevant metadata, such as the user ID and request ID.

Note

This view does not include requests originating from Cortex Code CLI. Requests originating from Cortex Code CLI are recorded in the [CORTEX\_CODE\_CLI\_USAGE\_HISTORY](/sql-reference/organization-usage/cortex_code_cli_usage_history) view.
Requests originating from Cortex Code Desktop are recorded in the [CORTEX\_CODE\_DESKTOP\_USAGE\_HISTORY](/sql-reference/organization-usage/cortex_code_desktop_usage_history) view.

To query usage across CoCo CLI, Desktop, and Snowsight in a single view, use [SNOWFLAKE\_COCO\_USAGE\_HISTORY](/sql-reference/organization-usage/snowflake_coco_usage_history).

See also:
:   [CORTEX\_CODE\_SNOWSIGHT\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_code_snowsight_usage_history) (Account Usage)

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
| USER\_ID | NUMBER | The unique identifier of the user who made the request. |
| USER\_TAGS | ARRAY | Tags associated with the user. Each object in the array contains the following value pairs:   - `level`: The level at which the tag is applied (for example, “ACCOUNT” or “USER”). - `tag_database`: The database where the tag is defined. - `tag_schema`: The schema where the tag is defined. - `tag_name`: The name of the tag. - `tag_value`: The value of the tag. |
| REQUEST\_ID | VARCHAR | The unique identifier for the request. |
| PARENT\_REQUEST\_ID | VARCHAR | The identifier of the parent request, if applicable. |
| USAGE\_TIME | TIMESTAMP\_TZ | The timestamp when the usage was recorded. |
| TOKEN\_CREDITS | NUMBER | The number of token credits used for the request. |
| TOKENS | NUMBER | The total number of tokens used for the request. |
| TOKENS\_GRANULAR | OBJECT | Granular breakdown of token usage by model. Each key is a model name, and each value is an object containing the following fields:   - `input`: Number of input tokens. - `cache_read_input`: Number of cache read input tokens. - `cache_write_input`: Number of cache write input tokens. - `output`: Number of output tokens. |
| CREDITS\_GRANULAR | OBJECT | Granular breakdown of credit usage by model. Each key is a model name, and each value is an object containing the following fields:   - `input`: Credit value for input tokens. - `cache_read_input`: Credit value for cache read input tokens. - `cache_write_input`: Credit value for cache write input tokens. - `output`: Credit value for output tokens. |
| METADATA | OBJECT | Additional metadata, including:   - `role_id`: ID of the primary role used for the request. - `role_name`: Name of the primary role used for the request. - `inference_region`: The [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) routing used for the request. Possible values are `global` (any Snowflake-supported region across any cloud provider) or `regional` (requests restricted to specific geographic boundaries). Contains NULL if the record predates the introduction of this field. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
- Credit rate usage is based on the number of tokens processed, as outlined in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

## Examples

Retrieve Cortex Code in Snowsight usage history across all accounts in the organization:

Copy code

```
SELECT *
  FROM SNOWFLAKE.ORGANIZATION_USAGE.CORTEX_CODE_SNOWSIGHT_USAGE_HISTORY;
```

Retrieve total credits consumed per account in the last 30 days:

Copy code

```
SELECT ACCOUNT_NAME,
       SUM(TOKEN_CREDITS) AS TOTAL_CREDITS
  FROM SNOWFLAKE.ORGANIZATION_USAGE.CORTEX_CODE_SNOWSIGHT_USAGE_HISTORY
  WHERE USAGE_TIME >= DATEADD('day', -30, CURRENT_TIMESTAMP())
  GROUP BY ACCOUNT_NAME
  ORDER BY TOTAL_CREDITS DESC;
```
