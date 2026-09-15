# DROP WAREHOUSE

Removes the specified [virtual warehouse](/user-guide/warehouses-overview) from the system.

See also:
:   [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) , [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse) , [DESCRIBE WAREHOUSE](/sql-reference/sql/desc-warehouse) , [SHOW WAREHOUSES](/sql-reference/sql/show-warehouses)

## Syntax

Copy code

```
DROP WAREHOUSE [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the warehouse to drop. If the identifier contains spaces, special characters, or mixed-case characters, the
    entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- Dropped warehouses can’t be recovered; they must be recreated.
- When this command is issued, Snowflake aborts any queries being processed by the specified warehouse and shuts down the compute
  resources utilized by the warehouse. Metering on the compute resources for the warehouse stops after all running statements complete.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

Tip

To prevent in-progress queries from being aborted for a dropped warehouse (i.e. you wish the queries to be completed):

1. First suspend the warehouse.
2. After all the queries have completed, drop the warehouse.
