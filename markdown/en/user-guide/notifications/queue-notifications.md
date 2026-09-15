# Sending notifications to cloud provider queues (Amazon SNS, Google Cloud PubSub, and Azure Event Grid)

You can configure Snowflake to send notifications to a queue provided by a cloud service (Amazon SNS, Google Cloud PubSub, or
Azure Event Grid).

- To configure [Snowpipe](/user-guide/data-load-snowpipe-intro) or specific [tasks](/user-guide/tasks-intro) to send
  notifications about errors to a queue, see the following topics:

  - [Snowpipe error notifications](/user-guide/data-load-snowpipe-errors)
  - [Set up error notifications for tasks](/user-guide/tasks-errors)
- To call a stored procedure to send a notification to a queue:

  1. Create a notification integration for the cloud provider queue. For details, see the following topics:

     - [Creating a notification integration to send notifications to an Amazon SNS topic](/user-guide/notifications/creating-notification-integration-amazon-sns)
     - [Creating a notification integration to send notifications to a Microsoft Azure Event Grid topic](/user-guide/notifications/creating-notification-integration-azure-event-grid)
     - [Creating a notification integration to send notifications to a Google Cloud Pub/Sub topic](/user-guide/notifications/creating-notification-integration-google-pubsub)

     Note

     Your account must be on the same [cloud platform](/user-guide/intro-cloud-platforms) as the cloud provider queue.
  2. Call the [SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) stored procedure to send the notification
     message to the queue. For details, see [Using SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION to send notifications](/user-guide/notifications/snowflake-notifications).
