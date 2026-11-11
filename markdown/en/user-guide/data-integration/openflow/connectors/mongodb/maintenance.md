# Openflow Connector for MongoDB: Maintenance

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

## Reinstall the connector

Use this procedure to move an existing connector to another runtime while preserving its
replication state and continuing to write to the same destination tables.

### Prerequisites

- Let any in-progress snapshot loads finish before exporting the connector. The downloaded flow definition
  does not include queued FlowFiles.
- Use Openflow Runtime Server version **2026.6.4.18** or later to download the flow definition with component state.
- Prepare a target runtime that meets the [MongoDB connector requirements](/user-guide/data-integration/openflow/connectors/mongodb/about).
  Configure source connectivity and destination access as described in [Connect to MongoDB](/user-guide/data-integration/openflow/connectors/mongodb/connect).
- Record the connector’s parameter values and have its credentials available. Sensitive values, such as
  passwords, aren’t included in the downloaded flow definition.

Warning

The MongoDB oplog must retain the history needed to resume from the saved change-stream position
throughout the move. If the resume token expires before the new connector starts, a full data
re-sync might be required. Keep the interruption within the source’s oplog retention window.

### Move the connector

1. In the existing connector’s canvas, stop **Set Collections for Replication** and
   **Read MongoDB Change Stream**. Wait for their active threads to finish.
2. Let the remaining processors finish processing all in-flight FlowFiles. Wait until the connector’s
   **Queued** value is zero. If you use a custom **Merge Task Schedule CRON**, temporarily set it
   to `* * * * * ?` so processing doesn’t wait for the next scheduled merge.
3. Stop all remaining processors, wait for their active threads to finish, and disable the controller services.
   Keep this connector stopped throughout the move and while the replacement connector runs.
4. Right-click the connector’s process group and select **Download flow definition**. Select both options:
   - **Export with External Services**: includes referenced controller services from parent process groups.
   - **Export with Components State**: includes the collection replication state and change-stream position.
5. Import the downloaded flow definition into the target runtime. Don’t start it yet.
6. Review the imported parameter contexts. Keep the same collection selection, **Destination Database**,
   **Destination Schema Pattern**, and **Object Identifier Resolution**. Re-enter **MongoDB Password**
   and any other sensitive values required by the MongoDB and Snowflake authentication settings. If you changed
   **Merge Task Schedule CRON** to drain the old connector, restore the original schedule.
7. Enable the required controller services and start the imported connector.
8. Verify that replication resumes and that changes made in MongoDB during the interruption arrive
   in the destination tables.

Note

Keep the existing destination and journal tables. Don’t remove and re-add collections as part of
this procedure; that is a separate operation to restart replication from scratch.
