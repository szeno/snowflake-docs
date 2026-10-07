# Validate and test multi-location resilience

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical Edition (or higher).
To inquire about upgrading, contact [Snowflake Support](/user-guide/contacting-support).

This is the last task in
[Set up multi-location resilience for data pipelines](/user-guide/multi-location-resilience-data-pipelines-setup). In it, you run
checks, record your setup for on-call responders, and test a failover and a
failback, so that you don’t discover a misconfiguration during a real outage.
Each check names the account to run it in, as defined in
[How multi-location resilience works](/user-guide/multi-location-resilience-data-pipelines#label-mlsi-how-it-works).

Before you begin, finish
[Configure your target account for multi-location resilience](/user-guide/multi-location-resilience-data-pipelines-setup-target-account).

## Run the validation checks

The checks only describe objects, list files and tasks, and read pipe status.
They don’t change any pipe, stage, task, or integration. If you’re rerunning
these checks after a failback, you’re done when they pass. Skip the checks that are marked for Snowpipe, a Multi-Queue Notification Integration (MQNI), or tasks if they don’t apply to your
pipelines.

The first two checks compare the `ACTIVE` value of each integration, including your Multi-Location Storage Integration (MLSI), with the following table. If you rerun these
checks after you changed an active queue as described in
[Change the active queue later](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-change-active-queue), compare with the values in
[the setup record](#label-mlsi-setup-record) instead. The table uses the
example names from these topics, so expect the names that you chose in your
own `DESCRIBE` output:

| Integration | `ACTIVE` in your source account | `ACTIVE` in your target account |
| --- | --- | --- |
| MLSI | Your primary location’s name, such as `my-s3-us-west-1` | Your secondary location’s name, such as `my-s3-us-east-1` |
| MQNI from Scenario A | `my-us-west-1` | `my-us-east-1` |
| MQNI from Scenario B on Amazon S3 | `MY_MQNI-queue1` | `MY_MQNI-queue2` |
| MQNI from Scenario B on Google Cloud or Azure | Your original integration’s name, such as `MY_AZURE_NI_1` | Your second integration’s name, such as `MY_AZURE_NI_2` |

Expand

Show lessSee more

On the Amazon SQS-only path, only the MLSI has an `ACTIVE` value.

### Check your source account

In your source account, confirm that the integrations point at your primary
location, and that your pipes are loading:

Copy code

```
DESCRIBE STORAGE INTEGRATION my_mlsi;
-- If you use an MQNI
DESCRIBE INTEGRATION my_mqni;
-- If you use Snowpipe
SELECT SYSTEM$PIPE_STATUS('my_db.my_schema.my_pipe');
```

Each `ACTIVE` value should match the source account column of
[the table of expected values](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-expected-active). In the
`SYSTEM$PIPE_STATUS` output, `executionState` should be `RUNNING`, and
`lastIngestedTimestamp` should advance as new files arrive. On Azure and Google
Cloud, record each pipe’s `notificationChannelName` for
[Check your pipes in your target account (Snowpipe only)](#label-mlsi-validate-pipes).

### Check your target account’s integrations

In your target account, confirm that the replicas arrived and point at your
secondary location:

Copy code

```
DESCRIBE STORAGE INTEGRATION my_mlsi;
-- If you use an MQNI
DESCRIBE INTEGRATION my_mqni;
```

Each `ACTIVE` value should match the target account column of
[the table of expected values](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-expected-active), so it differs from
the value in your source account. If the active storage locations match,
failing over doesn’t move ingestion to a healthy region.

Warning

If the active queues in your source and target accounts match, notifications
can be lost.

### Check access to your secondary location

In your target account, confirm that the replicated integration can reach your
secondary location. If you created more than one MLSI, run this command on at
least one stage for each MLSI:

Copy code

```
LIST @my_db.my_schema.my_ext_stage;
```

A listing that completes without a permission error shows that the replicated
integration can list your secondary location. If you haven’t written files
there yet, the listing is empty. A permission error means that the
integration’s cloud identity doesn’t have access. Return to
[Grant access to your secondary storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-storage). An error that the stage’s integration
can’t be found means that the stage was replicated before its MLSI. See
[Repair stages that replicated before their MLSI](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-repair-stages).

### Check your pipes in your target account (Snowpipe only)

Confirm in your target account that each pipe is ready to load from your
secondary location:

Copy code

```
SELECT SYSTEM$PIPE_STATUS('my_db.my_schema.my_pipe');
```

For a pipe that you created in your source account after you configured your
target account, and that you haven’t bound there yet or aren’t sure that you
have, first run the **Stage**, **Binding**, and **Notifications**
steps in [Add pipes after setup](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-add-pipes-later). For every pipe, check the following
in the output:

- **Expected state:** Before a failover, `executionState` is `READ_ONLY`,
  because a pipe in a secondary database receives notifications but doesn’t
  load data until you promote the account. If it shows another state, such as
  `PAUSED` or an error state, fix that first.
- **`PAUSED`:** Resume the pipe in your source account, and then refresh the
  failover group in your target account.
- **Binding errors:** Check the output for a `replicationBindingErrorDetails`
  field. Snowflake adds it when it can’t bind the pipe to a queue. In
  that case, `executionState` still shows `READ_ONLY`, so check for the field
  even when the state looks correct. For a pipe that uses an MQNI, run
  [Set the active queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-queue) again. For an SQS-only pipe, rebind it as
  described in [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind).
- **No `notificationChannelName` field:** The pipe isn’t bound to a queue in
  this account yet. If the output includes `replicationBindingErrorDetails`,
  fix that error first, as described earlier in this list. For a pipe that
  uses an MQNI, set the active queue as described in
  [Set the active queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-queue). For an SQS-only pipe, rebind it as
  described in [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind). If neither applies, wait a few
  minutes, and check again.
- **Binding on Azure and Google Cloud:** `notificationChannelName` names the
  active queue or Pub/Sub subscription, and it must differ from the value that
  you recorded in [Check your source account](#label-mlsi-validate-source). If it matches, return to
  [Set the active queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-queue).
- **Binding on Amazon S3:** Replication creates a separate SQS queue in your
  target account, so `notificationChannelName` always differs between accounts
  and doesn’t confirm the binding. For a pipe that uses an MQNI, run
  `DESCRIBE PIPE` and confirm that `notification_channel` shows the SNS topic
  for your secondary location. If it shows your primary location’s topic, run
  [Set the active queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-queue) again. For an SQS-only pipe, `DESCRIBE PIPE` confirms the binding
  only if the pipe’s most recent `SYSTEM$INGEST_REBIND_PIPE` call returned
  `Rebind succeeded`. If you aren’t sure that it did, rebind the pipe again as
  described in [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind). Then confirm that the
  `notification_channel` ARN from `DESCRIBE PIPE` is in your secondary bucket’s
  region, and that the event notification on your secondary bucket targets that
  ARN.

### Check your tasks in your target account (tasks only)

If your `COPY INTO` statements run in tasks, confirm in your target account
that the tasks run after a failover, with [SHOW TASKS](/sql-reference/sql/show-tasks):

Copy code

```
SHOW TASKS IN DATABASE my_db;
```

Before a failover, tasks in your target account don’t run, whatever their
`state`. After a failover, a task whose `state` is `started` is scheduled. A
replicated task is `suspended` in your target account if it was suspended in
your source account when the last refresh began, or if its owner role isn’t
available in your target account. To fix a suspended task, resume it in your
source account. Make sure that the group replicates the task’s owner role and
that the task’s warehouse exists in your target account. Then refresh the
failover group in your target account. For a task graph, check the root task:
a child task runs after a failover only if its root task is resumed. You can
resume a child task only while its root task is suspended, so resume the child
tasks before the root task. For more information, see
[Replication and tasks](/user-guide/account-replication-considerations#label-replication-and-tasks).

## Record your setup for on-call responders

The [failover steps](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-failover-steps) start from this record. Save
the following where your on-call responders can find it:

- The failover group name
- The source and target account names
- The names of your stages, integrations, pipes, and tasks, and which tasks
  are resumed in your source account
- Whether your producers use dual-write or single-write, and the teams that own
  them
- Which pipes use the Amazon SQS-only path
- Each MQNI’s `QUEUES` list
- The `ACTIVE` values in each account
- On Azure and Google Cloud, the `notificationChannelName` values in each
  account

Update the record when you add or remove stages, integrations, pipes, or
tasks, when you resume or suspend a task, and when you change an `ACTIVE`
value. Don’t record the task suspensions that the failover and failback
runbooks make, because the runbooks use this record to decide which tasks to
resume.

## Test a failover and a failback

Test both runbooks before you rely on this configuration during an outage. A
test fails over every database and integration in `my_fg`, so plan it as a
maintenance window for every pipeline that uses those databases. If you use
single-write, a test also includes rerouting your producers and running steps 1 and 9
of the failback runbook. To run a test, do the following:

1. Run [the validation checks](#label-mlsi-validate-setup).
2. Follow [Fail over data pipelines](/user-guide/multi-location-resilience-data-pipelines-failover),
   and confirm that your on-call responders can use the roles listed in its
   **Before you start** section. Because your source account is reachable,
   suspend its `COPY INTO` tasks first, as described in step 3 of that
   runbook.
3. Confirm that ingestion resumed in your target account, as described in
   [Verify data pipelines after failover or failback](/user-guide/multi-location-resilience-data-pipelines-verify#label-mlsi-verify-ingestion).
4. Follow [Fail back data pipelines](/user-guide/multi-location-resilience-data-pipelines-failback),
   and confirm that your on-call responders can use the roles listed in its
   **Before you start** section, including in your source account. Then
   confirm that ingestion resumed in your source account.

## After setup

- To add pipes or change the active queue later, see
  [Manage multi-location resilience after setup](/user-guide/multi-location-resilience-data-pipelines-manage).
- During an outage, follow
  [Fail over data pipelines](/user-guide/multi-location-resilience-data-pipelines-failover).
- After the outage, follow
  [Fail back data pipelines](/user-guide/multi-location-resilience-data-pipelines-failback).
