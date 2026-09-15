# Configure disaster recovery

Feature — Generally Available

The Snowflake Connector for ServiceNow® is generally available on supported cloud platforms.

The Snowflake Connector for ServiceNow® can be configured to use a second instance to support disaster recovery.

## About Snowflake Connector for ServiceNow® disaster recovery support

The Snowflake Connector for ServiceNow® stores metadata about configured tables and its own configuration within the application instance.
When the application is dropped or becomes corrupted, this internal state is lost.
To prevent this, the connector exports the metadata to the destination database alongside the ingested data during specific events, such as:

- Scheduling a new ingestion
- Finalizing the reload
- Cancelling the reload

The export process creates several tables in the destination schema to store the connector’s internal state.
These tables do not contain the ingested data but are essential for recovering the connector’s state after the application
is dropped or becomes corrupted. When replicated, these tables can also be used to recover the state of the connector on a different Snowflake account.
The following tables are created by the export process:

- `APP_CONFIG_SFSDKEXPORT_V1`
- `APP_STATE_SFSDKEXPORT_V1`
- `CONNECTOR_ERRORS_LOG_SFSDKEXPORT_V1`
- `INGESTION_PROCESS_SFSDKEXPORT_V1`
- `INGESTION_RUN_SFSDKEXPORT_V1`
- `NOTIFICATIONS_STATE_SFSDKEXPORT_V1`
- `RESOURCE_INGESTION_DEFINITION_SFSDKEXPORT_V1`
- `__CONNECTOR_STATE_EXPORT`

## Importing existing data and reports to a new instance of the connector

If the Snowflake Connector for ServiceNow® has been uninstalled or corrupted, it is possible to resume ingestion of previously configured tables, provided that the destination
database was not dropped. The metadata for tables configured in the connector is saved in the destination database alongside the ingested data.

To continue ingesting data after installing a new connector instance, perform the following:

1. Configure the connector

   Configure the connector by following the instructions in [Install and configure the connector with Snowsight](/connectors/servicenow/installing-snowsight) or [Install and configure the connector with SQL commands](/connectors/servicenow/installing-sql).
   When choosing the destination database and schema, select the existing schema that contains data ingested by the previous instance of the connector.
2. Grant required privileges to the connector

   Note

   This step is only required if you installed and configured the connector using SQL commands.
   If you installed the connector using Snowsight you can skip this step.

   Execute the following command to ensure that the newly installed connector becomes the owner of all objects in the existing schema:

   Copy code

   ```
   system$grant_ownership_to_application('your_application_instance', true, '<database>', '<schema>');
   ```

   Where `<database>` and `<schema>` are the names of the existing database and schema, respectively.
3. Pause the connector

   Copy code

   ```
   call pause_connector();
   ```
4. Import the existing data and table configuration

   Import the existing data and table configuration by executing the following command from the context of installed application:

   Copy code

   ```
   call import_state(force => true);
   ```

   The **force** parameter is set to **true** to ensure that any changes that might have been made to the freshly installed connector
   are overwritten with the table configuration and internal data from the old installation.
5. Resume the Connector

   Copy code

   ```
   call resume_connector();
   ```

At this point, the new instance of the Snowflake Connector for ServiceNow® connector should resume ingestion of the existing tables.

## Replicating the destination database and connector state to another snowflake deployment

This section describes the steps to replicate the content of the destination database.
The destination database contains the ingested data and the metadata for the tables configured in the connector.
If the connector or the data downloaded by the connector is critical for your business, consider setting up a secondary Snowflake account in a different region
and replicating the destination database to the secondary account.

### Terms and definitions

The following terms and definitions are used during the disaster recovery configuration process.

Destination Database
:   The database configured as the target for the data ingested by the connector. This is also the database where the connector’s internal state is exported to.

Destination Schema
:   The schema configured as the target for the data ingested by the connector.

Internal State
:   The internal data and configuration of the connector, for example table configurations, ingestion state, and error logs.

Connector instance
:   The Snowflake Connector for ServiceNow® connector instance installed on the Snowflake account.

ACCOUNT\_PRIM
:   Example name of primary account

ACCOUNT\_SEC
:   Example name of secondary (replica) account

APP\_PRIM
:   Example Snowflake Connector for ServiceNow® connector instance name installed on the primary account

