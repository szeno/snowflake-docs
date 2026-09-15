Categories:
:   [Context functions](/sql-reference/functions-context) (Session Object)

# CURRENT\_WAREHOUSE

Returns the name of the warehouse in use for the current session.

To specify a different warehouse for the session, execute the [USE WAREHOUSE](/sql-reference/sql/use-warehouse)
command.

## Syntax

Copy code

```
CURRENT_WAREHOUSE()
```

## Arguments

None.

## Examples

Show the current warehouse, database, and schema:

> Copy code
>
> ```
> SELECT CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();
> ```
>
> Output:
>
> Copy code
>
> ```
> +---------------------+--------------------+------------------+
> | CURRENT_WAREHOUSE() | CURRENT_DATABASE() | CURRENT_SCHEMA() |
> |---------------------+--------------------+------------------|
> | DEV_WAREHOUSE       | TEST_DATABASE      | UDF_TEST_SCHEMA  |
> +---------------------+--------------------+------------------+
> ```
