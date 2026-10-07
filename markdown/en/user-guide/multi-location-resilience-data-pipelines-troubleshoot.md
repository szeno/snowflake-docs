# Troubleshoot data pipelines after failover or failback

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical Edition (or higher).
To inquire about upgrading, contact [Snowflake Support](/user-guide/contacting-support).

Use this topic when one of [the verification checks](/user-guide/multi-location-resilience-data-pipelines-verify#label-mlsi-verify-ingestion) fails after a failover or failback. Run `SYSTEM$PIPE_STATUS` and `DESCRIBE INTEGRATION` in
the account that’s now the primary account, and then find the symptom or the
`executionState` value in the following sections. If a fix rebinds a pipe, sets the active queue of a Multi-Queue Notification Integration (MQNI), or adds or updates an event notification, load the files
that the pipe missed, as described in [After you fix a pipe](#label-mlsi-troubleshoot-after-fix).
After you fix a problem, run the verification checks again.

## Troubleshoot integrations and pipes

The following sections cover symptoms of a Multi-Location Storage Integration (MLSI), an MQNI, and pipe binding first, and then each `executionState` value.

### ACTIVE on the MLSI names the wrong location

Set the MLSI’s `ACTIVE` value to the location that should be active in this account, and then rebind
the pipes on its stages, because changing an MLSI’s `ACTIVE` value doesn’t rebind them:

- **After a failover:** Follow [Set the active storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-storage). Then follow
  [Set the active queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-queue) for pipes that use an MQNI, and rebind each
  SQS-only pipe as described in [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind).
- **After a failback:** Follow the **MLSI** and **Pipes to rebind** fixes in
  [An ACTIVE value isn’t your primary location in step 5](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-fix-active).

### ACTIVE on the MQNI is empty

Set the MQNI’s `ACTIVE` value to the queue for this account’s active location with
`ALTER INTEGRATION ... SET ACTIVE`. After a failover, follow
[Grant access to your secondary queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-queue) and [Set the active queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-queue). After
a failback, use your primary location’s queue, as described in
[An ACTIVE value isn’t your primary location in step 5](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-fix-active).

### ACTIVE on the MQNI names the queue in the region that’s down

Change the active queue to the queue in your healthy region, as described in
[Change the active queue later](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-change-active-queue).

### An MQNI doesn’t exist in your target account

`DESCRIBE INTEGRATION` in your target account returns an error that the MQNI
doesn’t exist or isn’t authorized, or a pipe’s `replicationBindingErrorDetails`
field says that its notification integration wasn’t found. If the setup record
lists the MQNI as created in your target account, it exists. Run
`DESCRIBE INTEGRATION` again with a role that has a privilege on it, and
continue with the check that sent you here. Otherwise, run `SHOW FAILOVER GROUPS` in your target account, and check
`allowed_integration_types` for your failover group:

- **Includes `NOTIFICATION INTEGRATIONS`:** The MQNI exists, unless you
  created it in your source account after the last refresh that completed.
  Run `DESCRIBE INTEGRATION` again with a role that has a privilege on it, such
  as `ACCOUNTADMIN`. If it succeeds, continue with the check that sent you
  here. If it still returns the error, the MQNI and the pipes that use it didn’t replicate
  before the outage, so don’t create the MQNI now. Note the pipes as pipes to
  recreate in [step 3 of the failover runbook](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-failover-step-3),
  as described in
  [Recreate pipes that can’t load after a failover](#label-mlsi-recreated-pipes). If you don’t recreate them in your target
  account, the refresh during failback drops them, and the rows that they
  loaded, from your source account. Then continue with the check that sent you
  here.
- **Doesn’t include it:** The group doesn’t replicate notification
  integrations, as on the Amazon SQS-only path, so an MQNI that you created
  after setup never reached your target account. Don’t change the failover
  group, because the refresh during failback would then drop the notification
  integrations that you created directly in your source account.

Snowflake binds a replicated pipe to the notification integration, in the
pipe’s own account, whose name matches the pipe’s `INTEGRATION` value. In your
target account, do the following:

1. Create an MQNI with the same name and the same `QUEUES` list as the MQNI in
   your source account, with `ACTIVE` set to the queue for your secondary
   location, as described in
   [CREATE NOTIFICATION INTEGRATION (inbound from multiple queues)](/sql-reference/sql/create-notification-integration-multi-queue). Get the
   name and queues from [the setup record](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-setup-record), or from
   `DESCRIBE INTEGRATION` in your source account if it’s reachable, or from
   your own deployment scripts. For each
   queue, include only `NAME`, `NOTIFICATION_PROVIDER`, and the provider’s
   queue fields:

   - **Amazon SNS:** `AWS_SNS_TOPIC_ARN`
   - **Google Cloud Pub/Sub:** `GCP_PUBSUB_SUBSCRIPTION_NAME`
   - **Azure Queue Storage:** `AZURE_STORAGE_QUEUE_PRIMARY_URI` and
     `AZURE_TENANT_ID`

   Leave out the other fields that `DESCRIBE INTEGRATION` shows, such as
   `GCP_PUBSUB_SERVICE_ACCOUNT` or `AZURE_CONSENT_URL`, because
   `CREATE NOTIFICATION INTEGRATION` rejects them. Don’t use
   `CREATE OR REPLACE`: if an MQNI with that name already exists, replacing it
   invalidates all pipes that use it, and you then have to set its active
   queue again and recreate each of those pipes.
2. Grant your target account access to your secondary queue, as described in
   [Grant access to your secondary queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-queue).
3. Set the active queue again with the name of your secondary location’s
   queue, which you set as `ACTIVE` in item 1, as described in
   [Set the active queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-queue). The statement binds the pipes that use the
   MQNI.
4. Add the MQNI, its `QUEUES` list, and its `ACTIVE` value in your target
   account to the setup record, and note that you created it in your target
   account. On Azure and Google Cloud, also run `SYSTEM$PIPE_STATUS` for each
   pipe that uses the MQNI, and record its `notificationChannelName` value for
   your target account.

Your source account keeps its own MQNI with the same name, so failback doesn’t
need to move this MQNI.

If you later add notification integrations to the failover group, the next
refresh drops the MQNI that you created in your target
account and replaces it with a replica that has no active queue, as described
in [Replicate your integrations to the target account](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-replicate-integrations). After that refresh, complete
[Grant access to your secondary queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-queue) and [Set the active queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-queue) for
the replica. Then, in the setup record, remove the note that you created the
MQNI in your target account, and update its `ACTIVE` value for your target
account. On Azure and Google Cloud, confirm that each pipe’s
`notificationChannelName` value still names your secondary queue.

### SYSTEM$PIPE\_STATUS has no notificationChannelName field

The pipe isn’t bound to a queue in this account. If the output includes
`replicationBindingErrorDetails`, read that field, and fix the cause. For a
pipe that uses an MQNI, run `DESCRIBE INTEGRATION`. If it returns an error
that the MQNI doesn’t exist or isn’t authorized, see
[An MQNI doesn’t exist in your target account](#label-mlsi-troubleshoot-mqni-missing). If `ACTIVE` is empty,
see [ACTIVE on the MQNI is empty](#label-mlsi-troubleshoot-mqni-empty). If `ACTIVE` names a queue, set the
active queue again with that queue name, as described in
[Set the active queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-queue). For an SQS-only pipe, rebind it as
described in [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind). If none of these applies, wait a few
minutes, and check again.

### notificationChannelName matches the other account’s value

On Azure or Google Cloud, a matching `notificationChannelName` value means that the active queue in this account is wrong. Change it as described in [Change the active queue later](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-change-active-queue).

### An SQS-only pipe is RUNNING, but lastIngestedTimestamp doesn’t advance

On Amazon S3, an SQS-only pipe has an `integration` of `NULL` and a
`notification_channel` that’s an Amazon SQS ARN. If you use single-write, first
confirm that your producers write new files to the location that’s now active,
as described in [step 5 of the failover runbook](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-failover-step-5) or
[step 2 of the failback runbook](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-step-2). If you use
dual-write, or if your producers already write there, the bucket for your
active location doesn’t send notifications to this account’s queue:

- **After a failover:** Confirm that you completed
  [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind), including the event
  notification on your secondary bucket. For a pipe that you created after you
  configured your target account, run the **Stage**, **Binding**, and
  **Notifications** steps in [Add pipes after setup](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-add-pipes-later). Make any stage change in your target account, which is now the primary
  account, and don’t change or refresh the failover group, even where those
  steps say to. For a stage that doesn’t use an MLSI, see
  [Recreate pipes that can’t load after a failover](#label-mlsi-recreated-pipes).
- **After a failback:** Confirm that the event notification on your primary
  bucket targets the `notification_channel` ARN that `DESCRIBE PIPE` reports in
  your source account. For a pipe that you created in your target account
  during the outage, run the **Stage**, **Binding**, and **Notifications**
  checks in [Check objects that you created during the outage](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-outage-objects). Make any stage change in
  your source account, which is now the primary account, and don’t repeat the
  failover group refresh. Then load the files that the pipe missed, as described in
  [After you fix a pipe](#label-mlsi-troubleshoot-after-fix).

### A pipe that uses an MQNI is RUNNING, but lastIngestedTimestamp doesn’t advance

Notifications for new files aren’t reaching the pipe in this account. Check the
following:

- If you use single-write, confirm that your producers write new files to the
  location that’s now active, as described in
  [step 5 of the failover runbook](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-failover-step-5) or
  [step 2 of the failback runbook](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-step-2).
- On Amazon S3, run `DESCRIBE PIPE`, and confirm that `notification_channel`
  shows the SNS topic for your active location. If it shows the other
  location’s topic, run `DESCRIBE INTEGRATION my_mqni`, and check `ACTIVE`:

  - If `ACTIVE` names the other location’s queue, change the active queue as
    described in [Change the active queue later](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-change-active-queue).
  - If `ACTIVE` is empty, see [ACTIVE on the MQNI is empty](#label-mlsi-troubleshoot-mqni-empty).
  - If `ACTIVE` names your active location’s queue, run
    `ALTER INTEGRATION my_mqni SET ACTIVE` again with that queue name.

  In each case, setting the active queue rebinds every pipe that uses the
  MQNI.
- On Azure and Google Cloud, run `SYSTEM$PIPE_STATUS`, and confirm that
  `notificationChannelName` differs from the value that the same pipe reports
  in the other account or, if that account is unreachable, from the other
  account’s value in [the setup record](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-setup-record). If it
  matches, change the active queue as described in
  [Change the active queue later](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-change-active-queue).
- Confirm that the event notifications for your active location cover the
  pipe’s path and reach the MQNI’s queue for that location, as described in
  [Prepare your messaging service for an MQNI](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-prepare-messaging).
- **After a failover:** For a pipe that you created after you configured your
  target account, run the **Stage**, **Binding**, and **Notifications** steps
  in [Add pipes after setup](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-add-pipes-later). Make any stage change in your target account, which is now the primary
  account, and don’t change or refresh the failover group, even where those
  steps say to. For a stage that doesn’t use an MLSI, see
  [Recreate pipes that can’t load after a failover](#label-mlsi-recreated-pipes). If the pipe’s MQNI doesn’t exist in your
  target account, see [An MQNI doesn’t exist in your target account](#label-mlsi-troubleshoot-mqni-missing).
- **After a failback:** For a pipe that you created during the outage, run the
  checks in [Check objects that you created during the outage](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-outage-objects).

### channelErrorMessage is present

Snowflake can’t read the active queue in this account:

- **After a failover:** For a pipe that uses an MQNI, repeat
  [Grant access to your secondary queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-queue). For an SQS-only pipe, confirm that you
  completed [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind) and that the result
  named your secondary region’s queue. For a pipe that you created after you
  configured your target account, run the **Stage**, **Binding**, and
  **Notifications** steps in [Add pipes after setup](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-add-pipes-later). Make any stage change in your target account, which is now the primary
  account, and don’t change or refresh the failover group, even where those
  steps say to. For a stage that doesn’t use an MLSI, see
  [Recreate pipes that can’t load after a failover](#label-mlsi-recreated-pipes). If the pipe’s MQNI doesn’t exist in your
  target account, see [An MQNI doesn’t exist in your target account](#label-mlsi-troubleshoot-mqni-missing).
- **After a failback:** For a pipe that uses an MQNI, confirm that your primary
  queue grants access to your source account. For an MQNI that you created
  during the outage, grant your source account access to its primary queue, as
  described in [An ACTIVE value isn’t your primary location in step 5](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-fix-active).

### executionState is FAILING\_OVER

Snowflake is still syncing the replicated load history for the table that the
pipe loads. The pipe can load new files in this state, and it changes to
`RUNNING` when the sync finishes. To monitor the sync, check
`loadHistoryRemainingEntriesToSync` in the output.

### executionState is READ\_ONLY

The pipe’s database, or the database of the table that it loads, is a secondary
database in the account that you’re connected to. Confirm that you promoted
every failover group that contains your pipeline databases.

### executionState is PAUSED

The pipe is paused. A paused pipe shows `PAUSED` even while its database is
still secondary. Because the paused state replicates, a pipe that was paused in
the other account at the last refresh is also paused here. Confirm that you
promoted the failover group, and then resume the pipe with
`ALTER PIPE <pipe_name> SET PIPE_EXECUTION_PAUSED = FALSE`.

### executionState is STALLED\_STAGE\_PERMISSION\_ERROR

The integration’s cloud identity in this account can’t read your active
location. After a failover, repeat [Grant access to your secondary storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-storage). After
a failback, repeat the grant for your primary location in
[Grant access to your primary location](/user-guide/multi-location-resilience-data-pipelines-setup-storage#label-mlsi-grant-primary-storage). On AWS, keep the existing trust policy
entries. For an MLSI that you created during the outage, grant access as
described in [An ACTIVE value isn’t your primary location in step 5](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-fix-active).

### Any other state

Check the `error` field, and see
[SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status).

### After you fix a pipe

If a fix in this topic rebinds a pipe, sets an MQNI’s active queue, or adds or
updates an event notification, the pipe didn’t receive notifications for files
that arrived before the fix. In the account that’s now the primary account, run
`ALTER PIPE ... REFRESH` for each affected pipe, as described in step 6 of
[Fail back your pipelines](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-steps). The affected pipes are every pipe that uses
each MQNI whose active queue you set, each pipe that you rebound, and each pipe
whose event notification you added or updated. For a pipe that you recreated during the
outage, follow [Load files for a recreated pipe](#label-mlsi-recreated-pipes-load) instead, for the last 7
days.

## Recreate pipes that can’t load after a failover

After a failover, a pipe whose stage doesn’t use an MLSI can’t load from your
secondary location, and a rebind doesn’t fix it. Changing the stage in your
target account to use an MLSI makes it resolve to a different location, so
Snowflake marks the stage’s pipes invalid. This section also applies to two
other kinds of pipe:

- A pipe on a stage whose MLSI can’t be found in your target account, as
  described in [An ACTIVE value doesn’t match in step 1](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-failover-fix-active). Recreate the stage with the
  MLSI in your target account first, with `CREATE OR REPLACE STAGE` and the
  stage’s existing name, and then its pipes.
- A pipe that you created in your source account after the last refresh that
  completed, so that it isn’t in your target account. If its MQNI isn’t in
  your target account either, create the MQNI there first. If `my_fg`
  replicates notification integrations, create the MQNI as described in
  [CREATE NOTIFICATION INTEGRATION (inbound from multiple queues)](/sql-reference/sql/create-notification-integration-multi-queue), with the
  name and `QUEUES` list from the setup record, or from `DESCRIBE INTEGRATION`
  in your source account if it’s reachable, or from your own deployment
  scripts. Include only the queue fields that
  item 1 of the numbered steps in [An MQNI doesn’t exist in your target account](#label-mlsi-troubleshoot-mqni-missing)
  lists, and follow the MQNI rules in [Create stages, integrations, or pipes during an outage](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-create-during-outage).
  If `my_fg`
  doesn’t replicate notification integrations, follow the numbered steps in
  [An MQNI doesn’t exist in your target account](#label-mlsi-troubleshoot-mqni-missing), and then return here. Get each pipe’s definition from
  your source account with `GET_DDL` if it’s reachable, or from your own
  deployment scripts.

In your target account, recreate each of those pipes as
described in [Associate the MLSI with your external stages](/user-guide/multi-location-resilience-data-pipelines-setup-storage#label-mlsi-stage-setup), and follow the rules in
[Create stages, integrations, or pipes during an outage](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-create-during-outage), including the event notification on your
secondary bucket for each recreated pipe’s path. A recreated pipe has no load
history, so load the files that it missed with `ALTER PIPE ... REFRESH`, with
`MODIFIED_AFTER` set to your `<last_snapshot>` time in ISO 8601 format, such as
`'2026-10-01T18:30:00-07:00'`. Don’t use an earlier time, because the pipe can
reload files whose rows your target account already has. To convert
`<last_snapshot>` to that format, run the following query:

Copy code

```
SELECT TO_VARCHAR('<last_snapshot>'::TIMESTAMP_LTZ, 'YYYY-MM-DD"T"HH24:MI:SSTZH:TZM');
```

Record each pipe that you recreate, as described in
[Values to save during failover](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-handoff-values).

## Load files for a recreated pipe

A recreated pipe has no load history from before you recreated it, so it doesn’t
skip files that the original pipe loaded. This section doesn’t replace the
`MODIFIED_AFTER` refresh that you run right after you recreate the pipe, as
described in [Recreate pipes that can’t load after a failover](#label-mlsi-recreated-pipes). When a later step or check in these topics tells you to run
`ALTER PIPE ... REFRESH` for a pipe that you recreated during the outage, or to
copy files for the table that it loads, do the following instead, in the
account that’s now the primary account:

1. Wait until `SYSTEM$PIPE_STATUS` shows `pendingFileCount` as `0` for the pipe
   on two checks a few minutes apart.
2. Query the Account Usage [COPY\_HISTORY view](/sql-reference/account-usage/copy_history) for
   the table that the pipe loads, for rows whose `last_load_time` is at or
   after the beginning of the period that the step covers. Include only rows
   whose `status` is `Loaded` or `Partially loaded`. Use a role that can
   query the `SNOWFLAKE` database, such as `ACCOUNTADMIN`. The view includes
   loads replicated from the other account, and their `last_load_time` is the
   time of the refresh that replicated them, which is later than the load, so
   the filter still includes them. Don’t rely on the
   [COPY\_HISTORY](/sql-reference/functions/copy_history) table function alone: recreating a
   pipe removes the original pipe’s loads from the function’s results, but the
   view keeps them. The view can lag by up to 2 hours, and by up to 2 days for
   some tables, so also run the table function for the same period, and
   combine the two results.
3. Compare the files from that period with the files in the combined result.
   The files from that period are the files in the location that the pipe
   reads or, in step 1 of [Fail back your pipelines](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-steps), the files that the
   source account query in that step lists. `file_name` is relative to `stage_location`, which includes
   any path that the pipe’s `COPY INTO` statement adds to the stage, such as
   `my_pipe/`. For each row, compare the path after the `STORAGE_BASE_URL` in
   `stage_location`, followed by `file_name`, not the full URL or `file_name`
   alone.
4. Act only on the files that the combined result doesn’t list. Load them with a manual
   `COPY INTO` command, or, in step 1 of [Fail back your pipelines](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-steps), copy
   them to your secondary location.
