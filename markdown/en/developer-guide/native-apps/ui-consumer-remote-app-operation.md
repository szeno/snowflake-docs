# Manage remote app operations

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

## About remote app operations

Remote app operations let a provider perform different types of operations on the consumer Snowflake Native App, such as running on-demand SQL statements or disabling the application.
Providers may use remote app operations to perform maintenance tasks or troubleshoot issues.
See [the provider guide](/developer-guide/native-apps/remote-app-operation) for more details.

Certain remote app operation types are *restricted*, and as a consumer, you must grant consent per-application to allow a provider to perform these restricted operations.

Currently, the supported operation types are `run_sql`, `disable`, `enable`, and `retry_upgrade`:

| Operation Type | Description | Restricted? / Consent Required? |
| --- | --- | --- |
| `run_sql` | Run a SQL statement on the application. | Yes |
| `disable` | Disable the application. | No |
| `enable` | Enable a disabled application. | No |
| `retry_upgrade` | Retry upgrading the application. | No |

Expand

Show lessSee more

See [SYSTEM$REMOTE\_APP\_OPERATION](/sql-reference/functions/system_remote_app_operation) for more information on how these operations are executed.

## Authorize restricted remote app operations

Currently, the only restricted operation type is `run_sql`.

You can grant consent 1) indefinitely, 2) temporarily, or 3) never, through the [ALTER APPLICATION](/sql-reference/sql/alter-application) or [CREATE APPLICATION](/sql-reference/sql/create-application) commands.
**By default, consent is not granted on any application.**

### Prerequisites

Before a provider can run remote app operations on an installed application, you must have an
active event table set up in your account. Both you and the provider use the event table to view the results of
the operation.

To set up an event table, see
[Set up event tracing for an app](/developer-guide/native-apps/ui-consumer-enable-logging).

Important

If event sharing is disabled for the application, the provider cannot see the results of a
`run_sql` operation. Make sure event sharing is enabled before the provider attempts a remote
app operation. For more information, see
[Enable event sharing for an app](/developer-guide/native-apps/ui-consumer-enable-logging#label-nativeapps-consumer-logging-enabling).

### Grant indefinite consent

You can grant consent indefinitely by either of the following commands:

Copy code

```
ALTER APPLICATION my_app
  SET AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL = 'INDEFINITE';
```

Copy code

```
CREATE APPLICATION my_app FROM LISTING <listing_id>
  AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL = 'INDEFINITE';
```

### Grant temporary consent

You can grant consent temporarily by specifying a timestamp:

Copy code

```
ALTER APPLICATION my_app
  SET AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL = '<timestamp>';
```

Copy code

```
CREATE APPLICATION my_app FROM LISTING <listing_id>
  AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL = '<timestamp>';
```

This value can be any valid date and time format. After the specified timestamp, the provider can no longer perform remote app operations on the application.

### Withdraw consent

You can withdraw consent at any time by any of these commands:

Copy code

```
ALTER APPLICATION my_app
  SET AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL = 'NEVER';
```

Copy code

```
ALTER APPLICATION my_app UNSET AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL;
```

Copy code

```
CREATE APPLICATION my_app FROM LISTING <listing_id>
  AUTHORIZE_RESTRICTED_PROVIDER_REMOTE_OPERATIONS_UNTIL = 'NEVER';
```

Note

Withdrawing consent prevents the provider from starting new remote operations, but a remote
operation that is already running may still run.

## Querying operation results

All remote app operation invocations are logged to the [ACCOUNT\_USAGE.APPLICATION\_REMOTE\_OPERATION\_HISTORY](/sql-reference/account-usage/application_remote_operation_history) view, with a latency of up to 1 hour.

Copy code

```
SELECT
    application_name,
    application_id,
    application_hash,
    request_id,
    operation_type,
    completed_on,
    request_status,
    request_config
FROM
    snowflake.account_usage.application_remote_operation_history
WHERE
    completed_on >= DATEADD(day, -7, CURRENT_TIMESTAMP());
```

### Event table logging

If the correct event definitions are enabled, remote app operations are also logged to the [event table](/developer-guide/native-apps/event-about). See [the provider guide](/developer-guide/native-apps/remote-app-operation#prerequisites-for-event-table-logging) for more details on the exact requirements.

For the `run_sql` operation, the event table also includes the result of the SQL statement executed in the `VALUE` column, which is not present in the [ACCOUNT\_USAGE.APPLICATION\_REMOTE\_OPERATION\_HISTORY](/sql-reference/account-usage/application_remote_operation_history) view.

Here is an example query on the event table:

Copy code

```
-- Get the latest ten invocations
SELECT timestamp,
       RECORD_ATTRIBUTES['snow.application.remote_app_operation.operation_type']::STRING AS operation_type,
       RECORD_ATTRIBUTES['snow.application.remote_app_operation.request_id']::STRING AS request_id,
       VALUE['status']::STRING     AS status,
       value
FROM   snowflake.telemetry.events
WHERE  SCOPE['name'] = 'snow.application.remote_app_operation'
AND    RECORD_ATTRIBUTES['snow.application.name'] = '<application_name>'
LIMIT  10;
```

Note

The [ACCOUNT\_USAGE.APPLICATION\_REMOTE\_OPERATION\_HISTORY](/sql-reference/account-usage/application_remote_operation_history) view is the source of truth for remote app operation invocation history. The event table should only be queried for additional information when needed, as with the `run_sql` operation.
