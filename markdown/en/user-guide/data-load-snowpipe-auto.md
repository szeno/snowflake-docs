# Automate Snowpipe with cloud event notifications

With automated loading, also called *auto-ingest*, your cloud storage service tells Snowpipe when a new file arrives, and Snowpipe loads the file without any code on your side. You create a pipe with `AUTO_INGEST = TRUE`, and you configure your storage location to send event notifications to a message queue that Snowflake reads. From then on, each file that lands in the pipe’s location loads into the target table, typically within a minute.

Event notifications contain the paths of new files, not their data. Snowpipe reads the files from your [stage](/user-guide/data-load-overview) with the access that you grant to Snowflake, usually through a [storage integration](/sql-reference/sql/create-storage-integration).

To set up automated loading, follow the guide for the cloud provider that stores your files:

- [Automate Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3)
- [Automate Snowpipe for Google Cloud Storage](/user-guide/data-load-snowpipe-auto-gcs)
- [Automate Snowpipe for Microsoft Azure Blob Storage](/user-guide/data-load-snowpipe-auto-azure)

The rest of this topic explains how automated loading works and what to decide before you start. If you want your application to decide when files load, use the [Snowpipe REST API](/user-guide/data-load-snowpipe-rest-overview) instead.

## How automated loading works

Automated loading works as follows:

1. Your application or partner writes the file to your bucket or container.
2. The cloud storage service publishes an event about the new file to a message service, which delivers it to a queue that Snowflake reads.
3. Snowflake reads the message and compares the file path with the location of each pipe that uses the queue. A pipe’s location is its stage URL plus the optional path in its `FROM` clause, called the *pipe path*.
4. Each pipe whose location contains the file adds the file to its ingest queue, and then loads it into its target table with the pipe’s `COPY INTO` statement. Snowpipe records the file in the pipe’s [load metadata](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-load-metadata) so that it doesn’t load the same file twice.

