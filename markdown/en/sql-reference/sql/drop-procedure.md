# DROP PROCEDURE

Removes the specified stored procedure from the current/specified schema.

See also:
:   [CREATE PROCEDURE](/sql-reference/sql/create-procedure) , [ALTER PROCEDURE](/sql-reference/sql/alter-procedure) , [SHOW PROCEDURES](/sql-reference/sql/show-procedures) , [DESCRIBE PROCEDURE](/sql-reference/sql/desc-procedure), [SHOW USER PROCEDURES](/sql-reference/sql/show-user-procedures)

## Syntax

Copy code

```
DROP PROCEDURE [ IF EXISTS ] <procedure_name> ( [ <arg_data_type> , ... ] )
```

## Usage notes

**All Languages**

- For each argument defined for the procedure, the data type for the argument must be specified. This is required because overloading of
  procedure names is supported and the data type(s) for the argument(s) are required to identify the procedure.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

**Java, Python, and Scala**

- For procedures that store code in a file (such as a .jar file or .py file) in a stage, the `DROP PROCEDURE` command does not remove
  the file. Different procedures can use different functions/methods in the same file, so the file should not be removed
  while any procedure refers to it. Snowflake does not store a count of the number of references to each staged file and
  does not remove that staged file when there are no remaining references.

## Examples

> Copy code
>
> ```
> DROP PROCEDURE add_accounting_user(varchar);
>
> -------------------------------------------+
>              status                        |
> -------------------------------------------+
>  ADD_ACCOUNTING_USER successfully dropped. |
> -------------------------------------------+
> ```
