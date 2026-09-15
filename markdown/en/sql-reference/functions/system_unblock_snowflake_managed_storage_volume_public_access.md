Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$UNBLOCK\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS

Allows traffic from public IP addresses to access the Snowflake-managed storage volume of the current Snowflake account on
Microsoft Azure.

This function reverses the Azure settings on the managed storage volume’s Azure storage account that were made when
SYSTEM$BLOCK\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS was executed. For details about these Azure settings, refer to
[Blocking public access](/user-guide/private-managed-volumes-azure#label-private-snowflake-managed-storage-volumes-azure-block-public).

See also:
:   [SYSTEM$BLOCK\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS](/sql-reference/functions/system_block_snowflake_managed_storage_volume_public_access),
    [SYSTEM$SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS\_STATUS](/sql-reference/functions/system_snowflake_managed_storage_volume_public_access_status)

## Syntax

> Copy code
>
> ```
> SYSTEM$UNBLOCK_SNOWFLAKE_MANAGED_STORAGE_VOLUME_PUBLIC_ACCESS()
> ```

## Arguments

None.

## Returns

This function returns the following status messages:

| Status Message | Description |
| --- | --- |
| Public Access to Snowflake-managed storage volumes is unblocked | Indicates that the function successfully unblocked public access. |
| Azure Error when attempting to unblock public access to Snowflake-managed storage volumes. Please contact Snowflake support. | Indicates that the function was unable to change the Azure settings in order to unblock public access. |
| No interop volumes configured on account | Indicates that there are no Snowflake-managed storage volumes configured for the account. |

Expand

Show lessSee more

## Usage notes

- Only account administrators (that is, users with the ACCOUNTADMIN role) can execute this function.
- This function can take a few minutes to finish executing.
- This function can be used with Snowflake accounts on Azure only. AWS and Google Cloud are not supported.

## Examples

Allow public IP addresses to access the Azure Snowflake-managed storage volume.

> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
>
> SELECT SYSTEM$UNBLOCK_SNOWFLAKE_MANAGED_STORAGE_VOLUME_PUBLIC_ACCESS();
> ```
