# Manage Snowpipe

After you create a pipe, you operate it with SQL or in [Snowsight](/user-guide/data-load-snowpipe-snowsight). The following table lists common tasks and the commands that perform them:

| Task | Command or function |
| --- | --- |
| [Check whether a pipe is running](#label-snowpipe-manage-check-status) | `SYSTEM$PIPE_STATUS` |
| [Pause or resume a pipe](#label-snowpipe-manage-pause-resume) | `ALTER PIPE ... SET PIPE_EXECUTION_PAUSED` |
| [Resume a pipe that was paused for more than 14 days](#label-snowpipe-resume-stale-pipe) | `SYSTEM$PIPE_FORCE_RESUME` |
| [Change error notifications, the event level, a comment, or tags](#label-snowpipe-management-recreate-pipes) | `ALTER PIPE ... SET` or `ALTER PIPE ... UNSET` |
| [Change the COPY INTO statement, AUTO\_INGEST, AWS\_SNS\_TOPIC, or INTEGRATION](#label-snowpipe-manage-when-to-recreate) | `CREATE OR REPLACE PIPE` |
| [Load files that were staged before you set up event notifications, or that Snowpipe missed](#label-snowpipe-load-historic-data) | `ALTER PIPE ... REFRESH` or `COPY INTO` |
| [Reload a file that Snowpipe already processed](#label-snowpipe-manage-reload-files) | Stage the file under a new name, or use `COPY INTO` |
| [Transfer ownership of a pipe](#label-snowpipe-manage-transfer-ownership) | `GRANT OWNERSHIP` and `SYSTEM$PIPE_FORCE_RESUME` |
| [Delete files after Snowpipe loads them](#label-snowpipe-delete-data-files) | `REMOVE`, or the lifecycle rules of your cloud storage service |

Expand

Show lessSee more

The following table lists the privileges for the tasks on this page:

| Task | Required privileges |
| --- | --- |
| Check a pipe’s status | `MONITOR` or `OWNERSHIP` on the pipe, or `MONITOR EXECUTION` on the account |
| Pause, resume, or force-resume a pipe | `OPERATE` or `OWNERSHIP` on the pipe |
| Pause or resume all pipes in a schema | `MODIFY` on the schema |
| Pause or resume all pipes in the account | The `ACCOUNTADMIN` role |
| Refresh a pipe | `OPERATE` or `OWNERSHIP` on the pipe, `USAGE` on an external stage or `READ` on an internal stage, `USAGE` on a named file format, and `SELECT` and `INSERT` on the target table |
| Change error notifications, the event level, a comment, or tags | `OWNERSHIP` on the pipe, except for setting `ERROR_INTEGRATION` or `LOG_EVENT_LEVEL`. To set tags, also `APPLY TAG` on the account or `APPLY` on each tag. To set `ERROR_INTEGRATION`, `USAGE` on the integration and either `OPERATE` or `OWNERSHIP` on the pipe. To set `LOG_EVENT_LEVEL`, `MODIFY LOG EVENT LEVEL` on the account and either `OPERATE` or `OWNERSHIP` on the pipe |
| Recreate a pipe | `OWNERSHIP` on the pipe and the privileges in the **Create a pipe** column of [Snowpipe access control](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-access-control). To keep tags, also `APPLY TAG` on the account or `APPLY` on each tag. To keep `LOG_EVENT_LEVEL`, also `MODIFY LOG EVENT LEVEL` on the account |
| Load or reload files with `COPY INTO` | `USAGE` on a warehouse, `USAGE` on an external stage or `READ` on an internal stage, `USAGE` on a named file format, and `INSERT` on the target table |
| Delete staged files with `REMOVE` | `USAGE` on an external stage, or `READ` and `WRITE` on an internal stage |
| Transfer ownership of a pipe | `OWNERSHIP` on the pipe and `INSERT` on the target table |

Expand

Show lessSee more

Every task also requires the `USAGE` privilege on the database and schema that contain each object that the task uses, such as the pipe, the stage, or the target table.

## Check the status of a pipe

To check whether a pipe is running and how many files are waiting to load, call [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status):

Copy code

```
SELECT SYSTEM$PIPE_STATUS('mydb.myschema.orders_pipe');
```

The function returns a JSON object. The following fields are the ones that you check most often:

- `executionState`: `RUNNING` when the pipe is healthy, or `PAUSED` when someone paused it. Most other values, such as `STOPPED_STAGE_ALTERED` or `STALLED_EXECUTION_ERROR`, mean that the pipe isn’t loading files. `FAILING_OVER` is an exception: after a failover, the pipe can load files while Snowflake finishes syncing its load metadata. For what each state means and how to fix it, see [Pipe execution states](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-execution-states).
- `pendingFileCount`: The number of files that are queued for loading.
- `oldestPendingFilePath` and `oldestFileTimestamp`: The oldest queued file, and when it was added to the queue. These fields appear only when `pendingFileCount` is greater than `0`.
- `lastIngestedTimestamp` and `lastIngestedFilePath`: When the pipe last loaded a file, and which file it was.

To see the same information in Snowsight, see [Manage Snowpipe in Snowsight](/user-guide/data-load-snowpipe-snowsight). If the pipe isn’t loading the files that you expect, follow the diagnostic steps in [Diagnose a problem](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-diagnose).

## Pause and resume pipes

While a pipe is paused, Snowpipe doesn’t start loading any more files, although a load that’s already in progress can finish. Snowflake keeps adding new files to the pipe’s queue from event notifications or REST API calls, so `pendingFileCount` can keep growing. Each queued file stays in the queue for up to 14 days. After you resume the pipe, Snowpipe loads the queued files.

### Pause or resume a single pipe

To pause or resume a pipe, set the `PIPE_EXECUTION_PAUSED` parameter by using [ALTER PIPE](/sql-reference/sql/alter-pipe):

Copy code

```
-- Pause the pipe.
ALTER PIPE mydb.myschema.orders_pipe SET PIPE_EXECUTION_PAUSED = TRUE;

-- Resume the pipe.
ALTER PIPE mydb.myschema.orders_pipe SET PIPE_EXECUTION_PAUSED = FALSE;
```

To confirm the change, call `SYSTEM$PIPE_STATUS` and check that `executionState` is `PAUSED` or `RUNNING`.

In two cases, setting `PIPE_EXECUTION_PAUSED = FALSE` doesn’t resume the pipe, and you must call [SYSTEM$PIPE\_FORCE\_RESUME](/sql-reference/functions/system_pipe_force_resume) instead:

- The pipe was paused for longer than 14 days. For more information, see [Resume a stale pipe](#label-snowpipe-resume-stale-pipe).
- Ownership of the pipe was transferred to another role. For more information, see [Transfer ownership of a pipe](#label-snowpipe-manage-transfer-ownership).

### Pause or resume all pipes in a schema or account

You can also set [PIPE\_EXECUTION\_PAUSED](/sql-reference/parameters#label-pipe-execution-paused) on a schema or on the account. A role with the `MODIFY` privilege on a schema can pause or resume all of the pipes in that schema. A user with the `ACCOUNTADMIN` role can pause or resume all of the pipes in the account. The following statements pause or resume all of the pipes in a schema or in the account:

Copy code

```
-- Pause all pipes in the schema.
ALTER SCHEMA mydb.myschema SET PIPE_EXECUTION_PAUSED = TRUE;

-- Resume all pipes in the schema.
ALTER SCHEMA mydb.myschema SET PIPE_EXECUTION_PAUSED = FALSE;

-- Pause all pipes in the account.
ALTER ACCOUNT SET PIPE_EXECUTION_PAUSED = TRUE;

-- Resume all pipes in the account.
ALTER ACCOUNT SET PIPE_EXECUTION_PAUSED = FALSE;
```

A schema-level or account-level setting applies only to pipes that don’t have `PIPE_EXECUTION_PAUSED` set at a lower level. This rule works in both directions:

- If someone paused a pipe directly with `ALTER PIPE ... SET PIPE_EXECUTION_PAUSED = TRUE`, resuming the schema or account doesn’t resume that pipe.
- If someone resumed a pipe directly with `ALTER PIPE ... SET PIPE_EXECUTION_PAUSED = FALSE`, pausing the schema or account doesn’t pause that pipe. This case includes pipes that you resumed after you [recreated them](#label-snowpipe-manage-recreate-steps).

To make a pipe follow the schema or account setting again, unset the parameter on the pipe:

Copy code

```
ALTER PIPE mydb.myschema.orders_pipe UNSET PIPE_EXECUTION_PAUSED;
```

After you pause or resume a schema or the account, call `SYSTEM$PIPE_STATUS` for the pipes that you care about, and check `executionState`. If a pipe didn’t change state, check whether it has its own setting. In the output of the following command, a `level` value of `PIPE` means that the pipe ignores the schema and account settings:

Copy code

```
SHOW PARAMETERS LIKE 'PIPE_EXECUTION_PAUSED' IN PIPE mydb.myschema.orders_pipe;
```

## Resume a stale pipe

A pipe becomes stale when it’s paused for longer than 14 days, which is how long a file can stay in a paused pipe’s queue. To resume a stale pipe, call [SYSTEM$PIPE\_FORCE\_RESUME](/sql-reference/functions/system_pipe_force_resume) with the `STALENESS_CHECK_OVERRIDE` argument, which confirms that you know that the pipe is stale:

Copy code

```
SELECT SYSTEM$PIPE_FORCE_RESUME('mydb.myschema.orders_pipe', 'staleness_check_override');
```

If ownership of the pipe was transferred to another role while the pipe was paused, also include the `OWNERSHIP_TRANSFER_CHECK_OVERRIDE` argument:

Copy code

```
SELECT SYSTEM$PIPE_FORCE_RESUME('mydb.myschema.orders_pipe', 'staleness_check_override, ownership_transfer_check_override');
```

When a queued file reaches the end of its 14-day retention period, Snowflake schedules it to be dropped. A resumed pipe might still process it, but only on a best-effort basis. For example, if you resume a pipe 15 days after you paused it, Snowpipe generally doesn’t process the files that were queued on the first day of the pause. If you resume it 16 days after you paused it, Snowpipe generally doesn’t process the files that were queued on the first two days, and so on.

The dropped files were staged more than 14 days ago, so `ALTER PIPE ... REFRESH` can’t queue them. To load them, see [Files staged more than 7 days ago](#label-snowpipe-manage-backfill).

## Change or recreate a pipe

Some changes, such as changing a pipe’s `COPY INTO` statement, require you to recreate the pipe with [CREATE OR REPLACE PIPE](/sql-reference/sql/create-pipe). For other changes, use [ALTER PIPE](/sql-reference/sql/alter-pipe) to set or unset the pipe’s `ERROR_INTEGRATION` for [error notifications](/user-guide/data-load-snowpipe-errors), set its `LOG_EVENT_LEVEL` to [record Snowpipe events](/user-guide/data-load-snowpipe-monitor-events), set a comment, or set or unset tags. These changes require the `OWNERSHIP` privilege on the pipe, with two exceptions. Setting `ERROR_INTEGRATION` requires the `OPERATE` or `OWNERSHIP` privilege on the pipe and the `USAGE` privilege on the integration. Setting `LOG_EVENT_LEVEL` requires the `OPERATE` or `OWNERSHIP` privilege on the pipe and the `MODIFY LOG EVENT LEVEL` privilege on the account.

Important

Recreating a pipe drops its load metadata, which is the record of the files that the pipe already processed. If you then run `ALTER PIPE ... REFRESH` without limiting it to new files, the new pipe can load files that the old pipe already loaded, which duplicates data. To avoid this situation, follow the steps in [Recreate a pipe safely](#label-snowpipe-manage-recreate-steps).

### When you must recreate a pipe

You must recreate a pipe in the following cases:

- You want to change the pipe’s `COPY INTO` statement, for example, to load a new column that the statement doesn’t select.
- You want to change the `AUTO_INGEST`, `AWS_SNS_TOPIC`, or `INTEGRATION` property.
- You changed the `URL` of the external stage that the pipe references. Changing the URL stops every pipe that references the stage, and `SYSTEM$PIPE_STATUS` reports `STOPPED_STAGE_ALTERED` until you recreate the pipes.
- The stage that the pipe references was renamed, dropped, or replaced. Pipe definitions aren’t updated when the stage changes.
- The notification integration that the pipe references was dropped or replaced.
- You want the pipe to load a target table that was renamed.

Changing the stage’s `STORAGE_INTEGRATION`, `CREDENTIALS`, or `ENCRYPTION` parameter doesn’t stop a pipe, because the pipe uses the stage’s current settings for each load. If Snowflake can’t access the storage location with the new settings, `SYSTEM$PIPE_STATUS` reports `STALLED_STAGE_PERMISSION_ERROR` until you fix access.

If the target table was dropped or renamed and you want the pipe to keep loading a table with the original name, you don’t need to recreate the pipe. Restore the table with `UNDROP TABLE` (or `UNDROP ICEBERG TABLE` for an Apache Iceberg™ table), rename the table back, or create a table with the original name, and the pipe resumes loading. Files that arrive while the table is missing aren’t queued, so load them afterward as described in [Load historical or missed files](#label-snowpipe-load-historic-data).

### Recreate a pipe safely

To recreate a pipe without losing or duplicating files, use a role that has the `OWNERSHIP` privilege on the pipe and the privileges in the **Create a pipe** column of [Snowpipe access control](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-access-control). To set tags on the new pipe, the role also needs the `APPLY TAG` privilege on the account or the `APPLY` privilege on each tag. To set `LOG_EVENT_LEVEL`, the role needs the `MODIFY LOG EVENT LEVEL` privilege on the account.

If the pipe already stopped, for example with `STOPPED_STAGE_ALTERED`, skip steps 1 and 2. Note the `lastIngestedTimestamp` value from `SYSTEM$PIPE_STATUS`, and use it in place of the saved time in steps 8 and 9. If you’re changing the stage’s `URL`, make the change after step 3 and before step 4.

Complete the following steps:

1. Pause the pipe, and then save the current time in the ISO 8601 format that `MODIFIED_AFTER` uses in step 8:

   Copy code

   ```
   ALTER PIPE mydb.myschema.orders_pipe SET PIPE_EXECUTION_PAUSED = TRUE;
   SELECT TO_VARCHAR(CONVERT_TIMEZONE('UTC', CURRENT_TIMESTAMP()), 'YYYY-MM-DD"T"HH24:MI:SSTZH:TZM') AS pause_time;
   ```
2. Call `SYSTEM$PIPE_STATUS`, and confirm the following:

   - `executionState` is `PAUSED`.
   - No file that was queued before the pause is still waiting: `pendingFileCount` is `0`, or `oldestFileTimestamp` is later than the time that you saved in step 1. Files that arrive after the pause also count toward `pendingFileCount`, so the count might not reach `0` while files keep arriving.

   If an older file is still queued, resume the pipe, wait until `pendingFileCount` is `0` or `oldestFileTimestamp` is later than the saved time, and then repeat step 1.
3. Save the pipe’s definition, grants, and settings, because the new pipe doesn’t keep them:

   Copy code

   ```
   SELECT GET_DDL('PIPE', 'mydb.myschema.orders_pipe');
   SHOW GRANTS ON PIPE mydb.myschema.orders_pipe;
   SHOW PARAMETERS LIKE 'LOG_EVENT_LEVEL' IN PIPE mydb.myschema.orders_pipe;
   ```

   [GET\_DDL](/sql-reference/functions/get_ddl) returns the statement that creates the pipe, including its `AUTO_INGEST`, `ERROR_INTEGRATION`, and `COMMENT` properties and its tags. You need to set `LOG_EVENT_LEVEL` again only if the `level` column of the `SHOW PARAMETERS` output is `PIPE`.
4. Recreate the pipe with `CREATE OR REPLACE PIPE`, or drop it with [DROP PIPE](/sql-reference/sql/drop-pipe) and create it with [CREATE PIPE](/sql-reference/sql/create-pipe). Start from the statement that `GET_DDL` returned in step 3, and change only what you need to, so that the new pipe keeps the same properties. If you leave out `AUTO_INGEST = TRUE`, the new pipe doesn’t load files from event notifications.
5. Pause the new pipe so that it doesn’t load files before you check its configuration. A new pipe starts running as soon as you create it, unless `PIPE_EXECUTION_PAUSED` is `TRUE` for its schema or account.

   Copy code

   ```
   ALTER PIPE mydb.myschema.orders_pipe SET PIPE_EXECUTION_PAUSED = TRUE;
   ```
6. Grant the privileges from step 3 to the same roles again, and set `LOG_EVENT_LEVEL` again if you need to. For automated loading, also confirm that the event notifications for your storage location are still configured correctly. For more information, see [Automating Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3), [Automating Snowpipe for Google Cloud Storage](/user-guide/data-load-snowpipe-auto-gcs), or [Automating Snowpipe for Microsoft Azure Blob Storage](/user-guide/data-load-snowpipe-auto-azure).
7. Resume the pipe, and then call `SYSTEM$PIPE_STATUS` to confirm that `executionState` is `RUNNING`:

   Copy code

   ```
   ALTER PIPE mydb.myschema.orders_pipe SET PIPE_EXECUTION_PAUSED = FALSE;
   ```

   Resuming sets `PIPE_EXECUTION_PAUSED` on the pipe itself, so later schema-level or account-level pauses don’t pause it. If the schema and the account aren’t paused, you can instead resume the pipe with `ALTER PIPE mydb.myschema.orders_pipe UNSET PIPE_EXECUTION_PAUSED;`, so that it keeps following those settings. For more information, see [Pause or resume all pipes in a schema or account](#label-snowpipe-manage-pause-many-pipes).
8. Refresh the new pipe for the files that were modified after the time that you saved:

   Copy code

   ```
   ALTER PIPE mydb.myschema.orders_pipe REFRESH MODIFIED_AFTER = '2026-10-02T21:30:00+00:00';
   ```

   The notifications for files that were staged while you recreated the pipe went to the old pipe, so the new pipe doesn’t load those files unless you refresh it. Because the new pipe has no load metadata, limiting the refresh to files staged after the pause keeps the new pipe from loading files that the old pipe already loaded. `REFRESH` covers only the last 7 days, so complete these steps within 7 days of the pause.
9. Check for files that were staged just before the pause. A notification can reach the queue shortly after its file is staged, so a file that was staged a few minutes before the pause might have been queued after the pause, and then dropped with the old pipe. Run `LIST` on the path that the pipe watches, find the files whose `last_modified` value, which `LIST` reports in GMT, is within a few minutes before the saved time, and confirm that each one appears in the [COPY\_HISTORY view](/sql-reference/account-usage/copy_history). The view is usually up to 2 hours behind, but it can be up to 2 days behind for a table that has had few recent loads, so wait before you treat a file as missing. The `COPY_HISTORY` table function doesn’t return loads by the old pipe after you recreate it.

   Copy code

   ```
   LIST @mydb.myschema.orders_stage/2026/10/02/;
   ```

   To load a file that’s missing from the view, or to reload a file with the `Load failed` or `Partially loaded` status, follow [Reload a file that Snowpipe already processed](#label-snowpipe-manage-reload-files).

## Load historical or missed files

With automated loading, a pipe loads only the files that it receives event notifications for. It doesn’t automatically load files that were staged before you configured event notifications, files whose notifications it missed, or files that were dropped from its queue while the pipe was stale. How you load these files depends on when they were staged.

If your application calls the Snowpipe REST API, you don’t need these steps: call the `insertFiles` endpoint with the list of files to load.

### Files staged within the last 7 days

Use [ALTER PIPE … REFRESH](/sql-reference/sql/alter-pipe) to add the files to the pipe’s ingest queue. `REFRESH` checks the load metadata of both the pipe and the target table, and queues only the files that the pipe hasn’t already processed and that a `COPY INTO` statement hasn’t loaded. Files that failed to load count as processed, so `REFRESH` doesn’t queue them again; to reload them, see [Reload a file that Snowpipe already processed](#label-snowpipe-manage-reload-files). To limit the files that it queues, use the `PREFIX` and `MODIFIED_AFTER` parameters:

Copy code

```
-- Queue the files from the last 7 days that haven't been loaded.
ALTER PIPE mydb.myschema.orders_pipe REFRESH;

-- Queue the files in the 2026/10/ path that were modified after the specified time and haven't been loaded.
ALTER PIPE mydb.myschema.orders_pipe REFRESH PREFIX = '2026/10/' MODIFIED_AFTER = '2026-10-01T00:00:00-07:00';
```

`REFRESH` is intended for occasional use, to recover files that a pipe missed. It isn’t a substitute for event notifications. Keep the following in mind:

- For a new pipe, run `REFRESH` after you configure event notifications, so that it also queues the files that arrived before the notifications started.
- If you recreated the pipe in the last 7 days, always include `MODIFIED_AFTER`. The new pipe has no load metadata, so a `REFRESH` without `MODIFIED_AFTER` queues files that the old pipe already loaded, which duplicates data. Use the time that you paused the old pipe or, if it had already stopped, the `lastIngestedTimestamp` value that you noted. For more information, see [Recreate a pipe safely](#label-snowpipe-manage-recreate-steps).

### Files staged more than 7 days ago

`REFRESH` can’t queue files that were staged more than 7 days ago. To load them, use a [COPY INTO <table>](/sql-reference/sql/copy-into-table) statement with a warehouse, and then let Snowpipe take over. If some of the missed files were staged within the last 7 days, load the older files first, and then run `REFRESH` for the rest, as described in step 3. `REFRESH` skips files that `COPY INTO` loaded, but `COPY INTO` doesn’t skip files that the pipe already loaded.

Complete the following steps. If event notifications are already configured for the pipe, skip step 2:

1. Load the historical files with `COPY INTO`, using the same file format and copy options as the pipe. Keep the following in mind:

   - `COPY INTO` doesn’t check the pipe’s load metadata, so it also loads files that the pipe already loaded. If the pipe already loaded some files from this location, list only the missed files with the `FILES` or `PATTERN` parameter. To find the files that the pipe loaded, query the [COPY\_HISTORY view](/sql-reference/account-usage/copy_history).
   - If some files were last modified more than 64 days ago, add `LOAD_UNCERTAIN_FILES = TRUE`. Otherwise, `COPY INTO` can skip them because it can’t tell whether they were already loaded. For more information, see [Loading older files](/user-guide/data-load-considerations-load#label-loading-older-files).
   - If the pipe’s statement doesn’t set `ON_ERROR`, add `ON_ERROR = SKIP_FILE` to match the pipe’s default. The `COPY INTO` default stops the load when any file contains an error.
2. If you haven’t already, configure automated loading for the stage. Snowpipe loads only files that generate new event notifications, so it doesn’t load the historical files again.
3. Run `ALTER PIPE ... REFRESH` to queue the files from the last 7 days that the pipe hasn’t loaded, including any files that were staged before event notifications started. `REFRESH` ignores the files that `COPY INTO` already loaded. If you recreated the pipe in the last 7 days, include `MODIFIED_AFTER`, as described in [Files staged within the last 7 days](#label-snowpipe-manage-refresh).

## Reload a file that Snowpipe already processed

Snowpipe ignores any file whose path and name match a file in the pipe’s [load metadata](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-load-metadata), including files that failed to load. If you fix a file and stage it again with the same name within 14 days after Snowpipe processed the original file, Snowpipe ignores it.

Before you reload a file, check whether Snowpipe loaded any rows from the original file, either completely or partially (for example, because the pipe uses `ON_ERROR = CONTINUE`). If it did, delete those rows from the target table first, or the reload duplicates them. You can find the rows that came from a file only if the pipe loads `METADATA$FILENAME` into a column. For a pipe that uses `MATCH_BY_COLUMN_NAME`, such as `orders_pipe`, load the file name with the `INCLUDE_METADATA` copy option. Adding this column requires you to recreate the pipe, and it applies only to files that load afterward. For more information, see [Query metadata for staged files](/user-guide/querying-metadata).

Then, to load the corrected or modified file, use one of the following options:

- **Stage the file under a new name.** Snowpipe treats a file with a new path or name as a new file and loads it. For example, add a version suffix such as `_v2` to the file name. This option doesn’t require a warehouse.
- **Load the file with `COPY INTO`.** Bulk loads use separate load metadata, so `COPY INTO` loads the file even though the pipe already processed it. Use the same file format and copy options as the pipe’s `COPY INTO` statement, which you can see with `DESCRIBE PIPE`, and list only the files to load with the `FILES` parameter. The following example reloads one file into the target table of the `orders_pipe` pipe from the [overview](/user-guide/data-load-snowpipe-intro):

  Copy code

  ```
  COPY INTO mydb.myschema.orders
    FROM @mydb.myschema.orders_stage
    FILES = ('2026/10/02/orders_0001.json')
    FILE_FORMAT = (TYPE = 'JSON')
    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
  ```

  `COPY INTO` runs on a warehouse, so it uses warehouse credits.
- **Recreate the pipe.** Recreating a pipe drops the load metadata for every file, not just the file that you want to reload. Use this option only when you also need to change the pipe. For more information, see [Recreate a pipe safely](#label-snowpipe-manage-recreate-steps).

## Transfer ownership of a pipe

Before you start, make sure that the new owner role has the privileges in the **Own a pipe** column of [Snowpipe access control](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-access-control). Without them, the pipe stops loading after you resume it. The exception is `USAGE` on the error notification integration: without it, the pipe keeps loading but stops sending [error notifications](/user-guide/data-load-snowpipe-errors#label-snowpipe-errors-grant-usage). `GRANT OWNERSHIP` fails unless the pipe is paused, and the role that runs `GRANT OWNERSHIP` needs the `INSERT` privilege on the target table.

To transfer ownership of a pipe to another role, complete the following steps:

1. Pause the pipe:

   Copy code

   ```
   ALTER PIPE mydb.myschema.orders_pipe SET PIPE_EXECUTION_PAUSED = TRUE;
   ```
2. Transfer ownership with [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership). The `COPY CURRENT GRANTS` option keeps the existing grants on the pipe:

   Copy code

   ```
   GRANT OWNERSHIP ON PIPE mydb.myschema.orders_pipe TO ROLE new_owner_role COPY CURRENT GRANTS;
   ```
3. Using the new owner role, call `SYSTEM$PIPE_STATUS`. Check `pendingFileCount` for how many files are queued, and `oldestPendingFilePath` for the oldest queued file, to confirm that only the files that you expect are waiting to load:

   Copy code

   ```
   USE ROLE new_owner_role;
   SELECT SYSTEM$PIPE_STATUS('mydb.myschema.orders_pipe');
   ```
4. Resume the pipe with `SYSTEM$PIPE_FORCE_RESUME`, because setting `PIPE_EXECUTION_PAUSED = FALSE` doesn’t resume a pipe after an ownership transfer:

   Copy code

   ```
   SELECT SYSTEM$PIPE_FORCE_RESUME('mydb.myschema.orders_pipe');
   ```

You can also pause a pipe and transfer its ownership in Snowsight, but you still resume it with `SYSTEM$PIPE_FORCE_RESUME`. For more information, see [Transfer ownership of a pipe](/user-guide/data-load-snowpipe-snowsight#label-snowsight-pipe-transfer-ownership).

## Delete files after Snowpipe loads them

Snowpipe doesn’t delete files after it loads them, because pipes don’t support the `PURGE` copy option.

Before you delete files, confirm that Snowpipe loaded them. Query the [COPY\_HISTORY](/sql-reference/functions/copy_history) table function and check that the `STATUS` column is `Loaded` for each file. Don’t delete a file whose status is `Load in progress`. Deleting a file while it’s loading can cause a partial load and lose data. If `SYSTEM$PIPE_STATUS` shows that `pendingFileCount` isn’t `0`, don’t delete files that don’t appear in the copy history yet, because they might still be queued.

To keep your stage from growing, use one of the following options:

- Run [REMOVE](/sql-reference/sql/remove) periodically to delete loaded files from the stage, after you confirm that every file in the path loaded. `REMOVE` works with both internal and external stages. For an external stage, the credentials that the stage uses must have permission to delete objects in your cloud storage, such as `s3:DeleteObject` in Amazon S3. The following example deletes the files in the `2026/09/` path of the stage:

  Copy code

  ```
  REMOVE @mydb.myschema.orders_stage/2026/09/;
  ```
- For an external stage, configure the lifecycle management rules of your cloud storage service to delete or archive files after a set period. Choose a period that’s longer than 14 days, so that files that wait in a paused pipe’s queue still exist when the pipe resumes.
