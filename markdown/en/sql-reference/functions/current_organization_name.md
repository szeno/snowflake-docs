Categories:
:   [Context functions](/sql-reference/functions-context) (Session)

# CURRENT\_ORGANIZATION\_NAME

Returns the name of the organization to which the current account belongs.

## Syntax

Copy code

```
CURRENT_ORGANIZATION_NAME()
```

## Arguments

None.

## Returns

The data type of the returned value is `VARCHAR`.

## Example

This shows how to call the CURRENT\_ORGANIZATION\_NAME function:

> Copy code
>
> ```
> SELECT CURRENT_ORGANIZATION_NAME();
> ```
>
> Output:
>
> ```
> +-----------------------------+
> | CURRENT_ORGANIZATION_NAME() |
> |-----------------------------|
> | bazco                       |
> +-----------------------------+
> ```
