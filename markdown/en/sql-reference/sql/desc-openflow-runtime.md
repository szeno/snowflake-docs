# DESCRIBE OPENFLOW RUNTIME

See also:
:   [CREATE OPENFLOW RUNTIME](/sql-reference/sql/create-openflow-runtime), [ALTER OPENFLOW RUNTIME](/sql-reference/sql/alter-openflow-runtime), [DROP OPENFLOW RUNTIME](/sql-reference/sql/drop-openflow-runtime), [SHOW OPENFLOW RUNTIMES](/sql-reference/sql/show-openflow-runtimes)

Returns properties for a single runtime.

## Syntax

Copy code

```
DESCRIBE OPENFLOW RUNTIME <name>
```

## Output

The command output provides runtime properties in the following columns:

| Column | Description |
| --- | --- |
| `name` | Runtime identifier. |
| `status` | Current lifecycle state. |
| `deployment` | Parent deployment name. |
| `min_nodes` | Minimum autoscaling bound. |
| `max_nodes` | Maximum autoscaling bound. |
| `node_type` | `SMALL`, `MEDIUM`, or `LARGE`. The node type, set at creation. |
| `display_name` | UI display name. |
| `external_access_integrations` | External access integration names (Snowflake deployments). |
| `initially_suspended` | Whether the runtime was created in a suspended state. |
| `execute_as_role` | Execute-as role bound to the runtime. Connectors that use `SNOWFLAKE_MANAGED` authentication run with this role’s privileges. |
| `key` | Internal identifier for the runtime. |
| `owner` | Role that owns the runtime. |
| `comment` | Comment for the runtime. |
| `server_url` | URL of the runtime’s Openflow canvas. |
| `node_type_tier` | Current instance tier. One of: `S1`, `S2`, `S3` (SMALL node type), `M4`, `M6` (MEDIUM node type), `L8` (LARGE node type). |

Expand

Show lessSee more
