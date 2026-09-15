Categories:
:   [Context functions](/sql-reference/functions-context) (Session)

# CURRENT\_ACCOUNT\_NAME

Returns the name of the current account.

The preferred [account identifier](/user-guide/admin-account-identifier#label-account-name) for the account consists of this account name along with the organization of the account (`orgname-account_name`).

## Syntax

Copy code

```
CURRENT_ACCOUNT_NAME()
```

## Arguments

None.

## Returns

Returns the name of the current account.

The data type of the returned value is `VARCHAR`.

## Example

This shows how to call the CURRENT\_ACCOUNT\_NAME function:

> Copy code
>
> ```
> SELECT CURRENT_ACCOUNT_NAME();
> ```
>
> Output:
>
> ```
> +-----------------------------+
> | CURRENT_ACCOUNT_NAME()      |
> |-----------------------------|
> | my_account1                 |
> +-----------------------------+
> ```
