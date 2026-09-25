# Overview of constraints

Snowflake provides the following constraint functionality:

- Constraint types from the ANSI SQL standard. For more information, see
  [Supported constraint types](#label-constraints-supported-types).
- Named constraints.
- Single-column and multi-column constraints.
- Creation of constraints inline and out-of-line.
- Creation, modification, and deletion of constraints.

For more information, see [CREATE | ALTER TABLE … CONSTRAINT](/sql-reference/sql/create-table-constraint).

## Supported constraint types

Snowflake supports the following constraint types from the ANSI SQL standard:

- **PRIMARY KEY**: Guarantees that all of the values in a column are distinct and that the column
  can’t store NULL values. The primary key uniquely identifies each row in a table.
- **UNIQUE**: Guarantees that all of the values in a column are distinct. Unlike a PRIMARY KEY constraint,
  a column with a UNIQUE constraint can have NULL values.
- **FOREIGN KEY**: Enforces referential integrity by requiring values in a column or set of columns
  to match values in another table or the same table.
- **NOT NULL**: Ensures that a column can’t store a NULL value.
- **CHECK**: Enforces a SQL expression as a condition on the values that can be inserted into or updated in one or more
  columns of a table. For more information, see [CHECK constraints](#label-constraints-check).

A table can have multiple unique keys and foreign keys, but only one primary key. A PRIMARY KEY constraint implies that the
column is both NOT NULL and UNIQUE.

All foreign keys must reference a corresponding primary or unique key that matches the column types of each column in the
foreign key. The primary key for a foreign key can be on a different table or the same table as the foreign key. When you
define FOREIGN KEY constraints across [hybrid tables](/user-guide/tables-hybrid), the tables must be in the same database.

The following table summarizes the differences in behavior between standard tables and hybrid tables,
with respect to the enforcement of constraints and whether constraints are required:

- A constraint is *enforced* when it protects a column from being updated in certain ways. For example, a column that is
  declared NOT NULL can’t contain a NULL value. An attempt to copy or insert a NULL value into a NOT NULL column results in an
  error. For hybrid tables, you can’t set the NOT ENFORCED property on PRIMARY KEY, FOREIGN KEY, and UNIQUE constraints. Setting
  this property results in an `invalid constraint property` error.
- A constraint is *required* when one or more columns in a table must have such a constraint, which is only true for
  PRIMARY KEY constraints on hybrid tables.

| Feature | Hybrid tables | Standard tables |
| --- | --- | --- |
| PRIMARY KEY constraints | Required, enforced | Optional, not enforced |
| FOREIGN KEY constraints | Optional, enforced (referential integrity) | Optional, not enforced |
| UNIQUE constraints | Optional, enforced | Optional, not enforced |
| NOT NULL constraints | Optional, enforced | Optional, enforced |
| CHECK constraints | Optional, enforced; can be defined only at table creation | Optional, enforced |

Expand

Show lessSee more

## Table constraints

Snowflake supports constraints on permanent, transient, temporary, and hybrid
tables. You can define constraints on columns of all data types, and you can
include any number of columns in a single constraint.

The following are considerations for constraints:

- When you copy a table by using CREATE TABLE … LIKE or CREATE TABLE … CLONE,
  all existing constraints on the table, including foreign keys, are copied to the
  new table. CREATE TABLE … CLONE isn’t supported for hybrid tables.
- For hybrid tables, adding a UNIQUE or FOREIGN KEY constraint with ALTER TABLE is an
  online operation that also validates the rows already in the table. For more information,
  see [Add and drop constraints on an existing hybrid table](/sql-reference/sql/create-hybrid-table#label-hybrid-table-online-constraints).
- Additional commands and functions, such as DROP, UNDROP, and GET\_DDL are
  supported for tables with constraints. They are also supported for schemas
  and databases.

  For [Snowflake Time Travel](/user-guide/data-time-travel), when previous versions of a table
  are copied, the current version of the constraints on the table are used because Snowflake
  doesn’t store previous versions of constraints in table metadata.

## Single-column and multi-column constraints

You can define constraints on a single column or on multiple columns in the same
table.

For multi-column constraints (composite primary keys or unique keys), the
columns are ordered, and each column has a corresponding key sequence.

## Inline and out-of-line constraints

Constraints are defined either inline or out-of-line during table creation or
modification:

- Inline constraints are created as part of the column definition and can only
  be used for single-column constraints.
- Out-of-line constraints are defined using a separate clause that specifies the
  column or columns on which the constraint is created. They can be used for creating
  either single-column or multi-column constraints, as well as for creating
  constraints on existing columns.

## Constraints in GET\_DDL

The SQL statements that [GET\_DDL](/sql-reference/functions/get_ddl) returns include the
clauses that define constraints; however, note the following:

- Single-column constraints, such as `NOT NULL` and `DEFAULT`, are
  reconstructed inline with the definition of the column.
- Table constraints, such as unique, primary, and foreign keys, are always reconstructed as
  out-of-line constraints, even if they consist of a single column.
- For unnamed constraints — that is, constraints with a system-generated name —
  [GET\_DDL](/sql-reference/functions/get_ddl) doesn’t return the system-generated name.

## CHECK constraints

A CHECK constraint enforces a SQL expression as a condition on the values that can be inserted into or updated in one or more
columns of a table. For example, a CHECK constraint might
ensure that the `quantity` column in a table only contains values that are greater than zero or that the
`salary` column in a table only contains values in a specific range.

You can specify a CHECK constraint by using [CONSTRAINT clause](/sql-reference/sql/create-table-constraint)
in the following SQL commands:

- [CREATE TABLE](/sql-reference/sql/create-table)
- [ALTER TABLE](/sql-reference/sql/alter-table)
- [CREATE HYBRID TABLE](/sql-reference/sql/create-hybrid-table)
- [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table)
- [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table)

You can show information about existing CHECK constraints by querying the
[CHECK\_CONSTRAINTS view](/sql-reference/info-schema/check_constraints).

Check constraints are enforced during the following DML operations:

- [INSERT](/sql-reference/sql/insert)
- [UPDATE](/sql-reference/sql/update)
- [MERGE](/sql-reference/sql/merge)
- [CREATE TABLE … AS SELECT (CTAS)](/sql-reference/sql/create-table#label-ctas-syntax)

If the condition evaluates to TRUE or NULL, the DML operation proceeds. If the condition
evaluates to FALSE, the CHECK constraint fails.

For examples of CHECK constraints, see [Examples of constraints with standard tables](/sql-reference/sql/create-table-constraint#label-create-constraint-examples).

### Usage notes

- Check constraints are always enforced.
- You can use the following [ALTER TABLE](/sql-reference/sql/alter-table) commands and the Iceberg equivalents to work
  with CHECK constraints:

  - ALTER TABLE … RENAME CONSTRAINT
  - ALTER TABLE … ADD [ CONSTRAINT <constraint\_name> ] CHECK ( <expr> ) ENABLE [ VALIDATE | NOVALIDATE ]

    - ENABLE VALIDATE, the default for CHECK constraints, enforces the constraint for all existing rows and for
      all rows that are inserted or updated after you run the command. ENABLE VALIDATE is only supported for
      new tables, not for existing tables.
    - ENABLE NOVALIDATE enforces the constraint for all rows that are inserted or updated after you run the
      command, but doesn’t enforce the constraint for existing rows.
  - ALTER TABLE … ALTER CONSTRAINT <constraint\_name> ENABLE [ VALIDATE | NOVALIDATE ]

    If you change a CHECK constraint from NOVALIDATE to VALIDATE, the constraint is enforced on all existing
    rows before it is changed to VALIDATE.
  - ALTER TABLE … DROP CONSTRAINT
- The following [ALTER TABLE](/sql-reference/sql/alter-table) commands and Iceberg equivalents can operate on
  a column with a CHECK constraint defined on it:

  - ALTER TABLE … ALTER COLUMN

    Only operations that don’t modify a CHECK constraint are supported.
  - ALTER TABLE … RENAME COLUMN

    Check constraints that reference the renamed column are implicitly updated to use the new
    column name.
  - ALTER TABLE … DROP COLUMN

    The operation fails if the column being dropped is used by an existing CHECK constraint that
    also references another column. In this case, delete the constraint before deleting the column.
- If records violate a CHECK constraint during ingestion, the entire batch operation fails the first time
  it encounters a record that isn’t valid.
- For [hybrid tables](/user-guide/tables-hybrid), you can define a CHECK constraint only when you create the table.
  ALTER TABLE … ADD CONSTRAINT … CHECK and ALTER TABLE … ALTER CONSTRAINT aren’t supported on a hybrid table.
  You can rename or drop an existing CHECK constraint on a hybrid table, but you can’t add it back afterward. For
  more information, see [CHECK constraints](/sql-reference/sql/create-hybrid-table#label-hybrid-table-check-constraints).

### Limitations

- Standard tables, hybrid tables, and Snowflake-managed Iceberg tables support CHECK constraints. Other types of
  tables don’t support CHECK constraints.
- The expression associated with an existing CHECK constraint can’t be modified using an ALTER TABLE command.
  To modify the expression, drop and re-create the CHECK constraint. On a hybrid table, you can’t re-create the
  constraint on the existing table, so you must re-create the table.
- CHECK constraints can’t be specified in CREATE OR ALTER TABLE commands.
- The following operations don’t support CHECK constraints:
  - If you attempt to COPY INTO a table with CHECK constraints, the operation fails.
  - If you attempt to create a pipe with a target table that has CHECK constraints, the operation fails.
  - [Snowpipe Streaming with the classic architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-overview) doesn’t support tables with CHECK constraints. If you attempt to open a channel on such a table, the operation fails. [Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview) supports CHECK constraints and enforces them during ingestion.
  - If you attempt external writes on Iceberg tables that have CHECK constraints, the operation fails.
