# CREATE OPENFLOW RUNTIME

See also:
:   [ALTER OPENFLOW RUNTIME](/sql-reference/sql/alter-openflow-runtime), [DROP OPENFLOW RUNTIME](/sql-reference/sql/drop-openflow-runtime), [SHOW OPENFLOW RUNTIMES](/sql-reference/sql/show-openflow-runtimes), [DESCRIBE OPENFLOW RUNTIME](/sql-reference/sql/desc-openflow-runtime)

Creates a runtime in a gen 2 deployment.

## Syntax

Copy code

```
CREATE OPENFLOW RUNTIME [ IF NOT EXISTS ] [ <database>.<schema>. ]<name>
  IN DEPLOYMENT <deployment_name>
  NODE_TYPE = { SMALL | MEDIUM | LARGE }
  [ NODE_TYPE_TIER = { 'S1' | 'S2' | 'S3' | 'M4' | 'M6' | 'L8' } ]
  MIN_NODES = <integer>
  MAX_NODES = <integer>
  EXECUTE_AS_ROLE = <role>
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <eai> [ , <eai> ... ] ) ]
  [ DISPLAY_NAME = <string> ]
  [ COMMENT = <string> ]
```

## Required parameters

`[ database.schema. ]name`
:   Specifies the identifier for the runtime. Use a fully qualified name or omit `database.schema` to
    use the session default. For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`IN DEPLOYMENT deployment_name`
:   Gen 2 deployment that hosts this runtime.

`NODE_TYPE = { SMALL | MEDIUM | LARGE }`
:   Node type. Cannot be changed after creation. Use `NODE_TYPE_TIER` to resize
    within the same node type after creation.

`MIN_NODES = integer`
:   Minimum number of nodes (1–50).

`MAX_NODES = integer`
:   Maximum number of nodes (1–50).

`EXECUTE_AS_ROLE = role`
:   Role connectors use when reading from and writing to Snowflake. See
    [Create an execute-as role](/user-guide/data-integration/openflow/gen2/quickstart#label-openflow-gen2-quickstart-execute-as-role).

## Optional parameters

`NODE_TYPE_TIER = { S1 | S2 | S3 | M4 | M6 | L8 }`
:   Instance tier within the node type. The tier determines the CPU and heap memory
    available to each node. The tier must match the `NODE_TYPE` value:
    `S1`, `S2`, and `S3` require `NODE_TYPE = SMALL`; `M4` and `M6` require
    `NODE_TYPE = MEDIUM`; `L8` requires `NODE_TYPE = LARGE`.

    | Tier | Node type | CPUs per node | Heap per node |
    | --- | --- | --- | --- |
    | `S1` | SMALL | 1 | 4 GB |
    | `S2` | SMALL | 2 | 8 GB |
    | `S3` | SMALL | 3 | 12 GB |
    | `M4` | MEDIUM | 4 | 16 GB |
    | `M6` | MEDIUM | 6 | 24 GB |
    | `L8` | LARGE | 8 | 33 GB |

    Expand

    Show lessSee more

    You can change the tier within the same node type after creation using
    [ALTER OPENFLOW RUNTIME … SET NODE\_TYPE\_TIER](/sql-reference/sql/alter-openflow-runtime).

    Default: `S1` for `SMALL`, `M4` for `MEDIUM`, `L8` for `LARGE`.

`IF NOT EXISTS`
:   Creates the runtime only if it does not already exist. If the runtime already exists, the statement
    does nothing and returns a success message.

`EXTERNAL_ACCESS_INTEGRATIONS = ( eai [ , ... ] )`
:   Snowflake deployments only. External access integrations that allow egress to external data sources.

    Default: No value

`DISPLAY_NAME = string`
:   UI display name. If unset, the SQL `name` is shown in the Openflow UI.

    Default: No value

`COMMENT = string`
:   Default: No value

## Access control

Requires `USAGE` on the containing database, `CREATE OPENFLOW RUNTIME` on the target schema (or
schema ownership), and `USAGE` on the parent deployment.

## Usage notes

- This command returns immediately. Runtime provisioning runs asynchronously and typically takes
  3–5 minutes. Use
  [SYSTEM$WAIT\_FOR\_OPENFLOW\_RUNTIME\_STATUS](/sql-reference/functions/system_wait_for_openflow_runtime_status)
  or
  [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_RUNTIMES](/sql-reference/functions/system_wait_for_stable_openflow_runtimes)
  to wait for the runtime to become `ACTIVE`.
- The optimal node count depends on your connector type and workload. See the setup topic for
  your connector for recommended values.

## Example

Copy code

```
CREATE OPENFLOW RUNTIME my_db.my_schema.my_runtime
  IN DEPLOYMENT my_deployment
  NODE_TYPE = MEDIUM
  NODE_TYPE_TIER = 'M4'
  MIN_NODES = 1
  MAX_NODES = 1
  EXECUTE_AS_ROLE = OPENFLOW_MY_RUNTIME_EXECUTE_AS_RL
  DISPLAY_NAME = 'My Runtime';
```
