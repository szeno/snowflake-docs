# Configure notifications for multi-location resilience

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical Edition (or higher).
To inquire about upgrading, contact [Snowflake Support](/user-guide/contacting-support).

This is the second task in
[Set up multi-location resilience for data pipelines](/user-guide/multi-location-resilience-data-pipelines-setup). Run it in your
source account, as defined in [How multi-location resilience works](/user-guide/multi-location-resilience-data-pipelines#label-mlsi-how-it-works). It applies only to
Snowpipe auto-ingest. If you load data only with `COPY INTO <table>`
statements, whether you run them yourself or in tasks, there are no file
notifications to redirect, so skip to
[Configure your target account for multi-location resilience](/user-guide/multi-location-resilience-data-pipelines-setup-target-account).

Before you begin, finish
[Configure storage locations for multi-location resilience](/user-guide/multi-location-resilience-data-pipelines-setup-storage), where
you create your Multi-Location Storage Integration (MLSI).

Snowflake needs a way to keep receiving file notifications after a failover.
You don’t need every section in this topic. Find your pipelines in the
following list, and follow only the sections that it names, in order:

- **Google Cloud or Azure, or locations on different cloud providers:** You use
  a Multi-Queue Notification Integration (MQNI). Follow
  [Choose how to create your MQNI](#label-mlsi-choose-mqni-scenario), [Prepare your messaging service for an MQNI](#label-mlsi-prepare-messaging), and
  then the scenario that you chose.
- **Both locations on Amazon S3:** Start with
  [Choose a notification path for Amazon S3](#label-mlsi-choose-aws-notification-path). Snowflake recommends Amazon SNS
  with an MQNI. If you choose it, continue as in the previous item. If you
  choose Amazon SQS only, follow only [Alternative: Set up the Amazon SQS-only path](#label-mlsi-sqs-only-setup).

## Choose a notification path for Amazon S3

The following table compares the two notification paths:

| Consideration | Amazon SNS with an MQNI | Amazon SQS only |
| --- | --- | --- |
| Cloud resources you configure | In each region, an SNS topic that receives the bucket’s S3 event notifications, with an access policy that lets Snowflake subscribe its SQS queue | An S3 event notification on each bucket path that targets the pipe’s Snowflake-managed SQS queue |
| Snowflake objects you configure | One MQNI with a queue for each topic | None |
| Redirecting notifications in the target account | Set the active queue once with `ALTER INTEGRATION ... SET ACTIVE`, and again after each refresh that replicates new pipes | Rebind each pipe once with `SYSTEM$INGEST_REBIND_PIPE`, including each pipe that you create later, after the refresh that replicates it |
| Work that scales with the number of pipes | None (one MQNI serves every pipe that uses it) | One function call for each pipe |
| Requires `ACCOUNTADMIN` | Only for existing pipes: one `SYSTEM$CONVERT_PIPES_SQS_TO_SNS` call for each bucket of SQS-only pipes, and one `SYSTEM$CONVERT_PIPES_TO_MULTI_QUEUE` call for each topic in Scenario B | Yes: one `SYSTEM$INGEST_REBIND_PIPE` call for each pipe |
| Works when another application already has an S3 event notification on the same bucket path | Yes | No |
| Can fan out the same notifications to other subscribers | Yes | No |
| Works when your secondary location isn’t on Amazon S3 | Yes, with an MQNI that you create in Scenario A | No |

Expand

Show lessSee more

**Use Amazon SNS with an MQNI** when you have many pipes, when another
application already has an S3 event notification on a path that your pipes
read, or when other subscribers need the same notifications. The active queue is
a property of the integration rather than of each pipe, so redirecting
notifications in the target account is a single statement no matter how many
pipes you run. If another application, such as an AWS Lambda workload,
already has an S3 event notification on a path that your pipes read, SNS is the only option. AWS doesn’t allow two event notifications in the same bucket for the same event type when their paths overlap, such as `load/` and `load/path1/`. A notification that already targets the Snowflake-managed
SQS queue doesn’t count: it’s the one that SQS-only pipes use.

**Use Amazon SQS only** when you can’t introduce an SNS topic, or when you have
few enough pipes that a rebind for each is manageable. Neither
path avoids the pipe changes in [Associate the MLSI with your external stages](/user-guide/multi-location-resilience-data-pipelines-setup-storage#label-mlsi-stage-setup): you recreate each pipe that moves to a
new stage or whose stage now resolves to a new location. Weigh these trade-offs:

- A call to [SYSTEM$INGEST\_REBIND\_PIPE](/sql-reference/functions/system_ingest_rebind_pipe) requires
  `ACCOUNTADMIN`, because it needs the `MODIFY` privilege on the account, which
  can’t be granted directly to a custom role.
- The function returns no error if it binds a pipe to the wrong queue. It also
  reports some failures in its return value instead of as an error, so check
  each result and verify each pipe yourself.

Then continue based on your choice:

- **Amazon SNS with an MQNI, for new pipes or pipes that already use SNS:**
  Continue with [Choose how to create your MQNI](#label-mlsi-choose-mqni-scenario).
- **Amazon SNS with an MQNI, for existing SQS-only pipes:** Continue with
  [Choose how to create your MQNI](#label-mlsi-choose-mqni-scenario), and use
  Scenario B. It starts by moving your pipes to Amazon SNS.
- **Amazon SQS only:** Skip to
  [Alternative: Set up the Amazon SQS-only path](#label-mlsi-sqs-only-setup).

## Choose how to create your MQNI

Pick the scenario that matches the pipes that you have today:

- **No auto-ingest pipes yet, or pipes that you’re willing to recreate:** Use
  [Scenario A](#label-mlsi-mqni-scenario-a) to create the MQNI yourself, and
  then create pipes that reference it.
- **Existing pipes that use a single-queue notification integration (Google
  Cloud or Azure) or a single Amazon SNS topic (Amazon S3):** Use
  [Scenario B](#label-mlsi-mqni-scenario-b). One function call creates the MQNI
  and moves those pipes onto it. These pipes include Amazon S3 SQS-only pipes, which you first move to Amazon
  SNS as part of Scenario B. They also include pipes that you recreated with their
  original `INTEGRATION` (Google Cloud and Azure) or `AWS_SNS_TOPIC` (Amazon S3)
  value against a new stage, as described in [Associate the MLSI with your external stages](/user-guide/multi-location-resilience-data-pipelines-setup-storage#label-mlsi-stage-setup).
- **Locations on different cloud providers, where one of them is on Amazon
  S3:** Use Scenario A. `SYSTEM$CONVERT_PIPES_TO_MULTI_QUEUE` combines either
  two SNS topics or two notification integrations, so it can’t combine an SNS
  topic with an Azure storage queue or a Pub/Sub subscription.

After you choose a scenario, complete
[Prepare your messaging service](#label-mlsi-prepare-messaging), and then follow
that scenario.

## Prepare your messaging service for an MQNI

Complete the following before you create the MQNI. From the linked topics, use
only the parts named here. Don’t create the stages or pipes that the linked topics describe: you already set up stages in [Associate the MLSI with your external stages](/user-guide/multi-location-resilience-data-pipelines-setup-storage#label-mlsi-stage-setup), and you create any new pipes later in this topic.

What you prepare depends on the scenario that you chose in
[Choose how to create your MQNI](#label-mlsi-choose-mqni-scenario). Prepare a topic or queue for every
location in Scenario A, or only for your secondary location in Scenario B. For
each location, follow the tab for the cloud provider that hosts it, even if
your two locations are on different cloud providers.

Amazon S3Google CloudAzure

1. Create an SNS topic in each AWS region in which your MLSI has storage locations. Record each topic’s ARN. You pass the ARNs to
   `CREATE NOTIFICATION INTEGRATION` in Scenario A or to
   `SYSTEM$CONVERT_PIPES_TO_MULTI_QUEUE` in Scenario B. For instructions, see
   [Option 2: Configuring Amazon SNS to automate Snowpipe using SQS notifications](/user-guide/data-load-snowpipe-auto-s3#label-configuring-amazon-sns-for-snowpipe).
2. In each topic’s access policy, allow Amazon S3 to publish to the topic, as
   described in “Step 1: Subscribe the Snowflake SQS Queue to the SNS Topic” in
   [Automating Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3). Don’t add the policy that
   `SYSTEM$GET_AWS_SNS_IAM_POLICY` returns yet.
3. On each bucket, configure an S3 event notification that sends object-created
   events for your stage’s path to the SNS topic in the bucket’s region. Use the
   same path in both buckets, and cover each path that your pipes read. For the
   event notification, see
   [Enabling and configuring event notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/enable-event-notifications.html)
   in the Amazon S3 documentation.

In Scenario B, do these items only for your secondary location, because your
existing pipes already use the SNS topic for your primary location, or start using it when you move them from SQS to SNS at the start of Scenario B.

Follow “Prerequisites” in [Configuring Automation Using GCS Pub/Sub](/user-guide/data-load-snowpipe-auto-gcs#label-gcp-pubsub-snowpipe) to create a Pub/Sub
topic and a subscription. In Scenario A, do this for each storage location. In
Scenario B, do it only for your secondary location, because your existing
notification integration already uses the subscription for your primary
location. For Scenario B, also create a notification integration for the new
subscription in your source account, as described in “Step 1: Create a
Notification Integration in Snowflake” in that topic.

Make the notifications for your secondary location cover the same paths as the
notifications for your primary location.

Follow “Step 1: Configuring the Event Grid Subscription” in
[Configuring Automation With Azure Event Grid](/user-guide/data-load-snowpipe-auto-azure#label-azure-configuring-automation), and then the “Retrieve the Storage
Queue URL and Tenant ID” section of Step 2. Skip the “Create a Storage Account
for Data Files” section, because your storage location already exists. In
Scenario A, do this for each storage location. In Scenario B, do it only for
your secondary location, and also create a notification integration for that
queue in your source account, as described in “Step 2: Creating the
Notification Integration” in that topic.

Make the Event Grid subscription for your secondary location cover the same
paths as the subscription for your primary location.

Don’t grant Snowflake access to the queues yet. Each Snowflake account gets
access only to the queue that’s active in that account. You grant your source
account access in Scenario A (in Scenario B, your existing pipes already have
access), and you grant your target account access in
[Grant access to your secondary queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-queue). The exception is
the Amazon SNS topic for your primary location when you convert SQS-only pipes:
both accounts subscribe to that topic, as described in
[Move existing SQS-only pipes to Amazon SNS](#label-mlsi-sqs-to-sns).

## Scenario A: Create a new MQNI and new pipes

Before you create the MQNI, complete
[Prepare your messaging service](#label-mlsi-prepare-messaging).

On Google Cloud and Azure, creating an MQNI follows the standard steps for
creating a notification integration, with the differences noted in this
section. On Amazon S3, auto-ingest pipes usually reference an SNS topic or use
the Snowflake-managed SQS queue directly, without a notification integration.

In your source account, create an MQNI by
providing values for each queue in the `QUEUES` list. For the full syntax, see
[CREATE NOTIFICATION INTEGRATION (inbound from multiple queues)](/sql-reference/sql/create-notification-integration-multi-queue).

Copy code

```
CREATE NOTIFICATION INTEGRATION my_mqni
  ENABLED = TRUE
  TYPE = MULTI_QUEUE
  DIRECTION = INBOUND
  QUEUES = (
    (
      NAME = 'my-us-west-1'
      NOTIFICATION_PROVIDER = AWS_SNS
      AWS_SNS_TOPIC_ARN = 'arn:aws:sns:us-west-1:12345:my-snowpipe-mlsi-west'
    ),
    (
      NAME = 'my-us-east-1'
      NOTIFICATION_PROVIDER = AWS_SNS
      AWS_SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:67890:my-snowpipe-mlsi-east'
    )
  )
  ACTIVE = 'my-us-west-1';
```

Where:

- **TYPE = MULTI\_QUEUE:** Specifies that this is a multi-queue integration between
  Snowflake and a third-party cloud message-queuing service.
- **DIRECTION = INBOUND:** Specifies that Snowflake receives notifications sent by
  the cloud messaging service.
- **QUEUES:** Specifies a list of one or more queues for the notification
  integration. An MQNI can have at most two queues by default.
- **NAME:** Required. String that specifies the identifier (name) for the queue.
- **ACTIVE:** Required. Specifies the name of the queue to set as the active
  queue for the notification integration in the current account. The value must
  match a queue’s `NAME` exactly, including case.

Each queue requires `NAME`, `NOTIFICATION_PROVIDER`, and the following
parameters for its cloud provider, and accepts no other parameters:

- **AWS:**
  - **NOTIFICATION\_PROVIDER = AWS\_SNS:** Specifies Amazon SNS as the third-party
    cloud message-queuing service.
  - **AWS\_SNS\_TOPIC\_ARN:** Required. ARN of the Amazon SNS topic to which
    notifications are pushed.
- **Google Cloud:**
  - **NOTIFICATION\_PROVIDER = GCP\_PUBSUB:** Specifies Google Cloud Pub/Sub as
    the third-party cloud message-queuing service.
  - **GCP\_PUBSUB\_SUBSCRIPTION\_NAME:** Required. Name of the Pub/Sub
    subscription. For more information, see
    [CREATE NOTIFICATION INTEGRATION (inbound from a Google Pub/Sub topic)](/sql-reference/sql/create-notification-integration-queue-inbound-gcp).
- **Azure:**
  - **NOTIFICATION\_PROVIDER = AZURE\_STORAGE\_QUEUE:** Specifies Azure Queue
    Storage as the third-party cloud message-queuing service.
  - **AZURE\_STORAGE\_QUEUE\_PRIMARY\_URI:** Required. URL of the storage queue.
  - **AZURE\_TENANT\_ID:** Required. ID of the Microsoft Entra ID tenant. For
    more information, see
    [CREATE NOTIFICATION INTEGRATION (inbound from an Azure Event Grid topic)](/sql-reference/sql/create-notification-integration-queue-inbound-azure).

Other notification integration parameters, such as `ENABLED`, `TYPE`, and
`DIRECTION`, aren’t allowed inside `QUEUES`.

Queues on Azure and Google Cloud have the following form in the `QUEUES` list:

Copy code

```
(
  NAME = 'my-azure-eastus'
  NOTIFICATION_PROVIDER = AZURE_STORAGE_QUEUE
  AZURE_STORAGE_QUEUE_PRIMARY_URI = 'https://myaccount.queue.core.windows.net/my-queue'
  AZURE_TENANT_ID = '<tenant_id>'
),
(
  NAME = 'my-gcp-us-central1'
  NOTIFICATION_PROVIDER = GCP_PUBSUB
  GCP_PUBSUB_SUBSCRIPTION_NAME = 'projects/my-project/subscriptions/my-subscription'
)
```

After you create the MQNI, and before you create pipes that use it, grant
Snowflake permission to access the queue that’s active in your source account.
Grant access only for that queue: you grant your target account access to its
own queue in [Grant access to your secondary queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-queue). On Google Cloud and Azure, the
values that the following instructions use, such as
`GCP_PUBSUB_SERVICE_ACCOUNT`, `AZURE_CONSENT_URL`, and
`AZURE_MULTI_TENANT_APP_NAME`, are in the active queue’s entry in the `QUEUES`
row of `DESCRIBE INTEGRATION my_mqni`. Follow the tab for the cloud provider
that hosts your primary location:

Amazon S3Google CloudAzure

Follow “Step 1: Subscribe the Snowflake SQS Queue to the SNS Topic” in
[Automating Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3).

Follow “Step 2: Grant Snowflake Access to the Pub/Sub Subscription” in
[Configuring Automation Using GCS Pub/Sub](/user-guide/data-load-snowpipe-auto-gcs#label-gcp-pubsub-snowpipe).

Follow “Grant Snowflake Access to the Storage Queue” in
[Configuring Automation With Azure Event Grid](/user-guide/data-load-snowpipe-auto-azure#label-azure-configuring-automation).

After you create an MQNI, you can use it to create a new pipe in your source
account with the [CREATE PIPE](/sql-reference/sql/create-pipe) command. The
following example creates a pipe that loads data from Amazon S3 into a table
through an external stage (`my_ext_stage`) that uses an MLSI. Type the integration name in all uppercase. Snowflake looks up a quoted integration name exactly as you type it, and `ALTER INTEGRATION ... SET ACTIVE` rebinds only pipes whose `INTEGRATION` value matches the MQNI’s name exactly:

Copy code

```
CREATE PIPE my_db.my_schema.my_pipe
  AUTO_INGEST = TRUE
  INTEGRATION = 'MY_MQNI'
  AS COPY INTO my_db.my_schema.my_table
    FROM @my_db.my_schema.my_ext_stage/my_pipe/;
```

Then continue with [the next step](#label-mlsi-notifications-next).

## Scenario B: Create an MQNI from your existing pipes’ queues

In your source account, with `ACCOUNTADMIN` as the primary role of your
session, use `SYSTEM$CONVERT_PIPES_TO_MULTI_QUEUE` to migrate pipes that use a
single-queue notification integration, or a single Amazon SNS topic, to a new
MQNI.

The function creates the MQNI and names it with the first argument. If no pipe uses the original topic or integration, the function
returns `Success` without creating the MQNI. The function sets the active queue
for your source account to the original queue. It migrates every pipe in your
source account that uses that topic or integration, including paused pipes and
pipes in databases outside the failover group. It doesn’t drop the
integrations that you pass, pause pipes, or interrupt ingestion.

Warning

Don’t create the MQNI first: the function replaces any existing integration
that has the same name. On Google Cloud and Azure, both integrations that you
pass become the MQNI’s queues, so if you later drop the MQNI, Snowflake drops
both integrations too.

If any of your existing Amazon S3 pipes are SQS-only pipes, first move them to
Amazon SNS, as described in the following section, even if other pipes on the
same bucket already use SNS. Otherwise, skip to
[Create the MQNI from your pipes’ queues](#label-mlsi-mqni-scenario-b-create).

### Move existing SQS-only pipes to Amazon SNS

Repeat the following steps for each bucket that your SQS-only pipes load from. Run each
step in your source account unless the step names another account:

1. Finish
   [associating the MLSI with your external stages](/user-guide/multi-location-resilience-data-pipelines-setup-storage#label-mlsi-stage-setup)
   for every pipe that loads from the bucket.
   In one call, `SYSTEM$CONVERT_PIPES_SQS_TO_SNS` converts every SQS-only pipe that loads from the bucket. If you recreate a converted pipe from its original definition, which specifies neither `AWS_SNS_TOPIC` nor `INTEGRATION`, the pipe becomes an SQS-only pipe again.
2. Create an SNS topic in the bucket’s region, or reuse an existing topic in
   that region, such as the topic that your SNS pipes on the same bucket already
   use. Pipes that share a topic move to one MQNI in Scenario B. In the topic’s
   access policy, allow Amazon S3 to publish to the topic from each bucket that
   uses the topic, and allow Snowflake to subscribe your source account’s SQS
   queue to the topic. Also allow Snowflake to subscribe your target account’s SQS queue:
   Snowflake subscribes that queue to the topic at the next refresh. To get each
   account’s policy statement, run `SYSTEM$GET_AWS_SNS_IAM_POLICY` with the
   topic ARN once in your source account and once in your target account. For instructions, see “Step 1: Subscribe the Snowflake SQS Queue to
   the SNS Topic” in [Automating Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3).

   Item 5 points the SQS-only pipes’ event notifications at this topic. Every
   subscriber to the topic, such as an AWS Lambda function, then also receives
   events for those paths, unless its subscription has a filter policy. If
   other applications subscribe to the topic and shouldn’t receive those
   events, create a separate topic.
3. With `ACCOUNTADMIN` as the primary role of your session, call
   [SYSTEM$CONVERT\_PIPES\_SQS\_TO\_SNS](/sql-reference/functions/system_convert_pipes_sqs_to_sns) with the bucket
   name, without `s3://`, and the topic ARN:

   Copy code

   ```
   SELECT SYSTEM$CONVERT_PIPES_SQS_TO_SNS(
     'my-bucket-west', 'arn:aws:sns:us-west-1:12345:my-snowpipe-mlsi-west');
   ```
4. Run `DESCRIBE PIPE` for each pipe that loads from the bucket, and confirm
   that `notification_channel` shows the topic ARN. If a pipe was created
   before Snowflake began storing the metadata that the function needs, the pipe
   stays on Amazon SQS, and the function doesn’t report it. Recreate that pipe, and then call the function again. Recreating a pipe drops its load history, as described in [Associate the MLSI with your external stages](/user-guide/multi-location-resilience-data-pipelines-setup-storage#label-mlsi-stage-setup).

   The function also converts the auto-refresh pipe of each directory table
   that refreshes from the bucket, including a directory table on a stage that
   doesn’t use an MLSI, so those directory tables keep refreshing after item 5.
   You can’t run `DESCRIBE PIPE` on a directory table’s auto-refresh pipe. For
   each stage whose directory table uses `AUTO_REFRESH`, run `DESCRIBE STAGE`,
   and confirm that the `AWS_SNS_TOPIC` property in the `DIRECTORY` group shows
   the topic ARN.
5. On the bucket, update each event notification that targets the Snowflake-managed SQS queue so that it targets the SNS topic instead. Don’t make this change until
   every pipe and directory table shows the topic in item 4.

If several buckets share one topic, one `SYSTEM$CONVERT_PIPES_TO_MULTI_QUEUE`
call in Scenario B moves the pipes for all of them. With a separate topic for
each bucket, you call the function once for each topic, and each call creates
its own MQNI. Give each call a different MQNI name, because the function
replaces an existing integration that has the same name. If you end up with
more than one MQNI, see the end of [Create the MQNI from your pipes’ queues](#label-mlsi-mqni-scenario-b-create).

After you convert the pipes for every bucket, continue with
[Create the MQNI from your pipes’ queues](#label-mlsi-mqni-scenario-b-create).

### Create the MQNI from your pipes’ queues

Before you call `SYSTEM$CONVERT_PIPES_TO_MULTI_QUEUE`, complete
[Prepare your messaging service](#label-mlsi-prepare-messaging) for your
secondary location. On Google Cloud and Azure, that includes the single-queue
notification integration that the function takes as its third argument.

Syntax:

Copy code

```
SYSTEM$CONVERT_PIPES_TO_MULTI_QUEUE(
  '<new_mqni_name>',
  '<original_sns_topic_arn_or_int_name>',
  '<new_sns_topic_arn_or_int_name>'
)
```

Where:

- **new\_mqni\_name:** String that specifies an identifier (name) to assign to the
  new MQNI that the function creates.
- **original\_sns\_topic\_arn\_or\_int\_name:**
  - For AWS, the Amazon Resource Name (ARN) of the original SNS topic
    associated with one or more pipes.
  - For Google Cloud or Azure, a string that specifies the identifier of your
    original single-queue notification integration associated with one or more
    pipes.
- **new\_sns\_topic\_arn\_or\_int\_name:**
  - For AWS, the Amazon Resource Name (ARN) of a new SNS topic to add as a
    queue to the MQNI.
  - For Google Cloud or Azure, a string that specifies the identifier of your
    new single-queue notification integration to combine with the original
    notification integration.

Both queue arguments must be the same kind: two SNS topic ARNs, or two
integration names.

**Example 1: Add a new SNS topic queue**

The following call combines your original SNS topic with a new SNS topic:

Copy code

```
SELECT SYSTEM$CONVERT_PIPES_TO_MULTI_QUEUE(
  'my_mqni',
  'arn:aws:sns:us-west-1:12345:my-snowpipe-mlsi-west',
  'arn:aws:sns:us-east-1:67890:my-snowpipe-mlsi-east'
);
```

This call results in an MQNI named `MY_MQNI` with the following queues:

- `MY_MQNI-queue1` (for the original, active SNS topic)
- `MY_MQNI-queue2` (for the new SNS topic)

**Example 2: Create an MQNI from two notification integrations**

The following call combines two Azure notification integrations:

Copy code

```
SELECT SYSTEM$CONVERT_PIPES_TO_MULTI_QUEUE(
  'my_mqni',
  'my_azure_ni_1',
  'my_azure_ni_2'
);
```

This call results in an MQNI named `MY_MQNI` with the following queues:

- `MY_AZURE_NI_1` (for the original, active queue)
- `MY_AZURE_NI_2` (for the new queue)

On Google Cloud, pass your integration names the same way.

The function names the queues that it creates, so their names don’t match the
example names in Scenario A. Run `DESCRIBE INTEGRATION` to see them before you
reference a queue name in a later step. To confirm that the pipes moved, run
[SHOW PIPES](/sql-reference/sql/show-pipes) and check that the `integration` column shows
the new MQNI.

If your pipes use more than one SNS topic or single-queue notification
integration, call the function once for each, with a different MQNI name each
time. Later, repeat the MQNI tasks for each MQNI:
[Grant access to your secondary queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-queue), [Set the active queue](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-queue), [the MQNI validation checks](/user-guide/multi-location-resilience-data-pipelines-setup-validate#label-mlsi-validate-setup), and the MQNI checks in
[Verify data pipelines after failover or failback](/user-guide/multi-location-resilience-data-pipelines-verify#label-mlsi-verify-ingestion).

Then continue with [the next step](#label-mlsi-notifications-next).

## Alternative: Set up the Amazon SQS-only path

This section applies only if you chose Amazon SQS only in
[Choose a notification path for Amazon S3](#label-mlsi-choose-aws-notification-path).

On this path, create each pipe in your source account without a notification
integration, as in the following example:

Copy code

```
CREATE PIPE my_db.my_schema.my_sqs_pipe
  AUTO_INGEST = TRUE
  AS COPY INTO my_db.my_schema.my_table
    FROM @my_db.my_schema.my_ext_stage/my_sqs_pipe/;
```

`DESCRIBE PIPE` then reports `NULL` in the `integration` column, which matches
the example in [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind).

For each new pipe, run `DESCRIBE PIPE` in your source account, and copy the ARN
in the `notification_channel` column. Then, on your primary bucket, make sure that an S3 event notification for the pipe’s path targets that ARN, as described in
[Configure event notifications](/user-guide/data-load-snowpipe-auto-s3#label-data-load-snowpipe-auto-s3-configure-sqs)
in [Automating Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3). Pipes that load from the same bucket share one queue, so an existing notification on the bucket might already cover the pipe’s path. If one does, confirm that it targets that ARN. If it targets an earlier Snowflake queue, update it to target that ARN. If it serves another application, such as an AWS Lambda function, use Amazon SNS with an MQNI instead, as described in [Choose a notification path for Amazon S3](#label-mlsi-choose-aws-notification-path). AWS doesn’t allow notifications whose paths overlap, such as a parent and a child path, so add a notification only for a path that doesn’t overlap an existing one. Don’t configure your secondary bucket yet:
the pipe in your target account uses a different queue. For a pipe that exists
when you configure your target account, you get that queue after you rebind
the pipe, as described in [Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind). For a
pipe that you create later, you get it after you rebind the pipe following the
refresh that replicates it, as described in [Add pipes after setup](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-add-pipes-later).

If you recreated existing SQS-only pipes in [Associate the MLSI with your external stages](/user-guide/multi-location-resilience-data-pipelines-setup-storage#label-mlsi-stage-setup), they
already match the example. Run `DESCRIBE PIPE` on each one, and compare its
`notification_channel` ARN with the queue that your primary bucket’s event
notifications target. If the ARNs differ, update the event notification to
target the pipe’s new ARN.

You don’t create an MQNI on this path.

## Next step

Continue with
[Configure your target account for multi-location resilience](/user-guide/multi-location-resilience-data-pipelines-setup-target-account).
On the Amazon SQS-only path, that topic also has you rebind your pipes, in
[Rebind SQS-only pipes](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-sqs-rebind).
