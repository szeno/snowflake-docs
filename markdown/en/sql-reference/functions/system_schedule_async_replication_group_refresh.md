Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$SCHEDULE\_ASYNC\_REPLICATION\_GROUP\_REFRESH

Starts a refresh operation for a replication group or a failover group, in the background.
You can call this function in a stored procedure to begin one or more refresh operations
and continue doing work while the refreshes are in progress.

See also:
:   [Replication groups and failover groups](/user-guide/account-replication-intro#label-replication-and-failover-groups),
    [ALTER REPLICATION GROUP](/sql-reference/sql/alter-replication-group),
    [ALTER FAILOVER GROUP](/sql-reference/sql/alter-failover-group),
    [REPLICATION\_GROUP\_REFRESH\_HISTORY view](/sql-reference/organization-usage/replication_group_refresh_history)

## Syntax

Copy code

```
SYSTEM$SCHEDULE_ASYNC_REPLICATION_GROUP_REFRESH(<replication_group_name>)
SYSTEM$SCHEDULE_ASYNC_REPLICATION_GROUP_REFRESH(<failover_group_name>)
```

## Arguments

`'replication_group_name'` or `'failover_group_name'`
:   The name of the replication group or failover group to refresh.

## Usage notes

- This function has the same effect as an
  ALTER REPLICATION GROUP … REFRESH or ALTER FAILOVER GROUP … REFRESH command,
  but doesn’t wait for the operation to complete.
- Only account administrators (that is, users with the ACCOUNTADMIN role) can execute this function.
- This function must be executed from the secondary account.

## Examples

Start refreshing two failover groups simultaneously:

> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
>
> SELECT SYSTEM$SCHEDULE_ASYNC_REPLICATION_GROUP_REFRESH('failover_group_1');
> SELECT SYSTEM$SCHEDULE_ASYNC_REPLICATION_GROUP_REFRESH('failover_group_2');
> ```
