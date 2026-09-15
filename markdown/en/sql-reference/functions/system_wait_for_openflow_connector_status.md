# SYSTEM$WAIT\_FOR\_OPENFLOW\_CONNECTOR\_STATUS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Waits until each named connector reaches one of the statuses you specify. Use this
function when you know the expected status after an `ALTER` command. When you only need
to wait until the connector settles, use
[SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_CONNECTORS](/sql-reference/functions/system_wait_for_stable_openflow_connectors) instead.

See also:
:   [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_DEPLOYMENTS](/sql-reference/functions/system_wait_for_stable_openflow_deployments), [SYSTEM$WAIT\_FOR\_OPENFLOW\_DEPLOYMENT\_STATUS](/sql-reference/functions/system_wait_for_openflow_deployment_status), [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_RUNTIMES](/sql-reference/functions/system_wait_for_stable_openflow_runtimes), [SYSTEM$WAIT\_FOR\_OPENFLOW\_RUNTIME\_STATUS](/sql-reference/functions/system_wait_for_openflow_runtime_status), [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_CONNECTORS](/sql-reference/functions/system_wait_for_stable_openflow_connectors)

## Syntax

Copy code

```
SELECT SYSTEM$WAIT_FOR_OPENFLOW_CONNECTOR_STATUS(
  <timeout_seconds>,
  '<allowed_statuses>',
  '<connector_name>' [ , '<connector_name>' ... ]
);
```

## Arguments

`timeout_seconds`
:   Maximum time to wait, in seconds.

`'allowed_statuses'`
:   Comma-separated list of acceptable statuses, for example `'RUNNING'` or `'RUNNING,STOPPED'`.

`'connector_name'`
:   One or more connector names. Use the fully qualified name `<database>.<schema>.<name>`. With `USE DATABASE` and `USE SCHEMA`
    set, a simple name resolves in the current session.

Common status values for connectors:

- `STOPPED` — after `STOP` or `COMMIT`
- `RUNNING` — after `START`
- `TERMINATED` — after `TERMINATE`

## Returns

Returns `'OK'` on success. Raises an error if the timeout elapses or if a
connector enters a failed state.

## Access control

Requires any privilege on the named connector.

## Usage notes

- The Openflow UI performs equivalent polling internally.
- Connector startup typically takes 1–3 minutes. A timeout of 300 seconds is a reasonable default.
- If the function times out, the underlying operation continues. Re-run the wait function with a
  fresh timeout.

## Examples

Wait for a connector to reach `RUNNING` after starting it:

Copy code

```
ALTER OPENFLOW CONNECTOR my_db.my_schema.my_connector START;

SELECT SYSTEM$WAIT_FOR_OPENFLOW_CONNECTOR_STATUS(
  600,
  'RUNNING',
  'my_db.my_schema.my_connector'
);
```
