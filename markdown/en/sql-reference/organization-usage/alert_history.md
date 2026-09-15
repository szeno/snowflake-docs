Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# ALERT\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view enables you to retrieve the history of [alert](/user-guide/alerts) usage. The view displays one row for
each run of an alert in the history.

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
| NAME | VARCHAR | Name of the alert. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the alert. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the alert. |
| ACTION | VARCHAR | The text of the SQL statement that serves as the action for the alert. |
| ACTION\_QUERY\_ID | VARCHAR | Internal/system-generated identifier for the SQL statement executed as the action of the alert. |
| CONDITION | VARCHAR | The text of the SQL statement that serves as the condition for the alert. |
| CONDITION\_QUERY\_ID | VARCHAR | Internal/system-generated identifier for the SQL statement executed as the condition of the alert. |
| ERROR\_CODE | NUMBER | Error code, if the alert returned an error or failed to execute (e.g. if the current user did not have privileges to execute the alert). |
| ERROR\_MESSAGE | VARCHAR | Error message, if the alert returned an error. |
| STATE | VARCHAR | Status of the alert. This can be one of the following:   - SCHEDULED: The alert will execute at the time specified by the SCHEDULED\_TIME column. This status does not apply to   [alerts on new data](/user-guide/alerts#label-alerts-type-streaming). - EXECUTING: The condition or action of the alert is currently executing. - FAILED: The alert failed. Either the alert condition or alert action encountered an error that prevented it from being   executed. - CANCELLED: The alert execution was cancelled (e.g. when the alert is suspended). - CONDITION\_FALSE: The condition was evaluated successfully but returned no data. As a result, the action was not executed.   This status does not apply to [alerts on new data](/user-guide/alerts#label-alerts-type-streaming). - CONDITION\_FAILED: The evaluation of the condition failed. For details on the failure, check the ERROR\_CODE and   ERROR\_MESSAGE columns. - ACTION\_FAILED: The condition was evaluated successfully, but the execution of the action failed. For details on the   failure, check the ERROR\_CODE and ERROR\_MESSAGE columns. - TRIGGERED: The condition was evaluated successfully, and the action was executed successfully. |
| SCHEDULED\_TIME | TIMESTAMP\_LTZ | Time when the scheduled alert is/was scheduled to start running.  Note that we make a best effort to ensure absolute precision, but only guarantee that alerts do not execute *before* the scheduled time. |
| COMPLETED\_TIME | TIMESTAMP\_LTZ | Time when the alert completed, or NULL if SCHEDULED\_TIME is in the future or if the alert is still running. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database containing the schema. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema. |
| SCHEDULED\_FROM | VARCHAR | Specifies what initiated the alert. The column contains one of the following values:   - `SCHEDULE`: The alert was scheduled to run normally, as described in SCHEDULE clause of   [CREATE ALERT](/sql-reference/sql/create-alert). - `EXECUTE ALERT`: The alert was scheduled to run using [EXECUTE ALERT](/sql-reference/sql/execute-alert). - `TRIGGER`: The [alert on new data](/user-guide/alerts#label-alerts-type-streaming) was run because the underlying table or view   contains new data. |
| RUNBOOK | VARCHAR | URL or free-text reference to a runbook for this alert. Returns NULL if not set. |
| WAS\_AUTO\_SUSPENDED | BOOLEAN | Indicates whether the alert was automatically suspended after this execution due to exceeding the consecutive failure threshold set by the `SUSPEND_ALERT_AFTER_NUM_FAILURES` parameter. |
| CONFIG | VARCHAR | JSON configuration string stored on the alert at the time of this execution. Returns NULL if not set. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- For increased performance, filter queries on the COMPLETED\_TIME or SCHEDULED\_TIME column.

## Examples

Retrieve records for the 10 most recent completed alert runs:

> Copy code
>
> ```
> SELECT account_name, name, condition, condition_query_id, action, action_query_id, state
>   FROM snowflake.organization_usage.alert_history
>   LIMIT 10;
> ```

Retrieve records for alert runs completed in the past hour:

> Copy code
>
> ```
> SELECT account_name, name, condition, condition_query_id, action, action_query_id, state
> FROM snowflake.organization_usage.alert_history
> WHERE COMPLETED_TIME > DATEADD(hours, -1, CURRENT_TIMESTAMP());
> ```
