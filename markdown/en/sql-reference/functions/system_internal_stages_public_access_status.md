Categories:
:   [System functions](/sql-reference/functions-system) (Information)

# SYSTEM$INTERNAL\_STAGES\_PUBLIC\_ACCESS\_STATUS

[Business Critical Feature](/user-guide/intro-editions)

This function requires Business Critical (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Checks to see whether public IP addresses are allowed to access the internal stage of the current Snowflake account on Microsoft Azure.

See also:
:   [SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS](/sql-reference/functions/system_block_internal_stages_public_access) , [SYSTEM$UNBLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS](/sql-reference/functions/system_unblock_internal_stages_public_access)

## Syntax

> Copy code
>
> ```
> SYSTEM$INTERNAL_STAGES_PUBLIC_ACCESS_STATUS()
> ```

## Arguments

None.

## Returns

This function returns the following status messages:

| Status Message | Description |
| --- | --- |
| Public Access to internal stages is blocked | Indicates that the Azure settings that control access to the internal stage are currently blocking all public IP addresses. |
| Public Access to internal stages is unblocked | Indicates that at least some public IP addresses can access the internal stage. |

Expand

Show lessSee more

## Usage notes

- Only account administrators (i.e. users with the ACCOUNTADMIN role) can execute this function.
- This function can take a few minutes to finish executing.
- This function can be used with Snowflake accounts on Azure only. AWS and Google Cloud are not supported.

## Examples

> Copy code
>
> ```
> USE ROLE accountadmin;
>
> SELECT SYSTEM$INTERNAL_STAGES_PUBLIC_ACCESS_STATUS();
> ```
>
> ```
> Public Access to internal stages is blocked
> ```
