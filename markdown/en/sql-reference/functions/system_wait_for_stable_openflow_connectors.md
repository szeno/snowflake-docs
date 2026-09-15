# SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_CONNECTORS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Waits until each named connector leaves a transitional state. Gen 2 Openflow commands
that change connector state run asynchronously, so call this function after an `ALTER`
command when a script must not continue until the change has settled. This is the
recommended default for automation.

See also:
:   [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_DEPLOYMENTS](/sql-reference/functions/system_wait_for_stable_openflow_deployments), [SYSTEM$WAIT\_FOR\_OPENFLOW\_DEPLOYMENT\_STATUS](/sql-reference/functions/system_wait_for_openflow_deployment_status), [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_RUNTIMES](/sql-reference/functions/system_wait_for_stable_openflow_runtimes), [SYSTEM$WAIT\_FOR\_OPENFLOW\_RUNTIME\_STATUS](/sql-reference/functions/system_wait_for_openflow_runtime_status), [SYSTEM$WAIT\_FOR\_OPENFLOW\_CONNECTOR\_STATUS](/sql-reference/functions/system_wait_for_openflow_connector_status)

## Syntax

Copy code

```
SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_CONNECTORS(
  <timeout_seconds>,
  '<connector_name>' [ , '<connector_name>' ... ]
);
```

## Arguments

`timeout_seconds`
:   Maximum time to wait, in seconds.

`'connector_name'`
:   One or more connector names. Use the fully qualified name `<database>.<schema>.<name>`. With `USE DATABASE` and `USE SCHEMA`
    set, a simple name resolves in the current session.

## Returns

Returns `'OK'` on success. Raises an error if the timeout elapses or if a
connector enters a failed state.

## Access control

Requires any privilege on the named connector.

## Usage notes

- The Openflow UI performs equivalent polling internally.
- If the function times out, the underlying operation continues. Re-run the wait function with a
  fresh timeout.

## Examples

Wait for a connector to start:

Copy code

```
ALTER OPENFLOW CONNECTOR my_db.my_schema.my_connector START;

SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_CONNECTORS(600, 'my_db.my_schema.my_connector');
```

Wait for a configuration commit to complete:

Copy code

```
ALTER OPENFLOW CONNECTOR my_db.my_schema.my_connector COMMIT;

SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_CONNECTORS(600, 'my_db.my_schema.my_connector');
```

Wait for termination before dropping the connector:

Copy code

```
ALTER OPENFLOW CONNECTOR my_db.my_schema.my_connector TERMINATE;

SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_CONNECTORS(600, 'my_db.my_schema.my_connector');

DROP OPENFLOW CONNECTOR my_db.my_schema.my_connector;
```
