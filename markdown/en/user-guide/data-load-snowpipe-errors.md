# Snowpipe error notifications

Snowpipe can push error notifications to a cloud messaging service when it encounters errors while loading data. The notifications describe the errors encountered in each file, enabling further analysis of the data in the files.

Note

Snowpipe error notifications only work when the ON\_ERROR copy option is set to SKIP\_FILE (the default). Snowpipe will not send any error notifications if the ON\_ERROR copy option is set to CONTINUE.

You can use the NOTIFICATION\_HISTORY table function to query the history of notifications sent through Snowpipe. For more information, refer to [NOTIFICATION\_HISTORY](/sql-reference/functions/notification_history).

Currently, cross-cloud support is not available for push notifications. Configure error notification support for the messaging service provided by the cloud platform where your Snowflake account is hosted.

**Next Topics:**

- [Enabling Snowpipe error notifications for Amazon SNS](/user-guide/data-load-snowpipe-errors-sns)
- [Enabling Snowpipe error notifications for Google Pub/Sub](/user-guide/data-load-snowpipe-errors-gcs)
- [Enabling Snowpipe error notifications for Microsoft Azure Event Grid](/user-guide/data-load-snowpipe-errors-azure)
