# DROP VIEW

Removes the specified view from the current/specified schema.

See also:
:   [CREATE VIEW](/sql-reference/sql/create-view) , [ALTER VIEW](/sql-reference/sql/alter-view) , [SHOW VIEWS](/sql-reference/sql/show-views) , [DESCRIBE VIEW](/sql-reference/sql/desc-view)

## Syntax

Copy code

```
DROP VIEW [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the view to drop. If the identifier contains spaces, special characters, or mixed-case characters, the
    entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

    If the view identifier is not fully-qualified (in the form of `db_name.schema_name.table_name` or
    `schema_name.table_name`), the command looks for the view in the current schema for the session.

## Usage notes

- Dropped views can’t be recovered; they must be recreated.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

> Copy code
>
> ```
> DROP VIEW myview;
> ```
>
> ```
> ------------------------------+
>            status             |
> ------------------------------+
>  MYVIEW successfully dropped. |
> ------------------------------+
> ```
