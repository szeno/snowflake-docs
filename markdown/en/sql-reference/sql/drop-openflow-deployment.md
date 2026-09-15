# DROP OPENFLOW DEPLOYMENT

See also:
:   [CREATE OPENFLOW DEPLOYMENT](/sql-reference/sql/create-openflow-deployment), [ALTER OPENFLOW DEPLOYMENT](/sql-reference/sql/alter-openflow-deployment), [SHOW OPENFLOW DEPLOYMENTS](/sql-reference/sql/show-openflow-deployments), [DESCRIBE OPENFLOW DEPLOYMENT](/sql-reference/sql/desc-openflow-deployment)

Removes the record for a terminated deployment.

## Syntax

Copy code

```
DROP OPENFLOW DEPLOYMENT [ IF EXISTS ] <name>
```

The deployment must be in `TERMINATED` status (after `ALTER ... TERMINATE` completes).
