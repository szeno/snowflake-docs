# Configure your target account for multi-location resilience

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical Edition (or higher).
To inquire about upgrading, contact [Snowflake Support](/user-guide/contacting-support).

This is the third task in
[Set up multi-location resilience for data pipelines](/user-guide/multi-location-resilience-data-pipelines-setup). In it, you
replicate your integrations to your target account, and then point that
account at your secondary location, so that a failover needs no further
configuration. Each section names the account to run it in, as defined in
[How multi-location resilience works](/user-guide/multi-location-resilience-data-pipelines#label-mlsi-how-it-works).

Before you begin, finish
[Configure storage locations for multi-location resilience](/user-guide/multi-location-resilience-data-pipelines-setup-storage) and, if
you use Snowpipe auto-ingest,
[Configure notifications for multi-location resilience](/user-guide/multi-location-resilience-data-pipelines-setup-notifications).

The sections that you run depend on your pipelines:

- **Every pipeline:** [Replicate your integrations to the target account](#label-mlsi-replicate-integrations),
  [Grant access to your secondary storage location](#label-mlsi-target-grant-storage), and [Set the active storage location](#label-mlsi-target-set-storage).
- **Snowpipe with a Multi-Queue Notification Integration (MQNI):** Also [Grant access to your secondary queue](#label-mlsi-target-grant-queue) and
  [Set the active queue](#label-mlsi-target-set-queue).
- **Snowpipe on the Amazon SQS-only path:** Also [Rebind SQS-only pipes](#label-mlsi-sqs-rebind).

## Replicate your integrations to the target account

In this section, you add your integrations to the failover group in your source
account, and then refresh the group in your target account.

Warning

If you created storage integrations, or notification integrations of a
replicated type, directly in your target account, the next refresh after you
add integrations to the group drops them. You can’t link an integration that
you created in your target account to a replica that has the same name. Inbound
single-queue notification integrations aren’t replicated and aren’t dropped. If
your group has a replication schedule, that refresh can run before you refresh
the group yourself. Run `SHOW INTEGRATIONS` in your target account before you
alter the group. If it lists integrations that you created there and still
need, create them in your source account so that they replicate. If an MQNI
that you created there has the same name as an MQNI in your source account, as
described in [An MQNI doesn’t exist in your target account](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-troubleshoot-mqni-missing), don’t create it in
your source account, which already has it.
After the refresh, complete [Grant access to your secondary queue](#label-mlsi-target-grant-queue) and
[Set the active queue](#label-mlsi-target-set-queue) for it, and update the setup record as
described at the end of [An MQNI doesn’t exist in your target account](/user-guide/multi-location-resilience-data-pipelines-troubleshoot#label-mlsi-troubleshoot-mqni-missing). For more
information, see [Replication and objects in target accounts](/user-guide/account-replication-considerations#label-replication-and-objects-in-target-accounts).

### Add your integrations to the failover group

If you already added integrations to the group when you created your Multi-Location Storage Integration (MLSI), run
`SHOW FAILOVER GROUPS` in your source account. If you created an MQNI, confirm
that `allowed_integration_types` includes `NOTIFICATION INTEGRATIONS`. If it
doesn’t, alter the group as described in the next paragraph, and keep
`STORAGE INTEGRATIONS` and every other type that the lists already show. Then
continue with [Refresh your target account](#label-mlsi-first-refresh).

Otherwise, in your source account, alter your existing failover group to
include `INTEGRATIONS` in the `OBJECT_TYPES` list and `STORAGE INTEGRATIONS` in
the `ALLOWED_INTEGRATION_TYPES` list. If you created an MQNI, or plan to create
one, also include `NOTIFICATION INTEGRATIONS` in `ALLOWED_INTEGRATION_TYPES`.
This change replicates your MLSI and, if you created one, your MQNI.

For example, if `SHOW FAILOVER GROUPS` reports `object_types` as `DATABASES`
and `allowed_integration_types` as empty, and you created an MQNI, run:

Copy code

```
ALTER FAILOVER GROUP my_fg SET
  OBJECT_TYPES = DATABASES, INTEGRATIONS
  ALLOWED_INTEGRATION_TYPES = STORAGE INTEGRATIONS, NOTIFICATION INTEGRATIONS;
```

If you didn’t create an MQNI, as on the Amazon SQS-only path or when you load
data only with `COPY INTO`, omit `NOTIFICATION INTEGRATIONS` unless the group
already replicates them.

Warning

`SET` replaces both lists. Include every object type and integration type
that the group already replicates, not only the values in this example. To
see the current lists, run [SHOW FAILOVER GROUPS](/sql-reference/sql/show-failover-groups) and
check the `object_types` and `allowed_integration_types` columns. Don’t add
other object types only because an example lists them: when you add a type,
the next refresh drops objects of that type that you created directly in
your target account.

### Refresh your target account

In your target account, perform a refresh operation:

Copy code

```
ALTER FAILOVER GROUP my_fg REFRESH;
```

### Repair stages that replicated before their MLSI

If a stage is replicated before its MLSI is in the group, you can’t use the
stage in your target account: commands on the stage fail because its integration
can’t be found. A later refresh repairs the stage when it replicates the stage
again. That’s why, when your group has a replication schedule, you add
integrations to the group right after you create the MLSI. If a stage was
already replicated before its MLSI, how you repair it depends on whether the
group uses Optimized Refresh:

- If the group doesn’t use
  [Optimized Refresh](/user-guide/account-replication-optimized-refresh#label-optimized-refresh),
  every refresh replicates the stage, so the next refresh after you add
  integrations to the group repairs it.
- With Optimized Refresh, a refresh replicates only the objects that changed.
  If you added `INTEGRATIONS` to `OBJECT_TYPES`, the next refresh replicates
  every object, which repairs the stage. If the group already included
  `INTEGRATIONS`, change the stage in your source account, for example with
  `ALTER STAGE <stage_name> SET COMMENT = '<comment>'`, and then refresh the
  failover group in your target account. Changing a stage’s comment doesn’t
  affect its pipes.

If a stage needs repair, don’t continue until the refresh that repairs it
finishes.

## Point your target account at your secondary location

After the refresh, configure your target account: grant access to the
secondary storage location and set it as active. With an MQNI, also grant
access to the secondary queue and set it as active. On the Amazon SQS-only
path, skip the queue sections, and follow [Rebind SQS-only pipes](#label-mlsi-sqs-rebind) instead.
Run these sections in your target account.

After the first refresh, the replicated MLSI in your target account has the
same active location as the MLSI in your source account, and the replicated
MQNI has no active queue. Pipes that replicate while the MQNI has no active
queue aren’t bound to a queue, and pipes that were already bound in your target
account stay on their previous queue or topic. Setting the active queue binds
both kinds of pipes to the queue that you set as active. Later refreshes keep
the values that you set in your target account. The exception is the MLSI’s
active location. If you remove your target account’s active storage location
from the MLSI in your source account, the next refresh resets the active
location in your target account to the one that’s active in your source
account.

### Grant access to your secondary storage location

The replicated storage integration in your target account has its own cloud
identity, different from the one in your source account, so you must grant that
identity access to your secondary storage location.

First, get the target account’s identity values:

Copy code

```
DESCRIBE STORAGE INTEGRATION my_mlsi;
```

Then follow the tab for the cloud provider that hosts your secondary location:

Amazon S3Google CloudAzure

Find the `STORAGE_LOCATION_<n>` row for `my-s3-us-east-1`, and record
`STORAGE_AWS_IAM_USER_ARN` and `STORAGE_AWS_EXTERNAL_ID` from its JSON. The IAM
user ARN differs from the one in your source account; the external ID is the
same. Then edit the trust policy of the IAM role for your secondary location
only: the `STORAGE_AWS_ROLE_ARN` of `my-s3-us-east-1` in
[Create a Multi-Location Storage Integration (MLSI)](/user-guide/multi-location-resilience-data-pipelines-setup-storage#label-mlsi-create-mlsi). Follow only Step 5 of
[Option 1: Configure a Snowflake storage integration to access Amazon S3](/user-guide/data-load-s3-config-storage-integration), and add an entry for
the IAM user ARN and external ID instead of replacing the existing entries,
which your other integrations might use. Don’t edit the role for
`my-s3-us-west-1`, because your source account still uses it.

Read the values from the JSON of the `STORAGE_LOCATION_<n>` row for your
secondary location. Record `STORAGE_GCP_SERVICE_ACCOUNT`, and then follow
Step 3 of [Configure an integration for Google Cloud Storage](/user-guide/data-load-gcs-config) for your secondary bucket only.

Read the values from the JSON of the `STORAGE_LOCATION_<n>` row for your
secondary location. Use the `AZURE_CONSENT_URL` and
`AZURE_MULTI_TENANT_APP_NAME` values, and follow “Step 2: Grant Snowflake
Access to the Storage Locations” in [Configure an Azure container for loading data](/user-guide/data-load-azure-config) for
your secondary container only.

On any cloud, don’t create a storage integration in your target account. While
the account is a secondary account for this group, `CREATE STORAGE INTEGRATION`
fails there, and a refresh drops any storage integration that you created there
earlier.

You configure this trust relationship once. For more information, see
[Configure cloud storage access for secondary storage integrations](/user-guide/account-replication-config#label-configure-cloud-storage-access-secondary-storage-integrations).

### Set the active storage location

In the target account, set the MLSI to use your secondary storage location,
choosing from the location names in the `DESCRIBE` output from
[Grant access to your secondary storage location](#label-mlsi-target-grant-storage). Use
[ALTER STORAGE INTEGRATION](/sql-reference/sql/alter-storage-integration):

Copy code

```
ALTER STORAGE INTEGRATION my_mlsi SET ACTIVE = 'my-s3-us-east-1';
```

Set only `ACTIVE` in this statement. On a replica, an
`ALTER STORAGE INTEGRATION` statement that changes anything else fails.

### Grant access to your secondary queue

If you use an MQNI, grant Snowflake permission to access your messaging service
for the queue that you want to set as active in your target account. Follow the
tab for the cloud provider that hosts your secondary location:

Amazon S3Google CloudAzure

Follow “Step 1: Subscribe the Snowflake SQS Queue to the SNS Topic” in
[Automating Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3). In your target account, run
`SYSTEM$GET_AWS_SNS_IAM_POLICY` with the ARN of the topic for your secondary
location, and add the statement that it returns to that topic’s access policy.

Follow “Step 2: Grant Snowflake Access to the Pub/Sub Subscription” in
[Configuring Automation Using GCS Pub/Sub](/user-guide/data-load-snowpipe-auto-gcs#label-gcp-pubsub-snowpipe), for your secondary location’s subscription
only, in your target account.

Snowflake creates the integrations behind the replicated MQNI with your target
account’s own Snowflake identity, so the values differ from the ones that you
used in your source account. To get them, run `DESCRIBE INTEGRATION my_mqni` in
your target account. The `QUEUES` row shows each queue’s
`GCP_PUBSUB_SERVICE_ACCOUNT`. This value belongs to the notification
integration, and it differs from the `STORAGE_GCP_SERVICE_ACCOUNT` value that
you used in [Grant access to your secondary storage location](#label-mlsi-target-grant-storage), so grant each one separately.

Follow “Grant Snowflake Access to the Storage Queue” in
[Configuring Automation With Azure Event Grid](/user-guide/data-load-snowpipe-auto-azure#label-azure-configuring-automation), for your secondary location’s queue
only, in your target account.

Snowflake creates the integrations behind the replicated MQNI with your target
account’s own Snowflake identity, so the values differ from the ones that you
used in your source account. To get them, run `DESCRIBE INTEGRATION my_mqni` in
your target account. The `QUEUES` row shows each queue’s `AZURE_CONSENT_URL`
and `AZURE_MULTI_TENANT_APP_NAME`. These values belong to the notification
integration, and they differ from the storage values that you used in
[Grant access to your secondary storage location](#label-mlsi-target-grant-storage), so grant each one separately.

### Set the active queue

If you use an MQNI, set the active queue to the queue for your secondary
location.

Queue names depend on how you created the MQNI, so look them up rather than
copying a name from this topic:

Copy code

```
DESCRIBE INTEGRATION my_mqni;
```

If you created the MQNI in Scenario A, the names are the ones that you chose,
such as `my-us-east-1`. If you created it with
`SYSTEM$CONVERT_PIPES_TO_MULTI_QUEUE` in Scenario B, the function named them:
on Amazon S3, `MY_MQNI-queue1` and `MY_MQNI-queue2`; on Google Cloud and Azure,
the names of the two integrations that you passed to it, in uppercase. The value
that you set must match a queue name in the `DESCRIBE INTEGRATION` output
exactly, including case. Run the statement for your scenario:

Copy code

```
-- Scenario A
ALTER INTEGRATION my_mqni SET ACTIVE = 'my-us-east-1';

-- Scenario B on Amazon S3
ALTER INTEGRATION my_mqni SET ACTIVE = 'MY_MQNI-queue2';

-- Scenario B on Google Cloud or Azure, if you passed my_azure_ni_1 and my_azure_ni_2
ALTER INTEGRATION my_mqni SET ACTIVE = 'MY_AZURE_NI_2';
```

Use `ALTER INTEGRATION`, without the `NOTIFICATION` keyword, as described in
[ALTER NOTIFICATION INTEGRATION (inbound from multiple queues)](/sql-reference/sql/alter-notification-integration-multi-queue). The
replicated MQNI is read-only in your target account, and only
`ALTER INTEGRATION ... SET ACTIVE` can change its active queue. Setting the
active queue rebinds every pipe that uses the MQNI, so set the MLSI’s active
location first, as described in [Set the active storage location](#label-mlsi-target-set-storage). In a
cross-cloud setup, the active queue must be on the same cloud provider as the
active storage location, or the pipe can’t bind to the queue. If you change the
MLSI’s active location later, run this statement again. If the
statement fails, a pipe can be left without a queue. For more information, see
[Change the active queue later](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-change-active-queue).

When you create a pipe that uses the MQNI in your source account later, run
this statement again after the refresh that replicates the pipe. The pipe’s
replica doesn’t load from your secondary location until you do, even if its
status looks normal. For the full procedure, see
[Add pipes after setup](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-add-pipes-later).

## Rebind SQS-only pipes

If you chose the Amazon SQS-only path in
[Choose a notification path for Amazon S3](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-choose-aws-notification-path), your pipes have no MQNI whose
active queue you can set. In your target account, rebind each existing pipe
once with [SYSTEM$INGEST\_REBIND\_PIPE](/sql-reference/functions/system_ingest_rebind_pipe). Run the
function as `ACCOUNTADMIN`. This call does for a single pipe what
`ALTER INTEGRATION ... SET ACTIVE` does for every pipe that shares an MQNI.

After this one-time rebind, whether you need the function again depends on the
case:

- **Pipes that you create later:** Rebind each one once in your target
  account, after the refresh that replicates it. The pipe’s replica doesn’t
  load from your secondary location until you do, even if its status looks
  normal, and later refreshes keep the binding. For the
  full procedure, see [Add pipes after setup](/user-guide/multi-location-resilience-data-pipelines-manage#label-mlsi-add-pipes-later).
- **Failover:** You run it only for the pipes that
  [step 1 of the failover runbook](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-failover-step-1) sends you to:
  an SQS-only pipe added after setup that might not be bound in your target
  account, and a pipe on the stages of an MLSI whose `ACTIVE` value isn’t your
  secondary location, as described in [An ACTIVE value doesn’t match in step 1](/user-guide/multi-location-resilience-data-pipelines-failover#label-mlsi-failover-fix-active).
- **Failback:** You run it in your source account for each SQS-only pipe that
  you created during the outage, as described in
  [Check objects that you created during the outage](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-outage-objects), and for each pipe that isn’t bound
  to your primary region’s queue, such as a pipe on the stages of an MLSI whose
  `ACTIVE` value you had to correct, as described in
  [An ACTIVE value isn’t your primary location in step 5](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-fix-active).

Before you call the function:

- Make sure that the pipe’s stage points at the storage location in your
  secondary region. The function derives the new notification queue from the stage’s
  current bucket region. Because the stage uses your MLSI, you already made that storage location
  active in [Set the active storage location](#label-mlsi-target-set-storage).
- Run `DESCRIBE PIPE`, and check the `integration` and `notification_channel`
  columns:
  - **`integration` is `NULL`, and `notification_channel` is an Amazon SQS
    queue ARN:** The pipe is an SQS-only pipe. Pass an empty string as the third
    argument.
  - **`integration` names another integration that isn’t an MQNI, and
    `notification_channel` is an Amazon SQS queue ARN:** Pass that integration
    name exactly as the third argument.
  - **`integration` names an MQNI:** The pipe isn’t an SQS-only pipe. Rebind it
    with [Grant access to your secondary queue](#label-mlsi-target-grant-queue) and
    [Set the active queue](#label-mlsi-target-set-queue) instead. On Amazon S3, this function doesn’t
    use a named integration’s SNS topic.
  - **`integration` is `NULL` or names an integration that isn’t an MQNI, and
    `notification_channel` is an SNS topic ARN:** The pipe isn’t an SQS-only
    pipe. On Amazon S3, this function keeps it on that topic, so it doesn’t
    move the pipe to your secondary location. Don’t call the function for that
    pipe. To protect it, use an MQNI, as described in
    [Choose a notification path for Amazon S3](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-choose-aws-notification-path).

Warning

The function can report success without moving the pipe to your secondary
region. If the stage still resolves to the previous region, the function
rebinds the pipe to that region’s queue and reports success. If the stage
resolves to an Azure container or a Google Cloud Storage bucket, the SQS-only
path doesn’t apply: the function unbinds the pipe and then fails. If the third
argument names an integration other than the pipe’s current one, a successful
rebind changes the pipe’s `integration` column to that integration. On Amazon
S3, the function doesn’t use that integration’s SNS topic.

For Amazon SQS auto-ingest, pass an empty string as the second argument. In the
following example, `my_sqs_pipe` is the pipe that you created in
[Alternative: Set up the Amazon SQS-only path](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-sqs-only-setup), and its `integration` column is `NULL`:

Copy code

```
SELECT SYSTEM$INGEST_REBIND_PIPE('my_db.my_schema.my_sqs_pipe', '', '');
```

Check the result of each call, and act on it as follows:

- **The result starts with `Rebind succeeded`:** Confirm that the region in
  the `New channel` ARN (`arn:aws:sqs:<region>:...`) is your secondary bucket’s
  region, such as `us-east-1`. If it shows your primary region, the stage still
  resolves to your primary location. Repeat
  [Set the active storage location](#label-mlsi-target-set-storage), and then run the
  function again. This region check is for the one-time setup in your target
  account. If you rebind a pipe during failback, as described in
  [An ACTIVE value isn’t your primary location in step 5](/user-guide/multi-location-resilience-data-pipelines-failback#label-mlsi-failback-fix-active), the new channel must be in your primary
  region.
- **The result starts with `Rebind failed`:** The pipe is no longer bound to
  any queue. Fix the cause, and run the function again.
- **The function raises an error about the integration argument, such as a
  name that doesn’t exist:** The pipe keeps its current binding. Fix the
  argument, and run the function again.
- **The function raises any other error:** Assume that the pipe isn’t bound to
  any queue. Fix the cause, and run the function again.

After a failed rebind, `DESCRIBE PIPE` can still show the previous queue in
`notification_channel`, so use the function’s result, not `DESCRIBE PIPE`, to
tell whether the rebind succeeded.

After your pipes rebind successfully, point your secondary bucket at their new queue.
In your target account, run [DESCRIBE PIPE](/sql-reference/sql/desc-pipe) to get
the ARN in the `notification_channel` column. Pipes that load from the same bucket report the
same ARN. Pipes on different buckets in the same region usually do too, but
Snowflake can use more than one queue in a region, so check each bucket’s
pipes. On the secondary bucket, configure an S3 event notification that
targets that ARN for each path that your primary bucket’s notifications cover,
as described in
[Configure event notifications](/user-guide/data-load-snowpipe-auto-s3#label-data-load-snowpipe-auto-s3-configure-sqs)
in [Automating Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3). AWS limits each bucket to 100 event
notification configurations, and doesn’t allow overlapping prefix and suffix
filters for the same event type. Mirror your primary bucket’s notifications
rather than adding one for each pipe. The queue in your
target account is a different queue from the one in your source account, so
the event notification on your primary bucket doesn’t cover it.

## Next step

Continue with
[Validate and test multi-location resilience](/user-guide/multi-location-resilience-data-pipelines-setup-validate).
