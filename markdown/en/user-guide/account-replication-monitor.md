# Monitoring replication and failover

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Database and share replication are available to all accounts.
- Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides information on how to monitor account replication progress, history, and costs.

## Use Snowsight to monitor replication

To monitor the replication progress and status for [replication and failover groups](/user-guide/account-replication-intro#label-replication-and-failover-groups) in an
organization, use the **Replication** page in Snowsight.

You can view the status and details of refresh operations, including:

- Current status of the most recent refresh operation.
- Replica lag time (time since the last refresh operation).
- Distribution of replica lag times across groups.
- Date and time of the next scheduled refresh operation.

Note

- Snowsight lists the replication and failover groups for which your role has the MONITOR, OWNERSHIP, or REPLICATE privilege.
- Refresh operation details are only available to users with the ACCOUNTADMIN role or the OWNERSHIP privilege on the group.
- You must be signed in to the source or target account to view refresh operation details. If you are not, you will be prompted to sign in.

  Both the source account and the target account must use the same connection type (public internet). Otherwise, signing in to
  the target account fails.
- Currently, if your account uses private connectivity, you can’t use Snowsight to create or modify groups or connection
  objects. However, you can use Snowsight to monitor groups that were created using SQL.

To view the replication status of each replication or failover group, complete the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Accounts**.
3. Select **Replication** and then select **Groups**.

The **Groups** page displays [refresh operation details](/user-guide/account-replication-monitor#label-ui-replication-groups-view) for all the groups for which your
role has a privilege to view. You can use the tiles to filter the view.

- For example, if the **Status** tile indicates there are failed refresh operations, you can select the tile to investigate the group(s)
  with failures.
- The lag time in the **Longest Replication lag** tile refers to the duration of time since the last refresh operation. This is the
  length of time that the secondary replication or failover group *lags* behind the primary group. The longest lag time is the
  length of time since the oldest secondary replication group was last refreshed.

  For example, if you have three failover groups, `fg_1`, `fg_2`, `fg_3`, with independent replication schedules of
  10 minutes, 2 hours, and 12 hours respectively, the longest lag time could be as long as 12 hours. If `fg_3`, however, was
  recently refreshed in the target account, its lag time resets to 0 and a different failover group could have a longer lag time.
- You can select an individual bar in the **Group Lag Distribution** tile to filter the results to an individual group.

You can also filter groups by using the search field or the dropdown menus:

- You can search by replication or failover group name using the [![Search icon](/static/images/snowsight/icons/search-icon.svg)](/static/images/snowsight/icons/search-icon.svg) (search) box.
- Choose **Type** to filter the results by replication or failover group.
- Choose **Replicating** to filter by primary (select **To**) or secondary groups (select **From**).
- Choose the [![Account icon](/static/images/snowsight/icons/account-icon.svg)](/static/images/snowsight/icons/account-icon.svg) (accounts) menu to filter the results by account name.
- Choose **Status** to filter results by refresh operation status:
  - **Refresh Cancelled**
  - **Refresh Failed**
  - **Refresh In Progress**
  - **Refresh Successful**

You can see the following details about your replication and failover groups:

| Column | Description |
| --- | --- |
| **Name** | Name of the replication or failover group. |
| **Is Replicating** | Indicates if the group is being replicated *to* a target account or *from* a source account.  If this column contains *destinations available*, there are no secondary replication or failover groups. The number of destinations available indicates the number of target accounts the primary group can be replicated to. |
| **Status** | Displays the status of the latest refresh operation.  You must be signed in to the source or target account in order to access replication details. If you are not signed in, select **Sign in** to view refresh operation status for the secondary group.  Both the source account and the target account must use the same connection type (public internet). Otherwise, signing in to the target account fails. |
| **Replication Lag** | The length of time since the last refresh operation. This is the length of time that the secondary replication group “lags” behind the primary replication group. |
| **Next Refresh** | The date and time of the next scheduled refresh operation. |

Expand

Show lessSee more

You can select a replication or failover group to view detailed information about each refresh operation. For more information, see
[the section on replication history in Snowsight](#label-replication-history-ui).

## Monitor the progress of refresh operations

This section provides information on how to monitor replication progress for a specific replication or failover group using either
Snowsight or SQL.

### Use Snowsight to monitor the progress of refresh operations

You can view the status of a refresh operation in progress and the details of historical refresh operations using Snowsight.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Accounts**.
3. Select **Replication**, select **Groups**.
4. Select the name of a replication or failover group.

Tip

If your account uses private connectivity, you can still use Snowsight to monitor groups.
Although creating or modifying groups or connection objects through Snowsight isn’t currently available
with private connectivity, Snowsight can monitor the groups that you create using SQL.

For more information about the detailed view, see [the section on replication history in Snowsight](#label-replication-history-ui).

### Use SQL to monitor the progress of refresh operations

To monitor the progress of a replication or failover group refresh, query the
[REPLICATION\_GROUP\_REFRESH\_PROGRESS, REPLICATION\_GROUP\_REFRESH\_PROGRESS\_BY\_JOB, REPLICATION\_GROUP\_REFRESH\_PROGRESS\_ALL](/sql-reference/functions/replication_group_refresh_progress) table function (in the [Snowflake Information Schema](/sql-reference/info-schema)).

#### Example

View the progress of the most recent refresh operation for the failover group `myfg`:

Copy code

```
SELECT phase_name, start_time, end_time, progress, details
  FROM TABLE(INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_PROGRESS('myfg'));
```

## View replication history

You can view replication history using Snowsight or using [SQL](#label-view-replication-history-using-sql).

Note

You can view the replication history for the replication and failover groups for which your role has the MONITOR, OWNERSHIP, or
REPLICATE privilege.

### Use Snowsight to view replication history

You can view the replication history and details for each refresh operation for a specific replication or failover group in the details
page for the group.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Accounts**.
3. Select **Replication**, select **Groups**.
4. Select the name of a replication or failover group.

You can review the following information about the group:

- Group type (replication group or failover group).
- Replication schedule (for example, every 10 minutes).
- Duration of each refresh operation.
- Replica lag time (length of time since last refresh operation).
- Date and time of the next scheduled refresh operation.

Tip

If your account uses private connectivity, you can still use Snowsight to monitor groups.
Although creating or modifying groups or connection objects through Snowsight isn’t currently available
with private connectivity, Snowsight can monitor the groups that you create using SQL.

You can filter the data on the page by status and time period:

- Choose **Status** to filter results by refresh operation status:

  - **Refresh Cancelled**
  - **Refresh Failed**
  - **Refresh In Progress**
  - **Refresh Successful**
- Choose **Duration** to show refresh operation details for:

  - **Last hour**
  - **Last 24 hours**
  - **Last 7 days**
  - **All**

  Selecting **All** displays the last 14 days of refresh operations.

The details for each refresh operation include the following columns:

| Column | Description |
| --- | --- |
| **Query ID** | Query ID of the refresh operation. |
| **Status** | Displays the status of the refresh operation. Valid values include `Successful`, `Failed`, `In Progress`. |
| **Ended** | Date and time the refresh operation ended. |
| **Duration** | The length of time the refresh operation took to complete.  The duration period is broken down and color coded by [replication phase](/sql-reference/functions/replication_group_refresh_progress#label-replication-phases). The width of each colored segment indicates the portion of the time spent in that phase.  The image below is for reference only. This graph is available when you [select the refresh operation](/user-guide/account-replication-monitor#label-ui-refresh-additional-details) for additional details. Color coded replication phase and duration. |
| **Transferred** | The number of bytes replicated. |
| **Objects** | The number of objects replicated. |

Expand

Show lessSee more

Select a row to view additional details about a specific refresh operation including:

- Duration of each replication phase.
- Error message (for failed refresh operations).
- List of database objects replicated by type and number.
- Number of databases replicated and database names.

### Use SQL to view replication history

To view the replication history of a specific replication or failover group within a specified date range, query one of the following:

- [REPLICATION\_GROUP\_REFRESH\_HISTORY, REPLICATION\_GROUP\_REFRESH\_HISTORY\_ALL](/sql-reference/functions/replication_group_refresh_history) table function (in the [Snowflake Information Schema](/sql-reference/info-schema)).
- [REPLICATION\_GROUP\_REFRESH\_HISTORY view](/sql-reference/account-usage/replication_group_refresh_history) (in [Account Usage](/sql-reference/account-usage)).

#### Examples

Query the Information Schema REPLICATION\_GROUP\_REFRESH\_HISTORY table function to view the account replication history of failover
group `myfg` in the last 7 days:

Copy code

```
SELECT PHASE_NAME, START_TIME, END_TIME, TOTAL_BYTES, OBJECT_COUNT
  FROM TABLE(information_schema.replication_group_refresh_history('myfg'))
  WHERE START_TIME >= CURRENT_DATE() - INTERVAL '7 days';
```

Query the Account Usage REPLICATION\_GROUP\_REFRESH\_HISTORY view to view the account replication history in the current month:

Copy code

```
SELECT REPLICATION_GROUP_NAME, PHASE_NAME, START_TIME, END_TIME, TOTAL_BYTES, OBJECT_COUNT
  FROM snowflake.account_usage.replication_group_refresh_history
  WHERE START_TIME >= DATE_TRUNC('month', CURRENT_DATE());
```

## Monitor replication costs

To monitor credit usage for replication, query one of the following:

- [REPLICATION\_GROUP\_USAGE\_HISTORY view](/sql-reference/account-usage/replication_group_usage_history) (in [Account Usage](/sql-reference/account-usage)).
- [REPLICATION\_GROUP\_USAGE\_HISTORY](/sql-reference/functions/replication_group_usage_history) table function (in the [Snowflake Information Schema](/sql-reference/info-schema)).

### Examples

Query the REPLICATION\_GROUP\_USAGE\_HISTORY table function to view credits used for account replication in the last 7 days:

Copy code

```
SELECT start_time, end_time, replication_group_name, credits_used, bytes_transferred
  FROM TABLE(information_schema.replication_group_usage_history(date_range_start=>DATEADD('day', -7, CURRENT_DATE())));
```

Query the Account Usage REPLICATION\_GROUP\_USAGE\_HISTORY view to view the credits used by replication or failover group for account
replication history in the current month:

Copy code

```
SELECT start_time,
  end_time,
  replication_group_name,
  credits_used,
  bytes_transferred
FROM snowflake.account_usage.replication_group_usage_history
WHERE start_time >= DATE_TRUNC('month', CURRENT_DATE());
```

## Monitor replication costs for databases

The cost for replication for an individual database included in a replication or failover group can be calculated by retrieving the
number of copied bytes for the database and associating it with the credits used.

### Examples

#### Query Account Usage views

The following examples calculate the costs for database replication in one replication group for the past 30 days.

1. Query the REPLICATION\_GROUP\_REFRESH\_HISTORY Account Usage view and calculate the sum of the number of bytes replicated per database.

   For example, to calculate the sum of the number of bytes replicated for databases in the replication group `myrg` in the last
   30 days:

   Copy code

   ```
   SELECT SUM(value:totalBytesToReplicate) as sum_database_bytes
     FROM snowflake.account_usage.replication_group_refresh_history rh,
    LATERAL FLATTEN(input => rh.total_bytes:databases)
     WHERE rh.replication_group_name = 'MYRG' AND
        rh.start_time >= CURRENT_DATE() - INTERVAL '30 days';
   ```

   Note the output of the sum of database bytes:

   ```
   +--------------------+
   | SUM_DATABASE_BYTES |
   |--------------------|
   |              22016 |
   +--------------------+
   ```
2. Query the REPLICATION\_GROUP\_USAGE\_HISTORY Account Usage view and calculate the sum of the number of credits used and the sum
   of the bytes transferred for replication.

   For example, to calculate the sum of the number of credits used and the sum of the bytes transferred for replication of the
   replication group `myrg` in the last 30 days:

   Copy code

   ```
   SELECT SUM(credits_used) AS credits_used, SUM(bytes_transferred) AS bytes_transferred
     FROM snowflake.account_usage.replication_group_usage_history
     WHERE replication_group_name = 'MYRG' AND
        start_time >= CURRENT_DATE() - INTERVAL '30 days';
   ```

   Note the output of the sum of the credits used and the sum of bytes transferred:

   ```
   +--------------+-------------------+
   | CREDITS_USED | BYTES_TRANSFERRED |
   |--------------+-------------------|
   |  1.357923604 |             22013 |
   +--------------+-------------------+
   ```
3. Calculate the replication costs for databases using the values of the bytes transferred for databases, sum of the credits used, and
   the sum of all bytes transferred for replication from the previous two steps:

   `(<database_bytes_transferred> / <bytes_transferred>) * <credits_used>`

   For example:

   `(22016 / 22013) * 1.357923604 = 1.35810866`

#### Query Information Schema table functions

For refresh operations within the past 14 days, query the associated Information Schema table functions.

- [REPLICATION\_GROUP\_REFRESH\_HISTORY, REPLICATION\_GROUP\_REFRESH\_HISTORY\_ALL](/sql-reference/functions/replication_group_refresh_history)
- [REPLICATION\_GROUP\_USAGE\_HISTORY](/sql-reference/functions/replication_group_usage_history)

1. Query the REPLICATION\_GROUP\_REFRESH\_HISTORY table function to view the sum of the number of bytes copied for database replication
   for the replication group `myrg`:

   Copy code

   ```
   SELECT SUM(value:totalBytesToReplicate)
     FROM TABLE(information_schema.replication_group_refresh_history('myrg')) AS rh,
     LATERAL FLATTEN(input => total_bytes:databases)
     WHERE rh.phase_name = 'COMPLETED' AND
        rh.start_time >= CURRENT_DATE() - INTERVAL '14 days';
   ```
2. Query the REPLICATION\_GROUP\_USAGE\_HISTORY table function to view sum of the number of credits used and the sum of the bytes
   transferred for replication for the replication group `myrg`:

   Copy code

   ```
   SELECT SUM(credits_used), SUM(bytes_transferred)
     FROM TABLE(information_schema.replication_group_usage_history(
    date_range_start => DATEADD('day', -14, CURRENT_DATE()),
    replication_group_name => 'myrg'));
   ```
