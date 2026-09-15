# Disaster recovery

The GAAD connector stores metadata about configured reports and its own configuration within the application instance.
When the application is dropped or becomes corrupted, this internal state is lost.
To prevent this, the connector exports the metadata to the destination database alongside the ingested data during specific events, such as the following:

> - Configuring a new report
> - Deleting a report
> - Fetching new batches of data from Google Analytics
> - Changing the fetch page size for a report

The export process creates several tables in the destination schema to store the connector’s internal state.
These tables do not contain the ingested data but are essential for recovering the connector’s state after the application
is dropped or becomes corrupted. When replicated, these tables can also be used to recover the state of the connector on a different Snowflake account.
The following tables are created by the export process:

> - `APP_CONFIG_SFSDKEXPORT_V1`
> - `APP_STATE_SFSDKEXPORT_V1`
> - `CONNECTOR_ERRORS_LOG_SFSDKEXPORT_V1`
> - `INGESTION_PROCESS_SFSDKEXPORT_V1`
> - `INGESTION_RUN_SFSDKEXPORT_V1`
> - `NOTIFICATIONS_STATE_SFSDKEXPORT_V1`
> - `RESOURCE_INGESTION_DEFINITION_SFSDKEXPORT_V1`

## Importing existing data and reports to a new instance of the connector.

If the GAAD connector has been uninstalled or corrupted, it is possible to resume ingestion of previously configured reports, provided that the destination
database was not dropped. The metadata for reports configured in the connector is saved in the destination database alongside the ingested data.
To continue ingesting data after installing a new connector instance, follow these steps:

1. Configure the connector.

   Configure the connector by following the instructions in [Install and configure the](/connectors/google/gaad/gaad-connector-installing) .
   When choosing the destination database and schema, select the existing schema that contains data ingested by the previous instance of the connector.
2. Grant required privileges to the connector.

   Note

   This step is not required if you installed and configured the new connector using Snowsight. Execute it only if you installed the connector using SQL commands.

   Execute the following command to ensure that the newly installed GAAD connector becomes the owner of all objects in the existing schema:

   Copy code

   ```
   system$grant_ownership_to_application('your_application_instance', true, 'database', 'schema');
   ```

   Where **database** and **schema** are the names of the existing database and schema, respectively.
3. Pause the connector.

   Copy code

   ```
   call pause_connector();
   ```
4. Import the existing data and reports.

   Import the existing data and reports by executing the following command from the context of installed application:

   Copy code

   ```
   call import_state(force => true);
   ```

   The **force** parameter is set to **true** to ensure that any changes that might have been made to the freshly installed connector
   are overwritten with the reports and internal data from the old installation.
5. Resume the Connector

   Copy code

   ```
   call resume_connector();
   ```

At this point, the new instance of the connector should resume ingestion of the existing reports.

## Replicating the destination database and connector state to another snowflake deployment

This section describes the steps to replicate the content of the destination database.
The destination database contains the ingested data and the metadata for the reports configured in the connector.
If the connector or the data downloaded by the GAAD connector is critical for your business, consider setting up a secondary Snowflake account in a different region
and replicating the destination database to the secondary account.

### Terms and definitions

> - **Destination Database** - the database configured as the target for the data ingested by the GAAD connector. This is also the database where the connector’s internal state is exported to.
> - **Sink Database** - the schema configured as the target for the data ingested by the GAAD connector.
> - **Internal State** - the internal data and configuration of the GAAD connector, for example report configurations, ingestion state, and error logs.
> - **GAAD instance** - the connector instance installed on the Snowflake account.
> - **GAAD** -
> - **ACCOUNT\_PRIM** - example name of primary account
> - **ACCOUNT\_SEC** - example name of secondary (replica) account
> - **APP\_PRIM** - example connector instance name installed on the primary account
> - **APP\_SEC** - example connector instance name installed on the secondary account
> - **DST\_DB.DST\_SCHEMA** - example destination schema name for the GAAD instance (where data is ingested and the connector’s internal state is saved)
> - **DST\_DB** - example destination database name configured for the GAAD connector
> - **MYORG** - example name of your organization (both accounts must be in the same organization)

