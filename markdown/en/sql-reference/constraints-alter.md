# Modifying constraints

After a constraint is created, you can modify it in the following ways:

- The constraint can be renamed.
- Some properties can be modified; for example, RELY.
- Some properties can’t be modified; for example, DEFERRABLE. To modify these properties, the constraint must
  be dropped and recreated.
- The column definition for a constraint can’t be modified; for example, add new columns, drop existing columns,
  or change the order of columns. To make these types of changes, the constraint must be dropped and recreated.

When modifying a constraint, identify the constraint using either the constraint name or the columns in the constraint
definition along with the type of the constraint. Primary keys can also be identified using the PRIMARY KEY keyword, because
each table can have only a single PRIMARY KEY.

If a table with constraints is modified, for example by renaming the table or swapping the table with another table, the
constraints are updated to reflect the changes.

## Renaming a constraint

Use the following syntax for the [ALTER TABLE](/sql-reference/sql/alter-table) command to rename a constraint:

Copy code

```
ALTER TABLE <table_name> RENAME CONSTRAINT <old_name> TO <new_name>;
```

## Modifying the properties of a constraint

Use the following syntax for the [ALTER TABLE](/sql-reference/sql/alter-table) command to modify the properties of a constraint:

Copy code

```
ALTER TABLE <table_name>
  { ALTER | MODIFY } {
      CONSTRAINT <name>
    | PRIMARY KEY
    | { UNIQUE | FOREIGN KEY } (<column_name>, [ ... ] )
  }
  { [ [ NOT ] ENFORCED ] [ VALIDATE | NOVALIDATE ] [ RELY | NORELY ] };
```

For CHECK constraints, the `constraint_name` is required. Also, you can’t modify the `expr` associated
with a CHECK constraint. To modify the `expr`, the CHECK constraint must be dropped and re-created.

Currently, Snowflake only supports setting the following constraint properties:

- [ NOT ] ENFORCED
- NOVALIDATE and VALIDATE
- RELY and NORELY

Snowflake doesn’t support setting ENFORCED. Snowflake only supports setting NOVALIDATE for CHECK constraints.
See also [Non-default values for ENABLE and VALIDATE properties](/sql-reference/sql/create-table-constraint#label-non-default-enable-validate).

For descriptions of the constraint properties, see [Constraint properties](/sql-reference/sql/create-table-constraint#label-extended-constraint-properties).

## Modifying a table with constraints

If a table with constraints is renamed, the constraints for the table, and any FOREIGN KEY constraints that reference
the table, are updated to reference the new name.

Likewise, if a table is swapped with another table, the existing table, all the constraints on the table, are maintained
on the swapped table.

For more details about renaming or swapping tables, see [ALTER TABLE](/sql-reference/sql/alter-table).
