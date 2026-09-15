[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Categories:
:   [System functions](/sql-reference/functions-system) (Control)

# SYSTEM$REMOTE\_APP\_OPERATION

Performs a [remote app operation](/developer-guide/native-apps/remote-app-operation) on a Snowflake Native App. This function is available only to providers.

## Syntax

Copy code

```
SYSTEM$REMOTE_APP_OPERATION(
  '<operation_type>',
  '<package_name>',
  '<application_hash>'
  [, '<configuration>' ]
)
```

## Arguments

**Required**

`'operation_type'`
:   The type of remote operation to perform. Possible values: `run_sql`, `enable`, `disable`, `retry_upgrade`.

`'package_name'`
:   The name of the application package associated with the Snowflake Native App.

`'application_hash'`
:   The hash value of the application. You can find this value in the [APPLICATION\_STATE view](/sql-reference/data-sharing-usage/application-state-view) or by calling
    [SYSTEM$GET\_HASH\_FOR\_APPLICATION](/sql-reference/functions/system_get_hash_for_application).

`'configuration'`
:   A JSON string that contains configuration fields for the operation. Required for the `run_sql` and `disable` operation types.

## Returns

Returns a JSON string containing a request ID that you can use to track the result of the operation in the event table.

Copy code

```
{"request_id": "<uuid>"}
```

## Operation type: `run_sql`

The `run_sql` operation runs a SQL statement on the consumer application.
Read the [remote app operation guide](/developer-guide/native-apps/remote-app-operation) for more details.

For the `configuration` argument, pass a JSON string that includes a `sql` key whose value is the SQL statement to run. For example:

Copy code

```
SELECT SYSTEM$REMOTE_APP_OPERATION(
  'run_sql',
  'package_name',
  'application_hash',
  '{"sql": "SELECT * FROM example_schema.example_table"}'
);
```

Only one SQL statement can be run at a time. Providing multiple SQL statements (for example, `{"sql": "SELECT 1; SELECT 2"}`) fails.

## Operation type: `disable`

The `disable` operation disables the consumer Snowflake Native App. Read the [remote app operation guide](/developer-guide/native-apps/remote-app-operation) for more details.
For the `configuration` argument, pass a JSON string that includes a `reason` key whose value is the reason for disabling the Snowflake Native App. For example:

Copy code

```
SELECT SYSTEM$REMOTE_APP_OPERATION(
  'disable',
  'package_name',
  'application_hash',
  '{"reason": "Application needs to be disabled for maintenance"}'
);
```

## Operation type: `enable`

The `enable` operation enables a consumer Snowflake Native App that has been disabled by the `disable` operation. For example:

Copy code

```
SELECT SYSTEM$REMOTE_APP_OPERATION(
  'enable',
  'package_name',
  'application_hash'
);
```

Note

This operation can only enable applications that have been disabled by the provider. If an application was disabled by Snowflake, see [What to do if an app is unavailable](/developer-guide/native-apps/ui-consumer-managing-applications#what-to-do-if-an-app-is-unavailable).

## Operation type: `retry_upgrade`

The `retry_upgrade` operation retries the upgrade of a consumer Snowflake Native App. It is non-blocking. For example:

Copy code

```
SELECT SYSTEM$REMOTE_APP_OPERATION(
  'retry_upgrade',
  'package_name',
  'application_hash'
);
```
