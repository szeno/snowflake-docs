# Use remote app operations

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

## About remote app operations

Remote app operations let a provider perform different types of operations on the consumer Snowflake Native App, such as running on-demand SQL statements for troubleshooting or disabling the application.

Currently, the supported operation types are `run_sql`, `disable`, `enable`, and `retry_upgrade`:

| Operation Type | Description | Consent Required? |
| --- | --- | --- |
| `run_sql` | Run a SQL statement on the application. | Yes |
| `disable` | Disable the application. | No |
| `enable` | Enable a disabled application. | No |
| `retry_upgrade` | Retry upgrading the application. | No |

Expand

Show lessSee more

## Prerequisites

Before you can use remote app operations, you need the following:

- Some remote app operations require the consumer to grant consent. See [the consumer guide](/developer-guide/native-apps/ui-consumer-remote-app-operation) for more details.
- The hash value of the application. You can find this value in the [APPLICATION\_STATE view](/sql-reference/data-sharing-usage/application-state-view) or by calling
  [SYSTEM$GET\_HASH\_FOR\_APPLICATION](/sql-reference/functions/system_get_hash_for_application).

### Prerequisites for event table logging

Remote app operation invocations are logged to the event table if the following prerequisites are met:

- Events with `RECORD_TYPE='EVENT'` must be enabled through event definitions, for example, `SNOWFLAKE$ALL` or `SNOWFLAKE$ALL_EVENTS`.
- The [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level) property must be set to `INFO` or lower.

You can set up the required configuration in the app manifest file. See [Configure event definitions for an app](/developer-guide/native-apps/event-definition) for more details.

## Operation type: `run_sql`

**Consumer consent required?** Yes.

To run a SQL statement on a Snowflake Native App, call the
[SYSTEM$REMOTE\_APP\_OPERATION](/sql-reference/functions/system_remote_app_operation) function
with the `run_sql` operation type. For example:

Copy code

```
SELECT SYSTEM$REMOTE_APP_OPERATION(
  'run_sql',
  'package_name',
  'application_hash',
  '{"sql": "SELECT * FROM app_schema.app_table"}'
);
```

This function call executes `SELECT * FROM app_schema.app_table` as the application.

The system function returns a JSON string `{"request_id": "<uuid>"}`. This `request_id` can be used to query the result of the operation in the event table. See the [Querying operation results](#querying-operation-results) section below for more details.

### Reading the result of the SQL statement

The execution of the SQL statement is logged in the event table, with information on the status, query result, and execution time.
See the [Querying operation results](#querying-operation-results) section below for more details.

## Operation type: `disable`

**Consumer consent required?** No.

To disable a Snowflake Native App, call the
[SYSTEM$REMOTE\_APP\_OPERATION](/sql-reference/functions/system_remote_app_operation) function
with the `disable` operation type. For example:

Copy code

```
SELECT SYSTEM$REMOTE_APP_OPERATION(
  'disable',
  'package_name',
  'application_hash',
  '{"reason": "Application needs to be disabled for maintenance"}'
);
```

The `reason` specified will be visible to the consumer as the application’s disablement reason, for instance in `DESCRIBE APPLICATION`.

The system function returns a JSON string `{"request_id": "<uuid>"}`. This `request_id` can be used to query the result of the operation in the event table. See the [Querying operation results](#querying-operation-results) section below for more details.

## Operation type: `enable`

**Consumer consent required?** No.

To re-enable a Snowflake Native App that you previously disabled, call the
[SYSTEM$REMOTE\_APP\_OPERATION](/sql-reference/functions/system_remote_app_operation) function
with the `enable` operation type. For example:

Copy code

```
SELECT SYSTEM$REMOTE_APP_OPERATION(
  'enable',
  'package_name',
  'application_hash'
);
```

Note

This operation can only enable applications that have been disabled by the provider.
If an application was disabled by Snowflake, see [What to do if an app is unavailable](/developer-guide/native-apps/ui-consumer-managing-applications#what-to-do-if-an-app-is-unavailable).

The system function returns a JSON string `{"request_id": "<uuid>"}`. This `request_id` can be used to query the result of the operation in the event table. See the [Querying operation results](#querying-operation-results) section below for more details.

## Operation type: `retry_upgrade`

**Consumer consent required?** No.

To retry a failed upgrade on a Snowflake Native App, call the
[SYSTEM$REMOTE\_APP\_OPERATION](/sql-reference/functions/system_remote_app_operation) function
with the `retry_upgrade` operation type. This operation is non-blocking. For example:

Copy code

```
SELECT SYSTEM$REMOTE_APP_OPERATION(
  'retry_upgrade',
  'package_name',
  'application_hash'
);
```

The system function returns a JSON string `{"request_id": "<uuid>"}`. This `request_id` can be used to query the result of the operation in the event table. See the [Querying operation results](#querying-operation-results) section below for more details.

## Querying operation results

Whenever `SYSTEM$REMOTE_APP_OPERATION` is called and modifies the consumer Snowflake Native App, the operation is logged in the [event table](/developer-guide/native-apps/event-about) for the consumer to view.

If event sharing is enabled, the provider can also query the operation results from the event table. Each successful `SYSTEM$REMOTE_APP_OPERATION` call returns a JSON string `{"request_id": "<uuid>"}`. Use this `request_id` to query the status and result of the operation in the event table.

Note

If `SYSTEM$REMOTE_APP_OPERATION` fails due to a syntax error or incorrect arguments (for example, the `enable` operation is called on an enabled application), the function call is *not* logged to the event table.

Here are example queries to get started:

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
AND    RECORD_ATTRIBUTES['snow.application.hash'] = '<application_hash>'
LIMIT  10;
```

Copy code

```
-- Query a specific invocation
SELECT PARSE_JSON(VALUE['result'])
FROM   snowflake.telemetry.events
WHERE  SCOPE['name'] = 'snow.application.remote_app_operation'
AND    RECORD_ATTRIBUTES['snow.application.remote_app_operation.request_id'] = '<request_id>';
```