### Introduction

When installed on your account, the connector (GAAD instance) appears as a regular database that contain data, procedures etc.
However, it cannot be replicated to a secondary account in the same way as a regular database.
Currently, there is no native mechanism to replicate the GAAD instance with its internal state to a replica account.
Specifically, the installed application cannot be added to a replication group.

Instead of replicating the GAAD instance directly, the connector exports the metadata for configured reports to the destination schema configured during the connector setup process.
The state is saved there and can be replicated alongside the ingested data.

For example, if you configured the connector to ingest data into the destination schema DEST\_DATABASE.PUBLIC,
the connector automatically saves its internal state to this schema.
You can then replicate both the ingested data and the internal state using the following command:

> Copy code
>
> ```
> create replication group gaad_dest_database_group
>   object_types = databases
>   allowed_databases = dst_db
>   allowed_accounts = ...;
> ```

### Setting up replication of ingested data and configured reports

> Note
>
> Always test your disaster recovery procedures to verify that data and state replication are functioning as expected.
>
> Note
>
> The following sections contain instructions applicable to all versions of Snowflake.
>
> Note
>
> Before proceeding, familiarize yourself with Snowflake Replication <https://docs.snowflake.com/en/user-guide/account-replication-intro>

1. **Installing GAAD on the primary account**

   Install and configure on the primary account. For detailed instructions, see [Install and configure the](/connectors/google/gaad/gaad-connector-installing) .

   On the primary account, create a replication group and add DST\_DB as an allowed database:

   Copy code

   ```
   -- on primary account
   create replication group gaad_rep_group_prim
     object_types = databases
     allowed_databases = dst_db
     allowed_accounts = myorg.account_sec
     replication_schedule = '10 minute';
   ```
2. **Setting up replication on the secondary account**

   To replicate DST\_DB from the primary account to the secondary account, create a new replication group on the secondary account:

   Copy code

   ```
   -- on secondary account
   create replication group gaad_rep_group_sec
     as replica of myorg.account_prim.gaad_rep_group_prim;

   alter replication group gaad_rep_group_sec refresh;
   ```

   At this point, a read-only DST\_DB database should be created on the secondary account, and data from the primary account
   will be replicated according to the configured schedule.
3. **Installing GAAD on the secondary account**

   Install and configure on the secondary account in the same way as on the primary account.
   Point the instance to ingest data into the replicated database and schema.
   While replication is ongoing (until the replication group on the secondary account is dropped),
   the database is in read-only mode. GAAD can be configured to use a read-only database as the ingestion target;
   however, it cannot ingest data until the database transitions to read-write mode.

   After configuring the connector on the secondary account, pause the connector by executing:

   Copy code

   ```
   -- on secondary account
   call pause_connector();
   ```

   At this point, the GAAD connector is installed and ready to take over if the primary account fails.

### Recovery procedure

When the primary deployment becomes unavailable, configure GAAD instance on the secondary account to continue ingestion.

> Note
>
> All steps must be executed on the secondary account.

1. **Drop the replication group**

   Drop the replication group on the secondary account to transition the replicated database to read-write mode:

   Copy code

   ```
   drop replication group gaad_rep_group_sec;
   ```
2. **Grant ownership of existing database objects to the connector**

   Grant ownership of all objects in the replicated schema to the GAAD connector by executing:

   Copy code

   ```
   call system$grant_ownership_to_application('app_sec', true, 'dst_db', 'dst_schema');
   ```
3. **Import the state**

   Initialize the connector with the state replicated from the primary account:

   Copy code

   ```
   call import_state(false);
   ```
4. **Resume the connector**

   Resume the connector by executing:

   Copy code

   ```
   call resume_connector();
   ```

   At this point, the GAAD connector on the secondary account should resume data ingestion, continuing from where the GAAD on primary account left off.

   > Note
   >
   > Ensure that both the primary and secondary accounts are part of the same organization. The replication schedule can be adjusted based on your requirements.
