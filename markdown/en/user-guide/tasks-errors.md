# Set up alerts and notifications for tasks

Snowflake can notify you when tasks run into errors, and when a task graph finishes successfully. You can do this in two
ways, and you can use both at the same time:

- A **task alert** notifies you by email or webhook when the error rate across your tasks crosses a threshold that you
  choose. Use this to monitor the health of your tasks. See [Configure error alerts and notifications for tasks](/user-guide/tasks-errors-integrate).
- A **notification integration** pushes a message to Amazon SNS, Microsoft Azure Event Grid, or Google Pub/Sub for each
  individual task failure, and for each successful task graph run. Use this to feed task events into downstream systems.
  See [Send task notifications to a cloud messaging service](#label-tasks-notifications-integrations).

For more information about alerts, see [Setting up alerts based on data in Snowflake](/user-guide/alerts).

## Prerequisites for task alerts

Task alerts read task execution events from the event table, and calculate the error rate as the number of failed runs
divided by the number of recorded runs. Successful runs must be recorded too, or the error rate is overstated. For
example, if only failures are recorded, one failure in 100 runs is evaluated as a 100% error rate instead of 1%.

Before you create a task alert, set the [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level) parameter to
`INFO` on every task that you want to monitor. At `INFO`, events are recorded for both successful and failed task runs.
You can set this parameter on an individual task, on the schema or database that contains the tasks, or on the account.
For more information, see [Set the severity level of the events to capture](/user-guide/tasks-events#label-task-monitor-events-level).

The role that owns the alert also needs privileges on the views in the `ACCOUNT_USAGE` schema that the alert queries.
For both requirements, see [Prerequisites for task alerts](/user-guide/alerts-ui#label-alerts-center-prerequisites-task).

Important

Set `LOG_EVENT_LEVEL` to `INFO`, `DEBUG`, or `TRACE` for the tasks that you want to monitor. At `WARN` or `ERROR`, only
failed runs are recorded, so the alert overstates the error rate. At `OFF`, which is the default, no task events are
recorded, so the alert never fires.

## Send task notifications to a cloud messaging service

Task integration is implemented using notification integration objects, which provide an interface between Snowflake and
third-party cloud message queuing services.

Snowflake guarantees at-least-once message delivery of notifications. Multiple attempts are made to deliver messages to
ensure at least one attempt succeeds, which can result in duplicate messages.

This feature is supported for both serverless tasks and user-managed tasks, which are tasks that rely on a virtual
warehouse to provide the compute resources.

Notifications rely on cloud messaging that uses one of the following services:

- Amazon Simple Notification Service (SNS)
- Microsoft Azure Event Grid
- Google Pub/Sub

Currently, cross-cloud support isn’t available for push notifications. You must configure notification support for the
messaging service that is provided by the cloud platform where your Snowflake account is hosted.

Note

The email and webhook notification integration types aren’t supported for `ERROR_INTEGRATION` or `SUCCESS_INTEGRATION`.
To receive task notifications by email or webhook, use a task alert instead. See
[Configure error alerts and notifications for tasks](/user-guide/tasks-errors-integrate).

You can use the NOTIFICATION\_HISTORY table function to query the history of task notifications. For more information, see
[NOTIFICATION\_HISTORY](/sql-reference/functions/notification_history).

To set up task notifications, complete the following steps:

1. Create a topic to receive the notifications, and set up a notification integration for that topic.

   For more information, see the instructions for your platform:

   - [AWS SNS](/user-guide/notifications/creating-notification-integration-amazon-sns)
   - [Google Pub/Sub](/user-guide/notifications/creating-notification-integration-google-pubsub)
   - [Azure Event Grid](/user-guide/notifications/creating-notification-integration-azure-event-grid)
2. Create or configure the task to use the notification integration for error and success notifications.

   See [Configure error alerts and notifications for tasks](/user-guide/tasks-errors-integrate) and [Configure a task to send success notifications](/user-guide/tasks-success-integrate).