APP\_SEC
:   Example Snowflake Connector for ServiceNow® connector instance name installed on the secondary account

DST\_DB.DST\_SCHEMA
:   Example destination schema name for the connector instance (where data is ingested and the connector’s internal state is saved)

DST\_DB
:   Example destination database name configured for the connector

MYORG
:   Example name of your organization (both accounts must be in the same organization)

### Introduction

When installed on your account, the Snowflake Connector for ServiceNow® connector (connector instance) appears as a normal database that contain data, procedures etc.
However, it cannot be replicated to a secondary account in the same way as a normal database.
Currently, there is no native mechanism to replicate the connector instance with its internal state to a replica account.
Specifically, the installed application cannot be added to a replication group.

Instead of replicating the connector instance directly, the connector exports the metadata of configured tables to the destination schema
configured during the connector setup process. The state is saved there and can be replicated alongside the ingested data.

For example, if you configured the connector to ingest data into the destination schema DST\_DB.DST\_SCHEMA,
the connector automatically saves its internal state to this schema.
You can then replicate both the ingested data and the internal state using the following command:

Copy code

```
create replication group connector_dest_database_group
  object_types = databases
  allowed_databases = dst_db
  allowed_accounts = ...;
```

### Setting up replication of ingested data and configured reports

Caution

Always test your disaster recovery procedures to verify that data and state replication are functioning as expected.

Before proceeding, familiarize yourself with [Snowflake Replication](/user-guide/account-replication-intro).

The following sections contain instructions applicable to all versions of Snowflake.

1. Installing the connector on the primary account

   Install and configure Snowflake Connector for ServiceNow® on the primary account. For detailed instructions, see [Install and configure the connector with Snowsight](/connectors/servicenow/installing-snowsight) or [Install and configure the connector with SQL commands](/connectors/servicenow/installing-sql).

   On the primary account, create a replication group and add DST\_DB as an allowed database:

   Copy code

   ```
   -- on primary account
   create replication group connector_rep_group_prim
     object_types = databases
     allowed_databases = dst_db
     allowed_accounts = myorg.account_sec
     replication_schedule = '10 minute';
   ```
2. Setting up replication on the secondary account

   To replicate DST\_DB from the primary account to the secondary account, create a new replication group on the secondary account:

   Copy code

   ```
   -- on secondary account
   create replication group connector_rep_group_sec
     as replica of myorg.account_prim.connector_rep_group_prim;

   alter replication group connector_rep_group_sec refresh;
   ```

   At this point, a read-only DST\_DB database should be created on the secondary account, and data from the primary account
   will be replicated according to the configured schedule.
3. Install the connector on the secondary account

   Install and configure Snowflake Connector for ServiceNow® on the secondary account in the same way as on the primary account.
   Point the instance to ingest data into the replicated database and schema.
   While replication is ongoing (until the replication group on the secondary account is dropped),
   the database is in read-only mode. The connector can be configured to use a read-only database as the ingestion target;
   however, it cannot ingest data until the database transitions to read-write mode.

   After configuring the connector on the secondary account, pause the connector by executing:

   Copy code

   ```
   -- on secondary account
   call pause_connector();
   ```

   At this point, the connector is installed and ready to take over if the primary account fails.

### Recovery procedure

When the primary deployment becomes unavailable, configure the connector instance on the secondary account to continue ingestion.

Important

All steps must be executed on the secondary account.

1. Drop the replication group

   Drop the replication group on the secondary account to transition the replicated database to read-write mode:

   Copy code

   ```
   drop replication group connector_rep_group_sec;
   ```
2. Grant ownership of existing database objects to the connector

   Grant ownership of all objects in the replicated schema to the connector by executing:

   Copy code

   ```
   call system$grant_ownership_to_application('app_sec', true, 'dst_db', 'dst_schema');
   ```
3. Import the state

   Initialize the connector with the state replicated from the primary account:

   Copy code

   ```
   call import_state(true);
   ```
4. Resume the connector

   Resume the connector by executing:

   Copy code

   ```
   call resume_connector();
   ```

   At this point, the connector on the secondary account should resume data ingestion, continuing from where the connector on primary account left off.

   Note

   Ensure that both the primary and secondary accounts are part of the same organization. The replication schedule can be adjusted based on your requirements.
