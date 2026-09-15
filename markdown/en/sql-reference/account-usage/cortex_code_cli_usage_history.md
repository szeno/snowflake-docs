Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# CORTEX\_CODE\_CLI\_USAGE\_HISTORY view

The CORTEX\_CODE\_CLI\_USAGE\_HISTORY view can be used to query the usage history of [Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli).

The information in the view includes the number of credits consumed each time a user interacts
with Cortex Code CLI. Each row in the view represents a single request and provides detail about
the aggregated tokens and credits as well as a granular breakdown by model. The view also includes
relevant metadata, such as the user ID and request ID.

Note

This view does not include requests originating from other Cortex Code interfaces. Requests originating from Snowsight are recorded in the [CORTEX\_CODE\_SNOWSIGHT\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_code_snowsight_usage_history) view. Requests originating from the desktop app are recorded in the [CORTEX\_CODE\_DESKTOP\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_code_desktop_usage_history) view.

To query usage across CoCo CLI, Desktop, and Snowsight in a single view, use [SNOWFLAKE\_COCO\_USAGE\_HISTORY](/sql-reference/account-usage/snowflake_coco_usage_history).

Tip

In [Cortex Code](/user-guide/cortex-code/cortex-code), including the [CLI](/user-guide/cortex-code/cortex-code-cli), [Desktop](/user-guide/cortex-code/cortex-code-desktop), and [Snowsight](/user-guide/cortex-code/cortex-code-snowsight) interfaces, you can use the [`cost-intelligence`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-cost-intelligence) bundled skill to answer questions about the usage data in this view. Invoke the skill with `/cost-intelligence`, or describe your question in plain language and Cortex Code selects the skill automatically.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| USER\_ID | NUMBER | The unique identifier of the user who made the request. |
| USER\_NAME | VARCHAR | The login name of the user who made the request. |
| USER\_TAGS | ARRAY | Tags associated with the user. Each object in the array contains the following value pairs:   - `level`: The level at which the tag is applied (for example, “ACCOUNT” or “USER”). - `tag_database`: The database where the tag is defined. - `tag_schema`: The schema where the tag is defined. - `tag_name`: The name of the tag. - `tag_value`: The value of the tag. |
| REQUEST\_ID | VARCHAR | The unique identifier for the request. |
| PARENT\_REQUEST\_ID | VARCHAR | The identifier of the parent request, if applicable. |
| USAGE\_TIME | TIMESTAMP\_TZ | The timestamp when the usage was recorded. |
| TOKEN\_CREDITS | NUMBER | The total number of credits consumed for the request. |
| TOKENS | NUMBER | The total number of tokens used for the request. |
| TOKENS\_GRANULAR | OBJECT | Granular breakdown of token usage by model. Each key is a model name, and each value is an object containing the following fields:   - `input`: Number of input tokens. - `cache_read_input`: Number of cache read input tokens. - `cache_write_input`: Number of cache write input tokens. - `output`: Number of output tokens. |
| CREDITS\_GRANULAR | OBJECT | Granular breakdown of credit usage by model. Each key is a model name, and each value is an object containing the following fields:   - `input`: Credit value for input tokens. - `cache_read_input`: Credit value for cache read input tokens. - `cache_write_input`: Credit value for cache write input tokens. - `output`: Credit value for output tokens. |
| METADATA | OBJECT | Additional metadata, including:   - `role_id`: ID of the primary role used for the request. - `role_name`: Name of the primary role used for the request. - `inference_region`: The [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) routing used for the request. Possible values are `global` (any Snowflake-supported region across any cloud provider) or `regional` (requests restricted to specific geographic boundaries). Contains NULL if the record predates the introduction of this field. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 1 hour.
- The view provides up-to-date credit usage for an account within the last 365 days (1 year).
- Credit rate usage is based on the number of tokens processed, as outlined in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
- The `USER_TAGS` column returns an empty array for usage records that predate the introduction of user tag support.

## Examples

Retrieve Cortex Code CLI usage history:

Copy code

```
SELECT *
  FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_CODE_CLI_USAGE_HISTORY;
```

Retrieve total credits consumed per user in the last 30 days:

Copy code

```
SELECT USER_ID,
       USER_NAME,
       SUM(TOKEN_CREDITS) AS TOTAL_CREDITS
  FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_CODE_CLI_USAGE_HISTORY
  WHERE USAGE_TIME >= DATEADD('day', -30, CURRENT_TIMESTAMP())
  GROUP BY USER_ID, USER_NAME
  ORDER BY TOTAL_CREDITS DESC;
```

Retrieve usage by model for a specific user in the last 7 days:

Copy code

```
SELECT REQUEST_ID,
       USAGE_TIME,
       TOKENS_GRANULAR,
       CREDITS_GRANULAR
  FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_CODE_CLI_USAGE_HISTORY
  WHERE USER_NAME = 'my_user'
    AND USAGE_TIME >= DATEADD('day', -7, CURRENT_TIMESTAMP())
  ORDER BY USAGE_TIME DESC;
```

Filter usage by a specific user tag:

Copy code

```
SELECT USER_ID,
       USER_NAME,
       SUM(TOKEN_CREDITS) AS TOTAL_CREDITS
  FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_CODE_CLI_USAGE_HISTORY,
       LATERAL FLATTEN(input => USER_TAGS) t
  WHERE t.value:tag_name::STRING = 'department'
    AND t.value:tag_value::STRING = 'engineering'
  GROUP BY USER_ID, USER_NAME
  ORDER BY TOTAL_CREDITS DESC;
```
