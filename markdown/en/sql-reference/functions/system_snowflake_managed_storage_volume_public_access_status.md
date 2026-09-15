Categories:
:   [System functions](/sql-reference/functions-system) (Information)

# SYSTEM$SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS\_STATUS

Checks to see whether public IP addresses are allowed to access the Snowflake-managed storage volume of the current Snowflake
account on Microsoft Azure.

See also:
:   [SYSTEM$BLOCK\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS](/sql-reference/functions/system_block_snowflake_managed_storage_volume_public_access),
    [SYSTEM$UNBLOCK\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS](/sql-reference/functions/system_unblock_snowflake_managed_storage_volume_public_access)

## Syntax

> Copy code
>
> ```
> SYSTEM$SNOWFLAKE_MANAGED_STORAGE_VOLUME_PUBLIC_ACCESS_STATUS()
> ```

## Arguments

None.

## Returns

This function returns the following status messages:

| Status Message | Description |
| --- | --- |
| Public Access to Snowflake-managed storage volumes is blocked | Indicates that the Azure settings that control access to the Snowflake-managed storage volume are currently blocking all public IP addresses. |
| Public Access to Snowflake-managed storage volumes is unblocked | Indicates that at least some public IP addresses can access the Snowflake-managed storage volume. |
| No interop volumes configured on account | Indicates that there are no Snowflake-managed storage volumes configured for the account. |

Expand

Show lessSee more

## Usage notes

- Only account administrators (that is, users with the ACCOUNTADMIN role) can execute this function.
- This function can take a few minutes to finish executing.
- This function can be used with Snowflake accounts on Azure only. AWS and Google Cloud are not supported.

## Examples

> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
>
> SELECT SYSTEM$SNOWFLAKE_MANAGED_STORAGE_VOLUME_PUBLIC_ACCESS_STATUS();
> ```
>
> ```
> Public Access to Snowflake-managed storage volumes is blocked
> ```
