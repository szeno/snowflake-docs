Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

# SNOWFLAKE\_COCO\_USAGE\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

The SNOWFLAKE\_COCO\_USAGE\_HISTORY view in the ORGANIZATION\_USAGE schema can be used to query the usage history of [CoCo](/user-guide/cortex-code/cortex-code) across all interfaces ([CLI](/user-guide/cortex-code/cortex-code-cli), [Desktop](/user-guide/cortex-code/cortex-code-desktop), and [Snowsight](/user-guide/cortex-code/cortex-code-snowsight)) and across all accounts in your organization.

The information in the view includes the number of credits consumed each time a user interacts
with CoCo. Each row in the view represents a single request and provides detail about
the aggregated tokens and credits as well as a granular breakdown by model. The view also includes
relevant metadata, such as the user ID, request ID, and the interface that originated the request.

Note

Interface-specific usage history is also available in the following views:

- [CORTEX\_CODE\_CLI\_USAGE\_HISTORY](/sql-reference/organization-usage/cortex_code_cli_usage_history) for CoCo CLI
- [CORTEX\_CODE\_DESKTOP\_USAGE\_HISTORY](/sql-reference/organization-usage/cortex_code_desktop_usage_history) for CoCo Desktop
- [CORTEX\_CODE\_SNOWSIGHT\_USAGE\_HISTORY](/sql-reference/organization-usage/cortex_code_snowsight_usage_history) for CoCo in Snowsight

See also:
:   [SNOWFLAKE\_COCO\_USAGE\_HISTORY view](/sql-reference/account-usage/snowflake_coco_usage_history) (Account Usage)

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
| USER\_ID | NUMBER | The unique identifier of the user who made the request. |
| USER\_NAME | VARCHAR | The login name of the user who made the request. |
| USER\_TAGS | ARRAY | Tags associated with the user. Each object in the array contains the following value pairs:   - `level`: The level at which the tag is applied (for example, “ACCOUNT” or “USER”). - `tag_database`: The database where the tag is defined. - `tag_schema`: The schema where the tag is defined. - `tag_name`: The name of the tag. - `tag_value`: The value of the tag. |
| REQUEST\_ID | VARCHAR | The unique identifier for the request. |
| PARENT\_REQUEST\_ID | VARCHAR | The identifier of the parent request, if applicable. |
| USAGE\_TIME | TIMESTAMP\_TZ | The timestamp when the usage was recorded. |
| INTERFACE | VARCHAR | The [CoCo](/user-guide/cortex-code/cortex-code) interface that originated the request. Possible values are:   - `cli`: [CoCo CLI](/user-guide/cortex-code/cortex-code-cli) - `desktop`: [CoCo Desktop](/user-guide/cortex-code/cortex-code-desktop) - `snowsight`: [CoCo in Snowsight](/user-guide/cortex-code/cortex-code-snowsight) |
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
- The `USER_TAGS` column returns an empty array for usage records that predate the introduction of user tag support.

## Examples

Retrieve CoCo usage history across all interfaces and accounts in the organization:

Copy code

```
SELECT *
  FROM SNOWFLAKE.ORGANIZATION_USAGE.SNOWFLAKE_COCO_USAGE_HISTORY;
```

Retrieve total credits consumed per interface in the last 30 days:

Copy code

```
SELECT INTERFACE,
       SUM(TOKEN_CREDITS) AS TOTAL_CREDITS
  FROM SNOWFLAKE.ORGANIZATION_USAGE.SNOWFLAKE_COCO_USAGE_HISTORY
  WHERE USAGE_TIME >= DATEADD('day', -30, CURRENT_TIMESTAMP())
  GROUP BY INTERFACE
  ORDER BY TOTAL_CREDITS DESC;
```

Retrieve total credits consumed per account in the last 30 days:

Copy code

```
SELECT ACCOUNT_NAME,
       SUM(TOKEN_CREDITS) AS TOTAL_CREDITS
  FROM SNOWFLAKE.ORGANIZATION_USAGE.SNOWFLAKE_COCO_USAGE_HISTORY
  WHERE USAGE_TIME >= DATEADD('day', -30, CURRENT_TIMESTAMP())
  GROUP BY ACCOUNT_NAME
  ORDER BY TOTAL_CREDITS DESC;
```
