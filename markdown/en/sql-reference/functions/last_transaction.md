Categories:
:   [Context functions](/sql-reference/functions-context) (Session)

# LAST\_TRANSACTION

Returns the transaction ID of the last transaction that was either committed or rolled back in the current session.

See also:
:   [CURRENT\_TRANSACTION](/sql-reference/functions/current_transaction) , [DESCRIBE TRANSACTION](/sql-reference/sql/desc-transaction)

## Syntax

Copy code

```
LAST_TRANSACTION()
```

## Arguments

None

## Examples

This example calls the `LAST_TRANSACTION` function:

> Copy code
>
> ```
> SELECT LAST_TRANSACTION();
> ```
>
> Output:
>
> Copy code
>
> ```
> +---------------------+
> | LAST_TRANSACTION()  |
> |---------------------|
> | 1661899308790000000 |
> +---------------------+
> ```
