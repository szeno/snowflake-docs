# ALTER OPENFLOW CONNECTOR

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

See also:
:   [CREATE OPENFLOW CONNECTOR](/sql-reference/sql/create-openflow-connector), [DROP OPENFLOW CONNECTOR](/sql-reference/sql/drop-openflow-connector), [SHOW OPENFLOW CONNECTOR DEFINITIONS](/sql-reference/sql/show-openflow-connector-definitions), [SHOW OPENFLOW CONNECTORS](/sql-reference/sql/show-openflow-connectors), [DESCRIBE OPENFLOW CONNECTOR](/sql-reference/sql/desc-openflow-connector), [SHOW VERSIONS IN OPENFLOW CONNECTOR](/sql-reference/sql/show-versions-in-openflow-connector)

Modifies connector configuration, metadata, or operational state.

## Configuration versioning

Copy code

```
ALTER OPENFLOW CONNECTOR <name> ADD VERSION FROM '<stage_reference>'

ALTER OPENFLOW CONNECTOR <name> ADD LIVE VERSION FROM { LAST | <alias> }
  [ COMMENT = <string> ]

ALTER OPENFLOW CONNECTOR <name> COMMIT [ COMMENT = <string> ]

ALTER OPENFLOW CONNECTOR <name> ABORT

ALTER OPENFLOW CONNECTOR [ IF EXISTS ] <name> SET DEFAULT_VERSION = { FIRST | LAST | '<version>' }
```

## Parameters

`name`
:   Specifies the identifier for the connector to alter.

`IF EXISTS`
:   Alters the connector only if it exists. If the connector does not exist, the statement does nothing
    and returns a success message.

    In this section, `IF EXISTS` is supported only with `SET DEFAULT_VERSION`.
    The `ADD VERSION`, `ADD LIVE VERSION`, `COMMIT`, and `ABORT` forms do not accept it.

`ADD VERSION FROM 'stage_reference'`
:   Imports configuration from a stage reference (`@<stage>[/path/]` or `snow://...`). Creates a new
    default version and auto-promotes it—no `COMMIT` step. Connector must be **STOPPED**.

`ADD LIVE VERSION FROM { LAST | alias } [ COMMENT = string ]`
:   Creates a writable **live** version seeded from an existing version. Skip on a newly created
    connector—it already has a live version.

    `LAST` seeds from the current default version. Specify a version alias to seed from a
    specific version instead.

    `COMMENT` attaches a comment to the new live version.

`COMMIT [ COMMENT = string ]`
:   Promotes the live version to a new immutable default and removes the live version.

    `COMMENT` attaches a comment to the newly promoted version.

`ABORT`
:   Discards the live version without changing the default.

`SET DEFAULT_VERSION = { FIRST | LAST | 'version' }`
:   Sets which committed version the connector uses as its default. `FIRST` selects the earliest
    committed version, `LAST` the most recent. Specify a version identifier to select a specific version.

    The current default appears in the `default_version` column of
    [SHOW OPENFLOW CONNECTORS](/sql-reference/sql/show-openflow-connectors#label-openflow-gen2-sql-connector-show) and
    [DESCRIBE OPENFLOW CONNECTOR](/sql-reference/sql/desc-openflow-connector#label-openflow-gen2-sql-connector-describe) output.

Use [File staging commands](/sql-reference/commands-file) (`LS`, `GET`, `PUT`) on the connector’s live or
`LAST` stage paths. See [gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning).

## Operational state

Copy code

```
ALTER OPENFLOW CONNECTOR [ IF EXISTS ] <name> START

ALTER OPENFLOW CONNECTOR [ IF EXISTS ] <name> STOP

ALTER OPENFLOW CONNECTOR [ IF EXISTS ] <name> TERMINATE [ FORCE ]
```

## Parameters

`START`
:   Starts a **STOPPED** connector. Transitions through **STARTING** to **RUNNING**. Requires a
    committed default configuration.

`STOP`
:   Stops a **RUNNING** connector. Transitions through **STOPPING** to **STOPPED**.

`TERMINATE [ FORCE ]`
:   Removes the connector from the runtime. The connector must be **STOPPED** first.

    `FORCE` terminates the connector without waiting for in-flight data to drain. Use this when a
    standard `TERMINATE` can’t complete because the connector is not responding. Does not exit
    transitional states such as `STOPPING`. Data still in flight is lost.

## Metadata and stage/Git sync

Copy code

```
ALTER OPENFLOW CONNECTOR [ IF EXISTS ] <name> SET
  [ DISPLAY_NAME = <string> ]
  [ COMMENT = <string> ]

ALTER OPENFLOW CONNECTOR [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER OPENFLOW CONNECTOR <name> PUSH [ TO '<git_branch_uri>' ]
  USERNAME = <string>
  PASSWORD = <string>
  NAME = <string>
  EMAIL = <string>
  [ COMMENT = <string> ]

ALTER OPENFLOW CONNECTOR <name> PULL
```

## Parameters

`SET ...`
:   Updates connector metadata. Requires `OWNERSHIP`.

`RENAME TO new_name`
:   Renames the connector. Requires `OWNERSHIP`.

`PUSH [ TO 'git_branch_uri' ]`
:   Exports connector configuration to a Git repository stage. Requires Git credentials with write
    access.

`PULL`
:   Imports the latest configuration from the connector’s linked Git repository. Same pattern as other
    Git-backed file-based entities.

For Git-based promote workflows, see
[Create from a known configuration](/user-guide/data-integration/openflow/gen2/connector-versioning#label-openflow-fbe-git-create) in
[gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning).

## Waiting for state transitions

After `COMMIT`, `START`, `STOP`, or `TERMINATE`, poll completion with
[SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_CONNECTORS](/sql-reference/functions/system_wait_for_stable_openflow_connectors).
