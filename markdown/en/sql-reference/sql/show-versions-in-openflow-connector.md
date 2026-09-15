# SHOW VERSIONS IN OPENFLOW CONNECTOR

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

See also:
:   [CREATE OPENFLOW CONNECTOR](/sql-reference/sql/create-openflow-connector), [ALTER OPENFLOW CONNECTOR](/sql-reference/sql/alter-openflow-connector), [DROP OPENFLOW CONNECTOR](/sql-reference/sql/drop-openflow-connector), [SHOW OPENFLOW CONNECTOR DEFINITIONS](/sql-reference/sql/show-openflow-connector-definitions), [SHOW OPENFLOW CONNECTORS](/sql-reference/sql/show-openflow-connectors), [DESCRIBE OPENFLOW CONNECTOR](/sql-reference/sql/desc-openflow-connector)

Lists the configuration versions of a connector, including the live version if one exists.

## Syntax

Copy code

```
SHOW VERSIONS IN OPENFLOW CONNECTOR <name>
```

## Parameters

`name`
:   Specifies the identifier for the connector whose versions you want to list.

## Output

The command output provides version properties in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the version was created. |
| `name` | Version identifier, such as `VERSION$1`. |
| `alias` | Alias for the version, if one is assigned. |
| `location_uri` | Stage URI of the version contents. |
| `is_default` | Whether this version is the connector’s default version. |
| `is_live` | Whether this is the writable live version. |
| `is_first` | Whether this is the earliest version. Corresponds to the `FIRST` keyword in `ALTER OPENFLOW CONNECTOR ... SET DEFAULT_VERSION`. |
| `is_last` | Whether this is the most recent version. Corresponds to the `LAST` keyword in `ALTER OPENFLOW CONNECTOR ... SET DEFAULT_VERSION`. |
| `comment` | Comment attached to the version. |
| `source_location_uri` | Stage URI the version was created from, if it was added from a stage. |
| `git_commit_hash` | Commit hash of the version, if it came from a Git repository. |

Expand

Show lessSee more

## Example

Copy code

```
SHOW VERSIONS IN OPENFLOW CONNECTOR my_db.my_schema.my_connector;
```
