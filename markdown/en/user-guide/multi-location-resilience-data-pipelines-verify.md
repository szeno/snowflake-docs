# Verify data pipelines after failover or failback

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical Edition (or higher).
To inquire about upgrading, contact [Snowflake Support](/user-guide/contacting-support).

After you initiate a failover or failback, connect to the account that’s now the
primary account, and use the following commands to verify that your data
pipelines were redirected successfully and have resumed ingestion. This topic
uses *source account* and *target account* as defined in
[How multi-location resilience works](/user-guide/multi-location-resilience-data-pipelines#label-mlsi-how-it-works).

Your pipelines have resumed when every check in this topic passes:

- Each integration’s `ACTIVE` value names your active location or its queue.
- Each pipe’s `executionState` is `RUNNING`, and its `lastIngestedTimestamp`
  advances as new files arrive.
- Each task’s runs since the promotion succeed.
- The load history shows new files loaded from your active location, with no
  file loaded twice.

If a check fails, see
[Troubleshoot data pipelines after failover or failback](/user-guide/multi-location-resilience-data-pipelines-troubleshoot).

## Check active integration states

Confirm that the `ACTIVE` value of each Multi-Location Storage Integration (MLSI) and Multi-Queue Notification Integration (MQNI) names the storage location or queue for the region that’s now primary. Run the following commands, and check
`ACTIVE` in the output:

Copy code

```
-- Check the active storage location
DESCRIBE STORAGE INTEGRATION my_mlsi;

-- Check the active message queue, if you use an MQNI
DESCRIBE INTEGRATION my_mqni;
```

Compare each `ACTIVE` value with the values that
[the setup record](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-setup-record) lists for this account, which
include any change that you made as described in
[Change the active queue later](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-change-active-queue). The following table shows the expected
values with the example names from the setup topics, so expect the names that
you chose in your own `DESCRIBE` output:

| Integration | After a failover, in your target account | After a failback, in your source account |
| --- | --- | --- |
| MLSI | Your secondary location’s name, such as `my-s3-us-east-1` | Your primary location’s name, such as `my-s3-us-west-1` |
| MQNI from [Scenario A](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-mqni-scenario-a) | `my-us-east-1` | `my-us-west-1` |
| MQNI from [Scenario B](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-mqni-scenario-b) on Amazon S3 | `MY_MQNI-queue2` | `MY_MQNI-queue1` |
| MQNI from Scenario B on Google Cloud or Azure | Your second integration’s name, such as `MY_AZURE_NI_2` | Your original integration’s name, such as `MY_AZURE_NI_1` |

Expand

Show lessSee more

On the Amazon SQS-only path, only the MLSI has an `ACTIVE` value.

If a value doesn’t match, see
[Troubleshoot data pipelines after failover or failback](/user-guide/multi-location-resilience-data-pipelines-troubleshoot).

## Check pipe status (Snowpipe only)

To list your pipes, run [SHOW PIPES](/sql-reference/sql/show-pipes). Use the
[SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status) function to confirm that each
pipe is running and bound to the queue in your active location:

Copy code

```
SELECT SYSTEM$PIPE_STATUS('my_db.my_schema.my_pipe');
```

In the output:

- `executionState` should be `RUNNING`.
- On Azure and Google Cloud, `notificationChannelName` should differ from the
  value that the same pipe reports in the other account. If the other account
  is unreachable, compare it with the values that you recorded in
  [Record your setup for on-call responders](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-setup-record).
- If the output has no `notificationChannelName` field, the pipe isn’t bound to
  a queue in this account. See
  [Troubleshoot data pipelines after failover or failback](/user-guide/multi-location-resilience-data-pipelines-troubleshoot).
- On Amazon S3, for a pipe that uses an MQNI, `notificationChannelName` doesn’t
  confirm the binding. Run `DESCRIBE PIPE`, and confirm that
  `notification_channel` shows the SNS topic for your active location. If it
  shows the other location’s topic, run `ALTER INTEGRATION my_mqni SET ACTIVE`
  again with the name of the queue that’s active in this account. Then run
  `ALTER PIPE ... REFRESH` for the pipe. For a pipe that you recreated during
  the outage, follow [Load files for a recreated pipe](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-recreated-pipes-load) instead, for the last
  7 days.
- On Amazon S3, for an SQS-only pipe, confirm that the bucket for your active
  location has an event notification that targets the `notification_channel`
  ARN from `DESCRIBE PIPE`.
- `lastIngestedTimestamp` should advance as new files arrive.

## Check task status

If your `COPY INTO` statements run in tasks, confirm that each task is resumed
and that its runs succeed. Run `SHOW TASKS` and the
[TASK\_HISTORY](/sql-reference/functions/task_history) table function. Replace
`my_copy_task` with your task’s name:

Copy code

```
SHOW TASKS IN DATABASE my_db;

SELECT name, state, scheduled_time, error_message
  FROM TABLE(my_db.INFORMATION_SCHEMA.TASK_HISTORY(
    TASK_NAME => 'my_copy_task',
    DATABASE_NAME => 'MY_DB',
    SCHEMA_NAME => 'MY_SCHEMA'))
  ORDER BY scheduled_time DESC
  LIMIT 10;
```

In the `SHOW TASKS` output, `state` should be `started`. If it’s `suspended`,
resume the task with `ALTER TASK ... RESUME`. For task graphs, follow the resume
order in [Resume suspended tasks and task graphs](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-failover-resume-tasks). In the `TASK_HISTORY` output, runs
scheduled after you promoted the account should show `SUCCEEDED` in the `state`
column. The first rows can be future runs with a `state` of `SCHEDULED`.
Scheduling can take a while to return to normal after a promotion, so the first
run might start later than its schedule.

## Check load history

To confirm that data is loading without errors or duplicates, query the
[COPY\_HISTORY](/sql-reference/functions/copy_history) table function, which shows which
files were ingested and when they were loaded. Run the following query with
`my_db.my_schema` as your current schema:

Copy code

```
SELECT file_name, stage_location, status, row_count, last_load_time
FROM TABLE(my_db.INFORMATION_SCHEMA.COPY_HISTORY(
  TABLE_NAME => 'my_table',
  START_TIME => '<promotion_time>'::TIMESTAMP_LTZ
));
```

Replace `<promotion_time>` with the time that you saved in step 3 of
[Fail over your pipelines](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-failover-steps) or step 6 of [Fail back your pipelines](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-steps). Verify that `status` shows `Loaded`, that `stage_location`
shows the URL of your active location, and that `last_load_time` is later than
`<promotion_time>`. `file_name` is relative to `stage_location`. For a table
that `COPY INTO` statements or tasks load, rows with the status
`Load skipped another location` are expected: `COPY INTO` skipped those files
because it already loaded them from your other storage location.

To confirm that no file was loaded twice across the failover, look for file
names that appear more than once. Start the search before the `<last_snapshot>`
value that was saved in step 2 of [Fail over your pipelines](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-failover-steps), as listed
in [Values to save during failover](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-handoff-values). If it wasn’t saved, use the time described
in [Values from failover weren’t saved](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-missing-values). The following query starts one day
earlier. The function returns at most the last 14 days of history, and an
earlier `START_TIME` is treated as 14 days ago. Run the following query:

Copy code

```
SELECT file_name, COUNT(*) AS load_count
FROM TABLE(my_db.INFORMATION_SCHEMA.COPY_HISTORY(
  TABLE_NAME => 'my_table',
  START_TIME => DATEADD(day, -1, '<last_snapshot>'::TIMESTAMP_LTZ)
))
WHERE status IN ('Loaded', 'Partially loaded')
GROUP BY file_name
HAVING COUNT(*) > 1;
```

An empty result means that no file was loaded more than once into `my_table`
during that period. The check includes loads made in the other account up to the last refresh before you promoted this account. For those loads, `last_load_time` can be the time of the refresh that replicated them rather than the time that the other account loaded the file. The check doesn’t show files that were never loaded.

If a pipe that you recreated during the outage loads `my_table`, the function
doesn’t return the loads of the pipe that it replaced, so an empty result
doesn’t rule out duplicates. For that table, also run the same check against
the Account Usage [COPY\_HISTORY view](/sql-reference/account-usage/copy_history), filtered on
`table_catalog_name`, `table_schema_name`, and `table_name`, with a role that
can query the `SNOWFLAKE` database, such as `ACCOUNTADMIN`. The view can lag by
up to 2 hours, and by up to 2 days for some tables, so it might not show the
recreated pipe’s most recent loads yet. Run the view check again after 2 hours,
or after 2 days for a table that has had few loads, and treat any file that
either check lists as a duplicate.

To find files that were never loaded, see step 9 of
[Fail back your pipelines](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-steps).

## After you verify

- If a check fails, see
  [Troubleshoot data pipelines after failover or failback](/user-guide/multi-location-resilience-data-pipelines-troubleshoot).
- After a failover, when your primary location is available again, follow
  [Fail back data pipelines](/user-guide/multi-location-resilience-data-pipelines-failback).
- After a failback, return to
  [the remaining failback tasks](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-after-failback) to update the
  setup record and run the validation checks again.
