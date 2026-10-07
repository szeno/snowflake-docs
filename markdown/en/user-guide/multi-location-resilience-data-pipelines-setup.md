# Set up multi-location resilience for data pipelines

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical Edition (or higher).
To inquire about upgrading, contact [Snowflake Support](/user-guide/contacting-support).

You set up multi-location resilience once, before an outage, so that a failover
needs no further configuration. Setup has four tasks, which you complete in
order. Each task has its own topic, and each topic except the last ends with a link to
the next task.

These topics use *source account* and *target account* as defined in
[How multi-location resilience works](/user-guide/multi-location-resilience-data-pipelines#label-mlsi-how-it-works). They use `my_fg` as the name of the existing
failover group that replicates your pipeline databases. Use your group’s name
wherever these topics show `my_fg`.

The examples in these topics assume that you use the `ACCOUNTADMIN` role in
both accounts, unless a step names another role or privilege. To use other
roles, see the access control requirements on the reference page for each
command.

## Before you start

Your notification choices determine what you configure in the notification
and target account tasks. How your producers write files determines which
steps you run when you
[fail over](/user-guide/multi-location-resilience-data-pipelines-failover) and
[fail back](/user-guide/multi-location-resilience-data-pipelines-failback).
Make the following decisions:

- Whether your producers use dual-write or single-write. For more information, see [Choose how your producer writes files](/user-guide/multi-location-resilience-data-pipelines#label-mlsi-choose-routing).
- On Amazon S3, whether your pipes use Amazon SNS with a Multi-Queue Notification Integration (MQNI) or Amazon SQS only. For more information, see [Choose a notification path for Amazon S3](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-choose-aws-notification-path).
- If you use an MQNI, whether you create it with new pipes (Scenario A) or
  create it from your existing pipes (Scenario B). If only one of your
  locations is on Amazon S3, use Scenario A. For more information, see [Choose how to create your MQNI](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-choose-mqni-scenario).

If you load data only with `COPY INTO`, only the first decision applies.

Also check whether your failover group has a replication schedule. Run
[SHOW FAILOVER GROUPS](/sql-reference/sql/show-failover-groups) in your source account, and look at
the `replication_schedule` column. If the group has a schedule, the first task
tells you when to add your integrations to the group.

## Setup tasks

Complete the following tasks in order:

| Task | Account | Who needs it |
| --- | --- | --- |
| 1. [Configure storage locations for multi-location resilience](/user-guide/multi-location-resilience-data-pipelines-setup-storage) | Source | Every pipeline |
| 2. [Configure notifications for multi-location resilience](/user-guide/multi-location-resilience-data-pipelines-setup-notifications) | Source | Snowpipe auto-ingest only. Skip this task if you load data only with `COPY INTO`. |
| 3. [Configure your target account for multi-location resilience](/user-guide/multi-location-resilience-data-pipelines-setup-target-account) | Source, and then target | Every pipeline |
| 4. [Validate and test multi-location resilience](/user-guide/multi-location-resilience-data-pipelines-setup-validate) | Source and target | Every pipeline |

Expand

Show lessSee more

Setup is complete when all of
[the validation checks](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-validate-setup) pass and you’ve saved
[the setup record](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-setup-record). Before you
rely on the configuration, test it, as described in
[Test a failover and a failback](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-test-failover).

## Which sections apply to you

Within the notification and target account tasks, you run only the sections
for your pipelines. Find your pipelines in the following table:

| Your pipelines | Configure notifications | Configure your target account |
| --- | --- | --- |
| `COPY INTO` only, with no Snowpipe auto-ingest | Skip | [Replicate your integrations to the target account](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-replicate-integrations), [Grant access to your secondary storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-storage), and [Set the active storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-storage) |
| Snowpipe with an MQNI from Scenario A (new pipes, or one location on Amazon S3 and the other on another cloud provider) | [Prepare your messaging service for an MQNI](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-prepare-messaging), and then [Scenario A: Create a new MQNI and new pipes](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-mqni-scenario-a) | Every section except [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind) |
| Snowpipe with an MQNI from Scenario B (existing pipes, unless only one of your locations is on Amazon S3) | [Prepare your messaging service for an MQNI](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-prepare-messaging), and then [Scenario B: Create an MQNI from your existing pipes’ queues](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-mqni-scenario-b). On Amazon S3, if any of your existing pipes are SQS-only pipes, Scenario B starts by moving them to Amazon SNS. | Every section except [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind) |
| Snowpipe on Amazon S3 with Amazon SQS only | [Alternative: Set up the Amazon SQS-only path](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-sqs-only-setup) | [Replicate your integrations to the target account](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-replicate-integrations), [Grant access to your secondary storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-storage), [Set the active storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-storage), and then [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind) |

Expand

Show lessSee more

If some of your Amazon S3 pipes use Amazon SNS and others use the Amazon SQS-only
path, follow the Scenario B row. Scenario B moves the SQS-only pipes to Amazon
SNS first.

In the validation checks, skip any check that’s marked for Snowpipe, an MQNI, or Snowflake tasks if it doesn’t apply to your pipelines.

## After setup

- To add pipes or change the active queue later, see
  [Manage multi-location resilience after setup](/user-guide/multi-location-resilience-data-pipelines-manage).
- During an outage, follow
  [Fail over data pipelines](/user-guide/multi-location-resilience-data-pipelines-failover).
- After the outage, follow
  [Fail back data pipelines](/user-guide/multi-location-resilience-data-pipelines-failback).
