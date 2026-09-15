Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$COMMIT\_MOVE\_ORGANIZATION\_ACCOUNT

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts that are Enterprise Edition (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Finalizes the process of moving an [organization account](/user-guide/organization-accounts) from one region to another.

The process of moving the organization account began when the [SYSTEM$INITIATE\_MOVE\_ORGANIZATION\_ACCOUNT](/sql-reference/functions/system_initiate_move_organization_account) was
called.

See also:
:   [SYSTEM$INITIATE\_MOVE\_ORGANIZATION\_ACCOUNT](/sql-reference/functions/system_initiate_move_organization_account) , [SYSTEM$SHOW\_MOVE\_ORGANIZATION\_ACCOUNT\_STATUS](/sql-reference/functions/system_show_move_organization_account_status)

## Syntax

Copy code

```
SYSTEM$COMMIT_MOVE_ORGANIZATION_ACCOUNT( <grace_period> )
```

## Arguments

`grace_period`
:   Specifies the number of days after which the organization account in the original region (that is, the source region) will be deleted.

## Access control requirements

Only users with the GLOBALORGADMIN role can call this function.

## Usage notes

- You are automatically logged out of Snowflake immediately after calling this function.
- Until the process of finalizing the move completes (usually within a few minutes), you cannot sign in to the organization account in the
  source region nor the organization account in the target region.
- When the finalization process completes, the name of the organization account in the new region changes from the temporary name that was
  specified by the [SYSTEM$INITIATE\_MOVE\_ORGANIZATION\_ACCOUNT](/sql-reference/functions/system_initiate_move_organization_account) function to the original name of the
  organization account.
- To check the status of the finalization process, call the [SYSTEM$SHOW\_MOVE\_ORGANIZATION\_ACCOUNT\_STATUS](/sql-reference/functions/system_show_move_organization_account_status)
  function.

## Examples

Delete the original organization account 14 days after the move is finalized:

Copy code

```
SELECT SYSTEM$COMMIT_MOVE_ORGANIZATION_ACCOUNT(14);
```
