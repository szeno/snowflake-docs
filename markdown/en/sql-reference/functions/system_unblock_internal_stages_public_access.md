Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$UNBLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS

[Business Critical Feature](/user-guide/intro-editions)

This function requires Business Critical (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Allows traffic from public IP addresses to access the internal stage of the current Snowflake account on Microsoft Azure.

This function reverses the Azure settings on the internal stage’s Azure storage account that were made when
SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS was executed. For details about these Azure settings, refer to [Unblocking public access](/user-guide/private-internal-stages-azure#label-private-internal-stage-azure-unblock-public).

See also:
:   [SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS](/sql-reference/functions/system_block_internal_stages_public_access), [SYSTEM$INTERNAL\_STAGES\_PUBLIC\_ACCESS\_STATUS](/sql-reference/functions/system_internal_stages_public_access_status)

## Syntax

> Copy code
>
> ```
> SYSTEM$UNBLOCK_INTERNAL_STAGES_PUBLIC_ACCESS()
> ```

## Arguments

None.

## Returns

This function returns the following status messages:

| Status Message | Description |
| --- | --- |
| Public Access to internal stages is unblocked | Indicates that the function successfully unblocked public access. |
| Azure Error when attempting to unblock public access to internal stages. Please contact Snowflake support. | Indicates that the function was unable to change the Azure settings in order to unblock public access. |

Expand

Show lessSee more

## Usage notes

- Only account administrators (i.e. users with the ACCOUNTADMIN role) can execute this function.
- This function can take a few minutes to finish executing.
- This function can be used with Snowflake accounts on Azure only. AWS and Google Cloud Platform are not supported.

## Examples

Allow public IP addresses to access the Azure internal stage.

> Copy code
>
> ```
> USE ROLE accountadmin;
>
> SELECT SYSTEM$UNBLOCK_INTERNAL_STAGES_PUBLIC_ACCESS();
> ```
