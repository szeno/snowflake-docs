Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# APPLICATION\_CALLBACK\_HISTORY view

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The `APPLICATION_CALLBACK_HISTORY` view provides a history of callback invocations for Snowflake Native Apps in your Snowflake account. Each row in the view represents a callback invocation, including the callback type, state, and any error information.

For more information about callbacks, see [Callbacks](/developer-guide/native-apps/callbacks).

The retention time for this view is 365 days (1 year).

## Columns

The following table provides definitions for the `APPLICATION_CALLBACK_HISTORY` view columns.

| Column | Data type | Description |
| --- | --- | --- |
| TYPE | VARCHAR | The callback type as defined in the manifest file. |
| APPLICATION\_NAME | VARCHAR | The name of the app that defines the callback. |
| STATE | VARCHAR | The state of the callback execution. Possible values are: `QUEUED`, `SCHEDULED`, `EXECUTING`, `COMPLETED`, `FAILED`, `ABORTED`. For descriptions of each state, see [Callback states](/sql-reference/functions/application_callback_history#label-application-callback-history-states). |
| STARTED\_ON | TIMESTAMP\_LTZ | The timestamp when the callback was invoked. |
| COMPLETED\_ON | TIMESTAMP\_LTZ | The completion timestamp. NULL if the callback has not yet completed. |
| TRIGGERING\_QUERY\_ID | VARCHAR | The query ID of the SQL statement that triggered the callback. NULL if not applicable. |
| QUERY\_ID | VARCHAR | The query ID of the callback procedure execution. |
| ERROR\_CODE | VARCHAR | The error code. NULL unless STATE is `FAILED` or `ABORTED`. |
| ERROR\_MESSAGE | VARCHAR | The error message. NULL unless STATE is `FAILED` or `ABORTED`. This column is redacted unless the app is installed on the same account as the app package. |

Expand

Show lessSee more

## Examples

Retrieve the callback history for all applications in the current account:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.APPLICATION_CALLBACK_HISTORY;
```

Retrieve the callback history for a specific app:

Copy code

```
SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.APPLICATION_CALLBACK_HISTORY
WHERE APPLICATION_NAME = 'my_app'
ORDER BY STARTED_ON DESC;
```

Retrieve only failed or aborted callback invocations:

Copy code

```
SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.APPLICATION_CALLBACK_HISTORY
WHERE STATE IN ('FAILED', 'ABORTED')
ORDER BY STARTED_ON DESC;
```
