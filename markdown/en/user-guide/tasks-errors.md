# Set up error notifications for tasks

Snowflake can push notifications to a cloud messaging service when it encounters errors while executing tasks, or when a task graph finishes successfully.
The notifications describe the errors encountered when a task executes SQL code, or identify the successfully completed task graphs.

This topic explains how to configure notification support for tasks that use cloud messaging.

Snowflake task integration is implemented using notification integration objects, which provide an interface between Snowflake and
third-party cloud message queuing services.

Snowflake guarantees at-least-once message delivery of notifications; that is, multiple attempts are made to deliver messages to ensure at
least one attempt succeeds, which can result in duplicate messages.

The task notification feature is supported for both serverless tasks and user-managed tasks; that is, tasks that rely on a virtual warehouse
to provide the compute resources.

Notifications rely on cloud messaging that uses one of the following services:

- Amazon Simple Notification Service (SNS)
- Microsoft Azure Event Grid
- Google Pub/Sub

Currently, cross-cloud support isn’t available for push notifications.
You must configure notification support for the messaging service that is provided by the cloud platform where your Snowflake account is hosted.

The email and webhook notification integration types aren’t supported for task error notifications.

You can use the NOTIFICATION\_HISTORY table function to query the history of task notifications. For more information, see [NOTIFICATION\_HISTORY](/sql-reference/functions/notification_history).

To set up task notifications, complete the following steps:

1. Create a topic to receive the notifications, and set up a notification integration for that topic.

   For more information, see the instructions for your platform:

   - [AWS SNS](/user-guide/notifications/creating-notification-integration-amazon-sns)
   - [Google Pub/Sub](/user-guide/notifications/creating-notification-integration-google-pubsub)
   - [Azure Event Grid](/user-guide/notifications/creating-notification-integration-azure-event-grid)
2. Create or configure the task to use the notification integration for error and success notifications.

   See [Configure a task to send error notifications](/user-guide/tasks-errors-integrate) and [Configure a task to send success notifications](/user-guide/tasks-success-integrate).
