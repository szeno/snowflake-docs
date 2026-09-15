# Enabling Snowpipe error notifications for Microsoft Azure Event Grid

This topic provides instructions for pushing Snowpipe error notifications to the [Microsoft Azure Event Grid](https://azure.microsoft.com/en-us/services/event-grid/) (Event Grid).

This feature can push error notifications for the following types of loads:

- Auto-ingest Snowpipe.
- Calls to the Snowpipe `insertFiles` REST API endpoint.
- Loads from Apache Kafka using the Snowflake Connector for Kafka with the Snowpipe ingestion method only.

## Cloud platform support

Currently, this feature is limited to Snowflake accounts hosted on Microsoft Azure. Snowpipe can load data from files in any supported cloud storage service; however, push notifications to Event Grid are only supported in Snowflake accounts hosted on Azure.

## Notes

- Snowflake guarantees at-least-once message delivery of error notifications (that is, multiple attempts are made to deliver messages to ensure at least one attempt succeeds, which can result in duplicate messages).
- This feature is implemented using the notification integration object. A notification integration is a Snowflake object that provides an
  interface between Snowflake and third-party cloud message queuing services. A single notification integration can support multiple pipes.

## Enabling error notifications

### Creating the notification integration

See [Creating a notification integration to send notifications to a Microsoft Azure Event Grid topic](/user-guide/notifications/creating-notification-integration-azure-event-grid).

### Enabling error notifications in pipes

A single notification integration can be shared by multiple pipes. The body of error messages identifies the pipe, external stage and
path, and file where the error originated, among other details.

To enable error notifications for a pipe, specify an ERROR\_INTEGRATION parameter value.

Note

Creating or modifying a pipe that references a notification integration requires a role that has the USAGE privilege on the notification
integration. In addition, the role must have either the CREATE PIPE privilege on the schema or the OWNERSHIP privilege on the pipe,
respectively.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

#### New pipe

Create a new pipe using [CREATE PIPE](/sql-reference/sql/create-pipe):

Copy code

```
CREATE PIPE <name>
  AUTO_INGEST = TRUE
  [ INTEGRATION = '<string>' ]
  ERROR_INTEGRATION = <integration_name>
  AS <copy_statement>
```

Where:

`ERROR_INTEGRATION = <integration_name>`
:   Name of the notification integration you created in [Create notification integration in Snowflake](/user-guide/notifications/creating-notification-integration-azure-event-grid#label-notification-integration-azure-creating-integration).

For example:

Copy code

```
CREATE PIPE mypipe
  AUTO_INGEST = TRUE
  INTEGRATION = 'my_storage_int'
  ERROR_INTEGRATION = my_notification_int
  AS
  COPY INTO mydb.public.mytable
  FROM @mydb.public.mystage;
```

#### Existing pipe

Modify an existing pipe using [ALTER PIPE](/sql-reference/sql/alter-pipe):

Copy code

```
ALTER PIPE <name> SET ERROR_INTEGRATION = <integration_name>;
```

Where `<integration_name>` is the name of the notification integration you created in
[Create notification integration in Snowflake](/user-guide/notifications/creating-notification-integration-azure-event-grid#label-notification-integration-azure-creating-integration).

For example:

Copy code

```
ALTER PIPE mypipe SET ERROR_INTEGRATION = my_notification_int;
```

## Error notification message payload

The body of error messages identifies the pipe and the errors encountered during a load.

The following is a sample message payload describing a Snowpipe error. The payload can include one or more error messages.

Copy code

```
{\"version\":\"1.0\",\"messageId\":\"a62e34bc-6141-4e95-92d8-f04fe43b43f5\",\"messageType\":\"INGEST_FAILED_FILE\",\"timestamp\":\"2021-10-22T19:15:29.471Z\",\"accountName\":\"MYACCOUNT\",\"pipeName\":\"MYDB.MYSCHEMA.MYPIPE\",\"tableName\":\"MYDB.MYSCHEMA.MYTABLE\",\"stageLocation\":\"azure://myaccount.blob.core.windows.net/mycontainer/mypath\",\"messages\":[{\"fileName\":\"/file1.csv_0_0_0.csv.gz\",\"firstError\":\"Numeric value 'abc' is not recognized\"}]}
```

Note that you must parse the string into a JSON object to process values in the payload.
