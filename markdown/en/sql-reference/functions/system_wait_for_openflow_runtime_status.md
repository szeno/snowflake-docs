# SYSTEM$WAIT\_FOR\_OPENFLOW\_RUNTIME\_STATUS

Waits until each named runtime reaches one of the statuses you specify. Use this
function when you know the expected status after an `ALTER` command. When you only need
to wait until the runtime settles, use
[SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_RUNTIMES](/sql-reference/functions/system_wait_for_stable_openflow_runtimes) instead.

See also:
:   [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_DEPLOYMENTS](/sql-reference/functions/system_wait_for_stable_openflow_deployments), [SYSTEM$WAIT\_FOR\_OPENFLOW\_DEPLOYMENT\_STATUS](/sql-reference/functions/system_wait_for_openflow_deployment_status), [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_RUNTIMES](/sql-reference/functions/system_wait_for_stable_openflow_runtimes), [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_CONNECTORS](/sql-reference/functions/system_wait_for_stable_openflow_connectors), [SYSTEM$WAIT\_FOR\_OPENFLOW\_CONNECTOR\_STATUS](/sql-reference/functions/system_wait_for_openflow_connector_status)

## Syntax

Copy code

```
SELECT SYSTEM$WAIT_FOR_OPENFLOW_RUNTIME_STATUS(
  <timeout_seconds>,
  '<allowed_statuses>',
  '<runtime_name>' [ , '<runtime_name>' ... ]
);
```

## Arguments

`timeout_seconds`
:   Maximum time to wait, in seconds.

`'allowed_statuses'`
:   Comma-separated list of acceptable statuses, for example `'ACTIVE'` or `'ACTIVE,SUSPENDED'`.

`'runtime_name'`
:   One or more runtime names. Use the fully qualified name `<database>.<schema>.<name>`. With `USE DATABASE` and `USE SCHEMA`
    set, a simple name resolves in the current session.

## Returns

Returns `'OK'` on success. Raises an error if the timeout elapses or if a
runtime enters a failed state.

## Access control

Requires any privilege on the named runtime.

## Usage notes

- The Openflow UI performs equivalent polling internally.
- Runtime provisioning typically takes 3–5 minutes. A timeout of 600 seconds is a reasonable default.
- If the function times out, the underlying operation continues. Re-run the wait function with a fresh
  timeout. Do not re-issue `CREATE OPENFLOW RUNTIME`: the runtime already exists and is still
  provisioning.

## Examples

Wait for a runtime to become `SUSPENDED` after suspending it:

Copy code

```
ALTER OPENFLOW RUNTIME my_db.my_schema.my_runtime SUSPEND;

SELECT SYSTEM$WAIT_FOR_OPENFLOW_RUNTIME_STATUS(600, 'SUSPENDED', 'my_db.my_schema.my_runtime');
```
