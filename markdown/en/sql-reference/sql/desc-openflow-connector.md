# DESCRIBE OPENFLOW CONNECTOR

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

See also:
:   [CREATE OPENFLOW CONNECTOR](/sql-reference/sql/create-openflow-connector), [ALTER OPENFLOW CONNECTOR](/sql-reference/sql/alter-openflow-connector), [DROP OPENFLOW CONNECTOR](/sql-reference/sql/drop-openflow-connector), [SHOW OPENFLOW CONNECTOR DEFINITIONS](/sql-reference/sql/show-openflow-connector-definitions), [SHOW OPENFLOW CONNECTORS](/sql-reference/sql/show-openflow-connectors), [SHOW VERSIONS IN OPENFLOW CONNECTOR](/sql-reference/sql/show-versions-in-openflow-connector)

Returns properties for a single connector, including status, runtime, connector definition, and
version state.

## Syntax

Copy code

```
DESCRIBE OPENFLOW CONNECTOR <name>
```

## Output

The command output provides connector properties in the following columns. Compared with
`SHOW OPENFLOW CONNECTORS`, the output adds the `last_version_*` columns and
`default_version_git_commit_hash`, and omits `database_name`, `schema_name`, `created_on`, and
`updated_on`. For live, default, and draft version behavior, see
[gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning).

| Column | Description |
| --- | --- |
| `name` | Connector identifier. |
| `status` | Current lifecycle state. |
| `runtime` | Parent runtime name. |
| `connector_definition` | Name of the connector definition the connector was created from, such as `OPENFLOW_POSTGRES_CDC`. |
| `display_name` | UI display name. |
| `owner` | Role that owns the connector. |
| `comment` | Comment for the connector. |
| `connector_url` | URL of the connector canvas in the Openflow UI. |
| `default_version` | Default version setting for the connector, such as `LAST`. |
| `default_version_name` | Version that `default_version` currently resolves to, such as `VERSION$4`. |
| `default_version_alias` | Alias of the default version, if one is assigned. |
| `default_version_location_uri` | Stage URI of the default version contents. |
| `default_version_source_location_uri` | Stage URI the default version was created from, if it was added from a stage. |
| `default_version_git_commit_hash` | Commit hash of the default version, if it came from a Git repository. |
| `last_version_name` | Most recent committed version, such as `VERSION$4`. |
| `last_version_alias` | Alias of the most recent version, if one is assigned. |
| `last_version_location_uri` | Stage URI of the most recent version contents. |
| `last_version_source_location_uri` | Stage URI the most recent version was created from, if it was added from a stage. |
| `last_version_git_commit_hash` | Commit hash of the most recent version, if it came from a Git repository. |
| `live_version_location_uri` | Stage URI of the writable live version. |

Expand

Show lessSee more
