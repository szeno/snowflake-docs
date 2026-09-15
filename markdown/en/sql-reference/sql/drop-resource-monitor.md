# DROP RESOURCE MONITOR

Removes the specified [resource monitor](/user-guide/resource-monitors) from the system.

See also:
:   [CREATE RESOURCE MONITOR](/sql-reference/sql/create-resource-monitor) , [ALTER RESOURCE MONITOR](/sql-reference/sql/alter-resource-monitor) , [SHOW RESOURCE MONITORS](/sql-reference/sql/show-resource-monitors)

## Syntax

Copy code

```
DROP RESOURCE MONITOR [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the resource monitor to drop. If the identifier contains spaces or special characters, the entire string
    must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- Dropped resource monitors cannot be recovered; they must be recreated.
- Dropping a resource monitor immediately enables resuming any assigned warehouses that have been suspended due to the monitor reaching
  its monthly threshold.

  For more information, see [Working with resource monitors](/user-guide/resource-monitors).

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Drop resource monitor `my_rm`, but don’t raise an error if the resource monitor doesn’t exist:

Copy code

```
DROP RESOURCE MONITOR IF EXISTS my_rm;
```
