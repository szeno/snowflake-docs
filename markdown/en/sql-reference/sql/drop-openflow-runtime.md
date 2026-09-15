# DROP OPENFLOW RUNTIME

See also:
:   [CREATE OPENFLOW RUNTIME](/sql-reference/sql/create-openflow-runtime), [ALTER OPENFLOW RUNTIME](/sql-reference/sql/alter-openflow-runtime), [SHOW OPENFLOW RUNTIMES](/sql-reference/sql/show-openflow-runtimes), [DESCRIBE OPENFLOW RUNTIME](/sql-reference/sql/desc-openflow-runtime)

## Syntax

Copy code

```
DROP OPENFLOW RUNTIME [ IF EXISTS ] <name> [ CASCADE ]
```

## Parameters

`IF EXISTS`
:   Drops the runtime only if it exists. If the runtime does not exist, the statement does nothing and
    returns a success message.

`CASCADE`
:   Drops the records for any connectors in the runtime along with the runtime record. Without
    `CASCADE`, the statement fails if connector records remain.

Allowed only when the runtime is in `TERMINATED` state (after `ALTER ... TERMINATE`).
