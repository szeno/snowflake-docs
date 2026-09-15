# CREATE OR ALTER *<object>*

CREATE OR ALTER commands are DDL commands that combine the functionality of the CREATE command and the ALTER command, enabling you to define
an object using the syntax supported by the CREATE <object> command with the limitations of the ALTER <object> command.

The commands maintain data and associations, meaning that data and other states, tag associations and attached policies, and privilege grants
on the object are preserved. However, some object transformations can result
in dropped data. For example, if a CREATE OR ALTER TABLE statement results in a dropped column, any data contained in the column is lost (but
can still be recovered with Time Travel).

CREATE OR ALTER commands enable you to apply incremental updates to objects using a declarative, idempotent method. When executed, a CREATE OR
ALTER statement results in one of these outcomes:

- If the object doesn’t exist, it’s created according to the definition.
- If the object exists, it’s altered into the object defined in the statement.
- If the object already matches the definition, it remains unchanged.

## How CREATE OR ALTER differs from CREATE and ALTER

`CREATE` and `ALTER` are imperative commands: each statement describes a specific operation to perform, such as adding a column, changing a
property, or renaming an object. `CREATE OR ALTER` is declarative: you describe the full desired state of the object, and Snowflake computes
what changes are needed to reach that state.

This distinction explains both the key benefit and the key limitations:

- **Idempotency.** Running the same statement multiple times always produces the same result. This makes `CREATE OR ALTER` safe for deployment
  scripts and infrastructure-as-code workflows where the same script runs in both new and existing environments. For a more complete solution
  that manages Snowflake objects as code using a plan-then-deploy workflow across environments, see [Snowflake DCM Projects](/user-guide/dcm-projects/dcm-projects-overview).
- **No renaming.** Because `CREATE OR ALTER` works by comparing the desired definition to the current state, it can detect that a column was
  added or removed, but it can’t determine whether a column was *renamed*. If column `b` exists in the current table but not in the new
  definition, and column `c` appears in the new definition but not in the current table, Snowflake treats this as a drop of `b` and an
  addition of `c`, not a rename. Use `ALTER TABLE ... RENAME COLUMN` for explicit renames.
- **ALTER limitations apply.** When an object already exists, Snowflake applies the computed delta using the same engine as the corresponding
  `ALTER` command. Any operation that `ALTER` doesn’t support is also unsupported in `CREATE OR ALTER`. For example, you can’t change a
  column’s data type to an incompatible type.

A `CREATE OR ALTER` statement defines the complete desired state of an object. Snowflake computes and applies the minimal set of changes
needed to reach that state, using the same operations available through the corresponding `ALTER` command.

See also:
:   [CREATE <object>](/sql-reference/sql/create), [ALTER <object>](/sql-reference/sql/alter)

## CREATE OR ALTER commands

For specific syntax, usage notes, and examples, see:

**Account Objects:**

