# Warehouse & resource monitor DDL

A virtual warehouse is a cluster of compute resources. A warehouse is needed to execute certain types of SQL statements because it provides resources such as CPU, memory, and local storage.

Resource monitors can be used to control credit usage for warehouses. A resource monitor specifies a monthly credit quota, one or more credit usage thresholds, and actions to perform when the thresholds are
reached. Each resource monitor can be associated with one or more warehouses.

## Virtual warehouses

- [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse)
- [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse)
- [DESCRIBE WAREHOUSE](/sql-reference/sql/desc-warehouse)
- [DROP WAREHOUSE](/sql-reference/sql/drop-warehouse)
- [USE WAREHOUSE](/sql-reference/sql/use-warehouse)
- [SHOW WAREHOUSES](/sql-reference/sql/show-warehouses)

## Resource monitors

- [CREATE RESOURCE MONITOR](/sql-reference/sql/create-resource-monitor)
- [ALTER RESOURCE MONITOR](/sql-reference/sql/alter-resource-monitor)
- [DROP RESOURCE MONITOR](/sql-reference/sql/drop-resource-monitor)
- [SHOW RESOURCE MONITORS](/sql-reference/sql/show-resource-monitors)
