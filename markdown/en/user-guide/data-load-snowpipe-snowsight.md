# Manage Snowpipe in Snowsight

In Snowsight, you can check the health of a [pipe](/user-guide/data-load-snowpipe-intro) and manage it without writing SQL. You can do the following:

- See whether a pipe is running, paused, or stopped, and how many files are waiting to load.
- Review which files the pipe loaded, partially loaded, or failed to load.
- Track success rates, row counts, and gaps between loads over time.
- See how the pipe connects stages and tables in a lineage graph.
- Pause, resume, refresh, or drop a pipe, transfer its ownership, or edit its comment.

## Before you begin

The privileges that you need depend on the task:

| Task | Required privileges |
| --- | --- |
| View pipe details | `MONITOR` or `OWNERSHIP` on the pipe, or `MONITOR EXECUTION` on the account |
| View copy history | Any privilege on the target table, or `MONITOR` on the account |
| Pause or resume a pipe | `OPERATE` or `OWNERSHIP` on the pipe |
| Refresh a pipe | `OPERATE` or `OWNERSHIP` on the pipe, `USAGE` on an external stage or `READ` on an internal stage, `USAGE` on a named file format, and `SELECT` and `INSERT` on the target table |
| Edit the comment or drop the pipe | `OWNERSHIP` on the pipe |
| Transfer ownership | `OWNERSHIP` on the pipe and `INSERT` on the target table |

Expand

Show lessSee more

