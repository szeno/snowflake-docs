# CREATE OPENFLOW CONNECTOR

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

See also:
:   [ALTER OPENFLOW CONNECTOR](/sql-reference/sql/alter-openflow-connector), [DROP OPENFLOW CONNECTOR](/sql-reference/sql/drop-openflow-connector), [SHOW OPENFLOW CONNECTOR DEFINITIONS](/sql-reference/sql/show-openflow-connector-definitions), [SHOW OPENFLOW CONNECTORS](/sql-reference/sql/show-openflow-connectors), [DESCRIBE OPENFLOW CONNECTOR](/sql-reference/sql/desc-openflow-connector), [SHOW VERSIONS IN OPENFLOW CONNECTOR](/sql-reference/sql/show-versions-in-openflow-connector)

Creates a connector in a gen 2 runtime.

## Syntax

Copy code

```
CREATE OPENFLOW CONNECTOR [ IF NOT EXISTS ] <name>
  IN RUNTIME <runtime_name>
  FROM DEFINITION <connector_definition_id>
  [ DISPLAY_NAME = <string> ]
  [ COMMENT = <string> ]

CREATE OPENFLOW CONNECTOR [ IF NOT EXISTS ] <name>
  IN RUNTIME <runtime_name>
  FROM '<stage_reference>'
  [ COMMENT = <string> ]
```

## Required parameters

`name`
:   Specifies the identifier for the connector within the runtime’s schema. For more information, see
    [Identifier requirements](/sql-reference/identifiers-syntax).

`IN RUNTIME runtime_name`
:   Gen 2 runtime that hosts the connector. Simple name or fully qualified name
    (`<database>.<schema>.<runtime_name>`).

Exactly one of the following source parameters is required:

`FROM DEFINITION connector_definition_id`
:   Catalog definition ID for the connector type (for example, `OPENFLOW_POSTGRES_CDC`). List available
    IDs with `SHOW OPENFLOW CONNECTOR DEFINITIONS`. Mutually exclusive with `FROM '<stage_reference>'`.
    Creates a **live** configuration version; the connector starts without a committed default version
    until you commit.

`FROM 'stage_reference'`
:   Complete configuration bundle on any stage reference—a Git repository stage (`@my_git_repo/...`),
    an internal named stage, or another connector’s stage (`snow://openflow_connector/...`). Path within
    the stage is optional. Mutually exclusive with `FROM DEFINITION`. Creates a **default** version;
    the connector can start immediately without committing. See
    [Create from a known configuration](/user-guide/data-integration/openflow/gen2/connector-versioning#label-openflow-fbe-git-create) in
    [gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning).

## Optional parameters

`IF NOT EXISTS`
:   Creates a connector only if it does not already exist. If the connector already exists, the
    statement does nothing and returns a success message.

`DISPLAY_NAME = string`
:   UI display name.

    Default: No value

`COMMENT = string`
:   Default: No value

## Access control

Requires `CREATE OPENFLOW CONNECTOR` on the schema and `USAGE` on the runtime.

## Examples

From definition:

Copy code

```
CREATE OPENFLOW CONNECTOR my_db.my_schema.my_postgres_connector
  IN RUNTIME my_db.my_schema.my_runtime
  FROM DEFINITION OPENFLOW_POSTGRES_CDC
  DISPLAY_NAME = 'My Postgres CDC Connector';
```

From a stage reference:

Copy code

```
-- From a Git repository stage
CREATE OPENFLOW CONNECTOR my_db.my_schema.my_connector
  IN RUNTIME my_db.my_schema.my_runtime
  FROM '@my_git_repo/branches/main/connectors/my_connector/'
  COMMENT = 'Created from Git stage';

-- From another connector's committed configuration
CREATE OPENFLOW CONNECTOR my_db.my_schema.my_connector_copy
  IN RUNTIME my_db.my_schema.my_other_runtime
  FROM 'snow://openflow_connector/my_db.my_schema.my_connector/versions/LAST/'
  COMMENT = 'Cloned from existing connector';
```
