# DROP MATERIALIZED VIEW

[Enterprise Edition Feature](/user-guide/intro-editions)

Materialized views require Enterprise Edition. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Removes the specified materialized view from the current/specified schema.

See also:
:   [ALTER MATERIALIZED VIEW](/sql-reference/sql/alter-materialized-view) , [CREATE MATERIALIZED VIEW](/sql-reference/sql/create-materialized-view) , [SHOW MATERIALIZED VIEWS](/sql-reference/sql/show-materialized-views) , [DESCRIBE MATERIALIZED VIEW](/sql-reference/sql/desc-materialized-view)

## Syntax

Copy code

```
DROP MATERIALIZED VIEW [ IF EXISTS ] <view_name>
```

## Usage notes

- Dropping a materialized view does not update references to that view. For example, if you create a view named “V1” on top of a
  materialized view, and then you drop the materialized view, the definition of view “V1” will become out of date.
- Dropped materialized views can’t be recovered; they must be recreated.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

> Copy code
>
> ```
> DROP MATERIALIZED VIEW mv1;
>
> ---------------------------+
>            status          |
> ---------------------------+
>  MV1 successfully dropped. |
> ---------------------------+
> ```
