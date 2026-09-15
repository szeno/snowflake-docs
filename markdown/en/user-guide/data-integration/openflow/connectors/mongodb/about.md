# About the Openflow Connector for MongoDB

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts of the Openflow Connector for MongoDB, its workflow, and limitations.

The Openflow Connector for MongoDB connects a MongoDB database to Snowflake and replicates data from selected
collections on a schedule. The connector performs an initial full load for each collection,
followed by incremental updates using MongoDB change streams.

## Use cases

The connector supports the following use cases:

Replication to Snowflake
:   Continuously mirror collections from MongoDB into Snowflake for downstream analytics and
    modeling. Incremental changes arrive on a schedule with a delay window of a few minutes.

Selective replication
:   Define which collections to include using names or regex filters for broad coverage with control.

Migration and change capture
:   Perform a one-time snapshot load for migrations, then run incremental syncs using MongoDB
    change streams to keep collections in sync.

## Limitations

The connector has the following limitations:

- Standalone MongoDB instances aren’t supported. The connector relies on the MongoDB oplog
  (operations log) to track changes. The MongoDB oplog is only available in a Replica Set or Sharded
  Cluster environment.
- The minimum supported version of MongoDB is version 4.4.
- The connector supports only username and password authentication with MongoDB.

## Snowflake table structure

The connector maps MongoDB documents to the corresponding Snowflake table. The entire payload
of the document is stored in the `data` field.

| Snowflake column | Description |
| --- | --- |
| id | ID of the MongoDB document |
| data | The payload of the document |

Expand

Show lessSee more

## Collection replication lifecycle

A collection’s replication cycle begins with an initial snapshot and transitions to incremental sync.

1. **Snowflake table creation:** The connector creates a table in Snowflake. The structure of the
   table is the same for each collection. For more information, see [Snowflake table structure](#label-mongodb-table-structure).
2. **Snapshot load:** After creating a table in Snowflake, the connector performs a full copy of
   all existing data from the MongoDB collection to the Snowflake table. This process runs
   sequentially for each collection in the configuration.
3. **Incremental sync:** After the initial load is complete, the collection enters incremental sync
   mode. The connector listens to the MongoDB change stream to read the journal document-level
   changes (inserts, updates, deletes) that accrued in the collection. These changes are then
   merged into the destination table in Snowflake.

## Openflow requirements

The runtime size must be at least Medium. Use Large for high-throughput workloads or for
replicating large collections.

- The connector doesn’t support multi-node Openflow runtimes. Configure the runtime for this connector with **Min nodes** and **Max nodes** set to `1`.

For information about creating a warehouse for the connector, see [Designate a warehouse](/user-guide/data-integration/openflow/connectors/mongodb/connect#label-designate-warehouse).

## Workflow

The workflow for the Openflow Connector for MongoDB involves steps performed by the MongoDB administrator and the Snowflake administrator.

### MongoDB administrator

The MongoDB administrator performs the following tasks:

1. Enable replication

   The MongoDB administrator configures a replica set or sharded cluster.
2. Ensure the oplog size is sufficient

   For high-volume data ingestion, the MongoDB administrator must ensure the `oplogSizeMB` is
   sufficiently large to retain the history of changes during the connector or connectivity
   downtime. If the connector is offline for longer than the Oplog’s retention period, the
   full re-sync of data might be required.

   Copy code

   ```
   replication:
     replSetName: "myReplicaSet"
     oplogSizeMB: 51200
   ```
3. Create a database user

   The MongoDB administrator creates a user with the necessary roles to monitor changes in the database.
   The user requires the `readAnyDatabase` role on the `admin` database.
4. Configure network access

   The MongoDB administrator configures network access from MongoDB to the Openflow Runtime.

### Snowflake administrator

The Snowflake administrator performs the following tasks:

1. Create a service user, a warehouse, and a destination database

   The administrator creates the necessary Snowflake objects for the replicated data.
2. Import the connector definition file

   The administrator imports the file into the Snowflake Openflow canvas.
3. Configure the flow

   The administrator configures the flow with the necessary MongoDB and Snowflake parameters.
4. Run the flow

   The administrator runs the flow.

## Next steps

For information about configuring the source MongoDB database and the target Snowflake account, see [Connect to MongoDB](/user-guide/data-integration/openflow/connectors/mongodb/connect).
