# Use the Openflow Connector for Google BigQuery

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes tasks you may need to perform after installing and configuring the
connector.

## Remove and re-add a table for replication

To remove a table from replication:

1. Verify the table’s state in the Table State Store.
2. If the state is `INCREMENTAL_IN_PROGRESS`, stop the **Trigger BigQuery Cdc On Incremental** processor.
   Wait for the state to change to `INCREMENTAL_REPLICATION`.
3. Remove the table from the **Included Table Names** or **Included Table Names Regex** parameters in the BigQuery Ingestion Parameters context.

To re-add a table for replication:

1. Drop the destination table in Snowflake.
2. Add the table back to the **Included Table Names** or **Included Table Names Regex** parameters.

This approach can also be used to recover from a failed table replication scenario.
