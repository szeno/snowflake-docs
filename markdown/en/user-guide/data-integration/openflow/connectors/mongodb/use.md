# Use the Openflow Connector for MongoDB

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes how to use the Openflow Connector for MongoDB after you have installed and configured it.

## Tracking data changes in MongoDB

The connector uses MongoDB change streams for incremental synchronization, subscribing to
data changes across the entire MongoDB deployment (replica sets or sharded clusters). The
connector processes changes only after they persist to a majority of replica set members.

The connector listens for inserts, updates, and deletes from the change stream and writes them
to a journal table in Snowflake. The connector manages these journal tables and uses them
to merge data into the destination table.

Warning

Do not modify journal tables. Manual modifications can disrupt synchronization and
compromise data integrity.

The merge operation handles changes as follows:

Inserts and updates:
:   The connector upserts `INSERT` and `UPDATE` operations into the Snowflake table.

Deletes:
:   The connector uses a soft-delete strategy to preserve history. It updates the target row
    by setting the `_SNOWFLAKE_DELETED` column to `TRUE` instead of deleting the row.

The connector adds the `_SNOWFLAKE_DELETED` (BOOLEAN) column to the destination table
during creation.

**Connection recovery**

If the connection to a change stream is lost, the connector attempts to reconnect through
another cluster node. To ensure data consistency, the connector tracks the resume token of
the last processed document. Upon reconnection, it uses this token to retrieve only changes
that occurred after the disconnection.

The MongoDB Oplog must be large enough to retain change history during downtime. If the
connector remains offline longer than the Oplog retention period, the resume token might
expire, which requires a full data re-sync.

## Remove and re-add a collection to replication

To remove a collection from replication:

1. Remove it from the `Included Collection Names` or `Included Collection Regex` parameters in the
   MongoDB ingestion parameters context.

To re-add a collection to replication:

1. Drop the corresponding destination table in Snowflake.
2. Add the collection back to the `Included Collection Names` or `Included Collection Regex`
   parameters.

This ensures that the replication process starts fresh for the collection.

You can also use this remove-and-re-add procedure to recover from a failed replication.

## Check the replication status of a collection

Interim failures, such as connection errors, don’t prevent collection replication. However, permanent failures, such as unsupported data, prevent collection replication.

To troubleshoot replication issues or verify that a collection has been successfully removed from the replication flow, check the Collection State Store:

1. In the Openflow runtime canvas, right-click a processor group and choose **Controller Services**. A table listing controller services displays.
2. Locate the row labeled **Collection State Store**, click the **More** [![Three vertical dots indicating more options](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png) button on the right side of the row, and then choose **View State**.

A list of collections and their current states displays. Use the search box to filter the list by collection name. The possible states are:

- **NEW**: The collection is scheduled for replication but replication hasn’t started.
- **SNAPSHOT\_REPLICATION**: The connector is copying existing documents. This status displays until all documents are stored in the destination table.
- **INCREMENTAL\_REPLICATION**: The connector is actively replicating changes. This status displays after snapshot replication ends and continues to display indefinitely until a collection is either removed from replication or replication fails.
- **FAILED**: Replication has permanently stopped due to an error.

Note

The Openflow runtime canvas doesn’t display state changes, only the current state. However, state changes are recorded in logs when they occur.

If a permanent failure prevents replication, follow the procedure in the preceding section to remove the collection from replication, address the underlying problem, and then re-add the collection.
