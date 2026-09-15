# Dropping constraints

Constraints are dropped using the following [ALTER TABLE](/sql-reference/sql/alter-table) commands:

- ALTER TABLE … DROP CONSTRAINT explicitly drops the specified constraint. Similar to modifying constraints,
  you can identify the constraint using the constraint name or column definition along with the constraint type.
  For a primary key, the constraint can also be identified using the PRIMARY KEY keyword.
- ALTER TABLE … DROP COLUMN drops a column and its associated constraints.

By default, when a primary or unique key is dropped, all foreign keys referencing the key being dropped are also dropped,
unless the RESTRICT drop option is specified.

Constraints are also dropped when the associated tables, schemas, or databases are dropped. The DROP commands support the
CASCADE | RESTRICT drop options.

Note

You can restore dropped tables, schemas, and databases using the UNDROP command. Dropped columns and constraints can’t
be restored.

## Dropping constraints

You can explicitly drop UNIQUE, PRIMARY KEY, FOREIGN KEY, and CHECK constraints using the ALTER TABLE … DROP CONSTRAINT command:

> Copy code
>
> ```
> ALTER TABLE <table_name> DROP { CONSTRAINT <name> | PRIMARY KEY | { UNIQUE | FOREIGN KEY } (<column>, [ ... ] ) } [ CASCADE | RESTRICT ]
> ```

For these constraints, when dropping a FOREIGN KEY constraint or a primary or unique key constraint with no foreign key references,
the constraints are dropped directly.

The default drop option is CASCADE, which means that dropping a unique or primary key with foreign key references drops all the referencing
foreign keys together with the unique or primary key.

If the RESTRICT drop option is specified, when dropping a primary or unique key, an error is returned if there exist foreign keys that
reference the keys being dropped.

## Dropping columns

Dropping columns using ALTER TABLE … DROP COLUMN behaves similarly to dropping constraints:

> Copy code
>
> ```
> ALTER TABLE <table_name> DROP COLUMN <name> [ CASCADE | RESTRICT ]
> ```

For PRIMARY KEY, UNIQUE, and FOREIGN KEY constraints, the default drop option is CASCADE, which means any constraint that contains
the column being dropped is also dropped. If a primary or unique key involving the column is referenced by other FOREIGN KEY constraints,
all referencing foreign keys are dropped. If the RESTRICT option is specified, an error is returned if the column has primary or unique
keys with foreign keys references. The drop command only succeeds if there are no constraints defined on or referring to the column being
dropped.

For CHECK constraints that reference a single column, the default drop option is CASCADE. However, for CHECK constraints that reference
multiple columns, the default drop option is RESTRICT, which prevents accidental deletion of constraints that might be required for
data integrity.

## Dropping tables, schemas, and databases

The DROP command drops the specified table, schema, or database and can also be specified to drop all constraints associated with the object:

> Copy code
>
> ```
> DROP { TABLE | SCHEMA | DATABASE } <name> [ CASCADE | RESTRICT ]
> ```

Similar to dropping columns and constraints, CASCADE is the default drop option, and all constraints that belong to or reference the object
being dropped are also dropped.

For example, when dropping a database, if the database contains a primary or unique key which is referenced by a foreign key from another database,
the referencing foreign keys are also dropped.

If the object is later undropped, all relevant constraints previously dropped are restored.

If the RESTRICT option is specified, an error is returned if any PRIMARY KEY or UNIQUE constraints under the object have foreign key references.
