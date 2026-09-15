# CREATE INDEX

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

Creates a new secondary index in an existing [hybrid table](/user-guide/tables-hybrid) and populates the index with data.

The creation of an index is an online (non-blocking) operation. The hybrid table remains available for SELECT and DML
statements while the index is being built. However, if the hybrid table isn’t in active use and downtime isn’t an issue,
Snowflake recommends that you recreate the hybrid table with the indexes defined. See also [Create hybrid tables](/user-guide/tables-hybrid-create)
and [Index hybrid tables](/user-guide/tables-hybrid-index).

See also:
:   [DROP INDEX](/sql-reference/sql/drop-index) , [SHOW INDEXES](/sql-reference/sql/show-indexes) , [CREATE HYBRID TABLE](/sql-reference/sql/create-hybrid-table) , [DROP TABLE](/sql-reference/sql/drop-table) , [DESCRIBE TABLE](/sql-reference/sql/desc-table) , [SHOW HYBRID TABLES](/sql-reference/sql/show-hybrid-tables)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] INDEX [ IF NOT EXISTS ] <index_name>
  ON <table_name>
    ( <col_name> [ , <col_name> , ... ] )
    [ INCLUDE ( <col_name> [ , <col_name> , ... ] ) ]
```

## Parameters

`index_name`
:   Specifies the identifier for the new index. You must specify a unique name for each new index on a given hybrid table.
    No other secondary index with either the same name or the same ordered set of columns can exist on the hybrid table.

`table_name`
:   Specifies the name of an existing hybrid table that will hold the new index.

`col_name`
:   Specifies the name of an existing column in the hybrid table. All the requirements for index columns defined at table creation
    apply to column identifiers.

    A hybrid table cannot contain two secondary indexes defined on the same ordered set of columns.

    Columns with [geospatial data types](/sql-reference/data-types-geospatial)
    (GEOGRAPHY and GEOMETRY), [semi-structured data types](/sql-reference/data-types-semistructured)
    (ARRAY, OBJECT, VARIANT), and [vector data types](/sql-reference/data-types-vector) (VECTOR) are not supported in secondary indexes.

## Optional parameters

`INCLUDE ( col_name [ , col_name , ... ] )`
:   Specifies one or more included columns for a secondary index. Using included columns with a secondary index is
    particularly useful when queries frequently contain a set of columns in the SELECT list but not in
    the list of WHERE predicates. For more information, see [INCLUDE columns](/user-guide/tables-hybrid-index#label-indexes-with-include-columns).

    INCLUDE columns can’t be semi-structured columns (VARIANT, OBJECT, ARRAY) or geospatial columns (GEOGRAPHY, GEOMETRY).

## Access control requirements

To create an index, you must use a role that has OWNERSHIP privilege on the hybrid table.

## Usage notes

- The CREATE INDEX command cannot be used to add a foreign, primary, or unique key constraint.
- The creation of a new index does not concurrently block other workloads. The hybrid table is available for concurrent SELECT
  and DML statements.
- Only one active index build operation per hybrid table can run at any time.
- You can track the progress of an index build by using [SHOW INDEXES](/sql-reference/sql/show-indexes). The `status` column can take the following values:

  - `ACTIVE`: Index is complete and can be used to retrieve data.
  - `SUSPENDED`: Index is only updated and is not used to retrieve data.
  - `BUILD FAILURE`: An error has occurred with the index build process. You need to drop and recreate the index.
  - `BUILD IN PROGRESS`: Index is being built and is not used to retrieve data.
  - `BUILD VALIDATION FAILURE`: The index backs a UNIQUE or FOREIGN KEY constraint that you added with
    [ALTER TABLE](/sql-reference/sql/alter-table), and rows already in the table violate that constraint. For more information,
    see [When existing data violates the constraint](/sql-reference/sql/create-hybrid-table#label-hybrid-table-constraint-validation-failure).
- You can rebuild a non-active index, where the status is `SUSPENDED`, `BUILD FAILURE`, or `BUILD IN PROGRESS`, by using DROP INDEX
  and CREATE INDEX. You can’t rebuild an index with a status of `BUILD VALIDATION FAILURE` this way, because it backs a constraint.
  Drop and re-add the constraint by using [ALTER TABLE](/sql-reference/sql/alter-table) instead.
- If you want to drop a column that is part of an index that is being built, first stop the index build by dropping the index, then
  drop the column. If you try to drop the column before dropping the index, you will receive this error message:

  ```
  Column '<col_name>' cannot be dropped because it is used by index '<index-name>'.
  ```
- Online index builds do not make progress until all the active transactions with DMLs on the same table at the time when the
  CREATE INDEX statement was issued are completed. If any of those transactions remain idle for more than 5 minutes, they will
  abort by default. See [Transactions](/sql-reference/transactions).
- During the index build process, any DML performs its writes to the new index, but does not use the index to retrieve data.
- A small number of concurrent DMLs, which began executing after the CREATE INDEX command was complete, may fail and return
  this error:

  ```
  DML was unaware of concurrent DDL. Please retry this query.
  ```

  If the aborted DML statements belong to a multi-statement transaction, the transaction will roll back only if the
  [TRANSACTION\_ABORT\_ON\_ERROR](/sql-reference/parameters#label-transaction-abort-on-error) parameter is set to TRUE.
- A newly created index will be used for retrieving data only when the index build process concludes successfully and the
  status of the index is `ACTIVE`.
- Indexed columns do not support collations. For more information, see [Collations on hybrid table columns](/sql-reference/sql/create-hybrid-table#label-hybrid-table-collations-disable) and
  [Collation control](/sql-reference/collation#label-collation-control).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

To run the following CREATE INDEX example, first create and load the hybrid table.

Copy code

```
CREATE OR REPLACE HYBRID TABLE mytable (
  pk INT PRIMARY KEY,
  val INT,
  val2 INT
);

INSERT INTO mytable SELECT seq, seq+100, seq+200
  FROM (SELECT seq8() seq FROM TABLE(GENERATOR(rowcount => 100)) v);
```

Now you can create an index on the table.

Copy code

```
CREATE OR REPLACE INDEX vidx ON mytable (val);
```

```
+----------------------------------+
| status                           |
|----------------------------------|
| Statement executed successfully. |
+----------------------------------+
```

If a failure occurs while the index is being built, the SHOW INDEXES command reports the following status:

```
BUILD FAILURE Index build failed. Please drop the index and re-create it.
```

If you decide to stop the index build, use a [DROP INDEX](/sql-reference/sql/drop-index) command:

Copy code

```
DROP INDEX mytable.vidx;
```

```
+-------------------------------------+
| status                              |
|-------------------------------------|
| Statement executed successfully.    |
+-------------------------------------+
```
