Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$SHOW\_MOVE\_ORGANIZATION\_ACCOUNT\_STATUS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts that are Enterprise Edition (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the status of an attempt to move an [organization account](/user-guide/organization-accounts).

See also:
:   [SYSTEM$INITIATE\_MOVE\_ORGANIZATION\_ACCOUNT](/sql-reference/functions/system_initiate_move_organization_account) , [SYSTEM$COMMIT\_MOVE\_ORGANIZATION\_ACCOUNT](/sql-reference/functions/system_commit_move_organization_account)

## Syntax

Copy code

```
SYSTEM$SHOW_MOVE_ORGANIZATION_ACCOUNT_STATUS( )
```

## Arguments

None.

## Returns

The following are the possible statuses:

| Code | Status |
| --- | --- |
| 060050 | Move of the current organization account has been initiated. |
| 060051 | Created a new organization account as the destination for migrating the existing organization account. |
| 060052 | Objects are being replicated from the current organization account to the target organization account. Target organization account is currently locked and not ready for use. |
| 060053 | Initial replication of objects is complete and the target organization account is ready to be reviewed. If you are ready to proceed with the move please run SYSTEM$COMMIT\_MOVE\_ORGANIZATION\_ACCOUNT(<GRACE\_PERIOD\_IN\_DAYS>). |
| 060054 | Commit of organization account move in progress. |
| 060055 | The move has been completed successfully. The original organization account is locked and will be deleted in x days. |
| 060056 | The organization account move failed. |
| 060057 | Cannot fetch status of organization account move. |

Expand

Show lessSee more

## Access control requirements

Only users with the GLOBALORGADMIN role can call this function.

## Usage notes

Only shows the status of the latest attempt to move the organization account.

## Example

Copy code

```
SELECT SYSTEM$SHOW_MOVE_ORGANIZATION_ACCOUNT_STATUS();
```
