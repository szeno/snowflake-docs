# Create hybrid tables

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

This topic provides an overview on creating [hybrid tables](/user-guide/tables-hybrid) in Snowflake.

Note

To create a hybrid table, you must have a running warehouse that is specified as the current warehouse for your session.
Errors may occur if no running warehouse is specified when you create a hybrid table.
For more information, see [Working with Warehouses](/user-guide/warehouses-tasks).

## CREATE HYBRID TABLE options

You can create a hybrid table by using one of the following methods.

- [CREATE HYBRID TABLE](/sql-reference/sql/create-hybrid-table). The following example
  creates a hybrid table with a required PRIMARY KEY constraint, inserts some rows, deletes a row, and queries the table:

  Copy code

  ```
  CREATE OR REPLACE HYBRID TABLE application_log (
    id NUMBER PRIMARY KEY AUTOINCREMENT,
    col1 VARCHAR(20),
    col2 VARCHAR(20) NOT NULL
    );

  INSERT INTO application_log (col1, col2) VALUES ('A1', 'B1');
  INSERT INTO application_log (col1, col2) VALUES ('A2', 'B2');
  INSERT INTO application_log (col1, col2) VALUES ('A3', 'B3');
  INSERT INTO application_log (col1, col2) VALUES ('A4', 'B4');

  SELECT * FROM application_log;

  UPDATE application_log SET col2 = 'B3-updated' WHERE id = 3;

  DELETE FROM application_log WHERE id = 4;

  SELECT * FROM application_log;
  ```
- [CREATE HYBRID TABLE … AS SELECT (CTAS)](/sql-reference/sql/create-hybrid-table#label-create-hybrid-table-as) or [CREATE HYBRID TABLE … LIKE](/sql-reference/sql/create-hybrid-table#label-create-hybrid-table-like). For example:

  Copy code

  ```
  CREATE OR REPLACE HYBRID TABLE dept_employees (
    employee_id INT PRIMARY KEY,
    department_id VARCHAR(200)
    )
  AS SELECT employee_id, department_id FROM company_employees;
  ```

## Loading data

Note

Because the primary storage for hybrid tables is a row store, hybrid tables typically
have a larger storage footprint than standard tables.
The main reason for the difference is that columnar data for standard tables often
achieves higher rates of compression. For details about storage costs, see
[Evaluate cost for hybrid tables](/user-guide/tables-hybrid-cost).

### Optimized bulk loads

You can bulk load data into hybrid tables by copying either from a data stage or from other tables.
The optimized bulk loading path supports [CTAS](/sql-reference/sql/create-table#label-ctas-syntax) (for new tables),
[COPY INTO <table>](/sql-reference/sql/copy-into-table), and all variants of [INSERT](/sql-reference/sql/insert)
except INSERT ALL. It accelerates loading whether the hybrid table is empty or already contains data.

You can check the **Statistics** information in Snowsight query profiles to see whether the bulk-load
fast path was used. **Number of rows inserted** is referred to as the **Number of rows bulk loaded** when the fast
path is used. For example, this CTAS operation bulk loaded 200000 rows into a new table:

![CTAS query profile that uses the optimized bulk loading](/static/images/screens/number_of_rows_bulk_loaded_new.png)

For more information about query profiles, see [Analyze query profiles for hybrid tables](/user-guide/tables-hybrid-read-query-profiles) and
[Monitor query activity with Query History](/user-guide/ui-snowsight-activity).

Attention

CTAS commands do not support FOREIGN KEY constraints. If your hybrid table requires FOREIGN KEY constraints,
use COPY or INSERT INTO … SELECT to load the table. You can also use CTAS to create and load the table
without the foreign key, then add the foreign key afterward with [ALTER TABLE](/sql-reference/sql/alter-table). See
[Add and drop constraints on an existing hybrid table](/sql-reference/sql/create-hybrid-table#label-hybrid-table-online-constraints).

Note

Other methods of loading data into Snowflake tables (for example, Snowpipe) are not currently supported.

### Index-building errors during loads

Index sizes are limited in width. When building indexes on columns in a hybrid table, especially
indexes on a large number of columns, any command that loads the table
(including CTAS, COPY, or INSERT INTO … SELECT) might return the following error. In this case, the table
contains an index named `IDX_HT100_COLS`:

```
The value is too long for index "IDX_HT100_COLS".
```

This error occurs because row-based storage imposes a limit on the size of the data (and metadata) that can
be stored per record. To reduce the record size, try creating the table without specifying larger columns,
such as wide VARCHAR columns, as indexed columns. You can also try creating indexes on fewer columns.

You can also try using INCLUDE columns on secondary indexes when you create a hybrid table or an index on a
hybrid table. For more information, see [INCLUDE columns](/user-guide/tables-hybrid-index#label-indexes-with-include-columns).
