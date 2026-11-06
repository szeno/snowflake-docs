Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

# USER\_AI\_USAGE\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

This Organization Usage view can be used to query the credits that users consume for AI services across all the accounts in your organization, aggregated by hour.

Each row represents the credits consumed by one user, for one service type and one object, during one hour. The view attributes usage to the user that ran the work, including [service users](/sql-reference/sql/create-user).

The view covers a subset of AI service types. It doesn’t include every service type that is billed as AI usage in the [METERING\_DAILY\_HISTORY](/sql-reference/organization-usage/metering_daily_history) view. For the service types that the view covers, see [Service types](#service-types).

See also:
:   [USER\_AI\_USAGE\_HISTORY view](/sql-reference/account-usage/user_ai_usage_history) (Account Usage)

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
| USAGE\_HOUR | TIMESTAMP\_LTZ | Start of the hour in which the usage occurred. The value is aligned to the hour. |
| USER\_ID | NUMBER | Internal identifier of the user that the usage is attributed to. `0` indicates usage that couldn’t be attributed to a user. See [Usage notes](#usage-notes). |
| USER\_NAME | VARCHAR | Name of the user. Empty when `USER_ID` is `0`. |
| SERVICE\_TYPE | VARCHAR | Service type that the usage is billed as. Values correspond to the `SERVICE_TYPE` column in the [METERING\_DAILY\_HISTORY](/sql-reference/organization-usage/metering_daily_history) view. |
| ENTITY\_TYPE | VARCHAR | Product category of the object that consumed the credits. See [Service types](#service-types). |
| ENTITY\_ID | NUMBER | Internal identifier of the object that consumed the credits. NULL for service types that aren’t tied to a specific object. |
| ENTITY\_NAME | VARCHAR | Name of the object that consumed the credits. See [Service types](#service-types). |
| CREDITS | NUMBER | Credits consumed by the user for the service type and object during the hour. Can be `0`. Doesn’t include warehouse credits. |

Expand

Show lessSee more

## Service types

The view returns the following combinations of `SERVICE_TYPE`, `ENTITY_TYPE`, and `ENTITY_NAME`:

| SERVICE\_TYPE | ENTITY\_TYPE | ENTITY\_NAME |
| --- | --- | --- |
| AI\_FUNCTIONS | AI FUNCTION | Name of the AI Function, such as `AI_COMPLETE` or `AI_EMBED`. `ENTITY_ID` is NULL. |
| CORTEX\_AGENTS | CORTEX AGENT | Name of the Cortex Agent. Use `ENTITY_ID` to distinguish agents that share a name. |
| SNOWFLAKE\_COWORK | SNOWFLAKE INTELLIGENCE | `SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT`. |
| SNOWFLAKE\_COCO\_CLI | CORTEX CODE | `CORTEX_CODE_CLI`. `ENTITY_ID` is NULL. |
| SNOWFLAKE\_COCO\_SNOWSIGHT | CORTEX CODE | `CORTEX_CODE_SNOWSIGHT`. `ENTITY_ID` is NULL. |
| SNOWFLAKE\_COCO\_DESKTOP | CORTEX CODE | `CORTEX_CODE_DESKTOP`. `ENTITY_ID` is NULL. |
| SNOWFLAKE\_COCO | CORTEX CODE | `CORTEX_CODE`. `ENTITY_ID` is NULL. |
| AI\_INFERENCE | AI GATEWAY | `SNOWFLAKE`. Usage for the AI Gateway only. Usage for the Cortex REST API isn’t included. |
| CORTEX\_TOOLS | AI GATEWAY | `SNOWFLAKE`. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
- The view provides credit usage within the last 365 days (1 year).
- Usage that Snowflake can’t attribute to a user is returned with `USER_ID` set to `0` and `USER_NAME` empty. A [task](/user-guide/tasks-intro#label-user-based-security-for-tasks) or a [dynamic table](/user-guide/dynamic-tables/privileges#refresh-with-specific-user-privileges-execute-as-user) runs as the system user unless you set `EXECUTE AS USER`. To attribute that usage to a user, run the task or dynamic table with `EXECUTE AS USER`.
- Rows can report `0` credits.
- The credits in this view reconcile with the `CREDITS_BILLED` column of the [METERING\_DAILY\_HISTORY](/sql-reference/organization-usage/metering_daily_history) view for the service types that the view covers, except `AI_INFERENCE`. The `AI_INFERENCE` service type includes AI Gateway usage only, so its credits are lower than the `AI_INFERENCE` total in `METERING_DAILY_HISTORY`.
- Credit rates are listed in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

## Examples

Retrieve credits consumed by each user in the last 30 days, across all accounts:

Copy code

```
SELECT account_name,
       user_name,
       SUM(credits) AS total_credits
  FROM SNOWFLAKE.ORGANIZATION_USAGE.USER_AI_USAGE_HISTORY
  WHERE usage_hour >= DATEADD('day', -30, CURRENT_TIMESTAMP())
    AND user_id > 0
  GROUP BY account_name, user_name
  ORDER BY total_credits DESC;
```

Retrieve credits consumed by each service type in the last 30 days:

Copy code

```
SELECT service_type,
       SUM(credits) AS total_credits
  FROM SNOWFLAKE.ORGANIZATION_USAGE.USER_AI_USAGE_HISTORY
  WHERE usage_hour >= DATEADD('day', -30, CURRENT_TIMESTAMP())
  GROUP BY service_type
  ORDER BY total_credits DESC;
```
