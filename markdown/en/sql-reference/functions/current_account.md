Categories:
:   [Context functions](/sql-reference/functions-context) (Session)

# CURRENT\_ACCOUNT

Returns the [account locator](/user-guide/admin-account-identifier#label-account-locator) used by the user’s current session.

Note

If you want to find the [account name](/user-guide/admin-account-identifier#label-account-name) rather than the account locator, use
[CURRENT\_ACCOUNT\_NAME](/sql-reference/functions/current_account_name) instead. The preferred account identifier (`orgname-account_name`) uses
the account name, not the account locator.

## Syntax

Copy code

```
CURRENT_ACCOUNT()
```

## Arguments

None.

## Returns

The data type of the returned value is `VARCHAR`.

## Examples

This shows how to call the `CURRENT_ACCOUNT` function:

> Copy code
>
> ```
> SELECT CURRENT_ACCOUNT();
> ```
>
> Output:
>
> Copy code
>
> ```
> +-------------------+
> | CURRENT_ACCOUNT() |
> |-------------------|
> | XY12345           |
> +-------------------+
> ```
