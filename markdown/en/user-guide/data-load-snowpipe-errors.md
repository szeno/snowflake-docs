# Snowpipe error notifications

Snowpipe can send a message to your cloud messaging service when a file fails to load, so you find out about failed loads without polling the copy history. Each message identifies the pipe, the target table, and the stage location, and lists the files that failed, with the first error in each file. You can subscribe any consumer to the topic that receives the messages: for example, a function that moves failed files aside, or a service that forwards the message to email, chat, or a ticketing system.

To send error notifications, a pipe needs an *error integration*: a notification integration that points to a topic in the messaging service of the cloud platform that hosts your Snowflake account. One integration can serve many pipes.

## Supported messaging services

The following table lists the messaging service for each cloud platform:

| Cloud platform that hosts your account | Messaging service |
| --- | --- |
| Amazon Web Services | Amazon SNS standard topic |
| Google Cloud | Google Cloud Pub/Sub topic |
| Microsoft Azure | Microsoft Azure Event Grid custom topic |

Expand

Show lessSee more

The messaging service must be on the same cloud platform as your Snowflake account, but the files that the pipe loads can be on any cloud platform. For example, an account hosted on AWS sends error notifications to Amazon SNS, even when its pipes load files from Google Cloud Storage.

## Errors that notifications report

Snowpipe sends an error notification when a file fails to load, such as when the file contains a data error or Snowpipe can’t find the file in the stage. In the copy history, these files have the `Load failed` status. Snowpipe sends error notifications for the following kinds of loads:

- Automated loads, which start from event notifications from your cloud storage service.
- Loads that start from calls to the `insertFiles` endpoint of the [Snowpipe REST API](/user-guide/data-load-snowpipe-rest-overview).
- Loads from Apache Kafka through the [Snowflake Connector for Kafka](/user-guide/kafka-connector), when the connector uses the Snowpipe ingestion method.

Error notifications don’t report the following problems:

- **Files that load partially.** If a pipe uses `ON_ERROR = CONTINUE`, Snowpipe loads the valid rows of a file that contains errors and sends a notification only if no rows from the file load. With `ON_ERROR` set to `SKIP_FILE_<num>` or `SKIP_FILE_<num>%`, Snowpipe sends a notification only for files that reach the error limit. To get a notification for every file that contains an error, use the default setting, `ON_ERROR = SKIP_FILE`.
- **Files that fail because of repeated internal errors.** In rare cases, Snowpipe marks a file as `Load failed` after repeated internal failures and doesn’t send a notification for it. To find these files, check the copy history.
- **Problems with the pipe itself.** Error notifications don’t tell you when a pipe stops or stalls, or when Snowflake can’t read the pipe’s notification channel. For those problems, record [Snowpipe events](/user-guide/data-load-snowpipe-monitor-events#label-snowpipe-events-enable) in an event table and create an [alert](/user-guide/data-load-snowpipe-monitor-events#label-snowpipe-events-alerts-errors) on them.
- **Files that never reach Snowpipe.** If your cloud storage service stops sending event notifications, or your application stops calling the REST API, no file fails, so Snowpipe sends no error notification. To catch this problem, create a [scheduled alert](/user-guide/data-load-snowpipe-monitor-events#label-snowpipe-events-alerts-idle) that calls [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status) and checks how long ago the pipe last loaded a file.

Snowflake delivers each error notification at least once. It retries messages that fail because of temporary errors, so your consumer might receive the same message more than once. To ignore duplicates, use the `messageId` field.

## Before you begin

Make sure that you have the following:

- **A topic in your cloud messaging service.** For Amazon SNS, use a standard topic. Snowpipe doesn’t support SNS FIFO topics. Messages that it sends to a FIFO topic fail, and the `NOTIFICATION_HISTORY` function shows them with the `FAILURE` status.
- **A role that can create the integration.** Creating a notification integration requires either the `CREATE NOTIFICATION INTEGRATION` privilege or the `CREATE INTEGRATION` privilege on the account. By default, only the `ACCOUNTADMIN` role has these privileges. `CREATE NOTIFICATION INTEGRATION` lets a role create notification integrations but no other types of integrations.
- **A role that can configure the pipe.** To add an error integration to a new pipe, you need the [privileges to create a pipe](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-access-control). To add one to an existing pipe, you need the `OPERATE` or `OWNERSHIP` privilege on the pipe. In both cases, you also need the `USAGE` privilege on the integration. For the privileges that the pipe owner must keep, see the **Own a pipe** column in [Snowpipe access control](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-access-control).

## Set up error notifications

To set up error notifications for a pipe, complete the following steps.

### Step 1: Create an error integration

Create an outbound notification integration for your topic, and grant Snowflake permission to publish messages to the topic. Follow the instructions for the cloud platform that hosts your account:

- [Creating a notification integration to send notifications to an Amazon SNS topic](/user-guide/notifications/creating-notification-integration-amazon-sns)
- [Creating a notification integration to send notifications to a Google Cloud Pub/Sub topic](/user-guide/notifications/creating-notification-integration-google-pubsub)
- [Creating a notification integration to send notifications to a Microsoft Azure Event Grid topic](/user-guide/notifications/creating-notification-integration-azure-event-grid)

An error integration must have `TYPE = QUEUE` and `DIRECTION = OUTBOUND`. Snowpipe can’t send error notifications through email or webhook notification integrations, or through the inbound notification integrations that pipes use for automated loading, such as the integrations for Google Cloud Storage and Microsoft Azure.

### Step 2: Grant the USAGE privilege on the integration

Grant the `USAGE` privilege on the integration to the role that owns the pipe. If a different role creates or alters the pipe, grant that role the `USAGE` privilege too. For example:

Copy code

```
GRANT USAGE ON INTEGRATION my_error_int TO ROLE pipe_owner_role;
```

The role that owns the pipe must keep this privilege. If you revoke it, or if you transfer ownership of the pipe to a role that doesn’t have it, Snowpipe stops sending error notifications for the pipe without reporting an error. The pipe keeps loading files.

### Step 3: Add the integration to the pipe

Add the error integration to a new pipe or to an existing pipe.

#### New pipe

To send error notifications from a new pipe, specify the `ERROR_INTEGRATION` property in the [CREATE PIPE](/sql-reference/sql/create-pipe) statement:

Copy code

```
CREATE PIPE mydb.myschema.orders_pipe
  ERROR_INTEGRATION = my_error_int
  AS
  COPY INTO mydb.myschema.orders
    FROM @mydb.myschema.orders_stage
    FILE_FORMAT = (TYPE = 'JSON')
    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
```

For a pipe that loads automatically, also set `AUTO_INGEST = TRUE`.

A pipe that loads automatically from Google Cloud Storage or Microsoft Azure, or from Amazon S3 through a Multi-Queue Notification Integration, also has an `INTEGRATION` property, which names the inbound notification integration that delivers event notifications from your storage. `ERROR_INTEGRATION` names a different, outbound integration that sends messages to your topic, so a pipe can have both.

#### Existing pipe

To send error notifications from an existing pipe, set the property with [ALTER PIPE](/sql-reference/sql/alter-pipe). You don’t need to recreate the pipe, and the pipe keeps its load metadata. The following statement adds the `my_error_int` integration to the `orders_pipe` pipe:

Copy code

```
ALTER PIPE mydb.myschema.orders_pipe SET ERROR_INTEGRATION = my_error_int;
```

To confirm the setting, run [DESCRIBE PIPE](/sql-reference/sql/desc-pipe) and check the `error_integration` column.

### Step 4: Test the setup

To confirm that Snowflake can publish messages to your topic, send a test message through the integration with the [SYSTEM$SEND\_SNOWFLAKE\_NOTIFICATION](/sql-reference/stored-procedures/system_send_snowflake_notification) stored procedure:

Copy code

```
CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
  SNOWFLAKE.NOTIFICATION.APPLICATION_JSON('{"test": "Snowpipe error notification test"}'),
  SNOWFLAKE.NOTIFICATION.INTEGRATION('my_error_int'));
```

If the message doesn’t arrive in your topic, [check the delivery status](#label-snowpipe-errors-check-delivery). The test message has `STORED_PROCEDURE` in the `MESSAGE_SOURCE` column, so remove the `WHERE message_source = 'SNOWPIPE'` filter from the query in that section.

Test the whole path from a failed load to your consumer. In the location that the pipe loads from, stage a file that the pipe can’t load. For example, stage a JSON file that’s missing a closing brace. If you load files with the REST API, also submit the file to the `insertFiles` endpoint. Within a few minutes, your topic receives an error notification for the file. Then delete the test file from the stage.

## Error notification messages

Each error notification is a JSON object. The following example describes one file that failed to load:

Copy code

```
{
  "version": "1.0",
  "messageId": "a62e34bc-6141-4e95-92d8-f04fe43b43f5",
  "messageType": "INGEST_FAILED_FILE",
  "timestamp": "2026-10-03T19:15:29.471Z",
  "accountName": "AB12345",
  "pipeName": "MYDB.MYSCHEMA.ORDERS_PIPE",
  "tableName": "MYDB.MYSCHEMA.ORDERS",
  "stageLocation": "s3://mybucket/orders/",
  "messages": [
    {
      "fileName": "2026/10/03/orders_0042.json.gz",
      "firstError": "Error parsing JSON: incomplete object value"
    }
  ]
}
```

Your messaging service delivers this object as a string inside its own message format. For example, Amazon SNS delivers it in the `Message` field of the notification. Parse the string as JSON to read the fields.

The message contains the following fields:

| Field | Description |
| --- | --- |
| `version` | The version of the message format. The current version is `1.0`. |
| `messageId` | A unique ID for the message. Because Snowflake delivers messages at least once, use this ID to ignore duplicate messages. |
| `messageType` | The type of message. For Snowpipe error notifications, the value is always `INGEST_FAILED_FILE`. |
| `timestamp` | The time when Snowflake created the message, in ISO 8601 format and in UTC. |
| `accountName` | The account locator of the Snowflake account that contains the pipe. This value isn’t the account name in your organization. |
| `pipeName` | The fully qualified name of the pipe. |
| `tableName` | The fully qualified name of the target table. |
| `stageLocation` | For an external stage, the cloud storage location of the files, such as `s3://mybucket/orders/`, `gcs://mybucket/orders/`, or `azure://myaccount.blob.core.windows.net/mycontainer/orders/`. For an internal stage, a path that Snowflake uses for the stage, not the stage name. This value matches the `STAGE_LOCATION` column in the copy history. |
| `messages` | An array with one object for each file that failed to load. One message can describe several files from the same pipe. |
| `messages[].fileName` | The path of the file in the stage location. This value matches the `FILE_NAME` column in the copy history. The `stageLocation` value doesn’t always end with `/`; the `/` that separates the two values can be at the start of `fileName` instead. |
| `messages[].firstError` | The first error that Snowpipe found in the file. To see every error in the file, use the [VALIDATE\_PIPE\_LOAD](/sql-reference/functions/validate_pipe_load) function. |

Expand

Show lessSee more

## Check the delivery status of error notifications

To find out whether Snowflake sent error notifications, and why a notification failed, query the [NOTIFICATION\_HISTORY](/sql-reference/functions/notification_history) table function. The following query returns the error notifications from Snowpipe in the last 24 hours:

Copy code

```
SELECT created,
       integration_name,
       message_source_info:pipe_name::STRING AS pipe_name,
       status,
       error_message
  FROM TABLE(mydb.INFORMATION_SCHEMA.NOTIFICATION_HISTORY(
    START_TIME => DATEADD('hour', -24, CURRENT_TIMESTAMP()),
    RESULT_LIMIT => 1000))
  WHERE message_source = 'SNOWPIPE'
  ORDER BY created DESC;
```

The function returns a row for each attempt to send a message. The `STATUS` column has one of the following values:

- `QUEUED`: Snowflake hasn’t sent the message yet.
- `SUCCESS`: Snowflake sent the message to your topic.
- `RETRIABLE_FAILURE`: An attempt failed, and Snowflake tries again later.
- `FAILURE`: Snowflake stopped trying to send the message, either because retrying can’t fix the error or because all retries failed. The `ERROR_MESSAGE` column explains why. For example, Snowflake might not have permission to publish to the topic.

To see the results, use the role that owns the integration or a role that has the `USAGE` privilege on the integration. The `ACCOUNTADMIN` role sees the results only if it owns the integration or has the `USAGE` privilege on it.

## Manage error notifications

To switch a pipe to a different topic, or to stop error notifications for one pipe, you unset the pipe’s `ERROR_INTEGRATION`. Before you do, check that your role has the privileges in the [ALTER PIPE access control requirements](/sql-reference/sql/alter-pipe#access-control-requirements). Use the following commands to change or stop error notifications:

- To send a pipe’s error notifications to a different topic, unset the current integration, and then set the new one. Setting a different integration while one is already set fails, and the pipe keeps the original integration. The following statements switch the pipe to the `my_other_error_int` integration:

  Copy code

  ```
  ALTER PIPE mydb.myschema.orders_pipe UNSET ERROR_INTEGRATION;
  ALTER PIPE mydb.myschema.orders_pipe SET ERROR_INTEGRATION = my_other_error_int;
  ```
- To stop error notifications for one pipe, unset the property:

  Copy code

  ```
  ALTER PIPE mydb.myschema.orders_pipe UNSET ERROR_INTEGRATION;
  ```
- To stop error notifications for every pipe that uses an integration, disable the integration:

  Copy code

  ```
  ALTER NOTIFICATION INTEGRATION my_error_int SET ENABLED = FALSE;
  ```

  Snowpipe doesn’t send notifications for files that fail while the integration is disabled, even after you enable the integration again.

To find the pipes that use an integration, run [SHOW PIPES](/sql-reference/sql/show-pipes) and check the `error_integration` column.

## Troubleshoot missing error notifications

If you expect an error notification but your topic doesn’t receive one, check the following in order:

1. **The file failed to load.** Query the [COPY\_HISTORY](/sql-reference/functions/copy_history) table function for the file. If its status is `Partially loaded`, the pipe loaded some rows, so Snowpipe didn’t send a notification. If its status is `Load failed` but steps 2 through 4 pass and step 5 finds no row for the notification, the file might have failed because of repeated internal errors, which don’t trigger error notifications. If the file doesn’t appear in the copy history at all, Snowpipe never received it. For automated loading, see [Some staged files were never loaded](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-missing-files). If you submit files with `insertFiles`, see [Files don’t load with the REST API](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-rest-api).
2. **The pipe has an error integration.** Run [DESCRIBE PIPE](/sql-reference/sql/desc-pipe) and check that the `error_integration` column shows the integration.
3. **The integration exists and is enabled.** Run [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration) and check that `ENABLED` is `true`. If the integration is disabled or was dropped, Snowpipe doesn’t send error notifications and doesn’t report an error.
4. **The pipe’s owner can use the integration.** Run `SHOW GRANTS ON INTEGRATION my_error_int;` and check that the role that owns the pipe has the `USAGE` or `OWNERSHIP` privilege.
5. **Snowflake sent the message.** [Check the delivery status](#label-snowpipe-errors-check-delivery). If the status is `FAILURE`, fix the problem that the `ERROR_MESSAGE` column describes. The problem is usually that Snowflake doesn’t have permission to publish to the topic or, for Amazon SNS, that the topic is a FIFO topic. If the status is `SUCCESS`, check the subscriptions on your topic.

## Limitations

- The topic must be in the messaging service of the cloud platform that hosts your Snowflake account.
- Error integrations must be outbound queue notification integrations for Amazon SNS, Google Cloud Pub/Sub, or Microsoft Azure Event Grid. Email and webhook notification integrations aren’t supported. To get email about failed loads, create an [alert on Snowpipe events](/user-guide/data-load-snowpipe-monitor-events#label-snowpipe-events-alerts-errors) instead.
- Amazon SNS FIFO topics aren’t supported.
- Files that load partially don’t trigger error notifications.
- Files that fail because of repeated internal errors don’t trigger error notifications.
- Snowflake delivers each message at least once, so consumers might receive duplicate messages.
