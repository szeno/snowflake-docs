# Configure a task to send success notifications

Snowflake can push success notifications to a cloud messaging service when a task graph completes successfully. This topic provides instructions for configuring success notification support for tasks using cloud messaging.

Success notification integration is only specified on a root task of a task graph. Snowflake only sends success notifications when the entire task graph is successfully executed and will not send notifications for any successfully executed standalone task, which is different from [error notification integration](/user-guide/tasks-errors-integrate).

Note

The task success notification feature is supported for both serverless tasks and user-managed tasks (that is, tasks that rely on a virtual warehouse to provide the compute resources).

To enable a task to send success notifications, you must associate the task with a message notification integration. Follow the task documentation to create a notification integration with [Amazon Web Services Simple Notification Service (AWS SNS)](/user-guide/notifications/creating-notification-integration-amazon-sns), [Microsoft Azure Event Grid](/user-guide/notifications/creating-notification-integration-azure-event-grid), or [Google Pub/Sub](/user-guide/notifications/creating-notification-integration-google-pubsub).

## Create a new task or modify an existing task to send success notifications

You can associate the task with a notification integration when running the [CREATE TASK](/sql-reference/sql/create-task) command to create a new task, or running the [ALTER TASK](/sql-reference/sql/alter-task) command to modify an existing task.

Note

Creating or modifying a task that references a notification integration requires a role that has the USAGE privilege on the notification integration. In addition, the role must have either the CREATE TASK privilege on the schema or the OWNERSHIP privilege on the task, respectively.

Copy code

```
CREATE [ OR REPLACE ] TASK [ IF NOT EXISTS ] <name>
    WAREHOUSE = <string>
    [...]
    SUCCESS_INTEGRATION = <integration_name>
```

Copy code

```
ALTER TASK <name> SET SUCCESS_INTEGRATION = <integration_name>;
```

Where:

`SUCCESS_INTEGRATION = integration_name`

Name of the notification integration created in one of [AWS SNS](/user-guide/notifications/creating-notification-integration-amazon-sns), [Microsoft Azure Event Grid](/user-guide/notifications/creating-notification-integration-azure-event-grid), or [Google Pub/Sub](/user-guide/notifications/creating-notification-integration-google-pubsub) platform level notifications.

## Display success notifications

You can run [SHOW TASKS](/sql-reference/sql/show-tasks) or [DESCRIBE TASK](/sql-reference/sql/desc-task) to see task success notifications. Snowflake adds a new column, success\_integration, to the output of SHOW TASKS and DESCRIBE TASK. This field displays null for all child tasks. This field displays the name of the graph-level success integration if the notification integration is specified on a root task, and null otherwise.

## Payload

The body of success messages includes information that identifies the task graph, such as rootTaskName, rootTaskID, queryID, and attemptNumber. The following is a sample message payload for a task graph success notification.

Copy code

```
{"version":"1.0",
 "messageId":"3ff1eff0-7ad7-493c-9552-c0307087e0c6",
 "messageType":"GRAPH_SUCCEEDED",
 "timestamp":"2021-11-11T19:46:39.648Z",
 "accountName":"XY12345",
 "rootTaskName":"AWS_UTEN_DPO_DB.AWS_UTEN_SC.UTEN_AWS_TK1",
 "rootTaskId":"01a03962-2b57-889e-0000-000000000001",
 "messages": [{
              "runId":"2021-11-11T19:46:23.826Z",
              "scheduledTime":"2021-11-11T19:46:23.826Z",
              "queryStartTime":"2021-11-11T19:46:24.879Z",
              "graphCompletedTime":"2021-11-11T19:54:24.5591",
              "queryId":"01a03962-0300-0002-0000-0000000034d8",
              "attemptNumber":5
}]}
```

Note that you must parse the string into a JSON object to process values in the payload.
