# Troubleshooting external tables

This topic describes how to troubleshoot issues with external tables.

## Automatic metadata refreshing is disabled

If ownership of an external table (that is, the OWNERSHIP privilege on the external table) is transferred to a different role, the AUTO\_REFRESH parameter for the external table is set to FALSE by default. To re-enable automatic refreshing of the external table metadata, set the AUTO\_REFRESH parameter to TRUE by using an [ALTER EXTERNAL TABLE](/sql-reference/sql/alter-external-table) statement.

Verify that the configured settings for the external cloud messaging service are still accurate. For more information, see the instructions for your cloud storage provider:

- [Refresh external tables automatically for Amazon S3](/user-guide/tables-external-s3)
- [Refresh external tables automatically for Azure Blob Storage](/user-guide/tables-external-azure)

## Checking the progress of automatic metadata refreshes

Retrieve the current status of the internal, hidden pipe used by the external table to refresh its metadata. The results are displayed in JSON format. For information, see [SYSTEM$EXTERNAL\_TABLE\_PIPE\_STATUS](/sql-reference/functions/system_external_table_pipe_status).

Verify the following values:

> `lastReceivedMessageTimestamp`
> :   Specifies the timestamp of the last event message received from the message queue.
>
>     If the timestamp is earlier than expected, this likely indicates an issue with either the cloud event notification service configuration or the service itself. If the field is empty, verify your service configuration settings. If the field contains a timestamp but it’s earlier than expected, verify whether any settings were changed in your service configuration.
>
> `lastForwardedMessageTimestamp`
> :   Specifies the timestamp of the last event message that was forwarded to the pipe.

### Error: Integration `{0}` associated with the stage `{1}` cannot be found

Copy code

```
003139=SQL compilation error:\nIntegration ''{0}'' associated with the stage ''{1}'' cannot be found.
```

This error can occur when the association between the external stage and the storage
integration linked to the stage has been broken. This happens when the storage integration
object has been recreated (using
[CREATE OR REPLACE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration)).
A stage links to a storage integration using a hidden ID rather than the name of the storage
integration. Behind the scenes, the CREATE OR REPLACE syntax drops the object and recreates
it with a different hidden ID.

If you must recreate a storage integration after it has been linked to one or more stages,
you must reestablish the association between each stage and the storage integration by
executing [ALTER STAGE](/sql-reference/sql/alter-stage)
`stage_name` SET STORAGE\_INTEGRATION = `storage_integration_name`, where:

- `stage_name` is the name of the stage.
- `storage_integration_name` is the name of the storage integration.

## Error: External table `{0}` marked invalid. Stage `{1}` location altered

Querying an external table might produce an error similar to the following error:

Copy code

```
091093 (55000): External table ''{0}'' marked invalid. Stage ''{1}'' location altered.
```

This error can occur when the URL for the referenced stage is modified after the external table was created (by using [ALTER STAGE … SET URL](/sql-reference/sql/alter-stage)).

If you must modify the stage URL, you must recreate any existing external tables that reference the stage (by using [CREATE OR REPLACE EXTERNAL TABLE](/sql-reference/sql/create-external-table)).
