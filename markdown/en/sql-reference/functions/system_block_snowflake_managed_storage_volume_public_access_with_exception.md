Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$BLOCK\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS\_WITH\_EXCEPTION

Prevents public traffic from accessing the Snowflake-managed storage volume of the current Snowflake account on Microsoft Azure, while
allowing access from specified IP addresses or CIDR blocks.

This function is similar to
[SYSTEM$BLOCK\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS](/sql-reference/functions/system_block_snowflake_managed_storage_volume_public_access). Instead of blocking all
public IP addresses, this function maintains an allowlist of IP addresses or CIDR blocks that are still permitted to access the
Snowflake-managed storage volume.

Calling SYSTEM$BLOCK\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS\_WITH\_EXCEPTION when an allowlist already exists replaces the
existing allowlist with the new one.

For more information, see [Blocking public access](/user-guide/private-managed-volumes-azure#label-private-snowflake-managed-storage-volumes-azure-block-public).

Important

Confirm that traffic via private connectivity is successfully reaching the Snowflake-managed storage volume before blocking
public access. Blocking public access without configuring private connectivity can cause unintended disruptions.

See also:
:   [SYSTEM$UNBLOCK\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS](/sql-reference/functions/system_unblock_snowflake_managed_storage_volume_public_access),
    [SYSTEM$BLOCK\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS](/sql-reference/functions/system_block_snowflake_managed_storage_volume_public_access),
    [SYSTEM$SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PUBLIC\_ACCESS\_STATUS](/sql-reference/functions/system_snowflake_managed_storage_volume_public_access_status)

## Syntax

Copy code

```
SYSTEM$BLOCK_SNOWFLAKE_MANAGED_STORAGE_VOLUME_PUBLIC_ACCESS_WITH_EXCEPTION( '<ip_address_or_cidr_range>' [ , '<ip_address_or_cidr_range>' , ... ] )
```

## Arguments

`'ip_address_or_cidr_range'`
:   A string that specifies one of the following:

    - A single IP address, such as `'100.0.0.1'`.
    - A range of IP addresses using Classless Inter-Domain Routing (CIDR) notation:

      `ip_address/prefix_length`

      For example, `'1.2.3.0/24'` or `'101.0.0.0/31'`.

    IP addresses or CIDR ranges specified in this argument are allowed to access the Snowflake-managed storage volume. Specify multiple values
    as separate, comma-separated arguments.

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

- Only account administrators, that is, users with the ACCOUNTADMIN role, can execute this function.
- This function can take a few minutes to finish executing.
- This function can be used with Snowflake accounts on Microsoft Azure only. Amazon Web Services and Google Cloud are not supported.
- Calling this function replaces any existing IP allowlist. To modify the allowlist, call the function again with the complete
  updated list.

## Examples

Block public access while allowing specific IP addresses and CIDR blocks:

Copy code

```
USE ROLE ACCOUNTADMIN;

SELECT SYSTEM$BLOCK_SNOWFLAKE_MANAGED_STORAGE_VOLUME_PUBLIC_ACCESS_WITH_EXCEPTION('100.0.0.1', '1.2.3.4/24', '101.0.0.0/31');
```