Every task also requires the `USAGE` privilege on the database and schema that contain each object that the task uses, such as the pipe, the stage, or the target table. For the privileges to create and own pipes, see [Snowpipe access control](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-access-control). For all pipe privileges, see [Pipe privileges](/user-guide/security-access-control-privileges#label-access-control-privileges-pipe).

## View pipe details

To open the details page for a pipe, complete the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Explorer**.
3. Expand the database and schema that contain the pipe.

   ![Screenshot of a pipe listed under a schema in the Snowsight object explorer](/static/images/snowsight/ui-snowpipe-intro.png)
4. Select the pipe.

![Screenshot of the Pipe Details page in Snowsight](/static/images/snowsight/ui-snowpipe-details.png)

The **Pipe Details** page shows the following information:

- The [status of the pipe](/sql-reference/functions/system_pipe_status#label-snowpipe-status), such as **Running** or **Paused**. If the pipe stopped loading files, see [Pipe execution states](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-execution-states).
- The number of files that are waiting to load, and when the pipe last loaded a file.
- The compute that the pipe uses, which is always **Serverless**.
- The [notification channel](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-stages-integrations) that tells the pipe when new files arrive.
- A lineage graph of the stages and tables that the pipe connects.
- The most recent loads.
- The pipe definition, which is the SQL statement that created the pipe.
- The [privileges](/user-guide/security-access-control-configure#label-snowsight-manage-object-privileges) granted on the pipe.

## Review copy history and pipe metrics

To review the files that a pipe processed, open the **Pipe Details** page, and then select the **Copy History** tab.

![Screenshot of the Copy History tab for a pipe in Snowsight](/static/images/snowsight/ui-snowpipe-copy-history.png)

The tab lists each file with its **STATUS**, **DURATION**, **ROWS**, **SIZE**, and **FILE NAME**. To find a specific file, search by file name, status, or date.

To find out why a file failed to load, see [Step 3: Get details about load errors](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-check-files). To load a file again after you fix it, see [Reload a file that Snowpipe already processed](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-reload-files).

A histogram shows up to 14 days of copy history. You can display one of the following measures, by day or by hour:

- **Copies** (default): The number of files processed, grouped by status. Use this measure to find failed loads and to follow ingestion trends.
- **Rows**: The number of rows inserted. Use this measure to follow throughput.
- **Duration**: The time that the pipe took to load files. Snowpipe is billed by data volume rather than by load time. For more information, see [Snowpipe costs](/user-guide/data-load-snowpipe-billing).

The pipe metrics show the health of the pipe for the selected time range:

- **Success rate**: The percentage of files that loaded successfully.
- **Max ingestion gap**: The longest gap between loads, which can reveal interruptions in continuous loading.
- **Time since last ingestion**: How long ago the pipe last loaded a file.
- **Min row count**: The smallest number of rows in a loaded file, which can reveal empty files or files with fewer rows than expected.
- **Pending files**: The number of files that the pipe detected but hasn’t loaded yet.

To get notified about failed loads instead of checking this page, set up [error notifications](/user-guide/data-load-snowpipe-errors) or an [alert on Snowpipe events](/user-guide/data-load-snowpipe-monitor-events#label-snowpipe-events-alerts).

## Manage a pipe

From the **Pipe Details** page, select the [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) menu in the top-right corner, and then select one of the following options:

- **Pause** or **Resume**: Stop or restart loading. While a pipe is paused, Snowflake keeps adding new files to the pipe’s queue, and each queued file stays in the queue for up to 14 days. To resume a pipe that was paused for longer, see [Resume a stale pipe](/user-guide/data-load-snowpipe-manage#label-snowpipe-resume-stale-pipe).
- **Manual Refresh**: Queue files that the pipe missed. For more information, see [Load files that the pipe missed](#label-snowsight-pipe-manual-refresh).
- **Edit**: Change the pipe’s comment. To change other properties, use SQL. You can set properties such as `ERROR_INTEGRATION` and `LOG_EVENT_LEVEL` with [ALTER PIPE](/sql-reference/sql/alter-pipe), but you must recreate the pipe to change its `COPY INTO` statement. For more information, see [Change or recreate a pipe](/user-guide/data-load-snowpipe-manage#label-snowpipe-management-recreate-pipes).
- **Transfer Ownership**: Give ownership of the pipe to another role. For the steps, see [Transfer ownership of a pipe](#label-snowsight-pipe-transfer-ownership).
- **Drop**: Delete the pipe. Dropping a pipe also deletes its load metadata, which is the record of the files that the pipe already processed.

### Load files that the pipe missed

To queue staged files that the pipe hasn’t processed yet, open the **Pipe Details** page, select the [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) menu in the top-right corner, and then select **Manual Refresh**.

Use this option to recover files that the pipe missed, such as files that were staged before you set up event notifications. Files that failed to load aren’t queued again; to reload them, see [Reload a file that Snowpipe already processed](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-reload-files). For files that were staged more than 7 days ago, see [Files staged more than 7 days ago](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-backfill).

After you refresh, check **Pending files** on the **Pipe Details** page to confirm that the files are queued, and then follow their progress on the **Copy History** tab.

Important

Don’t use **Manual Refresh** within 7 days after you recreate a pipe. The new pipe has no load metadata, so a refresh can load files that the old pipe already loaded. Instead, use `ALTER PIPE ... REFRESH` with `MODIFIED_AFTER`, as described in [Recreate a pipe safely](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-recreate-steps).

### Transfer ownership of a pipe

To transfer ownership of a pipe to another role, complete the following steps:

1. Make sure that the new owner role has the privileges in the **Own a pipe** column of [Snowpipe access control](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-access-control). Without them, the pipe stops loading after you resume it.
2. On the **Pipe Details** page, select the [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) menu, and then select **Pause**. The transfer fails while the pipe is running.
3. Select the [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) menu again, select **Transfer Ownership**, and then select the new owner role.
4. Switch to the new owner role, and then check **Pending files** on the **Pipe Details** page to confirm that only the files that you expect are waiting to load.
5. In a worksheet, use the new owner role to call `SYSTEM$PIPE_FORCE_RESUME`. After an ownership transfer, setting `PIPE_EXECUTION_PAUSED = FALSE` doesn’t resume the pipe:

   Copy code

   ```
   USE ROLE new_owner_role;
   SELECT SYSTEM$PIPE_FORCE_RESUME('mydb.myschema.orders_pipe');
   ```

For more information, see [Transfer ownership of a pipe](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-transfer-ownership).
