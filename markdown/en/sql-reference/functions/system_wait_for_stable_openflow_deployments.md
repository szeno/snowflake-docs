# SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_DEPLOYMENTS

Waits until each named deployment leaves a transitional state. Gen 2 Openflow commands
that change deployment state run asynchronously, so call this function after an `ALTER`
command when a script must not continue until the change has settled. This is the
recommended default for automation.

See also:
:   [SYSTEM$WAIT\_FOR\_OPENFLOW\_DEPLOYMENT\_STATUS](/sql-reference/functions/system_wait_for_openflow_deployment_status), [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_RUNTIMES](/sql-reference/functions/system_wait_for_stable_openflow_runtimes), [SYSTEM$WAIT\_FOR\_OPENFLOW\_RUNTIME\_STATUS](/sql-reference/functions/system_wait_for_openflow_runtime_status), [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_CONNECTORS](/sql-reference/functions/system_wait_for_stable_openflow_connectors), [SYSTEM$WAIT\_FOR\_OPENFLOW\_CONNECTOR\_STATUS](/sql-reference/functions/system_wait_for_openflow_connector_status)

## Syntax

Copy code

```
SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_DEPLOYMENTS(
  <timeout_seconds>,
  '<deployment_name>' [ , '<deployment_name>' ... ]
);
```

## Arguments

`timeout_seconds`
:   Maximum time to wait, in seconds.

`'deployment_name'`
:   One or more deployment names. Deployments use a simple name. With `USE DATABASE` and `USE SCHEMA`
    set, a simple name resolves in the current session.

## Returns

Returns `'OK'` on success. Raises an error if the timeout elapses or if a
deployment enters a failed state.

## Access control

Requires any privilege on the named deployment.

## Usage notes

- The Openflow UI performs equivalent polling internally.
- If the function times out, the underlying operation continues. Re-run the wait function with a
  fresh timeout. Do not re-issue the original command.

## Examples

Wait for a deployment to reach a stable state:

Copy code

```
SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_DEPLOYMENTS(600, 'my_deployment');
```
