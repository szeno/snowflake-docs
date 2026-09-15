Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# APPLICATION\_REMOTE\_OPERATION\_HISTORY view

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Use the APPLICATION\_REMOTE\_OPERATION\_HISTORY view to query the history of remote app operation invocations for Snowflake Native Apps in your Snowflake account.

The latency for this view is up to 1 hour, and the retention time is 365 days (1 year).

For more information about remote app operations, see [Use remote app operations](/developer-guide/native-apps/remote-app-operation) and
[Manage remote app operations](/developer-guide/native-apps/ui-consumer-remote-app-operation).

## Columns

The following table provides definitions for the APPLICATION\_REMOTE\_OPERATION\_HISTORY view columns.

| Column | Data type | Description |
| --- | --- | --- |
| APPLICATION\_NAME | VARCHAR | The name of the application on which the remote app operation was performed. |
| APPLICATION\_ID | NUMBER | The internal, system-generated identifier for the application. |
| APPLICATION\_HASH | VARCHAR | The provider-facing identifier for the application. |
| REQUEST\_ID | VARCHAR | The unique identifier for the remote app operation invocation. |
| OPERATION\_TYPE | VARCHAR | The type of remote operation. Possible values are: `run_sql`, `disable`, `enable`, `retry_upgrade`. |
| COMPLETED\_ON | TIMESTAMP\_LTZ | The timestamp when the operation was completed. |
| REQUEST\_STATUS | VARCHAR | The status of the remote app operation invocation. |
| REQUEST\_CONFIG | VARIANT | The configuration provided for the remote app operation invocation, such as `{"sql": "SELECT 1"}` for the `run_sql` operation. |

Expand

Show lessSee more

## Examples

Retrieve the remote app operation history for all applications in the current account:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.APPLICATION_REMOTE_OPERATION_HISTORY;
```

Retrieve the remote operation history for a specific application and specific operation type:

Copy code

```
SELECT
    *
FROM
    SNOWFLAKE.ACCOUNT_USAGE.APPLICATION_REMOTE_OPERATION_HISTORY
WHERE
    APPLICATION_NAME = 'my_app'
    AND OPERATION_TYPE = 'run_sql'
ORDER BY
    COMPLETED_ON DESC;
```
