Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS\_WITH\_EXCEPTION

[Business Critical Feature](/user-guide/intro-editions)

This function requires Business Critical (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Prevents public traffic from accessing the internal stage of the current Snowflake account on Microsoft Azure, while allowing
access from specified IP addresses or CIDR blocks.

This function is similar to [SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS](/sql-reference/functions/system_block_internal_stages_public_access). Instead of blocking
all public IP addresses, this function maintains an allowlist of IP addresses or CIDR blocks that are still permitted to access
the internal stage.

Calling SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS\_WITH\_EXCEPTION when an allowlist already exists replaces the existing allowlist with the
new one.

For more information, see [Blocking public access with IP allowlist exceptions](/user-guide/private-internal-stages-azure#label-private-internal-stage-block-public-with-exceptions).

Important

Confirm that traffic via private connectivity is successfully reaching the internal stage before blocking public access.
Blocking public access without configuring private connectivity can cause unintended disruptions, including interference with
managed services like Microsoft Azure Data Factory.

See also:
:   [SYSTEM$UNBLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS](/sql-reference/functions/system_unblock_internal_stages_public_access),
    [SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS](/sql-reference/functions/system_block_internal_stages_public_access),
    [SYSTEM$INTERNAL\_STAGES\_PUBLIC\_ACCESS\_STATUS](/sql-reference/functions/system_internal_stages_public_access_status)

## Syntax

Copy code

```
SYSTEM$BLOCK_INTERNAL_STAGES_PUBLIC_ACCESS_WITH_EXCEPTION( '<ip_address_or_cidr_range>' [ , '<ip_address_or_cidr_range>' , ... ] )
```

## Arguments

`'ip_address_or_cidr_range'`
:   A string that specifies one of the following:

    - A single IP address, such as `'100.0.0.1'`.
    - A range of IP addresses using Classless Inter-Domain Routing (CIDR) notation:

      `ip_address/prefix_length`

      For example, `'1.2.3.0/24'` or `'101.0.0.0/31'`.

    IP addresses or CIDR ranges specified in this argument are allowed to access the internal stage. Specify multiple values as
    separate, comma-separated arguments.

## Returns

This function returns the following status messages:

| Status Message | Description |
| --- | --- |
| Public Access to internal stages is blocked. Private link is required to connect to internal stages of this account. Exceptions: <ip\_or\_cidr\_list> | Indicates that the function successfully blocked public access and set the specified IP allowlist. |
| Network config is not found, Please contact support | Indicates that there is a problem with the system parameters. |
| Microsoft Azure Error when attempting to block public access to internal stages. Please contact Snowflake support. | Indicates that the function was unable to change the Microsoft Azure settings in order to block public access. |

Expand

Show lessSee more

## Usage notes

- Only account administrators, that is users with the ACCOUNTADMIN role can execute this function.
- This function can take a few minutes to finish executing.
- This function can be used with Snowflake accounts on Microsoft Azure only. Amazon Web Services and Google Cloud are not supported.
- Calling this function replaces any existing IP allowlist. To modify the allowlist, call the function again with the complete
  updated list.

## Examples

Block public access while allowing specific IP addresses and CIDR blocks:

Copy code

```
USE ROLE ACCOUNTADMIN;

SELECT SYSTEM$BLOCK_INTERNAL_STAGES_PUBLIC_ACCESS_WITH_EXCEPTION(100.0.0.1, '1.2.3.4/24, 101.0.0.0/31');
```
