# SYSTEM$WAIT\_FOR\_OPENFLOW\_DEPLOYMENT\_STATUS

Waits until each named deployment reaches one of the statuses you specify. Use this
function when you know the expected status after an `ALTER` command. When you only need
to wait until the deployment settles, use
[SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_DEPLOYMENTS](/sql-reference/functions/system_wait_for_stable_openflow_deployments) instead.

See also:
:   [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_DEPLOYMENTS](/sql-reference/functions/system_wait_for_stable_openflow_deployments), [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_RUNTIMES](/sql-reference/functions/system_wait_for_stable_openflow_runtimes), [SYSTEM$WAIT\_FOR\_OPENFLOW\_RUNTIME\_STATUS](/sql-reference/functions/system_wait_for_openflow_runtime_status), [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_CONNECTORS](/sql-reference/functions/system_wait_for_stable_openflow_connectors), [SYSTEM$WAIT\_FOR\_OPENFLOW\_CONNECTOR\_STATUS](/sql-reference/functions/system_wait_for_openflow_connector_status)

## Syntax

Copy code

```
SELECT SYSTEM$WAIT_FOR_OPENFLOW_DEPLOYMENT_STATUS(
  <timeout_seconds>,
  '<allowed_statuses>',
  '<deployment_name>' [ , '<deployment_name>' ... ]
);
```

## Arguments

`timeout_seconds`
:   Maximum time to wait, in seconds.

`'allowed_statuses'`
:   Comma-separated list of acceptable statuses, for example `'ACTIVE'`.

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
- Deployment provisioning typically takes 5–10 minutes. A timeout of 600 seconds (10 minutes) is a
  reasonable default for initial provisioning.
- If the function times out, the underlying provisioning continues. Re-run the wait function with a
  fresh timeout. Do not re-issue `CREATE OPENFLOW DEPLOYMENT`: the deployment already exists and is
  still provisioning.

## Examples

Wait for a deployment to become `ACTIVE`:

Copy code

```
SELECT SYSTEM$WAIT_FOR_OPENFLOW_DEPLOYMENT_STATUS(600, 'ACTIVE', 'my_deployment');
```
