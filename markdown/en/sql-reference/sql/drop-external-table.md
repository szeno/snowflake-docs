# DROP EXTERNAL TABLE

Removes an external table from the current or specified schema. This is a metadata-only operation. None of the files that the
external table refers to are dropped.

See also:
:   [CREATE EXTERNAL TABLE](/sql-reference/sql/create-external-table) , [ALTER EXTERNAL TABLE](/sql-reference/sql/alter-external-table) , [SHOW EXTERNAL TABLES](/sql-reference/sql/show-external-tables) , [DESCRIBE EXTERNAL TABLE](/sql-reference/sql/desc-external-table)

## Syntax

Copy code

```
DROP EXTERNAL TABLE [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

## Parameters

`name`
:   Specifies the identifier for the external table to drop. If the identifier contains spaces, special characters, or mixed-case characters,
    the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case sensitive;
    for example, `"My Object"`.

    If the external table identifier is not fully qualified, in the form of `db_name.schema_name.table_name` or
    `schema_name.table_name`, the command looks for the external table in the current schema for the session.

`CASCADE | RESTRICT`
:   Specifies whether the external table can be dropped if foreign keys exist that reference the table:

    - `CASCADE` drops the external table even if it has primary or unique keys that are referenced by foreign keys in other tables.
    - `RESTRICT` returns a warning about existing foreign key references and doesn’t drop the external table.

    Default: `CASCADE`

## Usage notes

- Unlike a standard table, dropping an external table purges it from the system. An external table can’t be recovered by using Time Travel;
  also, there is no UNDROP EXTERNAL TABLE command. A dropped external table must be recreated.
- After dropping an external table, creating an external table with the same name recreates the table. No history from the old version
  of the external table is retained.
- Before dropping an external table, verify that no views reference the table. Dropping an external table referenced by a view
  invalidates the view; that is, querying the view returns an “object does not exist” error.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Drop an external table:

> Copy code
>
> ```
> SHOW EXTERNAL TABLES LIKE 't2%';
>
> +-------------------------------+------------------+---------------+-------------+-----------------------+---------+-----------------------------------------+------------------+------------------+-------+-----------+----------------------+
> | created_on                    | name             | database_name | schema_name | owner                 | comment | location                                | file_format_name | file_format_type | cloud | region    | notification_channel |
> |-------------------------------+------------------+---------------+-------------+-----------------------+---------+-----------------------------------------+------------------+------------------+-------+-----------+----------------------|
> | 2018-08-06 06:00:42.340 -0700 | T2               | MYDB          | PUBLIC      | MYROLE                |         | @MYDB.PUBLIC.MYSTAGE/                   |                  | JSON             | AWS   | us-east-1 | NULL                 |
> +-------------------------------+------------------+---------------+-------------+-----------------------+---------+-----------------------------------------+------------------+------------------+-------+-----------+----------------------+
>
> DROP EXTERNAL TABLE t2;
>
> +--------------------------+
> | status                   |
> |--------------------------|
> | T2 successfully dropped. |
> +--------------------------+
>
> SHOW EXTERNAL TABLES LIKE 't2%';
>
> +------------+------+---------------+-------------+-------+---------+----------+------------------+------------------+-------+--------+----------------------+
> | created_on | name | database_name | schema_name | owner | comment | location | file_format_name | file_format_type | cloud | region | notification_channel |
> |------------+------+---------------+-------------+-------+---------+----------+------------------+------------------+-------+--------+----------------------|
> +------------+------+---------------+-------------+-------+---------+----------+------------------+------------------+-------+--------+----------------------+
> ```

Drop the table again, but don’t raise an error if the table doesn’t exist:

> Copy code
>
> ```
> DROP EXTERNAL TABLE IF EXISTS t2;
>
> +------------------------------------------------------------+
> | status                                                     |
> |------------------------------------------------------------|
> | Drop statement executed successfully (T2 already dropped). |
> +------------------------------------------------------------+
> ```
