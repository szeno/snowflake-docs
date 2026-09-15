# About the Openflow Connector for Salesforce Bulk API

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts of the Openflow Connector for Salesforce Bulk API, its workflow, and limitations.

## Zero-copy integration with Salesforce Data Cloud

Snowflake offers zero-copy bidirectional sharing and integration with Salesforce. This integration is recommended if you use Salesforce Data Cloud and require near real-time bidirectional integration.

For more information about zero-copy integration with Salesforce Data Cloud, see the following blog posts:

- [Share Your Data from Salesforce Data Cloud to Snowflake](https://developer.salesforce.com/blogs/2024/08/share-your-data-from-salesforce-data-cloud-to-snowflake)
- [Zero Copy Data Federation with Snowflake and Salesforce Data Cloud](https://developer.salesforce.com/blogs/2024/08/zero-copy-data-federation-with-snowflake-and-salesforce-data-cloud)

## About the Openflow Connector for Salesforce Bulk API

The Openflow Connector for Salesforce Bulk API provides replication-based data integration.
This connector is designed for users who do not use Salesforce Data Cloud and prefer a fully managed Snowflake Openflow connector.
The connector uses public Salesforce REST APIs to replicate data from Salesforce to Snowflake at a user-defined frequency.
The connector supports Change Data Capture (CDC) and keeps data in Snowflake in sync with Salesforce.

You can use one or both types of data integrations depending on your specific use cases. This topic describes how to set up and use the Openflow Connector for Salesforce Bulk API to replicate data from Salesforce to Snowflake.

## Use cases

Use the Openflow Connector for Salesforce Bulk API to replicate standard or custom objects from Salesforce to Snowflake at a user-specified frequency and keep them up to date in Snowflake.

## Workflow

The following workflow describes the steps to set up and use the Openflow Connector for Salesforce Bulk API.

1. A Salesforce administrator creates and configures an external client app in Salesforce and approves it for a specific user.
2. The Openflow administrator performs the following tasks:

   1. Create a service user for the connector, a warehouse for the connector, and a destination database and schema to replicate into.
   2. Install the connector.
   3. Specify the required parameters for the flow template.
3. The data engineer runs the flow to replicate objects from Salesforce to Snowflake.

## Limitations

Consider the following limitations when using the connector:

- Custom Salesforce domains are not supported.
- Traversing object relationships and fetching related objects is not supported.
- The connector does not support hard deletes in Snowflake. You can either run a
  query on the destination table to delete all rows where the `isDeleted` column is `true` or perform a full refresh of the destination table to reflect “hard deletes”.
- Fields of type `location` and `address` are not supported and are ignored.
- Fields of type `base64` (binary fields such as `Attachment.Body` and
  `ContentVersion.VersionData`) require a dedicated ingestion path. See
  [Configure blob field ingestion](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/configure-connector#blob-fields) for details.
- You cannot consolidate data from multiple Salesforce instances into a single database in Snowflake.
  Data from a single Salesforce instance or org is ingested into a single database in Snowflake. A table is created in this database for each Salesforce object replicated.
- Files attached to Salesforce records are ignored.
- Formula fields are not replicated as data from Salesforce. Instead, the connector
  can translate supported Salesforce formulas into Snowflake SQL views. See
  [Salesforce formula fields](#salesforce-formula-fields) for details on supported formulas and limitations.

## Authentication

The connector uses the OAuth 2.0 JWT Bearer Flow via an external client app to connect to Salesforce and to retrieve data. This is the only supported OAuth flow for the connector. Using a different OAuth flow type (such as Authorization Code Flow) or misconfiguring the external client app can result in `invalid_grant` errors.

See [Openflow Connector for Salesforce Bulk API: Set up Salesforce](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/setup-salesforce) for documentation on how to configure the external client app in Salesforce, and [Troubleshooting the Openflow Connector for Salesforce Bulk API](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/troubleshoot) for help with common authentication errors.

## Replication lifecycle

The connector replicates data in two stages: initial replication and incremental replication.

### Initial replication

The connector calls the Salesforce Bulk API 2.0 to discover standard and custom objects specified in the connector configuration. The connector respects Bulk API 2.0 API limits.

- The connector creates one table per custom or standard object with one column for each field.
- The connector uses Snowpipe Streaming v2 for the initial load to insert rows in the table based on the values of the fields from the Salesforce object.

### Incremental replication

Incremental updates use a Snowflake warehouse that can be configured in the connector parameters. Depending on your latency and data freshness requirements, you can configure the refresh frequency for updates from 1 minute to 24 hours, which determines how often the tables in Snowflake are refreshed.

Using the refresh frequency you specify, the connector calls the Salesforce Bulk API to detect changes in previously ingested objects. The connector identifies changed records by checking specific timestamp fields in the Salesforce objects.

For most objects, the connector uses the `SystemModstamp` field. If `SystemModstamp` is not available, the connector attempts to use the following fields, in order of preference:

1. `LastModifiedDate`
2. `CreatedDate`
3. `LoginTime`

Note

For history tables (objects where History Tracking is enabled), the connector always uses the `CreatedDate` field to detect changes.

The connector then uses Snowpipe Streaming v2 to push the incremental data into a staging table and executes a merge query to load the data into the final destination table.

## Schema evolution

The connector supports schema evolution when the source objects change in Salesforce.

When a new field is added to the source object:
:   The connector adds a new column to the destination table in Snowflake.

When an existing field is renamed in the source object:
:   The connector treats the rename as both a field deletion and a field addition. The field
    addition causes a new column to be added to the destination table. The field deletion
    is handled as described next.

When an existing field is deleted in the source object:
:   The connector supports three strategies:

    - Delete: Deletes the corresponding column in the destination table in Snowflake. This is the default behavior.
    - Ignore: Ignores the deleted field in the source and skips it in the future.
    - Rename: Renames the deleted field in the destination table.

For example, if the deletion strategy is set to `Ignore` and a field is renamed for a Salesforce object, the existing column in Snowflake will be unchanged and a new column with the new field name will be added.

## How objects are deleted

When objects are deleted in Salesforce, the connector does not “hard delete” them from Snowflake. The connector performs “soft deletes” for objects deleted in Salesforce and indicates that the source objects were deleted by setting the `isDeleted` column to `true` in the corresponding Snowflake tables.

The connector does not support “hard deletes”. You can either run a query on the destination table to delete all rows where the `isDeleted` column is `true` or perform a full refresh of the destination table to reflect “hard deletes”.

The connector may miss delete operations in situations where objects are deleted in Salesforce and purged from Salesforce’s recycling bin when the connector was not running, for example if the connector was paused or stopped. You must perform a full refresh of the destination table to recover in these situations.

## Automatic retry handling

The connector automatically retries failed operations or API errors using an exponential backoff strategy. The connector waits one second before the first retry, then doubles the wait time for each subsequent retry (two seconds, four seconds, and so on). If the failures persist, the connector stops retrying until the next scheduled run. You can monitor this activity in the [event table](/user-guide/data-integration/openflow/monitor).

## Use multiple connector instances to handle different sync schedules

If you need to sync different objects at different frequencies, for example some every 30 minutes and others every 24 hours, Snowflake recommends deploying two separate connector instances within the same runtime. You can then configure the sync parameters independently for each instance.

Note

Deploying multiple connector instances in the same runtime does not incur additional costs.

Similarly, if you need to fully fetch some objects every time the connector runs, Snowflake recommends deploying two separate connector instances within the same runtime and configuring the parameters for each instance.

## Salesforce formula fields

Salesforce formula fields are calculated fields whose values are derived from expressions defined in Salesforce. Because the Salesforce Bulk API does not support incremental retrieval of formula field values, the connector takes a different approach: it translates the Salesforce formula expressions into Snowflake SQL and creates a view for each object that contains formula fields.

To enable this feature, set the **Enable Views Creation** parameter to `true` in the connector configuration. See [Openflow Connector for Salesforce Bulk API: Configure the connector](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/configure-connector) for details.

For more information, see [Openflow Connector for Salesforce Bulk API: Salesforce formula fields](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/formula-fields).

## Next steps

For information on how to set up the connector, see the following topic:

- [Openflow Connector for Salesforce Bulk API: Set up Salesforce](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/setup-salesforce)
