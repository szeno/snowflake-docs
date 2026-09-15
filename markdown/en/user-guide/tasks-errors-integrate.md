# Configure a task to send error notifications

To enable a task to send error notifications, you must associate the task with a notification integration.
You can do this when running the [CREATE TASK](/sql-reference/sql/create-task) command to create a new task or
the [ALTER TASK](/sql-reference/sql/alter-task) command to modify an existing task.
When running these commands, set ERROR\_INTEGRATION to the name of the notification integration.

You only specify the error notification integrations on a root task of a task graph. Any failed child task sends error notifications to
the root task’s specified integration.

Tasks with `TASK_AUTO_RETRY_ATTEMPTS` set to a value greater than `0` send error notifications for each failed task run.

Note

Creating or modifying a task that references a notification integration requires a role that has the USAGE privilege on the notification
integration. In addition, the role must have either the CREATE TASK privilege on the schema or the OWNERSHIP privilege on the task.

## Create a new task that sends error notifications

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

## Update an existing task to send error notifications

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

## Task error notification message payload

The body of error messages identifies the task and the errors encountered during a task run.

The following is a sample message payload describing a task error. The payload can include one or more error messages.

Copy code

```
{\"version\":\"1.0\",\"messageId\":\"3ff1eff0-7ad7-493c-9552-c0307087e0c6\",\"messageType\":\"USER_TASK_FAILED\",\"timestamp\":\"2021-11-11T19:46:39.648Z\",\"accountName\":\"AWS_UTEN_DPO_ACC\",\"taskName\":\"AWS_UTEN_DPO_DB.AWS_UTEN_SC.UTEN_AWS_TK1\",\"taskId\":\"01a03962-2b57-889e-0000-000000000001\",\"rootTaskName\":\"AWS_UTEN_DPO_DB.AWS_UTEN_SC.UTEN_AWS_TK1\",\"rootTaskId\":\"01a03962-2b57-889e-0000-000000000001\",\"messages\":[{\"runId\":\"2021-11-11T19:46:23.826Z\",\"scheduledTime\":\"2021-11-11T19:46:23.826Z\",\"queryStartTime\":\"2021-11-11T19:46:24.879Z\",\"completedTime\":\"null\",\"queryId\":\"01a03962-0300-0002-0000-0000000034d8\",\"errorCode\":\"000630\",\"errorMessage\":\"Statement reached its statement or warehouse timeout of 10 second(s) and was canceled.\"}]}
```

Note that you must parse the string into a JSON object to process values in the payload.
