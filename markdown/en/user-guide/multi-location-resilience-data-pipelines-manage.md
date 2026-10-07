# Manage multi-location resilience after setup

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical Edition (or higher).
To inquire about upgrading, contact [Snowflake Support](/user-guide/contacting-support).

After you finish
[Set up multi-location resilience for data pipelines](/user-guide/multi-location-resilience-data-pipelines-setup), use these
procedures when you add pipelines or move an account to a different queue.
During a failover or failback, run only the steps that the runbooks or the
troubleshooting topic link to.

## Add pipes after setup

Create the pipe in your source account the same way as during setup, against a
stage that uses a Multi-Location Storage Integration (MLSI), as described in [Associate the MLSI with your external stages](/user-guide/multi-location-resilience-data-pipelines-setup-storage#label-mlsi-stage-setup):

- For a pipe that uses a Multi-Queue Notification Integration (MQNI), create
  the pipe as shown at the end of [Scenario A](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-mqni-scenario-a),
  with an existing MQNI or a new one. If you have more than one MQNI, use the
  one whose queue for your primary location receives the event notifications
  for the pipe’s path, such as the MQNI that other pipes on the same path or a
  parent path use. If you create a new MQNI for the pipe,
  first complete
  [Prepare your messaging service](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-prepare-messaging), and then
  create the MQNI and grant your source account access to its active queue,
  as described in Scenario A. In the pipe definition, type the integration name in uppercase. Make sure
  that your primary location’s event notifications cover the pipe’s path and
  reach the MQNI’s queue for your primary location.
- For an SQS-only pipe, configure the event notification on your primary
  bucket, as described in [Alternative: Set up the Amazon SQS-only path](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-sqs-only-setup).

Then wait for the refresh that replicates the pipe. The pipe’s replica in your
target account doesn’t load from your secondary location until you bind it
there once, even if its status looks normal. Later refreshes keep that binding.
In your target account, do the following:

1. **Stage:** Run `LIST` on the pipe’s stage, and confirm that the file URLs
   are in your secondary location. If they aren’t, fix the stage before you
   bind the pipe, because binding uses the stage’s current location:

   - If the stage doesn’t use an MLSI, change it in your source account as
     described in [Associate the MLSI with your external stages](/user-guide/multi-location-resilience-data-pipelines-setup-storage#label-mlsi-stage-setup), and then refresh the
     failover group in your target account.
   - If the stage uses an MLSI that you created after you configured your
     target account, complete [Grant access to your secondary storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-storage) and
     [Set the active storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-storage) for that MLSI. On AWS, if the trust
     policy of your secondary location’s role doesn’t already allow that IAM
     user ARN with that external ID, add an entry for it, and keep the
     existing entries, which your other integrations use.
2. **Binding:** Bind the pipe to the queue for your secondary location:

   - For a pipe that uses an MQNI that you created after you configured your
     target account, make sure that `my_fg` replicates notification
     integrations, as described in [Add your integrations to the failover group](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-add-integrations-to-group).
     On the Amazon SQS-only path, you omitted them there, so add them, and
     then refresh the failover group in your target account. Then complete
     [Grant access to your secondary queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-queue) and [Set the active queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-queue)
     for that MQNI. Its replica has no active queue until you set one.
     - If you added notification integrations to `my_fg` in this step, and the
       setup record lists an MQNI that you created in your target account, as
       described in [An MQNI doesn’t exist in your target account](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-troubleshoot-mqni-missing), the refresh
       replaced it with a replica that has no active queue. Complete
       [Grant access to your secondary queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-queue) and
       [Set the active queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-queue) for that MQNI, and then update the
       setup record as described at the end of
       [An MQNI doesn’t exist in your target account](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-troubleshoot-mqni-missing).
   - For a pipe that uses any other MQNI, set the MQNI’s active queue again
     with the queue that’s already active in your target account, as described
     in [Set the active queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-queue). The statement binds the new pipe and
     rebinds the MQNI’s other pipes to the same queue. If you add several
     pipes, you can run it once after the refresh that replicates all of them.
   - For an SQS-only pipe, rebind it as described in
     [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind), and confirm that the
     region in the `New channel` ARN is your secondary bucket’s region.
3. **Notifications:** Make sure that an event notification on your secondary
   bucket for the pipe’s path targets the pipe’s queue: the
   `notification_channel` ARN for an SQS-only pipe, or the MQNI’s queue for
   your secondary location. If none does, add one. For an SQS-only pipe, see
   the end of [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind).

Then check the pipe in your target account, as described in
[Check your pipes in your target account (Snowpipe only)](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-validate-pipes), and return here. On Azure and Google Cloud,
confirm that its `notificationChannelName` differs from the value that the
pipe reports in your source account. If it matches, return to
[Set the active queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-queue).

Add the pipe to [the setup record](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-setup-record), including that
you added it after setup and bound it in your target account, whether it uses
the Amazon SQS-only path, and, on Azure and Google Cloud, its `notificationChannelName` values. If you created a
new MLSI or MQNI for the pipe, also add the integration and its `ACTIVE` value
in each account, and for an MQNI, its `QUEUES` list.

If you added pipes earlier and, in your target account after they replicated,
didn’t set the active queue of each pipe’s MQNI or call
`SYSTEM$INGEST_REBIND_PIPE` for each SQS-only pipe, or you aren’t sure, do the numbered steps in your target account,
and the checks that follow them, for each of those pipes now. A
`notification_channel` or `notificationChannelName` value that looks correct
doesn’t show that a pipe is bound.

## Change the active queue later

To change the active queue of an MQNI in an account after this setup, follow these steps. You don’t need to pause pipes first.

1. Grant that account access to the new queue.
2. If you also change the MLSI’s active location in that account, change the
   location now. The rebind uses each stage’s current location.
3. If the previous queue is reachable, run `SYSTEM$PIPE_STATUS` in the account whose active queue you’re changing, and wait until it shows `numOutstandingMessagesOnChannel` as `0`.

   Warning

   Notifications that are still in the previous queue aren’t loaded after the
   change.
4. In the account whose active queue you’re changing, run
   `ALTER INTEGRATION ... SET ACTIVE = '<queue_name>'`.

   Setting the active queue rebinds every pipe that uses the integration. If
   Snowflake can’t bind a pipe to the new queue, the statement fails. Pipes that the statement already rebound stay on the new queue, and the pipe that failed isn’t bound
   to any queue. Grant the missing access to the new queue, and run the statement again with the same queue name.
5. In the same account, run `DESCRIBE INTEGRATION`, and confirm that `ACTIVE`
   names the new queue. Then update [the setup record](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-setup-record):

   - Replace this account’s `ACTIVE` value for the MQNI and, if you changed the
     MLSI’s active location in step 2, for the MLSI.
   - On Azure and Google Cloud, run `SYSTEM$PIPE_STATUS` for each pipe that uses
     the integration, and replace the pipe’s `notificationChannelName` value
     for this account.
6. If this account is the primary account, run `ALTER PIPE ... REFRESH` for each
   pipe that uses the integration. The refresh loads files whose notifications
   went to the previous queue but weren’t loaded, including any that arrived
   after step 3. For a pipe that you recreated during an outage, follow
   [Load files for a recreated pipe](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-recreated-pipes-load) instead, for the last 7 days.
