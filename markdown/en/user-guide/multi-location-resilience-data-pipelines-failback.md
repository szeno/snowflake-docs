# Fail back data pipelines

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical Edition (or higher).
To inquire about upgrading, contact [Snowflake Support](/user-guide/contacting-support).

Use this runbook after the outage is resolved and your primary location is
healthy, to move your pipelines back to your primary location. It assumes that
you failed over as described in
[Fail over data pipelines](/user-guide/multi-location-resilience-data-pipelines-failover). Your *source
account* is the account where you set up your pipelines, and your *target
account* holds the replicas, as described in [How multi-location resilience works](/user-guide/multi-location-resilience-data-pipelines#label-mlsi-how-it-works).

Each step names the account to run it in. The runbook has the following steps:

1. [Load primary-only files](#label-mlsi-failback-step-1), only if you use
   single-write.
2. [Reroute your producers](#label-mlsi-failback-step-2), only if you use
   single-write.
3. [Let your target account finish loading](#label-mlsi-failback-step-3).
4. [Sync data back to your source account](#label-mlsi-failback-step-4).
5. [Check your integrations and pipes](#label-mlsi-failback-step-5).
6. [Promote your source account](#label-mlsi-failback-step-6).
7. [Restart your `COPY INTO` jobs](#label-mlsi-failback-step-7), if you run
   them.
8. [Resume scheduled refreshes](#label-mlsi-failback-step-8).
9. [Reconcile stranded files](#label-mlsi-failback-step-9), only if you use
   single-write.

Then [verify that ingestion resumed](/user-guide/multi-location-resilience-data-pipelines-verify#label-mlsi-verify-ingestion). If a step
doesn’t go as described, see [If a step fails](#label-mlsi-failback-if-fails).

## Before you start

Before you run the steps, check the following:

- **Which steps you run:** Check [the setup record](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-setup-record)
  for whether your producers use dual-write or single-write, as described in
  [Choose how your producer writes files](/user-guide/multi-location-resilience-data-pipelines#label-mlsi-choose-routing). Snowflake doesn’t record this choice. Then
  run the steps for your method:
  - **Dual-write:** Run steps 3 through 8.
  - **Single-write:** Run every step.
- **Values from failover:** Get the values that were saved during failover, as
  listed in [Values to save during failover](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-handoff-values). If any of these values wasn’t
  saved, see [Values from failover weren’t saved](#label-mlsi-failback-missing-values).
- **Roles:** Failback runs steps in both accounts. Make sure that you can use
  roles with the following privileges, or `ACCOUNTADMIN`, in the account that
  each item names:
  - **Step 1, in your source account:** Access to the `SNOWFLAKE` database,
    for the Account Usage `COPY_HISTORY` view.
  - **Step 4, in your source account:** `OWNERSHIP` or `REPLICATE` on the
    failover group.
  - **Step 6, in your source account:** `OWNERSHIP` or `FAILOVER` on the
    failover group.
  - **Step 8, in your target account:** `OWNERSHIP` on the failover group.
  - **Step 9, in your source account, if `<reconcile_from_iso_8601>` is more
    than 14 days ago:** Access to the `SNOWFLAKE` database, for the Account
    Usage `COPY_HISTORY` view.
  - **Steps 1, 6, and 9, for a pipe that you recreated during the outage:**
    Access to the `SNOWFLAKE` database, in the account that’s primary when you
    run the step, to load the pipe’s files as described in
    [Load files for a recreated pipe](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-recreated-pipes-load).
  - **Other steps, in either account:** The privileges that each statement’s
    reference topic lists under access control requirements, such as those
    for the [COPY\_HISTORY](/sql-reference/functions/copy_history) function and
    `COPY INTO`. Also `OWNERSHIP` on each integration whose `ACTIVE` value
    you set, and `ACCOUNTADMIN` to rebind SQS-only pipes.
- **Cloud provider access:** Permission to edit the access policies and event
  notifications of your storage locations and queues, and to copy files
  between your locations, for step 1, the fixes in
  [An ACTIVE value isn’t your primary location in step 5](#label-mlsi-failback-fix-active), and the checks in
  [Check objects that you created during the outage](#label-mlsi-failback-outage-objects).

## Fail back your pipelines

Run the steps in order. If your producers use dual-write, skip the steps marked
single-write only.

### Step 1: Load primary-only files (single-write only)

Rows that your source account loaded after `<last_snapshot>` exist only in your
source account. Load the files that those rows came from into your target
account.

Warning

Complete this step before the refresh in step 4. That refresh overwrites the
database in your source account with the contents of the database in your
target account, so rows that exist only in your source account are permanently
erased.

1. In your source account, list the files that your tables loaded since one day
   before the `<last_snapshot>` time that you recorded in step 2 of
   [Fail over your pipelines](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-failover-steps). The extra day also covers loads that
   finished close to the time of that refresh. Copying a file that your target
   account already loaded is safe, because the pipe or `COPY INTO` job skips
   it. The following query covers every table in `my_db`. If `my_fg` contains
   more than one database, add each one to the `IN` list. To list them, run
   `SHOW DATABASES IN FAILOVER GROUP my_fg`. Run the query with a
   role that can query the `SNOWFLAKE` database, such as `ACCOUNTADMIN`:

   Copy code

   ```
   SELECT table_catalog_name, table_schema_name, table_name, pipe_name,
          stage_location, file_name, last_load_time
     FROM SNOWFLAKE.ACCOUNT_USAGE.COPY_HISTORY
     WHERE table_catalog_name IN ('MY_DB')
       AND last_load_time > DATEADD(day, -1, '<last_snapshot>'::TIMESTAMP_LTZ)
       AND status IN ('Loaded', 'Partially loaded')
     ORDER BY table_catalog_name, table_schema_name, table_name, last_load_time;
   ```

   The view can lag by up to 2 hours, and by up to 2 days for a table that has
   had few loads since its last update in the view. If `<last_snapshot>` is
   within the last 13 days, check each table with the
   [COPY\_HISTORY](/sql-reference/functions/copy_history) table function as well. Run it
   with `my_db.my_schema` as your current schema:

   Copy code

   ```
   SELECT file_name, last_load_time, row_count, pipe_name
     FROM TABLE(my_db.INFORMATION_SCHEMA.COPY_HISTORY(
       TABLE_NAME => 'my_table',
       START_TIME => DATEADD(day, -1, '<last_snapshot>'::TIMESTAMP_LTZ)))
     WHERE status IN ('Loaded', 'Partially loaded');
   ```

   `pipe_name` is `NULL` for files that a `COPY INTO` statement loaded, and for
   files that a pipe loaded if the pipe was dropped or your role can’t access
   it. `file_name` is relative to `stage_location`, which is the URL of the
   location that the file was loaded from.

   If a pipe that you recreated during the outage loads one of these tables,
   choose the files to copy for that table as described in
   [Load files for a recreated pipe](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-recreated-pipes-load), for the period since one day before
   `<last_snapshot>`.
2. Copy those files from your primary location to the same relative paths in
   your secondary location: the path after the `STORAGE_BASE_URL` in
   `stage_location`, followed by `file_name`. The pipes in your target account
   load them. For tables that a task or another `COPY INTO` job loads, you load
   those files in step 3. If your locations are on different cloud providers,
   use a tool that can read from one and write to the other, such as a cloud
   storage transfer service.

### Step 2: Reroute your producers (single-write only)

Point each producer application back at your primary cloud storage
location. Your source account’s pipes are still read-only, but they receive the
notifications and load the new files after you promote your source account. The
refresh in step 4 doesn’t discard these notifications, because your source
account receives them while it’s the secondary account.

### Step 3: Let your target account finish loading

In your target account, make sure that every file in your secondary location is
loaded. With dual-write, this includes files that your producers wrote only to
your secondary location, for example because a write to your primary location failed during
the outage. Your source account reads only your primary location, so a file that
your target account doesn’t load in this step isn’t loaded after you fail back.
Check each kind of job:

- **Pipes:** Run `SYSTEM$PIPE_STATUS` for each pipe and wait until
  `pendingFileCount` and `numOutstandingMessagesOnChannel` are both `0` on two
  checks a few minutes apart. `numOutstandingMessagesOnChannel` is approximate
  and counts every pipe that shares the queue. If the output doesn’t include
  `numOutstandingMessagesOnChannel`, check `pendingFileCount` only.
- **Tasks:** Suspend each standalone task, or the root task of each task
  graph, and run it once more, as described in
  [Finish task runs in your target account](#label-mlsi-failback-run-tasks). Then return to this step. Don’t start
  step 4 until each run succeeds.
- **Other `COPY INTO` jobs:** Run each job once more, and then stop it.

Warning

If your target account loads a file after the refresh in step 4 starts, the
rows from that file don’t reach your source account. With dual-write, your
source account loads the copy of that file in your primary location after you
fail back, because its load history doesn’t record the file. A file that exists
only in your secondary location isn’t loaded.

### Step 4: Sync data back to your source account

Pull all data and state changes that occurred during the outage back to your
source account. Log in to your source account, which is acting as the secondary
account at this point, and use a role with the `OWNERSHIP` or `REPLICATE`
privilege on the failover group to start a manual refresh:

Copy code

```
ALTER FAILOVER GROUP my_fg REFRESH;
```

Warning

Wait for this refresh operation to finish completely before moving to the next
step. Failing back before the sync completes can result in data loss.

The statement runs until the refresh finishes. To check progress, run the
following query in a separate session in your source account with
[REPLICATION\_GROUP\_REFRESH\_PROGRESS](/sql-reference/functions/replication_group_refresh_progress):

Copy code

```
SELECT phase_name, start_time, end_time, details
  FROM TABLE(my_db.INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_PROGRESS('my_fg'))
  ORDER BY start_time;
```

The refresh is finished when the last row shows `COMPLETED`. If it shows
`FAILED` or `CANCELED`, see [The refresh in step 4 fails or is canceled](#label-mlsi-failback-refresh-failed).

The refresh also copies the load history of your tables. Load history
identifies a file by its path relative to the stage, not by the storage
location that it was loaded from. After the refresh, your source account’s
pipes and `COPY INTO` statements skip a file in your primary location if your
target account already loaded a file with the same relative path from your
secondary location, even if the contents of the two files differ.

### Step 5: Check your integrations and pipes

After the refresh is complete, and while your source account is still the
secondary account, check the integrations and pipes in your source account.
Your pipes record notifications while your source account is secondary and load
them after the promotion in step 6, so fix any problem before you promote. Run the following checks:

1. Run `DESCRIBE STORAGE INTEGRATION my_mlsi`, and confirm that `ACTIVE` is
   your primary location, such as `my-s3-us-west-1`. If you created more than one Multi-Location Storage Integration (MLSI), check each one.
2. If you use a Multi-Queue Notification Integration (MQNI), run `DESCRIBE INTEGRATION` for each MQNI, including any
   that you created in your target account during the outage, and confirm that
   `ACTIVE` names your primary location’s queue. For an MQNI that existed
   before the outage, that’s your source account’s value in
   [the setup record](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-setup-record), which the **After a
   failback** column of [the table of expected values](/user-guide/multi-location-resilience-data-pipelines-verify#label-mlsi-check-active)
   shows with example names. An MQNI that you created in your target account by
   following
   [the numbered steps for a missing MQNI](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-troubleshoot-mqni-missing)
   doesn’t replicate. Your source account keeps its own MQNI with that name,
   so check it like an MQNI that existed before the outage. Any other MQNI that
   you created during the outage has no active queue in your source account
   yet, so its `ACTIVE` value is empty, and the next item applies to it.
3. If an `ACTIVE` value from the previous items isn’t your primary location or
   queue, or is empty, fix it as described in
   [An ACTIVE value isn’t your primary location in step 5](#label-mlsi-failback-fix-active).
4. If you created stages, integrations, or pipes during the outage, check them
   as described in [Check objects that you created during the outage](#label-mlsi-failback-outage-objects). Use the names
   saved during failover or, if they weren’t saved, the names that you found
   as described in [Values from failover weren’t saved](#label-mlsi-failback-missing-values).
5. Run `SYSTEM$PIPE_STATUS` for each pipe, and check whether the output includes
   a `replicationBindingErrorDetails` field. The field appears when the refresh
   couldn’t bind the pipe to a queue, even though `executionState` is still
   `READ_ONLY`. If it appears, set the active queue of the pipe’s MQNI again,
   or rebind the SQS-only pipe, as described in
   [An ACTIVE value isn’t your primary location in step 5](#label-mlsi-failback-fix-active).

### Step 6: Promote your source account

1. In your source account, use a role with the `OWNERSHIP` or `FAILOVER`
   privilege on the failover group to promote your source account back to primary:

   Copy code

   ```
   ALTER FAILOVER GROUP my_fg PRIMARY;
   ```
2. As soon as the statement succeeds, run `SELECT CURRENT_TIMESTAMP()`, and
   save the result, including its time zone offset, as `<promotion_time>` to
   verify ingestion.
3. If you set an MQNI’s active queue or rebound pipes in step 5, or added or
   updated an event notification there, the affected pipes didn’t receive
   notifications for files that arrived before the change. The affected pipes
   are every pipe that uses each MQNI whose active queue you set, each pipe
   that you rebound, and each pipe whose event notification you added or
   updated. Load those files by running `ALTER PIPE ... REFRESH` for each
   affected pipe. The statement
   covers files staged within the last 7 days, and the pipe skips files that
   its load history records as loaded:

   Copy code

   ```
   ALTER PIPE my_db.my_schema.my_pipe REFRESH;
   ```

   For a pipe that you recreated during the outage, don’t run this statement.
   Follow [Load files for a recreated pipe](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-recreated-pipes-load) instead, for the last 7 days.

### Step 7: Restart your COPY INTO jobs in your source account (if you run them)

- **Tasks:** The refresh in step 4 copied each task’s state from your target
  account, so a task that you suspended in step 3 is also suspended in your
  source account. Run `SHOW TASKS IN DATABASE my_db`. If a task that you
  suspended in step 3, or that your setup record lists as resumed, has a
  `state` of `suspended`, resume it with
  [ALTER TASK … RESUME](/sql-reference/sql/alter-task). For task graphs,
  follow the resume order in [Resume suspended tasks and task graphs](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-failover-resume-tasks).
- **Other `COPY INTO` jobs:** Run them in your source account, or point the
  scheduler that runs them back at your source account.

### Step 8: Resume scheduled refreshes

Failing back suspends scheduled refreshes of the secondary group in your target
account. Until you resume them, your target account doesn’t receive changes.
For more information, see
[Resume scheduled replication in target accounts](/user-guide/account-replication-failover-failback#label-resume-scheduled-replication-in-target-accounts). In your target account, use a role with the `OWNERSHIP` privilege on the
failover group to run the following command:

Copy code

```
ALTER FAILOVER GROUP my_fg RESUME;
```

### Step 9: Reconcile stranded files (single-write only)

In your source account, load the files that were never loaded. A file can be
missed because the outage stopped its notification from arriving, because the
outage outlasted the queue’s message retention period, or because your source
account had read the notification but hadn’t loaded the file when the outage
began. To load these files, do the following:

1. For files staged within the last 7 days, run
   [ALTER PIPE … REFRESH](/sql-reference/sql/alter-pipe) for each pipe, with
   `MODIFIED_AFTER` set to the `<reconcile_from_iso_8601>` value from step 2 of
   [Fail over your pipelines](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-failover-steps). That value is one day before your last
   refresh’s snapshot time, so `ALTER PIPE ... REFRESH` also picks up files
   that were in flight at that refresh. The pipe skips files that its load
   history records as loaded. The value must be in ISO 8601 format with a time
   zone offset, such as `'2026-10-01T18:30:00-07:00'`. A value older than 7
   days is treated as 7 days ago. Run the following statement for each pipe:

   Copy code

   ```
   ALTER PIPE my_db.my_schema.my_pipe REFRESH
     MODIFIED_AFTER = '<reconcile_from_iso_8601>';
   ```

   For a pipe that you recreated during the outage, don’t run this statement.
   Follow [Load files for a recreated pipe](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-recreated-pipes-load) instead, for the period since
   `<reconcile_from_iso_8601>`.
2. For older files that pipes didn’t load, compare your primary storage bucket
   against [COPY\_HISTORY](/sql-reference/functions/copy_history). If
   `<reconcile_from_iso_8601>` is more than 14 days ago, use the Account Usage
   [COPY\_HISTORY view](/sql-reference/account-usage/copy_history) instead. Then run a manual
   `COPY INTO` command for the files that weren’t loaded. Skip this comparison
   for the files that a pipe you recreated during the outage reads, because
   [the steps for a recreated pipe](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-recreated-pipes-load) already
   cover every one of those files in that period.

For tables that only `COPY INTO` statements or tasks load, no action is needed.
The next run of each statement loads files in your primary location that the
table’s load metadata doesn’t record as loaded.

## After you fail back

- To confirm that ingestion resumed, see [Verify data pipelines after failover or failback](/user-guide/multi-location-resilience-data-pipelines-verify#label-mlsi-verify-ingestion).
- To keep [the setup record](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-setup-record) current, add the
  stages, integrations, and pipes that you created during the outage. For a
  pipe that replaces an earlier pipe, replace the earlier pipe’s entry. Also
  record the following:

  - Each new integration’s `ACTIVE` value in each account
  - Which new pipes use the Amazon SQS-only path
  - On Azure and Google Cloud, each new pipe’s `notificationChannelName`
    values
- To confirm that your target account is ready for the next failover, do the
  following:

  1. In your target account, wait for a refresh of `my_fg` that starts after
     step 8, or run
     `ALTER FAILOVER GROUP my_fg REFRESH`. If that statement reports that the
     group is already being refreshed, wait for that refresh instead. Until
     this refresh completes, the tasks that you suspended in step 3 still show
     `suspended` in your target account.
  2. In your target account, run the progress query from step 4. The refresh
     is complete when the
     first row’s `start_time` is later than the time that you ran step 8 and
     the last row shows `COMPLETED`. To find that time, look up the
     `ALTER FAILOVER GROUP my_fg RESUME` statement in your target account’s
     query history. If someone else ran step 8, use a role that can see every
     user’s queries, such as `ACCOUNTADMIN`.
  3. Run [the validation checks](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-validate-setup) again, in the
     account that each check names.

## Finish task runs in your target account

In step 3, for each task that runs your `COPY INTO` statements in your target
account, do the following. Skip all of these items for a standalone or root
task that’s already suspended and that
[the setup record](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-setup-record) doesn’t list as resumed, because
it didn’t run during the outage:

1. Suspend each standalone task, or the root task of each task graph, with
   `ALTER TASK ... SUSPEND`. Don’t suspend child tasks, because `EXECUTE TASK`
   skips suspended child tasks.
2. If [TASK\_HISTORY](/sql-reference/functions/task_history) shows a run of the task that’s
   still `EXECUTING`, wait for it to finish.
3. Run the task once with [EXECUTE TASK](/sql-reference/sql/execute-task), which runs a
   suspended task without resuming it.
4. Wait for the run to succeed:

   - **Standalone task:** Wait until `TASK_HISTORY` shows that run as
     `SUCCEEDED`.
   - **Task graph:** The root task’s run finishes before its child tasks run,
     so wait until [COMPLETE\_TASK\_GRAPHS](/sql-reference/functions/complete_task_graphs) shows a
     row whose `scheduled_from` is `EXECUTE_TASK` and whose `scheduled_time` is
     after you ran `EXECUTE TASK`, with a `state` of `SUCCEEDED`. The function
     returns only graph runs that completed in the past 60 minutes, so check
     within an hour of the run finishing:

     Copy code

     ```
     SELECT root_task_name, state, scheduled_from, scheduled_time, completed_time
       FROM TABLE(my_db.INFORMATION_SCHEMA.COMPLETE_TASK_GRAPHS(
         ROOT_TASK_NAME => 'my_root_task'))
       ORDER BY scheduled_time DESC;
     ```

If the run shows `FAILED` or `CANCELLED`, fix the cause, and run
`EXECUTE TASK` again.

## Check objects that you created during the outage

In step 5, check the stages, integrations, and pipes that you created in your
target account while it was the primary account. Pipes that existed before the
outage, and that you didn’t recreate during it, keep their binding in your
source account.

Pipes that you created during the outage need a one-time bind in your source
account. The refresh in step 4 replicated them there, but a pipe’s replica
doesn’t load from your primary location until you bind it in that account,
even if its status looks normal. Later refreshes keep that binding.

An MLSI or MQNI that you created during the outage needs the fixes in
[An ACTIVE value isn’t your primary location in step 5](#label-mlsi-failback-fix-active): an MLSI arrives with your target account’s
active location and a cloud identity that has no access to your primary
location yet, and an MQNI arrives with no active queue. An MQNI that you
created by following
[the numbered steps for a missing MQNI](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-troubleshoot-mqni-missing) doesn’t
replicate, so it doesn’t need these fixes.

For each pipe that you created during the outage, check the following in your
source account:

- **Stage:** Run `LIST` on the pipe’s stage, and confirm that the file URLs are
  in your primary location. If they aren’t, fix the stage before you bind the
  pipe, because binding uses the stage’s current location. If the stage uses
  an MLSI, set that MLSI’s `ACTIVE` value to your primary location, as
  described in [An ACTIVE value isn’t your primary location in step 5](#label-mlsi-failback-fix-active). If the stage doesn’t use
  an MLSI, change it as described in [Associate the MLSI with your external stages](/user-guide/multi-location-resilience-data-pipelines-setup-storage#label-mlsi-stage-setup). The stage is
  read-only in your source account, so change it in your target account,
  which is still the primary account, and then repeat the refresh in step 4.
- **Binding:** Bind the pipe as described in the **Pipes to rebind** fix in
  [An ACTIVE value isn’t your primary location in step 5](#label-mlsi-failback-fix-active). For a pipe that uses an MQNI, set the
  MQNI’s active queue again with your primary location’s queue name. One
  statement binds every pipe that uses the MQNI, so run it after you check the
  stages of all of those pipes. For an SQS-only pipe, run
  `SYSTEM$INGEST_REBIND_PIPE`.
- **Notifications:** Make sure that an event notification on your primary
  bucket for the pipe’s path targets the pipe’s queue: the current
  `notification_channel` ARN for an SQS-only pipe, or the MQNI’s queue for your
  primary location.

If you’re running this runbook, return to step 5, and continue with item 5.

## If a step fails

Find the problem in the following sections. Each section says where to continue
in the runbook.

### Values from failover weren’t saved

If `<last_snapshot>` wasn’t saved, use a time that you know is earlier than the
start of the last refresh that completed before the failover. For example,
start from the beginning of the outage, and subtract twice your replication
schedule’s interval or twice the time that a refresh usually takes, whichever
is longer. Use an earlier time if refreshes were failing before the outage. An
earlier time is safe for this runbook, because pipes and `COPY INTO` jobs
skip files that their load history records as loaded. A pipe that you recreated
during the outage is the exception, as described in
[Load files for a recreated pipe](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-recreated-pipes-load).

If you use single-write and `<reconcile_from_iso_8601>` wasn’t saved,
get it from `<last_snapshot>` with the following query:

Copy code

```
SELECT TO_VARCHAR(DATEADD(day, -1, '<last_snapshot>'::TIMESTAMP_LTZ),
                  'YYYY-MM-DD"T"HH24:MI:SSTZH:TZM') AS reconcile_from_iso_8601;
```

If the names of the stages, integrations, and pipes that you created during
the outage weren’t saved, find them in your target account before you start.
Run `SHOW STAGES IN ACCOUNT`, `SHOW INTEGRATIONS`, and `SHOW PIPES IN ACCOUNT`.
These commands list only the objects that your role can access, so use a role
that can access every integration and every stage and pipe in your pipeline
databases. Check only the stages and pipes in databases that `my_fg` replicates. Treat an object as created during the outage if its `created_on` value is later than the failover’s `<promotion_time>`. If `<promotion_time>` wasn’t saved, compare `created_on` with the start of the outage instead. For each such pipe, check whether it replaces a
pipe in [the setup record](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-setup-record), such as a pipe with the
same name, because steps 1, 6, and 9 handle recreated pipes differently.

Then return to [Fail back your pipelines](#label-mlsi-failback-steps), and start with the first step
that applies to you.

### The refresh in step 4 fails or is canceled

If the last row of the progress query shows `FAILED`, read `errorMessage` in
the `details` column, fix the cause, and run the refresh again. If it shows
`CANCELED`, run the refresh again. Don’t continue with step 5 until the
refresh shows `COMPLETED`.

### An ACTIVE value isn’t your primary location in step 5

Run the fixes that apply in your source account. During failback, run them
while it’s still the secondary account:

- **MLSI:** If an MLSI’s `ACTIVE` value isn’t your primary location, set it:

  Copy code

  ```
  ALTER STORAGE INTEGRATION my_mlsi SET ACTIVE = 'my-s3-us-west-1';
  ```

  An MLSI that you created during the outage has a different cloud identity in
  your source account, and nothing has granted that identity access to your
  primary location yet. Grant it by following
  [Grant access to your secondary storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-storage) in your source account, with your
  primary location in place of your secondary one. On AWS, if the trust policy
  of your primary location’s role doesn’t already allow that IAM user ARN with
  that external ID, add an entry for it, and keep the existing entries, which
  your other integrations use. Then run `LIST` on one of the MLSI’s stages in
  your source account to confirm access.
- **MQNI:** An MQNI that you created during the outage arrives with no active
  queue, so its pipes aren’t bound to any queue. If `ACTIVE` is empty or names
  another queue, grant your source account access to your primary location’s
  queue, and then set it, as described in steps 1, 4, and 5 of
  [Change the active queue later](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-change-active-queue).
- **Pipes to rebind:** Changing an MLSI’s `ACTIVE` value doesn’t rebind the
  pipes on that MLSI’s stages. If you changed it, rebind those pipes now. Also
  rebind each pipe that item 5 of step 5 or
  [Check objects that you created during the outage](#label-mlsi-failback-outage-objects) sent you here for:

  - For pipes that use an MQNI, set the MQNI’s active queue again with your
    primary location’s queue name, as described in step 4 of
    [Change the active queue later](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-change-active-queue).
  - For each SQS-only pipe, run `SYSTEM$INGEST_REBIND_PIPE` with the same
    arguments as in [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind). Check that the result starts
    with `Rebind succeeded` and that the region in the `New channel` ARN is
    your primary bucket’s region, such as `us-west-1`. If the result starts
    with `Rebind failed`, or the function raises an error, act on the result as
    described in [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-rebind-results). If the ARN
    shows another region, check the pipe’s stage as described in the
    **Stage** check in [Check objects that you created during the outage](#label-mlsi-failback-outage-objects).

After you finish the fixes, continue where you left off:

- **From item 3 of step 5:** Continue with item 4.
- **From [Check objects that you created during the outage](#label-mlsi-failback-outage-objects):** Continue with the next
  check or the next pipe in that section.
- **From item 5 of step 5:** Continue with step 6.
- **From [Troubleshoot data pipelines after failover or failback](/user-guide/multi-location-resilience-data-pipelines-troubleshoot),
  after you failed back:** Load the files that the affected pipes missed, as
  described in [After you fix a pipe](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-troubleshoot-after-fix).