> - [CREATE OR ALTER AUTHENTICATION POLICY](/sql-reference/sql/create-authentication-policy#label-create-or-alter-auth-policy-syntax)
> - [CREATE OR ALTER DATABASE](/sql-reference/sql/create-database#label-create-or-alter-database-syntax)
> - [CREATE OR ALTER NETWORK POLICY](/sql-reference/sql/create-network-policy#label-create-or-alter-network-policy-syntax)
> - [CREATE OR ALTER ROLE](/sql-reference/sql/create-role#label-create-or-alter-role-syntax)
> - [CREATE OR ALTER SHARE](/sql-reference/sql/create-share#label-create-or-alter-share-syntax)
> - [CREATE OR ALTER WAREHOUSE](/sql-reference/sql/create-warehouse#label-create-or-alter-warehouse-syntax)

**Database Objects:**

> - [CREATE OR ALTER APPLICATION ROLE](/sql-reference/sql/create-application-role#label-create-or-alter-app-role-syntax)
> - [CREATE OR ALTER BACKUP POLICY](/sql-reference/sql/create-backup-policy#label-create-or-alter-backup-policy-syntax)
> - [CREATE OR ALTER BACKUP SET](/sql-reference/sql/create-backup-set#label-create-or-alter-backup-set-syntax)
> - [CREATE OR ALTER DATABASE ROLE](/sql-reference/sql/create-database-role#label-create-or-alter-db-role-syntax)
> - [CREATE OR ALTER DATA METRIC FUNCTION](/sql-reference/sql/create-data-metric-function#label-create-or-alter-dmf-function-syntax)
> - [CREATE OR ALTER DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table#label-create-or-alter-dt-syntax)
> - [CREATE OR ALTER EXTERNAL FUNCTION](/sql-reference/sql/create-external-function#label-create-or-alter-external-function-syntax) (Preview)
> - [CREATE OR ALTER FILE FORMAT](/sql-reference/sql/create-file-format#label-create-or-alter-file-format-syntax)
> - [CREATE OR ALTER FUNCTION](/sql-reference/sql/create-function#label-create-or-alter-function-syntax)
> - [CREATE OR ALTER FUNCTION (Snowpark Container Services)](/sql-reference/sql/create-function-spcs#label-create-or-alter-function-spcs-syntax) (Preview)
> - [CREATE OR ALTER MASKING POLICY](/sql-reference/sql/create-masking-policy#label-create-or-alter-masking-policy-syntax)
> - [CREATE OR ALTER NETWORK RULE](/sql-reference/sql/create-network-rule#label-create-or-alter-network-rule-syntax)
> - [CREATE OR ALTER PIPE](/sql-reference/sql/create-pipe#label-create-or-alter-pipe-syntax) (Preview)
> - [CREATE OR ALTER PROCEDURE](/sql-reference/sql/create-procedure#label-create-or-alter-procedure-syntax)
> - [CREATE OR ALTER ROW ACCESS POLICY](/sql-reference/sql/create-row-access-policy#label-create-or-alter-row-access-policy-syntax)
> - [CREATE OR ALTER SCHEMA](/sql-reference/sql/create-schema#label-create-or-alter-schema-syntax)
> - [CREATE OR ALTER SEMANTIC VIEW](/sql-reference/sql/create-semantic-view#label-create-or-alter-semantic-view-syntax)
> - [CREATE OR ALTER STAGE](/sql-reference/sql/create-stage#label-create-or-alter-stage-syntax)
> - [CREATE OR ALTER STREAM](/sql-reference/sql/create-stream#label-create-or-alter-stream-syntax) (Preview)
> - [CREATE OR ALTER TABLE](/sql-reference/sql/create-table#label-create-or-alter-table-syntax)
> - [CREATE OR ALTER TAG](/sql-reference/sql/create-tag#label-create-or-alter-tag-syntax)
> - [CREATE OR ALTER TASK](/sql-reference/sql/create-task#label-create-or-alter-task-syntax)
> - [CREATE OR ALTER VERSIONED SCHEMA](/sql-reference/sql/create-versioned-schema) (Preview)
> - [CREATE OR ALTER VIEW](/sql-reference/sql/create-view#label-create-or-alter-view-syntax)

## General usage notes

- **Data governance**: The CREATE OR ALTER commands don’t support data governance changes. Existing tags or policies are unaffected by CREATE
  OR ALTER statements and remain unchanged.
- **Unsetting object properties and parameters**: If a previously set property or parameter is absent in the modified object definition, it’s unset.

  If you unset an explicit [parameter](/sql-reference/parameters) value, the parameter is reset to the default value. If the parameter
  is set on an object that contains the target object, the target object inherits the value set on the object that contains it. Otherwise,
  the parameter value for the object is reset to the default value.

  Unlike other properties, the CHANGE\_TRACKING and ROW\_TIMESTAMP properties will not be unset if not specified in a CREATE OR ALTER command.
- **Atomicity**: The CREATE OR ALTER TABLE command does not guarantee atomicity. In the very rare case that a CREATE OR ALTER TABLE
  statement for an extremely wide table fails during execution, it is possible that a subset of changes might have been applied to the table. If there is a possibility
  of partial changes, the error message, in most cases, includes the following text:

  ```
  CREATE OR ALTER execution failed. Partial updates may have been applied.
  ```

  For example, if the statement is attempting to drop column `A` and add a new column `B` to a table, and the
  statement is aborted, it is possible that column `A` was dropped but column `B` was not added.

  Note

  If changes are partially applied, the resulting table is still in a valid state, and you can use additional ALTER TABLE
  statements to complete the original set of changes.

  To recover from partial updates, Snowflake recommends the following recovery mechanisms:

  - Fix forward

    - Re-execute the CREATE OR ALTER TABLE statement. If the statement succeeds on the second attempt, the target
      state is achieved.
    - Investigate the error message. If possible, fix the error and re-execute the CREATE OR ALTER TABLE statement.
  - Roll back

    If it is not possible to fix forward, Snowflake recommends manually rolling back partial changes:

    - Investigate the state of the table using the [DESCRIBE TABLE](/sql-reference/sql/desc-table) and [SHOW TABLES](/sql-reference/sql/show-tables) commands. Determine which partial
      changes were applied, if any.
    - If any partial changes were applied, execute the appropriate ALTER TABLE statements to transform the table back to its
      original state.

      Note

      In some cases, you might not be able to undo partial changes. For more information, see the supported and unsupported
      actions for modifying column properties in the [ALTER TABLE … ALTER COLUMN](/sql-reference/sql/alter-table-column) topic.
  - If you need help recovering from a partial update, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Limitations

The specific limitations of the CREATE OR ALTER <object> command depend on the object. Some examples of limitations are as follows:

- CREATE OR ALTER TABLE commands don’t support search optimization because search optimization is not part of the CREATE TABLE syntax.
- You can’t change the data type of a column in a table to an incompatible data type.
- You must suspend a task before you can alter it.
- CREATE OR ALTER TABLE … AS SELECT is currently not supported.
- You can’t rename objects or columns, or change column order.

For the limitations for a specific object, see [the reference topic for the object](/sql-reference/sql/create-or-alter#label-coa-supported-objects).
