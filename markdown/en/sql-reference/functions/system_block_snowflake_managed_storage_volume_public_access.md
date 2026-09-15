Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$BLOCK\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS

Prevents all public traffic from accessing the Snowflake-managed storage volume of the current Snowflake account on Microsoft
Azure.

This function uses settings for the managed storage volume’s Azure storage account to block public IP addresses. For details on
which Azure settings are affected, refer to [Blocking public access](/user-guide/private-managed-volumes-azure#label-private-snowflake-managed-storage-volumes-azure-block-public).

Important

Confirm that traffic via private connectivity is successfully reaching the managed storage volume before blocking
public access. Blocking public access without configuring private connectivity can cause unintended disruptions.

See also:
:   [SYSTEM$UNBLOCK\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS](/sql-reference/functions/system_unblock_snowflake_managed_storage_volume_public_access),
    [SYSTEM$SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS\_STATUS](/sql-reference/functions/system_snowflake_managed_storage_volume_public_access_status)

## Syntax

> Copy code
>
> ```
> SYSTEM$BLOCK_SNOWFLAKE_MANAGED_STORAGE_VOLUME_PUBLIC_ACCESS()
> ```

## Arguments

None.

## Returns

This function returns the following status messages:

| Status Message | Description |
| --- | --- |
| Public Access to Snowflake-managed storage volumes is blocked. | Indicates that the function successfully blocked public access. |
| Network config is not found, Please contact support | Indicates that there is a problem with the system parameters. |
| No interop volumes configured on account | Indicates that there are no Snowflake-managed storage volumes configured for the account. |
| Azure Error when attempting to block public access to Snowflake-managed storage volumes. Please contact Snowflake support. | Indicates that the function was unable to change the Azure settings in order to block public access. |

Expand

Show lessSee more

## Usage notes

- Only account administrators (that is, users with the ACCOUNTADMIN role) can execute this function.
- This function can take a few minutes to finish executing.
- This function can be used with Snowflake accounts on Azure only. AWS and Google Cloud are not supported.

## Examples

Block all public traffic trying to access the Snowflake-managed storage volume of an Azure account.

> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
>
> SELECT SYSTEM$BLOCK_SNOWFLAKE_MANAGED_STORAGE_VOLUME_PUBLIC_ACCESS();
> ```
