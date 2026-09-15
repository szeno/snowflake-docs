# SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_RUNTIMES

Waits until each named runtime leaves a transitional state. Gen 2 Openflow commands
that change runtime state run asynchronously, so call this function after an `ALTER`
command when a script must not continue until the change has settled. This is the
recommended default for automation.

See also:
:   [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_DEPLOYMENTS](/sql-reference/functions/system_wait_for_stable_openflow_deployments), [SYSTEM$WAIT\_FOR\_OPENFLOW\_DEPLOYMENT\_STATUS](/sql-reference/functions/system_wait_for_openflow_deployment_status), [SYSTEM$WAIT\_FOR\_OPENFLOW\_RUNTIME\_STATUS](/sql-reference/functions/system_wait_for_openflow_runtime_status), [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_CONNECTORS](/sql-reference/functions/system_wait_for_stable_openflow_connectors), [SYSTEM$WAIT\_FOR\_OPENFLOW\_CONNECTOR\_STATUS](/sql-reference/functions/system_wait_for_openflow_connector_status)

## Syntax

Copy code

```
SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_RUNTIMES(
  <timeout_seconds>,
  '<runtime_name>' [ , '<runtime_name>' ... ]
);
```

## Arguments

`timeout_seconds`
:   Maximum time to wait, in seconds.

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
- If the function times out, the underlying operation continues. Re-run the wait function with a
  fresh timeout. Do not re-issue the original command.

## Examples

Suspend, terminate, and drop a runtime, waiting at each step:

Copy code

```
ALTER OPENFLOW RUNTIME my_db.my_schema.my_runtime SUSPEND;
SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_RUNTIMES(600, 'my_db.my_schema.my_runtime');

ALTER OPENFLOW RUNTIME my_db.my_schema.my_runtime TERMINATE;
SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_RUNTIMES(600, 'my_db.my_schema.my_runtime');

DROP OPENFLOW RUNTIME my_db.my_schema.my_runtime;
```
