Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# USER\_AI\_USAGE\_HISTORY view

This Account Usage view can be used to query the credits that users consume for AI services, aggregated by hour.

Each row represents the credits consumed by one user, for one service type and one object, during one hour. The view attributes usage to the user that ran the work, including [service users](/sql-reference/sql/create-user).

The view covers a subset of AI service types. It doesn’t include every service type that is billed as AI usage in the [METERING\_DAILY\_HISTORY](/sql-reference/account-usage/metering_daily_history) view. For the service types that the view covers, see [Service types](#service-types).

See also:
:   [USER\_AI\_USAGE\_HISTORY view](/sql-reference/organization-usage/user_ai_usage_history) (Organization Usage)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| USAGE\_HOUR | TIMESTAMP\_LTZ | Start of the hour in which the usage occurred. The value is aligned to the hour. |
| USER\_ID | NUMBER | Internal identifier of the user that the usage is attributed to. `0` indicates usage that couldn’t be attributed to a user. See [Usage notes](#usage-notes). |
| USER\_NAME | VARCHAR | Name of the user. NULL when the user name can’t be resolved, including unattributed usage with `USER_ID` set to `0`. |
| SERVICE\_TYPE | VARCHAR | Service type that the usage is billed as. Values correspond to the `SERVICE_TYPE` column in the [METERING\_DAILY\_HISTORY](/sql-reference/account-usage/metering_daily_history) view. |
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
| SNOWFLAKE\_COWORK | SNOWFLAKE INTELLIGENCE | Name of the Snowflake Intelligence object, such as `SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT`. Can be NULL if the object name can’t be resolved. |
| SNOWFLAKE\_COCO\_CLI | CORTEX CODE | `CORTEX_CODE_CLI`. `ENTITY_ID` is NULL. |
| SNOWFLAKE\_COCO\_SNOWSIGHT | CORTEX CODE | `CORTEX_CODE_SNOWSIGHT`. `ENTITY_ID` is NULL. |
| SNOWFLAKE\_COCO\_DESKTOP | CORTEX CODE | `CORTEX_CODE_DESKTOP`. `ENTITY_ID` is NULL. |
| SNOWFLAKE\_COCO | CORTEX CODE | `CORTEX_CODE`. `ENTITY_ID` is NULL. |
| AI\_INFERENCE | AI GATEWAY | Name of the AI Gateway. Use `ENTITY_ID` to distinguish gateways. Can be NULL if the gateway name can’t be resolved. Includes gateway-routed inference only. Requests sent directly to the Cortex REST API aren’t included. |
| CORTEX\_TOOLS | AI GATEWAY | Name of the AI Gateway. Use `ENTITY_ID` to distinguish gateways. Can be NULL if the gateway name can’t be resolved. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 1 hour.
- The view retains credit usage for 12 calendar months, including the current month.
- Only usage that occurred on or after March 1, 2026 is included.
- Usage that Snowflake can’t attribute to a user is returned with `USER_ID` set to `0` and `USER_NAME` empty. A [task](/user-guide/tasks-intro#label-user-based-security-for-tasks) or a [dynamic table](/user-guide/dynamic-tables/privileges#refresh-with-specific-user-privileges-execute-as-user) runs as the system user unless you set `EXECUTE AS USER`. To attribute that usage to a user, run the task or dynamic table with `EXECUTE AS USER`.
- Rows can report `0` credits.
- The credits in this view reconcile with the `CREDITS_BILLED` column of the [METERING\_DAILY\_HISTORY](/sql-reference/account-usage/metering_daily_history) view for the service types that the view covers, except `AI_INFERENCE`. The `AI_INFERENCE` service type includes AI Gateway usage only, so its credits are lower than the `AI_INFERENCE` total in `METERING_DAILY_HISTORY`.
- Credit rates are listed in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

## Examples

Retrieve credits consumed by each user in the last 30 days:

Copy code

```
SELECT user_name,
       SUM(credits) AS total_credits
  FROM SNOWFLAKE.ACCOUNT_USAGE.USER_AI_USAGE_HISTORY
  WHERE usage_hour >= DATEADD('day', -30, CURRENT_TIMESTAMP())
    AND user_id > 0
  GROUP BY user_id, user_name
  ORDER BY total_credits DESC;
```

Retrieve credits consumed by each service type in the last 30 days:

Copy code

```
SELECT service_type,
       SUM(credits) AS total_credits
  FROM SNOWFLAKE.ACCOUNT_USAGE.USER_AI_USAGE_HISTORY
  WHERE usage_hour >= DATEADD('day', -30, CURRENT_TIMESTAMP())
  GROUP BY service_type
  ORDER BY total_credits DESC;
```

Retrieve credits consumed by each Cortex Agent in the last 30 days:

Copy code

```
SELECT entity_name,
       SUM(credits) AS total_credits
  FROM SNOWFLAKE.ACCOUNT_USAGE.USER_AI_USAGE_HISTORY
  WHERE service_type = 'CORTEX_AGENTS'
    AND usage_hour >= DATEADD('day', -30, CURRENT_TIMESTAMP())
  GROUP BY entity_id, entity_name
  ORDER BY total_credits DESC;
```
