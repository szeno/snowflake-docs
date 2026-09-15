# DROP OPENFLOW CONNECTOR

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

See also:
:   [CREATE OPENFLOW CONNECTOR](/sql-reference/sql/create-openflow-connector), [ALTER OPENFLOW CONNECTOR](/sql-reference/sql/alter-openflow-connector), [SHOW OPENFLOW CONNECTOR DEFINITIONS](/sql-reference/sql/show-openflow-connector-definitions), [SHOW OPENFLOW CONNECTORS](/sql-reference/sql/show-openflow-connectors), [DESCRIBE OPENFLOW CONNECTOR](/sql-reference/sql/desc-openflow-connector), [SHOW VERSIONS IN OPENFLOW CONNECTOR](/sql-reference/sql/show-versions-in-openflow-connector)

## Syntax

Copy code

```
DROP OPENFLOW CONNECTOR [ IF EXISTS ] <name>
```

## Parameters

`IF EXISTS`
:   Drops the connector only if it exists. If the connector does not exist, the statement does nothing
    and returns a success message.

Requires `OWNERSHIP`. The connector must be terminated first (`ALTER ... TERMINATE`). Stop the
connector before terminating. `TERMINATE` drains in-flight data.

Typical deletion sequence:

Copy code

```
ALTER OPENFLOW CONNECTOR my_db.my_schema.my_connector STOP;
SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_CONNECTORS(600, 'my_db.my_schema.my_connector');

ALTER OPENFLOW CONNECTOR my_db.my_schema.my_connector TERMINATE;
SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_CONNECTORS(600, 'my_db.my_schema.my_connector');

DROP OPENFLOW CONNECTOR my_db.my_schema.my_connector;
```
