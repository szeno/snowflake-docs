Categories:
:   [Context functions](/sql-reference/functions-context) (Session)

# CURRENT\_STATEMENT

Returns the SQL text of the statement that is currently executing.

## Syntax

Copy code

```
CURRENT_STATEMENT()
```

## Arguments

None.

## Examples

This shows a simple example of using the `CURRENT_STATEMENT` function:

> Copy code
>
> ```
> SELECT 2.71, CURRENT_STATEMENT();
> ```
>
> Output:
>
> Copy code
>
> ```
> +------+-----------------------------------+
> | 2.71 | CURRENT_STATEMENT()               |
> |------+-----------------------------------|
> | 2.71 | SELECT 2.71, CURRENT_STATEMENT(); |
> +------+-----------------------------------+
> ```
