# ALTER OPENFLOW DEPLOYMENT

See also:
:   [CREATE OPENFLOW DEPLOYMENT](/sql-reference/sql/create-openflow-deployment), [DROP OPENFLOW DEPLOYMENT](/sql-reference/sql/drop-openflow-deployment), [SHOW OPENFLOW DEPLOYMENTS](/sql-reference/sql/show-openflow-deployments), [DESCRIBE OPENFLOW DEPLOYMENT](/sql-reference/sql/desc-openflow-deployment)

Modifies or changes the state of a gen 2 deployment.

## Syntax

Copy code

```
ALTER OPENFLOW DEPLOYMENT [ IF EXISTS ] <name> SET
  [ DISPLAY_NAME = <string> ]
  [ COMMENT = <string> ]
  [ EVENT_TABLE = { '<database>.<schema>.<tablename>' | NONE } ]

ALTER OPENFLOW DEPLOYMENT [ IF EXISTS ] <name> UNSET
  { DISPLAY_NAME | COMMENT | EVENT_TABLE } [ , ... ]

ALTER OPENFLOW DEPLOYMENT [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER OPENFLOW DEPLOYMENT [ IF EXISTS ] <name> UPGRADE

ALTER OPENFLOW DEPLOYMENT [ IF EXISTS ] <name> TERMINATE
```

## Parameters

`name`
:   Specifies the identifier for the deployment to alter.

`IF EXISTS`
:   Alters the deployment only if it exists. If the deployment does not exist, the statement does
    nothing and returns a success message.

`SET ...`
:   Updates metadata properties. Requires `OWNERSHIP`.

`UNSET ...`
:   Removes metadata properties. Requires `OWNERSHIP`.

`RENAME TO new_name`
:   Renames the deployment. Requires `OWNERSHIP` and `CREATE OPENFLOW DEPLOYMENT`.

`UPGRADE`
:   Upgrades the deployment to the latest version. Requires `OPERATE`.

`TERMINATE`
:   Irreversibly terminates the deployment. The deployment must be terminated before it can be dropped.
    Requires `OWNERSHIP`.

    For BYOC deployments, first run `destroy.sh` on the data plane agent, wait for
    `NOT_REPORTING` status, remove the CloudFormation stack, then run `TERMINATE`.
