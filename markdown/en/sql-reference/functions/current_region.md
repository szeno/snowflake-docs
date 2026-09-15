Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# CURRENT\_REGION

Returns the name of the region for the account where the current user is logged in.

For organizations that have accounts in multiple [region groups](/user-guide/admin-account-identifier#label-region-groups), returns `region_group.region`.

## Syntax

Copy code

```
CURRENT_REGION()
```

## Arguments

None.

## Examples

Show the current region:

> Copy code
>
> ```
> SELECT CURRENT_REGION();
> ```
>
> Output:
>
> Copy code
>
> ```
> +------------------+
> | CURRENT_REGION() |
> |------------------|
> | AWS_US_WEST_2    |
> +------------------+
> ```

Show the current region when the current user is logged into an account in an organization that spans multiple region groups:

> Copy code
>
> ```
> SELECT CURRENT_REGION();
> ```
>
> Output:
>
> Copy code
>
> ```
> +----------------------+
> | CURRENT_REGION()     |
> |----------------------|
> | PUBLIC.AWS_US_WEST_2 |
> +----------------------+
> ```
