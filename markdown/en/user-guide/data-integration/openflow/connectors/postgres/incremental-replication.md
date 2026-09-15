# Openflow Connector for PostgreSQL: Set up incremental replication without snapshots

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

You can configure the Openflow Connector for PostgreSQL connector to immediately replicate incremental changes for newly added tables, bypassing snapshots. Use incremental load to continue replication without snapshotting every table again when you reinstall the connector over previously replicated data.

To enable incremental replication in a new connector instance:

1. Set up the connector as described in [Set up the Openflow Connector for PostgreSQL](/user-guide/data-integration/openflow/connectors/postgres/setup).
2. In the `PostgreSQL Ingestion Parameters` context, set the `Ingestion Type` parameter to `incremental`.

## Enable incremental replication without snapshots

To enable incremental replication on an existing connector:

1. sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. in the navigation menu, select **Ingestion** » **Openflow**.
3. In the **Openflow** pane select the **Runtimes** tab.
4. Select the runtime containing the connector.
5. Select the connector.
6. In the `Ingestion Parameters` context, specify `Ingestion Type` = `incremental`.
7. Add new replication tables. These tables immediately switch to their incremental load.

Note

To return to replicating tables with the snapshot load, change **Ingestion Type** from `incremental` to `full`.

# Usage notes

- Changing the value of **Ingestion Type** does not impact any tables that have begun replicating data.
  Tables currently in the snapshot phase continue until the snapshot load is complete.
- While **Ingestion Type** is set to `incremental`, new tables added to the list of replicated tables bypass the snapshot phase.
  This includes new tables added to the source database that match the `Included Table Regex` parameter.
  Ensure that the ingestion type is set to `incremental` to bypass the snapshot phase.

  Note

  Connectors should only remain in `incremental` mode as long as required as it bypasses snapshots.
  Once customer needs for incremental updates have been satisfied the connector should be returned to `full` mode.
- For tables that bypass snapshot load, the connector creates a destination table in Snowflake,
  by executing `CREATE TABLE IF NOT EXISTS`, only if no destination table already exists.
  Tables going through the snapshot require that no destination table exist.
