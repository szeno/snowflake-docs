# Maintain the Openflow Connector for Shopify

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes maintenance tasks for the Openflow Connector for Shopify, including how to reset connector state to trigger a fresh bulk load.

## Reset connector state

The connector maintains an internal state to track bulk-load completion status and the
incremental watermark for each object type. In some situations, you might need to
reset the connector to perform a fresh bulk load, for example, after resolving a data issue
or after the connector has been stopped for an extended period.

### Reset all objects

To reset all objects and force a full bulk reload:

1. Stop all processors in the flow by right-clicking on the connector process group and
   selecting **Stop**.
2. Ensure that no in-flight FlowFiles are being processed. You can verify this by checking
   that all queues in the flow are empty.
3. Right-click on the canvas and select **Disable all controller services**.
4. Go to **Controller services** and locate the **Shopify State Service**.
5. Select the menu for **Shopify State Service**, then select **View state** and select
   **Clear state**.
6. Right-click on the canvas and select **Enable all controller services**, then start all
   processors to resume the connector.

The connector treats a cleared state as a fresh start and performs a bulk load for all
configured objects on the next execution.

### Reset a specific object

To reset a single object type and re-ingest it from scratch without affecting other objects:

1. Stop all processors in the flow.
2. Ensure all queues are empty.
3. Right-click on the canvas and select **Disable all controller services**.
4. Go to **Controller services** and locate the **Shopify State Service**.
5. Select the menu for **Shopify State Service**, then select **View state**.
6. Select the trash icon next to the specific object type (for example, `orders`) to delete
   its state entry.
7. Re-enable all controller services and start the flow.

The connector performs a fresh bulk load for that object type and then resumes incremental
updates, while other objects continue from their existing watermark.
