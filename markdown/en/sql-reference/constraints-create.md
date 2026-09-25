# Creating constraints

A constraint can be created at table creation using [CREATE TABLE](/sql-reference/sql/create-table), or added to a table later using [ALTER TABLE](/sql-reference/sql/alter-table):

- Single-column constraints can be created inline as part of the column definition.
- Multi-column constraints must be created with a separate out-of-line clause that specifies the columns in the constraint.

To create a constraint, certain access control privileges must be granted on the role used to create the constraint. For more information, see [Access control requirements](/sql-reference/sql/create-table-constraint#label-access-control-create-constraint).

## Creating constraints inline

The following inline syntax can only be used for single-column constraints:

Copy code

```
CREATE [ OR REPLACE ] TABLE <name> (<column_name> <column_type> [ <inline_constraint> ] , ... )

ALTER TABLE <name> ADD COLUMN <column_name> <column_type> [ <inline_constraint> ]
```

For `inline_constraint` syntax details, see [CREATE | ALTER TABLE … CONSTRAINT](/sql-reference/sql/create-table-constraint).

## Creating constraints out-of-line

The following out-of-line syntax must be used for multi-column constraints, but can also be used for single-column constraints:

Copy code

```
CREATE [ OR REPLACE ] TABLE <name> ( ... , [ <outofline_constraint> ], ... )

ALTER TABLE <name> ADD <outofline_constraint>
```

For `outofline_constraint` syntax details, see [CREATE | ALTER TABLE … CONSTRAINT](/sql-reference/sql/create-table-constraint).

For [hybrid tables](/user-guide/tables-hybrid), adding a UNIQUE or FOREIGN KEY constraint with ALTER TABLE is an online
operation that also validates the rows already in the table. For more information, see
[Add and drop constraints on an existing hybrid table](/sql-reference/sql/create-hybrid-table#label-hybrid-table-online-constraints).

ALTER TABLE can’t add a CHECK constraint to a hybrid table. Define CHECK constraints on a hybrid table when you create
the table. For more information, see [CHECK constraints](/sql-reference/sql/create-hybrid-table#label-hybrid-table-check-constraints).

## Constraints in CREATE TABLE … LIKE and CLONE

Snowflake supports creating copies of tables using [CREATE TABLE](/sql-reference/sql/create-table):

- To create an empty copy, use CREATE TABLE … LIKE.
- To create a clone, use CREATE TABLE … CLONE.

In addition, copies of tables are automatically created when a schema or database is cloned.

Regardless of how a copy is created for a table, the constraints on the original table are also copied. When copying a foreign key with a referencing table (foreign key table) and a referenced table (primary key table), the following scenarios may occur:

- If both tables are copied in the same command (such as during cloning of a schema or database), a new foreign key is created between the new referencing table and the referenced table.
- If only the referencing table is copied, a new foreign key is created on the referencing table, which points to the original primary key table as the referenced table.
- If only the referenced table is copied, no new foreign keys are created, although the primary or unique keys are copied.

As a result, if you copy a referencing and referenced table separately, you must manually create a new foreign key, or change the primary key table for the new foreign key manually.
