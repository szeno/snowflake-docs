Categories:
:   [Context functions](/sql-reference/functions-context) (Session)

# CURRENT\_TRANSACTION

Returns the transaction id of an open transaction in the current session.

See also:
:   [LAST\_TRANSACTION](/sql-reference/functions/last_transaction) , [DESCRIBE TRANSACTION](/sql-reference/sql/desc-transaction)

## Syntax

Copy code

```
CURRENT_TRANSACTION()
```

## Arguments

None.

## Examples

This shows the transaction ID of the current transaction:

> Copy code
>
> ```
> SELECT CURRENT_TRANSACTION();
> ```
>
> Output:
>
> Copy code
>
> ```
> +-----------------------+
> | CURRENT_TRANSACTION() |
> |-----------------------|
> | 1661899308790000000   |
> +-----------------------+
> ```
