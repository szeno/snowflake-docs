# DROP INDEX

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

Drops a secondary index.

See also:
:   [CREATE INDEX](/sql-reference/sql/create-index) , [SHOW INDEXES](/sql-reference/sql/show-indexes) , [CREATE HYBRID TABLE](/sql-reference/sql/create-hybrid-table) , [DROP TABLE](/sql-reference/sql/drop-table) , [DESCRIBE TABLE](/sql-reference/sql/desc-table) , [SHOW HYBRID TABLES](/sql-reference/sql/show-hybrid-tables)

## Syntax

Copy code

```
DROP INDEX [ IF EXISTS ] <table_name>.<index_name>
```

## Parameters

`table_name`
:   Specifies the identifier for the table.

`index_name`
:   Specifies the identifier for the index.

## Usage notes

- This command can only be used to drop a *secondary* index. To drop an index that is used to enforce a UNIQUE
  or FOREIGN KEY constraint, use the [ALTER TABLE](/sql-reference/sql/alter-table) command to drop the constraint.
- Indexes cannot be undropped.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Removes the secondary index `c_idx` on table `t0`:

Copy code

```
DROP INDEX t0.c_idx;
```
