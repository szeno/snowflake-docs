# Fail over data pipelines

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical Edition (or higher).
To inquire about upgrading, contact [Snowflake Support](/user-guide/contacting-support).

Use this runbook during an outage of your primary location to move your data
ingestion to your secondary location. It assumes that you completed
[Set up multi-location resilience for data pipelines](/user-guide/multi-location-resilience-data-pipelines-setup). Your *source
account* is the account where you set up your pipelines, and your *target
account* holds the replicas, as described in [How multi-location resilience works](/user-guide/multi-location-resilience-data-pipelines#label-mlsi-how-it-works). You
run every step in your target account, so you don’t need your source account,
except for an optional part of step 3.

The runbook has the following steps:

1. [Check your setup and integrations](#label-mlsi-failover-step-1).
2. [Record the snapshot time of your last refresh](#label-mlsi-failover-step-2).
3. [Promote your target account](#label-mlsi-failover-step-3).
4. [Start your `COPY INTO` jobs](#label-mlsi-failover-step-4), if you run them.
5. [Reroute your producers](#label-mlsi-failover-step-5), only if you use
   single-write.
6. [Leave refreshes suspended in your source account](#label-mlsi-failover-step-6),
   only if you use single-write.

Then [verify that ingestion resumed](/user-guide/multi-location-resilience-data-pipelines-verify#label-mlsi-verify-ingestion). If a step
doesn’t go as described, see [If a step fails](#label-mlsi-failover-if-fails).

## Before you start

Make sure that your on-call responders can use roles with the following
privileges, or `ACCOUNTADMIN`:

- **Step 2:** `OWNERSHIP` on the failover group, to suspend its replication
  schedule.
- **Step 2, if `LAST_SNAPSHOT` is `NULL`:** Access to the `SNOWFLAKE`
  database, for the Account Usage view that
  [the fallback query](#label-mlsi-failover-null-snapshot) reads.
- **Step 3:** `OWNERSHIP` or `FAILOVER` on the failover group.
- **Other steps, including creating objects during the outage:** The
  privileges that each statement’s reference topic lists under access control
  requirements. Also `OWNERSHIP` on each integration whose `ACTIVE` value you
  set, `ACCOUNTADMIN` to rebind SQS-only pipes, and
  `CREATE INTEGRATION` on the account to create an integration, as described
  in [Create stages, integrations, or pipes during an outage](#label-mlsi-create-during-outage).

Your on-call responders also need permission in your cloud provider to edit
the access policies and event notifications of your storage locations and
queues, for the fixes in [An ACTIVE value doesn’t match in step 1](#label-mlsi-failover-fix-active) and for objects
that you create during the outage.

### Which steps you run

The steps that you run depend on whether your producers use dual-write or
single-write, as described in [Choose how your producer writes files](/user-guide/multi-location-resilience-data-pipelines#label-mlsi-choose-routing). Snowflake doesn’t
record this choice, so check [the setup record](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-setup-record). Then
run the steps for your method:

- **Dual-write:** Run steps 1 through 4.
- **Single-write:** Run every step.

### Values to save during failover

The engineer who fails back might not be the one who failed over. During
failover, save the following values for each failover group in a place where
whoever fails back can find them, such as your incident record:

- `<last_snapshot>`, from step 2. You use it to check for duplicate loads, to
  load missed files for a pipe that you recreate, and, if you use single-write,
  to load primary-only files in step 1 of the failback
  runbook.
- `<reconcile_from_iso_8601>`, also from step 2, only if you use single-write. You use it in step 9 of the failback runbook.
- `<promotion_time>`, from step 3. You use it to verify ingestion.
- The name of each stage, integration, and pipe that you create in your target
  account during the outage, and which of those pipes replace a pipe that
  existed before. Step 5 of the failback runbook checks them, and steps 1, 6,
  and 9 handle recreated pipes differently.

## Fail over your pipelines

Because you preconfigured the active storage location and queue during setup,
failover in Snowflake takes one `ALTER FAILOVER GROUP ... PRIMARY` command for
each failover group. The other steps prepare for that command and restart the
loads that pipes don’t run automatically.

### Step 1: Check your setup and integrations

1. In the setup record that you saved in [Record your setup for on-call responders](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-setup-record), check
   whether your producers use dual-write or single-write. Snowflake doesn’t record this choice, and the choice determines which steps you run. If you use
   single-write, ask the teams that own your producers to get ready to reroute
   them in step 5.
2. In your target account, run [SHOW FAILOVER GROUPS](/sql-reference/sql/show-failover-groups) to
   find your failover group. The output has a row for each account in the
   group. In the row whose `account_name` is your target account, `is_primary`
   is `false`. To get your account name, run `SELECT CURRENT_ACCOUNT_NAME();`.
   Use the group’s name wherever this topic shows `my_fg`. If more than one
   group contains your pipeline databases or integrations, run the following
   steps for each group.
3. On Amazon S3, list the pipes that use the Amazon SQS-only path. A protected
   pipe uses that path if its `integration` is `NULL` and its
   `notification_channel` is an Amazon SQS ARN (`arn:aws:sqs:...`). You need
   this list for the pipe checks in [Verify data pipelines after failover or failback](/user-guide/multi-location-resilience-data-pipelines-verify#label-mlsi-verify-ingestion). The
   following statements return the list:

   Copy code

   ```
   SHOW PIPES IN ACCOUNT;

   SELECT "database_name", "schema_name", "name", "notification_channel"
     FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
     WHERE "integration" IS NULL
       AND "notification_channel" LIKE 'arn:aws%:sqs:%';
   ```

   `SHOW PIPES` lists only the pipes that your role can access, so compare the
   result with the SQS-only pipes in your setup record.
4. Confirm that your integrations still point at your secondary location. In
   your target account, run `DESCRIBE STORAGE INTEGRATION` for each Multi-Location Storage Integration (MLSI), and `DESCRIBE INTEGRATION` for each Multi-Queue Notification Integration (MQNI). Compare each `ACTIVE` value with your target account’s values in
   [the setup record](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-setup-record), which include any change that
   you made after setup. The **After a failover** column in
   [the table of expected values](/user-guide/multi-location-resilience-data-pipelines-verify#label-mlsi-check-active) shows the same
   values with example names. If a value doesn’t
   match, fix it before you promote, as described in
   [An ACTIVE value doesn’t match in step 1](#label-mlsi-failover-fix-active). If `DESCRIBE INTEGRATION` returns an
   error that an MQNI doesn’t exist or isn’t authorized, follow
   [An MQNI doesn’t exist in your target account](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-troubleshoot-mqni-missing) before you promote. If you create
   the MQNI there, add every pipe that uses it to the pipes that you load in
   step 3.
   Then continue with the next integration in this item, or with item 5.
5. If you use Snowpipe, check each pipe that was added after setup. A pipe
   that wasn’t bound in your target account, as described in step 2 of
   [Add pipes after setup](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-add-pipes-later), doesn’t load after you promote, and its
   status can look normal. If a pipe isn’t in your target account because
   you created it after the last refresh that completed, note it as a pipe to
   recreate, and skip the rest of this item for it. Also skip each pipe that
   you noted to recreate in [An ACTIVE value doesn’t match in step 1](#label-mlsi-failover-fix-active). For each pipe
   that wasn’t bound,
   or that you aren’t sure about, do the following:

   1. Run `LIST` on the pipe’s stage. If it returns an error or file URLs that
      aren’t in your secondary location, and the stage uses an MLSI, complete the **Stage**
      step in [Add pipes after setup](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-add-pipes-later) for that MLSI now. If the stage
      doesn’t use an MLSI, don’t bind the pipe. Note it as a pipe to
      recreate, and skip the rest of this list for it.
   2. Bind the pipe. For a pipe that uses an MQNI, set the MQNI’s active queue
      again with the queue that’s already active, as described in
      [Set the active queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-queue). For an SQS-only pipe, follow [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind).
   3. Make sure that your secondary location’s event notifications cover the
      pipe, as described in the **Notifications** step in
      [Add pipes after setup](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-add-pipes-later).
   4. Note the pipes that use each MQNI whose active queue you set, each pipe
      that you rebound, and each pipe whose event notification you added or
      updated, so that you load their files in step 3.

   Then continue with step 2.

### Step 2: Record the snapshot time of your last refresh

In your target account, before you promote it, do the following:

1. If `my_fg` has a replication schedule, suspend it, so that a scheduled
   refresh can’t finish after you record the snapshot time. The schedule is in
   the `replication_schedule` column of the `SHOW FAILOVER GROUPS` output from
   step 1. Use a role with the `OWNERSHIP` privilege on `my_fg`:

   Copy code

   ```
   ALTER FAILOVER GROUP my_fg SUSPEND;
   ```

   If the statement reports that the schedule is already suspended, continue.
   If no role with `OWNERSHIP` is available, see
   [You can’t suspend the replication schedule in step 2](#label-mlsi-failover-no-ownership). Suspending the schedule doesn’t stop
   a refresh that’s already in progress. Step 3 covers that case.
2. Run the following query, and save the `LAST_SNAPSHOT` value, including its
   time zone offset, as `<last_snapshot>`. If you use single-write, also save the
   `RECONCILE_FROM_ISO_8601` value as `<reconcile_from_iso_8601>`:

   Copy code

   ```
   SELECT MAX(primary_snapshot_timestamp) AS last_snapshot,
          TO_VARCHAR(DATEADD(day, -1, MAX(primary_snapshot_timestamp)),
                     'YYYY-MM-DD"T"HH24:MI:SSTZH:TZM') AS reconcile_from_iso_8601
     FROM TABLE(my_db.INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_HISTORY('my_fg'))
     WHERE phase_name = 'COMPLETED';
   ```

   `PRIMARY_SNAPSHOT_TIMESTAMP` is the point in time of your source account’s
   data that the refresh copied.
   [REPLICATION\_GROUP\_REFRESH\_HISTORY](/sql-reference/functions/replication_group_refresh_history)
   takes only the group name and returns refreshes from the last 14 days.
   `RECONCILE_FROM_ISO_8601` is one day before the snapshot, in the ISO 8601
   format that step 9 of [Fail back your pipelines](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-steps) needs.

   If `LAST_SNAPSHOT` is `NULL`, don’t continue with that value. See
   [LAST\_SNAPSHOT is NULL in step 2](#label-mlsi-failover-null-snapshot).

### Step 3: Promote your target account

1. If you didn’t suspend the replication schedule in step 2, run the query in
   step 2 again now, and save the new values.
2. If your source account is reachable, for example during a test, suspend the
   tasks that run your `COPY INTO` statements there, or their root tasks. Until
   your source account learns that it’s the secondary account, its tasks can
   still start runs.
3. In your target account, use a role with the `OWNERSHIP` or `FAILOVER` privilege on the
   failover group to run the following command:

   Copy code

   ```
   ALTER FAILOVER GROUP my_fg PRIMARY;
   ```

   If the command fails because a refresh operation is still in progress, see
   [A refresh is in progress when you promote in step 3](#label-mlsi-failover-refresh-in-progress).
4. As soon as `ALTER FAILOVER GROUP my_fg PRIMARY` succeeds, run the following
   query, and save the result, including its time zone offset, as
   `<promotion_time>`. You need it to verify ingestion.

   Copy code

   ```
   SELECT CURRENT_TIMESTAMP();
   ```
5. If you noted pipes to load in step 1 or in [An ACTIVE value doesn’t match in step 1](#label-mlsi-failover-fix-active), run the following
   statement for each of them now. It loads files staged within the last 7
   days, and the pipe skips files that its load history records as loaded:

   Copy code

   ```
   ALTER PIPE my_db.my_schema.my_pipe REFRESH;
   ```
6. For each pipe that you noted as a pipe to recreate in step 1 or in
   [An ACTIVE value doesn’t match in step 1](#label-mlsi-failover-fix-active), follow [Recreate pipes that can’t load after a failover](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-recreated-pipes)
   now.

Your target account is now the primary account and your source account is the
secondary account. The failover group in your source account is now a secondary
group, which is why the refresh operation during failback runs there. With
dual-write, your pipes automatically resume loading from your secondary
location. Tasks and other `COPY INTO` jobs resume in step 4.

### Step 4: Start your COPY INTO jobs (if you run them)

- **Tasks:** Run `SHOW TASKS IN DATABASE my_db`. A task whose `state` is
  `started` is scheduled again automatically. Resume each task that your setup
  record lists as resumed and whose `state` is `suspended`, in the order
  described in [Resume suspended tasks and task graphs](#label-mlsi-failover-resume-tasks). Then return to this
  step.
- **Other `COPY INTO` jobs:** Run them in your target account, or point the
  scheduler that runs them at your target account.

### Step 5: Reroute your producers (single-write only)

Point each producer application at your secondary cloud storage
location, using the same relative paths as your primary location. For how
those paths resolve, see [How paths resolve in each location](/user-guide/multi-location-resilience-data-pipelines-setup-storage#label-mlsi-path-structure). Snowflake doesn’t
replicate your storage files, so no new data from those producers arrives until
you do this.

### Step 6: Leave refreshes suspended in your source account (single-write only)

Failing over suspends scheduled refreshes of the secondary group in your source
account. Don’t run `ALTER FAILOVER GROUP my_fg RESUME` there, even though the
[Resume scheduled replication in target accounts](/user-guide/account-replication-failover-failback#label-resume-scheduled-replication-in-target-accounts) section says to
resume them after a failover.

Warning

A refresh in your source account overwrites rows that exist only in your source
account. Failback runs manual refreshes only from its step 4 onward, after its
steps 1 and 3 load those rows into your target account.

## After you fail over

- To confirm that ingestion resumed, see [Verify data pipelines after failover or failback](/user-guide/multi-location-resilience-data-pipelines-verify#label-mlsi-verify-ingestion).
- When your primary location is available again, follow
  [Fail back data pipelines](/user-guide/multi-location-resilience-data-pipelines-failback).

## Resume suspended tasks and task graphs

Resume each suspended task with
[ALTER TASK … RESUME](/sql-reference/sql/alter-task). In a task graph, you
can resume a child task only while its root task is suspended:

- If a root task is suspended, resume its child tasks first and then the root
  task. If your setup record lists every task in the graph as resumed, you can
  instead resume them all with
  [SYSTEM$TASK\_DEPENDENTS\_ENABLE](/sql-reference/functions/system_task_dependents_enable).
- If only a child task is suspended, suspend its root task, resume the child
  task, and then resume the root task.

## If a step fails

Find the problem in the following sections. Each section says where to continue
in the runbook.

### An ACTIVE value doesn’t match in step 1

Fix each integration whose `ACTIVE` value doesn’t match your target account’s
value in [the setup record](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-setup-record):

- **MLSI:** If the setup record doesn’t show your target account’s value for
  the MLSI, or you aren’t sure that your target account can access your
  secondary location through it, follow [Grant access to your secondary storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-storage).
  Then follow [Set the active storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-storage), and run `LIST` on each of the
  MLSI’s stages to confirm access. If it returns a permission error, follow
  [Grant access to your secondary storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-storage), and run `LIST` again. A cloud
  provider’s policy change can take a few minutes to take effect, so if the
  error persists, wait, and run it again. If the permission error still
  persists, or `LIST` returns any error other than one that
  says the stage’s integration can’t be found, run `DESCRIBE STORAGE INTEGRATION` in your target account, and confirm
  that your secondary location’s policy allows the identity in the
  `STORAGE_LOCATION_<n>` row for your secondary location. On Amazon S3, check
  that the trust policy of that row’s `STORAGE_AWS_ROLE_ARN` has an entry
  for the row’s `STORAGE_AWS_IAM_USER_ARN` value with its
  `STORAGE_AWS_EXTERNAL_ID` value. If
  the identity isn’t allowed, follow [Grant access to your secondary storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-storage) for
  that identity, and run `LIST` again. If the policy that grants the identity
  access to your secondary location doesn’t cover the stage’s path, update it
  to cover the path, and run `LIST` again. On Amazon S3, that’s the
  permissions policy of the IAM role, not its trust policy. For the permissions that it needs, see
  [Configure access permissions for the S3 bucket](/user-guide/data-load-s3-config-storage-integration#label-s3-storage-integration-required-actions). Otherwise, contact
  [Snowflake Support](/user-guide/contacting-support). Don’t
  refresh the failover group or change your source account. If `LIST` returns an error
  that the stage’s integration can’t be found, don’t refresh the failover
  group. Note the stage’s pipes as pipes to recreate in step 3. When you
  recreate them in step 3, also recreate the stage with the MLSI in your
  target account, as described in [Associate the MLSI with your external stages](/user-guide/multi-location-resilience-data-pipelines-setup-storage#label-mlsi-stage-setup), with
  `CREATE OR REPLACE STAGE` and the stage’s existing name. Changing an MLSI’s `ACTIVE`
  value doesn’t rebind the pipes on its stages, so rebind them, except the
  pipes that you noted to recreate:
  - For pipes that use an MQNI, follow [Set the active queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-queue). If the
    setup record doesn’t show that you granted your target account access to
    the MQNI’s secondary queue, follow [Grant access to your secondary queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-queue)
    first. If `DESCRIBE INTEGRATION` returns
    an error that the MQNI doesn’t exist or isn’t authorized, skip it here. Item 4 of step 1 sends you to
    [An MQNI doesn’t exist in your target account](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-troubleshoot-mqni-missing).
  - For each SQS-only pipe on those stages, follow [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind).
- **MQNI:** Follow [Grant access to your secondary queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-queue) and
  [Set the active queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-queue).

If you changed any `ACTIVE` value or rebound any pipe, note every pipe that
uses each MQNI whose active queue you set and each pipe that you rebound,
except pipes that you noted to recreate.
They didn’t receive notifications for files that arrived before the change, so
you load those files in step 3, after you promote. In
[the setup record](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-setup-record), record each `ACTIVE` value that
you set in your target account. Then return to item 4 of step 1, and continue
with the next integration, or with item 5 if you’ve checked every integration.

### You can’t suspend the replication schedule in step 2

If no role with the `OWNERSHIP` privilege on `my_fg` is available, skip the
`ALTER FAILOVER GROUP my_fg SUSPEND` statement, and continue with the query in
step 2. Then run that query again just before you promote in step 3.

### LAST\_SNAPSHOT is NULL in step 2

Run the query again with a role that has a privilege on `my_fg`, such as the
role that you use in step 3. If it’s still `NULL`, no refresh completed in the
last 14 days. Run the following query instead, with a role that can query the
`SNOWFLAKE` database, such as `ACCOUNTADMIN`. It reads the
[Account Usage view](/sql-reference/account-usage/replication_group_refresh_history)
of the same history:

Copy code

```
SELECT MAX(primary_snapshot_timestamp) AS last_snapshot,
       TO_VARCHAR(DATEADD(day, -1, MAX(primary_snapshot_timestamp)),
                  'YYYY-MM-DD"T"HH24:MI:SSTZH:TZM') AS reconcile_from_iso_8601
  FROM SNOWFLAKE.ACCOUNT_USAGE.REPLICATION_GROUP_REFRESH_HISTORY
  WHERE replication_group_name = 'MY_FG'
    AND phase_name = 'COMPLETED';
```

If either query returns a value, save `LAST_SNAPSHOT`, including its time zone
offset, as `<last_snapshot>` and, if you use single-write, `RECONCILE_FROM_ISO_8601` as
`<reconcile_from_iso_8601>`. Then continue with step 3.

If this query also returns `NULL`, your target account might not have a
complete copy of your data. Don’t promote it until you find out why. For help,
contact [Snowflake Support](/user-guide/contacting-support).

### A refresh is in progress when you promote in step 3

Check the refresh’s phase before you decide whether to cancel it. In your
target account, run the following query:

Copy code

```
SELECT phase_name, start_time, end_time
  FROM TABLE(my_db.INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_PROGRESS('my_fg'))
  ORDER BY start_time;
```

Then act on the phase in the last row:

- **`SECONDARY_DOWNLOADING_METADATA` or `SECONDARY_DOWNLOADING_DATA`:** Don’t
  cancel the refresh, because canceling it in these phases can leave your
  target account in an inconsistent state. A refresh in these phases finishes
  even while your source account is unavailable. Wait until the last row shows
  `COMPLETED`, `FAILED`, or `CANCELED`.
- **Any other phase:** You can safely cancel the refresh. How you cancel it
  depends on how the refresh started:

  1. If `my_fg` has no replication schedule, or you know that someone started
     the refresh manually, skip the next item.
  2. If no role with the `OWNERSHIP` privilege on `my_fg` is available, wait
     until the last row shows `COMPLETED`, `FAILED`, or `CANCELED`, as for the
     downloading phases. Otherwise, use a role with `OWNERSHIP` on `my_fg` to
     run `ALTER FAILOVER GROUP my_fg SUSPEND IMMEDIATE`, and then run the
     preceding query again. If the last row shows `COMPLETED`, `FAILED`, or
     `CANCELED` within a few minutes, the refresh has ended. If it doesn’t,
     continue with the next item.
  3. Run the preceding query again. If the last row shows `COMPLETED`,
     `FAILED`, or `CANCELED`, the refresh has ended. If it shows a downloading
     phase, don’t cancel the refresh, and wait as described for the
     downloading phases. Otherwise, cancel the refresh as described in steps 1
     and 2 of
     [Cancel an in-progress refresh operation that wasn’t automatically scheduled](/user-guide/account-replication-failover-failback#label-cancel-manually-triggered-refresh-operation). Then return to
     this topic, and continue with the paragraph that follows the list of
     phases.

After the refresh ends or you cancel it, run the query in step 2 again, and save
the new values. Then run `ALTER FAILOVER GROUP my_fg PRIMARY` again. When it
succeeds, continue with item 4 of step 3. For more information, see
[Resolving failover statement failure due to an in-progress refresh operation](/user-guide/account-replication-failover-failback#label-failover-resolve-in-progress-refresh).

## Create stages, integrations, or pipes during an outage

If you create stages, integrations, or auto-ingest pipes in your target account
while it’s the primary account, set them up so that failback can move them:

- Use an MLSI for each new stage, as described in [Associate the MLSI with your external stages](/user-guide/multi-location-resilience-data-pipelines-setup-storage#label-mlsi-stage-setup).
- In a new MLSI or MQNI, include both your primary and secondary storage
  locations or queues, and set `ACTIVE` to your secondary one. During failback,
  you make the primary one active in your source account, as described in step
  5 of [Fail back your pipelines](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-steps).
- Grant your target account access to the secondary location of each new MLSI
  and the secondary queue of each new MQNI, as described in
  [Grant access to your secondary storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-storage) and [Grant access to your secondary queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-queue).
  Don’t follow the primary-location grant steps in
  [Grant access to your primary location](/user-guide/multi-location-resilience-data-pipelines-setup-storage#label-mlsi-grant-primary-storage) and
  [Scenario A](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-mqni-scenario-a). On AWS, if the trust policy of
  your secondary location’s role doesn’t already allow the IAM user ARN and
  external ID that you recorded in [Grant access to your secondary storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-storage), add an
  entry for them, and keep the existing entries.
- Create an MQNI only if `my_fg` already replicates notification integrations,
  as set in [Add your integrations to the failover group](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-add-integrations-to-group). Otherwise, the MQNI
  doesn’t reach your source account. If the group doesn’t replicate them, as on
  the Amazon SQS-only path, don’t change the group during the outage. Create
  SQS-only pipes instead, unless the MQNI already exists in your source
  account. For that case, see [An MQNI doesn’t exist in your target account](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-troubleshoot-mqni-missing).
- Make sure that an event notification on your secondary bucket for each new
  pipe’s path targets the pipe’s queue: the `notification_channel` ARN from
  `DESCRIBE PIPE` for an SQS-only pipe, or the MQNI’s queue for your secondary
  location.
- If you recreate a pipe, follow
  [Recreate pipes that can’t load after a failover](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-recreated-pipes), which also loads the files that the pipe
  missed.
- Record the name of each object that you create, alongside the values that you
  saved during failover, as described in [Values to save during failover](#label-mlsi-handoff-values).

When you fail back, step 5 of [Fail back your pipelines](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-steps) checks the objects
that you created.
