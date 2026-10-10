# Configure error alerts and notifications for tasks

There are two ways to be notified about task errors:

- A [task alert](#label-tasks-errors-alert) notifies you by email or webhook when the cumulative error rate of your tasks
  crosses a threshold that you choose.
- [ERROR\_INTEGRATION](#label-tasks-errors-integration) pushes a message to a cloud messaging service for each failed
  task run.

## Monitor the task error rate with an alert

Snowflake provides a built-in alert template, `TASKS_ERROR_RATE`, that notifies you by email or webhook when the
cumulative error rate of your tasks crosses a threshold that you choose. The template defines the condition and the
action for you, so you supply only the threshold, the scope, and the notification target.

An alert tells you that your tasks are failing more often than you’re willing to tolerate. It doesn’t send a message for
each failure. If you need that, use `ERROR_INTEGRATION` instead. See [Send a notification for each failed task run](#label-tasks-errors-integration).

Task alerts require `LOG_EVENT_LEVEL` to be set to `INFO` on the tasks you want to monitor, so that both successful and
failed runs are recorded. For details, see [Prerequisites for task alerts](/user-guide/tasks-errors#label-tasks-notifications-prerequisites).

To create the alert, choose the **Error rate alert** template in the **TASKS** template group. See
[Creating a new alert](/user-guide/alerts-ui#label-alerts-center-create) for the Snowsight steps, or
[Creating an alert from a template with SQL](/user-guide/alerts#label-alerts-create-from-template) for the SQL equivalent.

The template delivers notifications by email or webhook. To send alert notifications to a cloud provider queue instead,
create a custom alert whose action calls `SYSTEM$SEND_SNOWFLAKE_NOTIFICATION` with a queue notification integration.
See [Setting up alerts based on data in Snowflake](/user-guide/alerts) and [Sending notifications to cloud provider queues (Amazon SNS, Google Cloud PubSub, and Azure Event Grid)](/user-guide/notifications/queue-notifications).

## Send a notification for each failed task run

To enable a task to send error notifications, you must associate the task with a notification integration.
You can do this when running the [CREATE TASK](/sql-reference/sql/create-task) command to create a new task or
the [ALTER TASK](/sql-reference/sql/alter-task) command to modify an existing task.
When running these commands, set `ERROR_INTEGRATION` to the name of the notification integration.

You only specify the error notification integrations on a root task of a task graph. Any failed child task sends error notifications to
the root task’s specified integration.

Tasks with `TASK_AUTO_RETRY_ATTEMPTS` set to a value greater than `0` send error notifications for each failed task run.

Note

Creating or modifying a task that references a notification integration requires a role that has the USAGE privilege on the notification
integration. In addition, the role must have either the CREATE TASK privilege on the schema or the OWNERSHIP privilege on the task.

### Create a new task that sends error notifications

Create a new task using [CREATE TASK](/sql-reference/sql/create-task). For descriptions of all available task parameters, see the SQL command
topic:

Copy code

```
CREATE TASK <name>
  [...]
  ERROR_INTEGRATION = <integration_name>
  AS <sql>
```

Where:

`ERROR_INTEGRATION = integration_name`
:   Specifies the name of a notification integration created using [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration). For more information, see
    [AWS SNS](/user-guide/notifications/creating-notification-integration-amazon-sns), [Google Pub/Sub](/user-guide/notifications/creating-notification-integration-google-pubsub), or [Azure Event Grid](/user-guide/notifications/creating-notification-integration-azure-event-grid).

The following example creates a serverless task that supports error notifications. The task inserts the current timestamp into a table
column every 5 minutes:

Copy code

```
CREATE TASK mytask
  SCHEDULE = '5 MINUTE'
  ERROR_INTEGRATION = my_notification_int
  AS
  INSERT INTO mytable(ts) VALUES(CURRENT_TIMESTAMP);
```

### Update an existing task to send error notifications

Modify an existing task using [ALTER TASK](/sql-reference/sql/alter-task):

Copy code

```
ALTER TASK <name> SET ERROR_INTEGRATION = <integration_name>;
```

Where `integration_name` is the name of the notification integration created in one of
[AWS SNS](/user-guide/notifications/creating-notification-integration-amazon-sns), [Google Pub/Sub](/user-guide/notifications/creating-notification-integration-google-pubsub), or [Azure Event Grid](/user-guide/notifications/creating-notification-integration-azure-event-grid) platform level notifications.

For example:

Copy code

```
ALTER TASK mytask SET ERROR_INTEGRATION = my_notification_int;
```

### Task error notification message payload

The body of error messages identifies the task and the errors encountered during a task run.

The following is a sample message payload describing a task error. The payload can include one or more error messages.

Copy code

```
{\"version\":\"1.0\",\"messageId\":\"3ff1eff0-7ad7-493c-9552-c0307087e0c6\",\"messageType\":\"USER_TASK_FAILED\",\"timestamp\":\"2021-11-11T19:46:39.648Z\",\"accountName\":\"AWS_UTEN_DPO_ACC\",\"taskName\":\"AWS_UTEN_DPO_DB.AWS_UTEN_SC.UTEN_AWS_TK1\",\"taskId\":\"01a03962-2b57-889e-0000-000000000001\",\"rootTaskName\":\"AWS_UTEN_DPO_DB.AWS_UTEN_SC.UTEN_AWS_TK1\",\"rootTaskId\":\"01a03962-2b57-889e-0000-000000000001\",\"messages\":[{\"runId\":\"2021-11-11T19:46:23.826Z\",\"scheduledTime\":\"2021-11-11T19:46:23.826Z\",\"queryStartTime\":\"2021-11-11T19:46:24.879Z\",\"completedTime\":\"null\",\"queryId\":\"01a03962-0300-0002-0000-0000000034d8\",\"errorCode\":\"000630\",\"errorMessage\":\"Statement reached its statement or warehouse timeout of 10 second(s) and was canceled.\"}]}
```

Note that you must parse the string into a JSON object to process values in the payload.
