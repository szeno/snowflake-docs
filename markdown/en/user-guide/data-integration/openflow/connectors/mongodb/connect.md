# Connect to MongoDB

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes how to configure the source MongoDB database and the target
Snowflake account for the Openflow Connector for MongoDB.

## Set up the source MongoDB database

The connector requires a MongoDB deployment running as either a Replica Set or a
Sharded Cluster. This architecture ensures high availability and enables the use
of Change Streams, which the connector uses to track and sync data changes in
real time.

To configure the MongoDB environment, perform the following steps:

1. Configure a basic Replica Set.

   Ensure all nodes have the same `replSetName` in their `mongod.conf` as shown in the following example:

   Copy code

   ```
   replication:
     replSetName: "myReplicaSet"
   ```
2. Initialize the replica set.

   Run this command in the `mongosh` console. In this example, the replica set
   consists of two nodes:

   Copy code

   ```
   rs.initiate({
     _id: "myReplicaSet",
     members: [
       {
         _id: 0,
         host: "10.11.98.246:27017",
       },
       {
         _id: 1,
         host: "10.11.104.58:27017",
       },
     ],
   });
   ```
3. Create a dedicated database user.

   The connector opens a cluster-level Change Stream, which requires the
   `readAnyDatabase` role on the `admin` database. Create the user with the
   following role by running the following command in the `mongosh` console:

   Copy code

   ```
   use admin
   db.createUser(
     {
    user: "openflowUser",
    pwd: "yourSecurePassword",
    roles: [
      {
        role: "readAnyDatabase",
        db: "admin"
      }
    ]
     }
   );
   ```

   Note

   The `readAnyDatabase` role is required because the connector currently monitors
   change events at the cluster level. Database-scoped Change Stream support, which
   would allow a narrower `read` role on a specific database, is not currently supported.

   When configuring the connector, set **MongoDB Authentication Source** to `admin`.
   For more information, see [MongoDB source parameters](setup#label-mongodb-source-parameters).

## Set up the target Snowflake account

To set up the target Snowflake account, perform the following steps:

1. Create a Snowflake user.

   Create a Snowflake user with the type as SERVICE.

   Copy code

   ```
   USE ROLE USERADMIN;
   CREATE USER <openflow_service_user>
     TYPE=SERVICE
     COMMENT='Service user for Openflow automation';
   ```

   Store the private key for that user in a file to supply to the connector’s
   configuration. For more information, see [key-pair authentication](/user-guide/key-pair-auth).

   Copy code

   ```
   ALTER USER <openflow_service_user> SET RSA_PUBLIC_KEY = '<pubkey>';
   ```
2. Create a database.

   Create a database that stores the replicated data, and set up
   permissions for the Snowflake user to create objects in that database by
   granting USAGE and CREATE SCHEMA privileges.

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   CREATE DATABASE IF NOT EXISTS <destination_database>;
   GRANT USAGE ON DATABASE <destination_database> TO USER <openflow_service_user>;
   GRANT CREATE SCHEMA ON DATABASE <destination_database> TO USER <openflow_service_user>;
   ```
3. Create a new warehouse or use an existing warehouse for the connector.

   To create a new warehouse, perform the following steps:

> Copy code
>
> ```
> CREATE WAREHOUSE <openflow_warehouse>
> WITH
> WAREHOUSE_SIZE = 'MEDIUM'
> AUTO_SUSPEND = 300
> AUTO_RESUME = TRUE;
> GRANT USAGE, OPERATE ON WAREHOUSE <openflow_warehouse> TO USER <openflow_service_user>;
> ```

- Start with the MEDIUM warehouse size, then experiment with size depending on the
  number of tables being replicated and the amount of data transferred.
- To determine if you should increase, monitor the connector and database while data
  replication is in progress. If you observe significant delays during incremental
  replication, experiment with a larger warehouse size. However, large table numbers
  typically scale better using [multi-cluster warehouses](/user-guide/warehouses-multicluster)
  instead of increasing the warehouse size.

## Next steps

After setting up the source MongoDB database and the target Snowflake account,
[Set up the connector](/user-guide/data-integration/openflow/connectors/mongodb/setup).
