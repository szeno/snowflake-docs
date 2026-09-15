# ALTER OPENFLOW RUNTIME

See also:
:   [CREATE OPENFLOW RUNTIME](/sql-reference/sql/create-openflow-runtime), [DROP OPENFLOW RUNTIME](/sql-reference/sql/drop-openflow-runtime), [SHOW OPENFLOW RUNTIMES](/sql-reference/sql/show-openflow-runtimes), [DESCRIBE OPENFLOW RUNTIME](/sql-reference/sql/desc-openflow-runtime)

Modifies properties or changes the state of a gen 2 runtime.

## Syntax

Copy code

```
ALTER OPENFLOW RUNTIME [ IF EXISTS ] <name> SET
  [ DISPLAY_NAME = <string> ]
  [ MIN_NODES = <integer> ]
  [ MAX_NODES = <integer> ]
  [ NODE_TYPE_TIER = { 'S1' | 'S2' | 'S3' | 'M4' | 'M6' | 'L8' } ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <eai> [ , <eai> ... ] ) ]
  [ EXECUTE_AS_ROLE = <role> ]
  [ COMMENT = <string> ]

ALTER OPENFLOW RUNTIME [ IF EXISTS ] <name> UNSET
  { DISPLAY_NAME | EXTERNAL_ACCESS_INTEGRATIONS | COMMENT } [ , ... ]

ALTER OPENFLOW RUNTIME [ IF EXISTS ] <name> ADD EXTERNAL_ACCESS_INTEGRATIONS = ( <eai> [ , ... ] )

ALTER OPENFLOW RUNTIME [ IF EXISTS ] <name> REMOVE EXTERNAL_ACCESS_INTEGRATIONS = ( <eai> [ , ... ] )

ALTER OPENFLOW RUNTIME [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER OPENFLOW RUNTIME [ IF EXISTS ] <name> UPGRADE [ RECOVERY | FORCE ]

ALTER OPENFLOW RUNTIME [ IF EXISTS ] <name> SUSPEND

ALTER OPENFLOW RUNTIME [ IF EXISTS ] <name> RESUME [ RECOVERY ]

ALTER OPENFLOW RUNTIME [ IF EXISTS ] <name> RESTART [ RECOVERY ]

ALTER OPENFLOW RUNTIME [ IF EXISTS ] <name> TERMINATE [ CASCADE ]
```

## Parameters

`name`
:   Specifies the identifier for the runtime to alter.

`IF EXISTS`
:   Alters the runtime only if it exists. If the runtime does not exist, the statement does nothing and
    returns a success message.

`SET ...`
:   Updates runtime properties. `NODE_TYPE` (SMALL, MEDIUM, or LARGE) cannot
    be changed. Use `NODE_TYPE_TIER` to resize within the same node type. Requires `OWNERSHIP`.

`SET NODE_TYPE_TIER = { S1 | S2 | S3 | M4 | M6 | L8 }`
:   Resizes the runtime to a different tier within its current node type. `S1`,
    `S2`, and `S3` are all SMALL node type; `M4` and `M6` are both MEDIUM node type; `L8`
    is the only LARGE tier. Resizing is bidirectional within the node type. You cannot
    change the node type (SMALL, MEDIUM, or LARGE) with `ALTER`; to change the node type,
    migrate the connector to a new runtime of the target node type. Requires `OWNERSHIP`.

    Example:

    Copy code

    ```
    ALTER OPENFLOW RUNTIME my_runtime SET NODE_TYPE_TIER = 'S2';
    ```

`UNSET ...`
:   Removes runtime properties. Requires `OWNERSHIP`.

`ADD EXTERNAL_ACCESS_INTEGRATIONS = ( eai [ , ... ] )`
:   Adds external access integrations to the runtime. Requires `OWNERSHIP`.

`REMOVE EXTERNAL_ACCESS_INTEGRATIONS = ( eai [ , ... ] )`
:   Removes external access integrations from the runtime. Requires `OWNERSHIP`.

`RENAME TO new_name`
:   Renames the runtime. Requires `OWNERSHIP` and `CREATE OPENFLOW RUNTIME`.

`UPGRADE [ RECOVERY | FORCE ]`
:   Upgrades to the latest runtime version. Do not upgrade a runtime while its parent deployment is
    upgrading. Requires `OPERATE`.

    `RECOVERY` upgrades the runtime in recovery mode. Use this when a runtime is in a failed state and a
    standard upgrade can’t proceed.

    `FORCE` upgrades the runtime even when preflight checks would otherwise block the operation. Use
    this only when a standard upgrade fails and you’ve confirmed the runtime can safely be upgraded.

`SUSPEND`
:   Suspends the runtime. Requires `OPERATE`.

`{ RESUME | RESTART } [ RECOVERY ]`
:   Changes runtime power state. Requires `OPERATE`.

    `RECOVERY` resumes or restarts the runtime in recovery mode, which starts the runtime without
    starting its flows. Use recovery mode to regain access to a runtime whose flows prevent it from
    starting normally.

`TERMINATE [ CASCADE ]`
:   Irreversibly destroys the runtime. Requires `OWNERSHIP`.

    If the runtime contains connectors, plain `TERMINATE` fails. Use `TERMINATE CASCADE` to terminate
    all connectors in the runtime first, then terminate the runtime. `TERMINATE CASCADE` is not allowed
    while the parent deployment is not `ACTIVE`, or while any connector is in a transitional state.

## Usage notes

- Gen 2 runtime deletion: suspend → terminate → drop (UI or SQL). To terminate connectors and the
  runtime in one step from SQL, use `ALTER OPENFLOW RUNTIME … TERMINATE CASCADE` after suspend. See [Runtime deletion workflow](/user-guide/data-integration/openflow/gen2/openflow-generations#label-openflow-generations-runtime-deletion) in [Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations). In the UI,
  **Delete** corresponds to `ALTER ... TERMINATE`; **Drop** corresponds to `DROP OPENFLOW RUNTIME`.
- `ALTER` is not permitted when the runtime is in `CREATING`, `CREATE_FAILED`, `TERMINATING`,
  or `TERMINATED` state.
- Users need `USAGE`, `OPERATE`, or `MONITOR` on the runtime, and `USAGE` on its database
  and schema, to access it.