Snowflake ignores notifications for files that are outside every pipe’s location. These notifications don’t load data, but a high volume of them can slow down how quickly Snowpipe finds the notifications that matter. For this reason, Snowflake recommends that you [filter events](#label-snowpipe-auto-filter-events) at the source.

## What you configure for each cloud provider

The overall flow is the same for every cloud provider, but the message service, the party that creates the queue, and the way that Snowflake connects to the queue differ. The following table summarizes the differences:

| Setup detail | Amazon S3 | Google Cloud Storage | Microsoft Azure |
| --- | --- | --- | --- |
| Events that trigger a load | `s3:ObjectCreated:*` (all object create events) | `OBJECT_FINALIZE` | `Microsoft.Storage.BlobCreated`, for the [operations that finish writing a file](/user-guide/data-load-snowpipe-auto-azure#label-data-load-snowpipe-auto-azure-supported) |
| Message service | Amazon SQS, optionally with Amazon SNS in front of it, or with Amazon EventBridge and Amazon SNS in front of it | Google Cloud Pub/Sub topic and pull subscription | Microsoft Azure Event Grid subscription and Azure Queue Storage queue |
| Who creates the queue | Snowflake. For a pipe that doesn’t use an Amazon SNS topic, the `notification_channel` column in the output of [DESCRIBE PIPE](/sql-reference/sql/desc-pipe) shows the Amazon Resource Name (ARN) of its Snowflake-managed SQS queue. | You create the topic and the subscription. | You create the Event Grid subscription and the storage queue. |
| How the pipe connects to the queue | You point the bucket’s event notification at the pipe’s SQS queue. If you use Amazon SNS, you set `AWS_SNS_TOPIC` in the pipe, and Snowflake subscribes its queue to your topic. | You create a [notification integration](/sql-reference/sql/create-notification-integration) for the subscription, and set `INTEGRATION` in the pipe. | You create a notification integration for the storage queue, and set `INTEGRATION` in the pipe. |
| Access to the message service that you grant to Snowflake | For Amazon SNS and Amazon EventBridge, an access policy statement on the SNS topic that lets Snowflake subscribe to it | The Pub/Sub Subscriber role on the subscription, and the Monitoring Viewer role on the project | The Storage Queue Data Contributor role on the storage queue |

Expand

Show lessSee more

## Supported storage and accounts

A Snowflake account on any [cloud platform](/user-guide/intro-cloud-platforms) can automatically load files from the following storage services, so your storage doesn’t need to be on the same cloud platform or in the same region as your account:

- Amazon S3
- Google Cloud Storage
- Microsoft Azure Blob Storage, Data Lake Storage Gen2, and general-purpose v2 storage accounts

Automated loading from named internal stages is in public preview and is available only for accounts hosted on AWS. For more information, see the `AUTO_INGEST` parameter in [CREATE PIPE](/sql-reference/sql/create-pipe#optional-parameters).

Automated loading isn’t available in the following cases:

- Files in [S3-compatible storage](/user-guide/data-load-s3-compatible-storage).
- Files in Microsoft Fabric OneLake.
- Files in a government region when your account is in a commercial region, or the reverse. Cloud providers don’t deliver event notifications between government and commercial regions. For more information, see [Automated loading doesn’t work across government and commercial regions](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-gov-regions).

To load these files continuously, use the [Snowpipe REST API](/user-guide/data-load-snowpipe-rest-overview), which accepts file paths from your application instead of event notifications.

When your storage is in a different region or on a different cloud platform from your account, your cloud provider might charge an egress fee for the data that Snowpipe reads. For more information, see [Snowpipe costs](/user-guide/data-load-snowpipe-billing).

## Plan your setup

Before you create pipes, review the following considerations so that your files load once, quickly, and without surprises.

### Give each pipe its own location

Each pipe loads every file in its location, independently of other pipes. If the locations of two pipes overlap, for example `s3://mybucket/orders/` and `s3://mybucket/orders/2026/`, both pipes load the files in the overlapping path. If both pipes load the same table, the table gets duplicate rows.

To prevent overlaps, follow these practices:

- **End stage URLs and pipe paths with a forward slash (`/`).** Without the slash, a location also matches every folder and file whose name starts with the same characters. For example, `s3://mybucket/orders` also matches `s3://mybucket/orders_archive/`.
- **Check existing pipes before you create one.** Compare the location of your new pipe with the location of every existing pipe, which is its stage URL plus the pipe path in its `definition` column. SHOW commands return only the objects that your current role has privileges on, so a role that owns only the new pipe doesn’t see other pipes. To see every pipe, run [SHOW PIPES IN ACCOUNT](/sql-reference/sql/show-pipes) with a role that has the `MONITOR EXECUTION` privilege, and get each stage’s URL from the `url` column of [SHOW STAGES IN ACCOUNT](/sql-reference/sql/show-stages). To include stages that your role can’t see, query the `DEFINITION` column of the [PIPES](/sql-reference/account-usage/pipes) view and the `STAGE_URL` column of the [STAGES](/sql-reference/account-usage/stages) view in the `ACCOUNT_USAGE` schema. These views can lag by up to 3 hours, so they might not show pipes and stages that you created recently.

If duplicate rows already appeared, see [Duplicate data in the target table](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-duplicate-data).

### Filter events at the source

Configure your cloud storage service to send only the events that Snowpipe acts on, and only for the paths that your pipes load. Filtering reduces event noise and latency. For instructions, see the filtering documentation for [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-filtering.html), [Google Cloud Storage](https://cloud.google.com/storage/docs/reporting-changes), or [Azure Event Grid](https://learn.microsoft.com/en-us/azure/event-grid/event-filtering).

Use the `PATTERN` copy option in a pipe only when your cloud provider’s filtering isn’t precise enough. Snowpipe still receives and reads the notifications for files that `PATTERN` excludes.

### Share notifications between pipes

You don’t need a separate notification setup for each pipe:

- **Amazon S3**: Snowflake usually reuses one SQS queue for the pipes in your account that load from buckets in the same AWS region, so one event notification on a bucket can serve every pipe that loads from that bucket. When the access policy of a queue reaches its size limit, Snowflake creates another queue, so check the queue ARN for each new pipe.
- **Google Cloud Storage and Microsoft Azure**: Several pipes can use the same notification integration. Each notification integration reads from one Pub/Sub subscription or one storage queue. Create only one integration for each subscription or queue. If a pipe already reads a subscription or queue through one integration, creating a pipe that reads it through a different integration fails with a `Notification queue already in use with another integration` error. For Google Cloud Storage, several buckets can send notifications to the same Pub/Sub topic, so one subscription and integration can serve pipes that load from several buckets.

### Load files that are already in the stage

A new pipe loads only the files that arrive after you configure event notifications. Each setup guide ends with a step that loads files staged within the last 7 days. For older files, see [Files staged more than 7 days ago](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-backfill).

### Know what happens when a pipe is paused

While a pipe is paused, Snowflake keeps receiving event notifications for it and holds them for 14 days. When you resume the pipe, it loads the files from those notifications. If a pipe is paused for longer than 14 days, it becomes *stale*, and Snowflake can’t guarantee that the pipe loads files from notifications older than 14 days. To resume a stale pipe, see [Resume a stale pipe](/user-guide/data-load-snowpipe-manage#label-snowpipe-resume-stale-pipe).

### Plan network connectivity

By default, Snowflake doesn’t read event notifications over private connectivity:

- **Amazon S3**: Traffic between Amazon S3, Amazon SNS, and Amazon SQS stays on the Amazon network, but it doesn’t flow through your virtual private cloud (VPC). This routing also applies to [Virtual Private Snowflake (VPS)](/user-guide/intro-editions) and [AWS PrivateLink](/user-guide/admin-security-privatelink) accounts.
- **Microsoft Azure**: You can configure Snowflake to read your storage queue over private connectivity. For more information, see [Private connectivity to external stages and Snowpipe automation for Microsoft Azure](/user-guide/data-load-azure-private).

### Plan for region-wide outages

An auto-ingest pipe reads notifications about files in one storage location from one message queue. You can replicate pipes to an account in another region or on another cloud provider. With Business Critical Edition or higher, you can also configure that account to use a second storage location and queue, so that your pipes keep loading after a region-wide cloud provider outage. If you plan to replicate pipes that load from Amazon S3, choose Amazon SNS when you set up notifications. For more information, see [Multi-Location Resilience for Data Pipelines](/user-guide/multi-location-resilience-data-pipelines). For details about replicating pipes, see [Stage, pipe, and load history replication](/user-guide/account-replication-stages-pipes-load-history).

## Monitor automated loading

To check that notifications reach a pipe, call [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status). For auto-ingest pipes, the output includes the following fields, in addition to the fields that every pipe returns:

- `notificationChannelName`: The queue or subscription that the pipe reads.
- `lastReceivedMessageTimestamp`: The time when Snowflake last received a notification on the queue, for any pipe that uses it.
- `lastForwardedMessageTimestamp`: The time when Snowflake last forwarded a notification for a file in this pipe’s location to the pipe.
- `numOutstandingMessagesOnChannel`: The number of notifications that are waiting in the queue.
- `channelErrorMessage`: For Google Cloud Storage and Microsoft Azure, the most recent error that Snowflake received when it tried to read messages or metrics from the subscription or queue. On Google Cloud Storage, a value that starts with `no monitoring permission` means that Snowflake can’t read the subscription’s metrics, but Snowpipe still loads files.

To use these fields to find out why a pipe doesn’t load files, see [Files don’t load with automated loading](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-auto-ingest).

To find out about problems without checking each pipe, set up [error notifications](/user-guide/data-load-snowpipe-errors) for failed loads, and [alerts](/user-guide/data-load-snowpipe-monitor-events#label-snowpipe-events-alerts) for pipes that stop loading or can’t read their queue.

## What’s next

- To set up automated loading, see [Automate Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3), [Automate Snowpipe for Google Cloud Storage](/user-guide/data-load-snowpipe-auto-gcs), or [Automate Snowpipe for Microsoft Azure Blob Storage](/user-guide/data-load-snowpipe-auto-azure).
- To pause, resume, or recreate pipes, see [Manage Snowpipe](/user-guide/data-load-snowpipe-manage).
- To resolve load problems, see [Troubleshooting Snowpipe](/user-guide/data-load-snowpipe-ts).
- To understand Snowpipe costs, see [Snowpipe costs](/user-guide/data-load-snowpipe-billing).
