# Set up the Openflow Connector for SQL Server (CDC)

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes how to set up the Openflow Connector for SQL Server (CDC).

For information on the incremental load process, see [Incremental replication](/user-guide/data-integration/openflow/connectors/sql-server-cdc/incremental-replication).

## Prerequisites

Before setting up the connector, ensure that you have completed the following prerequisites:

1. Ensure that you have reviewed [About Openflow Connector for SQL Server (CDC)](/user-guide/data-integration/openflow/connectors/sql-server-cdc/about).
2. Ensure that you have reviewed [Supported SQL Server versions](/user-guide/data-integration/openflow/connectors/sql-server-cdc/about#label-sql-server-cdc-versions).
3. Ensure that you have set up your runtime deployment. For more information, see the following topics:

   - [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs)
   - [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc).
4. If you use Openflow - Snowflake Deployments, ensure that you have reviewed
   [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list) and have granted access to the required domains for the [SQL Server](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-sqlserver) connector.

## Set up your SQL Server instance

Before setting up the connector, perform the following tasks in your SQL Server environment:

Note

You must perform these tasks as a database administrator.

1. Enable Change Data Capture on the
   [databases](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/enable-and-disable-change-data-capture-sql-server)
   and tables that you plan to replicate:

   Copy code

   ```
   USE <database>;
   EXEC sys.sp_cdc_enable_db;

   EXEC sys.sp_cdc_enable_table
     @source_schema = N'<schema>',
     @source_name = N'<table>',
     @role_name = NULL;
   ```

   Note

   Run the `sp_cdc_enable_table` procedure for every table that you plan to replicate.
   Run `sp_cdc_enable_db` once per database.

   The connector requires that CDC is enabled on the databases and tables before replication
   starts. You can also enable CDC on additional tables while the connector is running.

   Note

   **Platform-specific variants for enabling CDC at the database level.** The
   `sp_cdc_enable_table` call shown above is the same on every platform; only the
   database-level enable procedure differs.

   - **AWS RDS for SQL Server.** You can’t call `sys.sp_cdc_enable_db` directly on RDS
     because RDS doesn’t expose the `sysadmin` server role. Use the RDS-provided wrapper
     instead:

     Copy code

     ```
     EXEC msdb.dbo.rds_cdc_enable_db '<database>';
     ```

     See [Using change data capture for Amazon RDS for SQL Server](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.SQLServer.CommonDBATasks.CDC.html).
     CDC isn’t supported on the Web edition of RDS for SQL Server.
   - **Google Cloud SQL for SQL Server.** You can’t call `sys.sp_cdc_enable_db` directly.
     Use the Cloud SQL-provided wrapper instead:

     Copy code

     ```
     EXEC msdb.dbo.gcloudsql_cdc_enable_db '<database>';
     ```

     See [Enable change data capture (CDC) on Cloud SQL for SQL Server](https://cloud.google.com/sql/docs/sqlserver/replication/enable-cdc). Cloud SQL for
     SQL Server currently offers SQL Server 2017, 2019, and 2022 only.
   - **Azure SQL Database (single database).** Use the standard `sys.sp_cdc_enable_db`
     procedure. On the DTU-based purchasing model, CDC requires the S3 service tier or
     higher (CDC isn’t supported on Basic, S0, S1, or S2). On the vCore-based purchasing
     model, CDC is supported on any tier. See
     [Change data capture with Azure SQL Database](https://learn.microsoft.com/en-us/azure/azure-sql/database/change-data-capture-overview?view=azuresql).
   - **Azure SQL Managed Instance.** Use the standard `sys.sp_cdc_enable_db` procedure.
     Enabling CDC requires membership in the `sysadmin` server role.

   **Raise max text repl size for large LOB columns**

   If replicated tables contain LOB columns (such as `VARCHAR(MAX)`, `NVARCHAR(MAX)`, or `VARBINARY(MAX)`) with values larger than 64 KB, raise the SQL Server `max text repl size` setting on the source instance. SQL Server CDC defaults this setting to 65536 bytes (64 KB), which is lower than the connector’s 16 MB per-value limit. Without raising it, replication can fail with an error such as the following:

   > *Length of LOB data (N) to be replicated exceeds configured maximum 65536. Use the stored procedure sp\_configure to increase the configured maximum value for max text repl size option.*

   Set the value based on the largest LOB sizes in your source data. It must be at least as large as the biggest value SQL Server CDC needs to replicate, including when **Oversized Value Strategy** is set to **Set Null** (the connector still reads the full value before replacing it with `NULL`).

   Warning

   Raising `max text repl size` allows SQL Server CDC to capture larger LOB values, but those values are written to the transaction log and copied into CDC change tables. Capturing very large values can increase transaction log generation, storage consumption, and latency in CDC capture and cleanup jobs. Set the limit to match the LOB sizes you actually need rather than the maximum, unless you require that headroom.

   How you change this setting depends on your platform:

   - **On-premises SQL Server, Azure SQL Managed Instance, and Google Cloud SQL for SQL Server.** Use `sp_configure`. The example below sets the maximum allowed value of `2147483647` (~2 GB):

     Copy code

     ```
     EXEC sp_configure 'show advanced options', 1;
     RECONFIGURE;
     EXEC sp_configure 'max text repl size', 2147483647;
     RECONFIGURE;
     ```

     For more information, see [Configure the max text repl size server configuration option](https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/configure-the-max-text-repl-size-server-configuration-option).
   - **AWS RDS for SQL Server.** You can’t change this setting with `sp_configure` or `msdb.dbo.rds_set_configuration`. Configure it through an RDS DB parameter group instead:

     1. Create a custom DB parameter group for your SQL Server version family (for example, `sqlserver-se-16.0`):

        Copy code

        ```
        aws rds create-db-parameter-group \
          --db-parameter-group-name <name> \
          --db-parameter-group-family sqlserver-se-16.0 \
          --description "Custom SQL Server params"
        ```
     2. Set `max text repl size (b)` (note the exact parameter name, including `(b)` in lowercase). The example below uses `2147483647` (~2 GB), the maximum allowed value:

        Copy code

        ```
        aws rds modify-db-parameter-group \
          --db-parameter-group-name <name> \
          --parameters "ParameterName='max text repl size (b)',ParameterValue=2147483647,ApplyMethod=immediate"
        ```
     3. Attach the parameter group to the RDS instance:

        Copy code

        ```
        aws rds modify-db-instance \
          --db-instance-identifier <instance-id> \
          --db-parameter-group-name <name> \
          --apply-immediately
        ```
     4. Reboot the RDS instance. This parameter requires a reboot to take effect on RDS for SQL Server.
   - **Azure SQL Database (single database).** Open a query window connected to the specific database and run:

     Copy code

     ```
     EXEC sp_configure 'max text repl size', 2147483647;
     RECONFIGURE;
     ```

     A value of `-1` is also supported and removes the size limit other than the limit imposed by the column data type.
2. Create a login for the SQL Server instance:

   Copy code

   ```
   CREATE LOGIN <user_name> WITH PASSWORD = '<password>';
   ```

   This login is used to create users for the databases you plan to replicate.
3. Create a user for each database you are replicating by running the following
   SQL Server command in each database:

   Copy code

   ```
   USE <source_database>;
   CREATE USER <user_name> FOR LOGIN <user_name>;
   ```
4. Grant the required permissions to the user for each database that you are replicating.

   Add the user to the `db_datareader` role and grant SELECT on the `cdc` schema so the
   connector can read both the source tables and the CDC change tables:

   Copy code

   ```
   ALTER ROLE db_datareader ADD MEMBER <user_name>;
   GRANT SELECT ON SCHEMA::cdc TO <user_name>;
   ```

   Run these commands in each database that you plan to replicate.

   Note

   These permissions give the connector read access to every user table in the database.
   To scope access more tightly, grant `SELECT` only on the specific tables being
   replicated and on `SCHEMA::cdc` instead of adding the user to the `db_datareader` role.

   Note

   **Azure SQL Database (single database) only — database owner before deploying wrapper scripts.** The wrapper procedures use `EXECUTE AS OWNER`. If the database owner is a Microsoft Entra ID principal (common after importing a database from a `.bacpac` file) and the connector authenticates with SQL Server authentication, calls to `dbo.sf_openflow_cdc_enable_table` and `dbo.sf_openflow_cdc_disable_table` fail with an error such as `Only active directory users can impersonate other active directory users` (error 33171). The connector does not receive extra privileges from this step; it only changes who owns the database.

   Before deploying the Openflow CDC wrapper scripts in step 5, connect to each replicated database as the server administrator and run:

   Copy code

   ```
   ALTER AUTHORIZATION ON DATABASE::[<database>] TO [<sql_server_admin_login>];
   ```

   Use the SQL Server authentication login that administers the logical server (for example, the login you specified when you created the server), not the connector login.
5. Deploy the Openflow CDC wrapper procedures so the connector can rotate capture instances when supported schema changes occur. For deployment instructions, see [Deploy the Openflow CDC wrapper procedures](#label-sql-server-cdc-wrapper-procedures). If permissions or internal policy blocks deployment, see [When the wrapper procedures aren’t deployed](/user-guide/data-integration/openflow/connectors/sql-server-cdc/about#label-sql-server-cdc-wrapper-procedures-missing).
6. (Optional) Grant the VIEW DEFINITION privilege on the User Defined Data Types (UDDT).

   If your tables contain columns that use User Defined Data Types (UDDT), and the UDDT is owned by
   a different user than the connector user, you must grant the VIEW DEFINITION permission
   to the connector user as shown in the following SQL Server example:

   Copy code

   ```
   GRANT VIEW DEFINITION TO <user_name>;
   ```

   Without this permission, columns using UDDT are silently excluded from replication.
7. (Optional) Configure SSL connection.

   If you use an SSL connection to connect SQL Server, create the root certificate for your database
   server. This is required when configuring the connector.

## Deploy the Openflow CDC wrapper procedures

Note

Deploy these procedures during connector setup (step 5). Without them, replication runs normally until a supported schema change occurs; at that point a DBA must run the SQL from the WARN bulletin on the **MultiDatabaseCaptureChangeCdcSqlServer** processor for each change. Only take that path when permissions or internal policy blocks deployment. For what to look for, see [When the wrapper procedures aren’t deployed](/user-guide/data-integration/openflow/connectors/sql-server-cdc/about#label-sql-server-cdc-wrapper-procedures-missing).

The connector applies supported source table schema changes (DDL) without stopping replication or
requiring a manual re-snapshot. To do this, the connector manages SQL Server capture instances
autonomously: when a tracked table’s schema changes, the connector creates a new capture instance for
the updated schema and drops the old one after it finishes the transition. For an overview of the
process, see [Schema changes](/user-guide/data-integration/openflow/connectors/sql-server-cdc/about#label-sql-server-cdc-schema-changes).

Creating and dropping capture instances normally requires `db_owner`. Rather than granting the
connector that level of access, deploy a small set of wrapper procedures that perform these
operations on the connector’s behalf and grant the connector permission to run only those two
procedures.

This design has the following properties:

- **The connector can run only the two wrapper procedures.** For capture-instance management, the
  connector is granted `EXECUTE` on only `dbo.sf_openflow_cdc_enable_table` and
  `dbo.sf_openflow_cdc_disable_table`. It doesn’t hold `db_owner` and can’t call the underlying
  `sys.sp_cdc_enable_table` or `sys.sp_cdc_disable_table` procedures directly. The wrapper procedures
  run with `EXECUTE AS OWNER`, so they supply the elevated privileges only for the specific,
  audited operation.
- **Every operation is recorded in an audit table.** Each invocation of a wrapper procedure writes an
  `attempt` row to the `dbo.openflow_cdc_audit` table before it calls the engine, then a `success` or
  `failure` row (including the SQL Server error number and message on failure) after the call. The
  rows are append-only: the wrappers never update or delete audit rows.

Deploy the procedures as a database administrator. Run the following scripts, in order, in each
CDC-enabled database being replicated. Run them as a principal that already holds
`db_owner`.

Note

Perform these tasks as a database administrator, after creating the connector’s database
user as described in [Set up your SQL Server instance](#label-sql-server-cdc-connector-setup-instance).

1. **`openflow_cdc_audit_setup.sql`**: Creates the append-only `dbo.openflow_cdc_audit` table that the
   wrapper procedures write to.

   Copy code

   ```
   SET NOCOUNT ON;

   -- Audit log. Each wrapper invocation writes one 'attempt' row before delegating to
   -- sys.sp_cdc_*, then either a 'success' or 'failure' row sharing the same attempt_id.
   -- Rows are append-only.
   IF OBJECT_ID(N'dbo.openflow_cdc_audit', N'U') IS NULL
   BEGIN
       CREATE TABLE dbo.openflow_cdc_audit (
           audit_id         bigint           IDENTITY(1,1) NOT NULL CONSTRAINT pk_openflow_cdc_audit PRIMARY KEY,
           attempt_id       uniqueidentifier NOT NULL,
           event_time       datetime2(3)     NOT NULL,
           event_kind       varchar(16)      NOT NULL,
           action           varchar(16)      NOT NULL,
           source_schema    sysname          NOT NULL,
           source_name      sysname          NOT NULL,
           capture_instance sysname          NOT NULL,
           caller           sysname          NOT NULL,
           error_number     int              NULL,
           error_message    nvarchar(4000)   NULL,
           CONSTRAINT ck_openflow_cdc_audit_event_kind CHECK (event_kind IN ('attempt', 'success', 'failure')),
           CONSTRAINT ck_openflow_cdc_audit_action     CHECK (action     IN ('enable',  'disable'))
       );

       CREATE INDEX ix_openflow_cdc_audit_attempt    ON dbo.openflow_cdc_audit(attempt_id);
       CREATE INDEX ix_openflow_cdc_audit_event_time ON dbo.openflow_cdc_audit(event_time);
   END;
   GO
   ```
2. **`sf_openflow_cdc_enable_table.sql`**: Creates the wrapper procedure that the connector calls to
   add a new capture instance during a schema transition.

   Copy code

   ```
   CREATE OR ALTER PROCEDURE dbo.sf_openflow_cdc_enable_table
       @source_schema    sysname,
       @source_name      sysname,
       @capture_instance sysname
   WITH EXECUTE AS OWNER
   AS
   BEGIN
       SET NOCOUNT ON;

       -- 1. Table must exist and not be a system table.
       IF OBJECT_ID(QUOTENAME(@source_schema) + N'.' + QUOTENAME(@source_name), N'U') IS NULL
           THROW 50001, 'Source table does not exist or is not a user table.', 1;

       -- 2. The connector supplies the full capture instance name. Validate that
       --    it is present and fits within the 100-character limit imposed by CDC.
       IF @capture_instance IS NULL OR LEN(@capture_instance) = 0
           THROW 50002, 'Capture instance name must be provided.', 1;

       IF LEN(@capture_instance) > 100
           THROW 50003, 'Capture instance name exceeds the 100-character limit.', 1;

       -- 3. Record the attempt.
       DECLARE @attempt_id uniqueidentifier = NEWID();
       DECLARE @caller     sysname          = ORIGINAL_LOGIN();

       INSERT INTO dbo.openflow_cdc_audit
           (attempt_id, event_time, event_kind, action, source_schema, source_name, capture_instance, caller)
       VALUES
           (@attempt_id, SYSUTCDATETIME(), 'attempt', 'enable',
            @source_schema, @source_name, @capture_instance, @caller);

       -- 4. Delegate to the engine procedure and record the outcome.
       BEGIN TRY
           EXEC sys.sp_cdc_enable_table
               @source_schema    = @source_schema,
               @source_name      = @source_name,
               @capture_instance = @capture_instance,
               @role_name        = NULL;

           INSERT INTO dbo.openflow_cdc_audit
               (attempt_id, event_time, event_kind, action, source_schema, source_name, capture_instance, caller)
           VALUES
               (@attempt_id, SYSUTCDATETIME(), 'success', 'enable',
                @source_schema, @source_name, @capture_instance, @caller);
       END TRY
       BEGIN CATCH
           DECLARE @err_num int            = ERROR_NUMBER();
           DECLARE @err_msg nvarchar(4000) = ERROR_MESSAGE();

           INSERT INTO dbo.openflow_cdc_audit
               (attempt_id, event_time, event_kind, action, source_schema, source_name,
                capture_instance, caller, error_number, error_message)
           VALUES
               (@attempt_id, SYSUTCDATETIME(), 'failure', 'enable',
                @source_schema, @source_name, @capture_instance, @caller,
                @err_num, @err_msg);

           ;THROW;
       END CATCH
   END;
   GO
   ```
3. **`sf_openflow_cdc_disable_table.sql`**: Creates the wrapper procedure that the connector calls to
   drop the old capture instance after a schema transition completes.

   Copy code

   ```
   CREATE OR ALTER PROCEDURE dbo.sf_openflow_cdc_disable_table
       @source_schema    sysname,
       @source_name      sysname,
       @capture_instance sysname
   WITH EXECUTE AS OWNER
   AS
   BEGIN
       SET NOCOUNT ON;

       -- 1. The connector supplies the full capture instance name. Validate that it is present.
       IF @capture_instance IS NULL OR LEN(@capture_instance) = 0
           THROW 50002, 'Capture instance name must be provided.', 1;

       -- 2. Record the attempt.
       DECLARE @attempt_id uniqueidentifier = NEWID();
       DECLARE @caller     sysname          = ORIGINAL_LOGIN();

       INSERT INTO dbo.openflow_cdc_audit
           (attempt_id, event_time, event_kind, action, source_schema, source_name, capture_instance, caller)
       VALUES
           (@attempt_id, SYSUTCDATETIME(), 'attempt', 'disable',
            @source_schema, @source_name, @capture_instance, @caller);

       -- 3. Delegate to the engine procedure and record the outcome.
       BEGIN TRY
           EXEC sys.sp_cdc_disable_table
               @source_schema    = @source_schema,
               @source_name      = @source_name,
               @capture_instance = @capture_instance;

           INSERT INTO dbo.openflow_cdc_audit
               (attempt_id, event_time, event_kind, action, source_schema, source_name, capture_instance, caller)
           VALUES
               (@attempt_id, SYSUTCDATETIME(), 'success', 'disable',
                @source_schema, @source_name, @capture_instance, @caller);
       END TRY
       BEGIN CATCH
           DECLARE @err_num int            = ERROR_NUMBER();
           DECLARE @err_msg nvarchar(4000) = ERROR_MESSAGE();

           INSERT INTO dbo.openflow_cdc_audit
               (attempt_id, event_time, event_kind, action, source_schema, source_name,
                capture_instance, caller, error_number, error_message)
           VALUES
               (@attempt_id, SYSUTCDATETIME(), 'failure', 'disable',
                @source_schema, @source_name, @capture_instance, @caller,
                @err_num, @err_msg);

           ;THROW;
       END CATCH
   END;
   GO
   ```
4. **`openflow_cdc_grants.sql`**: Grants the connector’s database user permission to run the two
   wrapper procedures and to read the CDC metadata, change tables, and audit trail. Replace
   `<user_name>` with the connector’s database user created in
   [Set up your SQL Server instance](#label-sql-server-cdc-connector-setup-instance), then run the script.

   Copy code

   ```
   SET NOCOUNT ON;

   -- Replace <user_name> with the connector's SQL Server database user.
   DECLARE @connector sysname = N'<user_name>';

   -- The principal must already exist in this database.
   IF DATABASE_PRINCIPAL_ID(@connector) IS NULL
       THROW 50100,
             'Connector principal does not exist in this database. Create the user first, then re-run this script.',
             1;

   DECLARE @sql nvarchar(max);

   -- 1. Allow the connector to call the two wrapper procedures. All CDC management
   --    goes through these wrappers, so no elevated role is required.
   SET @sql = N'GRANT EXECUTE ON dbo.sf_openflow_cdc_enable_table  TO ' + QUOTENAME(@connector);
   EXEC sys.sp_executesql @sql;

   SET @sql = N'GRANT EXECUTE ON dbo.sf_openflow_cdc_disable_table TO ' + QUOTENAME(@connector);
   EXEC sys.sp_executesql @sql;

   -- 2. Allow the connector to read its own audit trail.
   SET @sql = N'GRANT SELECT ON dbo.openflow_cdc_audit TO ' + QUOTENAME(@connector);
   EXEC sys.sp_executesql @sql;

   -- 3. Allow the connector to enumerate capture instances and read CDC change tables.
   SET @sql = N'GRANT SELECT ON SCHEMA::cdc TO ' + QUOTENAME(@connector);
   EXEC sys.sp_executesql @sql;
   GO
   ```

Note

The connector also needs `SELECT` on each replicated source table. SQL Server applies row-level
filtering to `cdc.change_tables` for callers that don’t hold `db_owner`, returning only rows for
source tables that the caller can read. The `db_datareader` role granted in
[Set up your SQL Server instance](#label-sql-server-cdc-connector-setup-instance) satisfies this requirement. If access was scoped
more tightly instead of using `db_datareader`, make sure the connector has `SELECT` on every source
table that it replicates.

5. **Verify the deployment.** Confirm that the two wrapper procedures exist and that the audit table
   is queryable:

   Copy code

   ```
   SELECT name FROM sys.procedures WHERE name LIKE 'sf_openflow%';
   SELECT TOP 1 1 FROM dbo.openflow_cdc_audit;
   ```

   The first query returns both `sf_openflow_cdc_enable_table` and `sf_openflow_cdc_disable_table`.
   The second query confirms that the audit table exists and is readable.

## Set up your Snowflake environment

As an Openflow administrator, perform the following tasks for this connector. With the
default `SNOWFLAKE_MANAGED` authentication strategy, the runtime’s execute-as role is the identity
the connector uses to access Snowflake, so you grant these privileges to that role.

Note

If you’re deploying the connector in Openflow - BYOC Deployments and using the `KEY_PAIR` authentication
strategy instead of the recommended `SNOWFLAKE_MANAGED`, you’ll also grant this same execute-as
role to a service user rather than relying on the runtime’s managed token. See
[Set up key-pair authentication for Openflow - BYOC Deployments](/user-guide/data-integration/openflow/setup-openflow-byoc-key-pair-auth)
to create the service user.

1. Create a database to store the replicated data, and grant the execute-as role
   [USAGE and CREATE SCHEMA](/user-guide/security-access-control-privileges#label-database-privileges) on it. The connector creates
   destination schemas automatically. Snowflake recommends a dedicated destination database per
   connector, to avoid collisions with other data sources including other connectors.

   Keep this destination database separate from the database that holds your Openflow
   infrastructure objects, such as the runtime, the connector, and any secrets. A connector
   creates destination objects based on the source schema and table names, so those names aren’t
   under your control and can change as the source changes.

   Copy code

   ```
   CREATE DATABASE IF NOT EXISTS <destination_database>;

   GRANT USAGE ON DATABASE <destination_database> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   GRANT CREATE SCHEMA ON DATABASE <destination_database> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```
2. Designate a warehouse for the connector to use, and grant the execute-as role **USAGE** and
   **OPERATE** on it. Start with the `XSMALL` warehouse size, then experiment with size depending
   on the number of tables being replicated, and the amount of data transferred. Large table
   numbers typically scale better with
   [multi-cluster warehouses](/user-guide/warehouses-multicluster), rather than the warehouse size.

   Copy code

   ```
   CREATE WAREHOUSE <ingest_warehouse>
     WITH
       WAREHOUSE_SIZE = 'XSMALL'
       AUTO_SUSPEND = 300
       AUTO_RESUME = TRUE;

   GRANT USAGE, OPERATE ON WAREHOUSE <ingest_warehouse> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```
3. **Snowflake deployments only:** Make sure this connector’s source host and port are permitted
   by a network rule that your runtime’s external access integration (EAI) allows.

   The EAI itself belongs to the runtime, not to this connector. You create it once, attach it to
   the runtime, and grant the execute-as role `USAGE` on it. For those steps, see
   [Creating network rules and external access integrations](/user-guide/data-integration/openflow/setup-openflow-spcs-create-rr#label-create-network-rules-and-external-access-integrations).
   What is specific to this connector is getting its source host into a rule that EAI references.

   The rule takes the source’s host and port as a single value, such as `db.example.com:<port>`.
   That’s the host and port from the connector’s connection URL, without the `jdbc:` scheme, the
   driver name, or the database path.

   BYOC deployments handle outbound connectivity in the cloud environment and don’t use EAIs or
   network rules.

## Install the connector

To install the connector, do the following as a data engineer:

1. Navigate to the **Connector library** tab in Openflow.
2. On the Openflow connectors page, find the connector and select **Install**.
3. In the **Select runtime** dialog, select your runtime from the **Available runtimes** drop-down list and click **Install**.

   Note

   Before you install the connector, ensure that you have created a database and schema in Snowflake for the connector to store ingested data.
4. Authenticate to the deployment with your Snowflake account credentials and select **Allow** when prompted to allow the runtime application to access your Snowflake account. The connector installation process takes a few minutes to complete.
5. Authenticate to the runtime with your Snowflake account credentials.

The Openflow canvas appears with the connector process group added to it.

## Runtime sizing

For sizing guidance, including node type tiers and how to resize after creation,
see [Runtime sizing and packing for CDC connectors](/user-guide/data-integration/openflow/connectors/cdc-runtime-sizing).

For migration instructions, see [Reinstall the connector](/user-guide/data-integration/openflow/connectors/sql-server-cdc/maintenance#label-sql-server-cdc-reinstall-connector).

## Configure the connector

To configure the connector, do the following as a data engineer:

1. Right-click on the imported process group and select **Parameters**.
2. Populate the required parameter values.

   For more information on the required parameter values, see the following sections:

   - [SQLServer Source Parameters](#label-of-sqlserver-cdc-source-parameters): Used to establish a connection with SQL Server.
   - [SQLServer Destination Parameters](#label-of-sqlserver-cdc-destination-parameters): Used to establish a connection with Snowflake.
   - [SQLServer Ingestion Parameters](#label-of-sqlserver-cdc-ingestion-parameters): Used to specify the tables to replicate.

Start by setting the parameters of the SQLServer Source Parameters context, then the SQLServer Destination Parameters context.
After you complete this, enable the connector. The connector connects to both SQL Server and Snowflake and starts running.
However, the connector doesn’t replicate any data until tables to be replicated are explicitly added to its configuration.

To configure specific tables for replication, edit the SQLServer Ingestion Parameters context. After you apply the changes to the
SQLServer Ingestion Parameters context, the configuration is picked up by the connector, and the replication lifecycle starts for every table.

To run multiple CDC connector instances on one runtime, see .

### SQLServer Source Parameters

| Parameter | Description |
| --- | --- |
| SQLServer Connection URL | The full JDBC URL used to connect to the source.  For a standalone SQL Server instance or Azure SQL Managed Instance, point the URL at the instance. The connector discovers the databases to replicate from that instance.   - `jdbc:sqlserver://example.com:1433;encrypt=false`   For Always On Availability Groups, see [Always On Availability Groups](#label-sql-server-availability-groups).  For Azure SQL Database, point the URL at a specific database using the `databaseName` property. Use one connector instance per database you want to replicate.   - `jdbc:sqlserver://your-server.database.windows.net:1433;encrypt=true;databaseName=your_database` |
| SQLServer JDBC Driver | Select the **Reference asset** checkbox to upload the [SQL Server JDBC driver](https://learn.microsoft.com/sql/connect/jdbc/download-microsoft-jdbc-driver-for-sql-server). |
| SQLServer Username | The username for the connector. |
| SQLServer Password | The password for the connector. |
| SQLServer Query Interval | The minimum time interval that must elapse before scheduling the next query for table changes. This controls the frequency of database polling during incremental replication to prevent excessive querying. Default: `10 sec`. |

Expand

Show lessSee more

Note

To connect with Windows authentication using NTLMv2, configure the SQL Server source parameters as follows:

- **SQLServer Connection URL**: `jdbc:sqlserver://<host>:1433;databaseName=<db>;integratedSecurity=true;authenticationScheme=NTLM;domain=<domain>;`
- **SQLServer JDBC Driver**: Upload the `mssql-jdbc` JAR. The driver class name is `com.microsoft.sqlserver.jdbc.SQLServerDriver`.
- **SQLServer Username**: Enter the domain user.
- **SQLServer Password**: Enter the domain password.

Note

Azure SQL Database refers to the single-database PaaS offering, not Azure SQL Managed Instance.

### Always On Availability Groups

Configure the connector to connect through the availability group **listener** (the virtual network name for the group), not through an individual replica node. Set the listener hostname in the **SQLServer Connection URL** parameter in the SQLServer Source Parameters context.

[Always On Availability Groups](https://learn.microsoft.com/sql/database-engine/availability-groups/windows/overview-of-always-on-availability-groups-sql-server) provide high availability through a shared listener and automatic failover between replicas. Always On Availability Groups are separate from SQL Server transactional replication.

Warning

Do not change the connection target after replication has started. Each database maintains its own replication position independently, so switching to a different server or listener can cause the connector to lose track of which changes have already been processed. This might result in data loss.

For `ApplicationIntent` in the JDBC URL on Always On Availability Groups:

Note

To route reads to a readable secondary, append `;ApplicationIntent=ReadOnly` to the **SQLServer Connection URL** when read-only routing is configured on the availability group listener.

On topologies that do not expose a readable secondary (for example, AWS RDS Multi-AZ with a single endpoint), the driver connects to the primary even when `ApplicationIntent=ReadOnly` is set.

When connections are routed to a readable secondary, the connector reads from CDC change tables on that replica. Those tables reflect changes only after capture lag and redo lag on the primary, so replication latency can be higher than when you connect to the primary. To reduce lag, tune SQL Server CDC capture and availability group redo settings on the primary.

During availability group failovers, replication resumes automatically and tables are not moved to `FAILED`. During each failover window, the connector logs a transient error that the database is not accessible for queries while data movement is suspended or a replica is not enabled for read access. This error is expected during the transition; the connector retries and recovers once failover completes.

To connect to the primary through the listener without read-only routing, omit `ApplicationIntent` or use the default `ReadWrite` intent.

For failover behavior, see [Always On Availability Groups and source failover](/user-guide/data-integration/openflow/connectors/sql-server-cdc/about#label-sqlserver-source-failover-resilience).

### SQLServer Destination Parameters

| Parameter | Description | Required |
| --- | --- | --- |
| Destination Database | The database where data is persisted. It must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase. | Yes |
| Destination Schema Pattern | A pattern for the names of destination schemas where data is persisted. The connector creates the schemas if they don’t exist.  You can customize the pattern per ingested table using these optional variables:   - `${source.database.name}`: a source table’s database. - `${source.schema.name}`: a source table’s schema. - `${source.table.name}`: a source table’s name.   For example, for a table with the qualified name `source_db.tenant_a.data`, the pattern `prefix_${source.database.name}_${source.schema.name}` evaluates to `prefix_source_db_tenant_a`.  To ingest all tables into a single schema, provide a schema name without any variables, like `destination_schema`.  Important  Don’t change this setting after the connector has begun ingesting data. Changing this setting after ingestion has begun breaks the existing ingestion. If you must change this setting, create a new connector instance. | Yes |
| Snowflake Authentication Strategy | When using:   - **Snowflake Openflow Deployment** or **BYOC**: Use SNOWFLAKE\_MANAGED.   This token is managed automatically by Snowflake.   BYOC deployments must have previously configured   [execute-as roles](/user-guide/data-integration/openflow/setup-openflow-byoc#label-deployment-byoc-setup-runtime-role) to use SNOWFLAKE\_MANAGED. - **BYOC**: Alternatively, BYOC can use KEY\_PAIR as the value for the authentication strategy. | Yes |
| Snowflake Account Identifier | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Snowflake account name formatted as [organization-name]-[account-name]. | Yes |
| Snowflake Connection Strategy | When using KEY\_PAIR, specify the strategy for connecting to Snowflake:   - **STANDARD** (default): Connect using standard public routing to Snowflake services. - **PRIVATE\_CONNECTIVITY**: Connect using private addresses associated with the supporting cloud platform such as AWS PrivateLink. | Required for BYOC with KEY\_PAIR only, otherwise ignored. |
| Snowflake Object Identifier Resolution | Specifies how source object identifiers such as schemas, tables, and column names are stored and queried in Snowflake. This setting dictates whether you must use double quotes in SQL queries.  Option 1: Default, case-insensitive (recommended).   - **Transformation**: All identifiers are converted to uppercase. For   example, `My_Table` becomes `MY_TABLE`. - **Queries**: SQL queries are case-insensitive and don’t require SQL   double quotes.   For example, `SELECT * FROM my_table;` returns the same results as `SELECT * FROM MY_TABLE;`.  Note  Snowflake recommends using this option if database objects are not expected to have mixed case names.  Important  Do not change this setting after connector ingestion has begun. Changing this setting after ingestion has begun breaks the existing ingestion. If you must change this setting, create a new connector instance.  Option 2: Case-sensitive.   - **Transformation**: Case is preserved.   For example, `My_Table` remains `My_Table`. - **Queries**: SQL queries must use double quotes to match the exact   case for database objects.   For example, `SELECT * FROM "My_Table";`.   Note  Snowflake recommends using this option if you must preserve source casing for legacy or compatibility reasons. For example, the source database includes table names that differ in case only, such as `MY_TABLE` and `my_table`, which result in a name collision when using case-insensitive comparisons. | Yes |
| Snowflake Private Key | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Must be the RSA private key used for authentication, formatted according to PKCS8   standards and including standard PEM headers and footers. Note that either a Snowflake Private   Key File or a Snowflake Private Key must be defined. | No |
| Snowflake Private Key File | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: The private key file must be blank. - **KEY\_PAIR**: Upload the file that contains the RSA private key used for authentication to Snowflake,   formatted according to PKCS8 standards and including standard PEM headers and footers.   The header line begins with `-----BEGIN PRIVATE`.   To upload the private key file, select the **Reference asset** checkbox. | No |
| Snowflake Private Key Password | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the password associated with the Snowflake Private Key File. | No |
| Snowflake Role | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Use the runtime’s execute-as role (or a child role granted to it).   You can find your execute-as role in the Openflow UI by navigating to **View Details** for your runtime. - **KEY\_PAIR**: Use a valid role configured for your service user. | Yes |
| Snowflake Username | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the user name used to connect to the Snowflake instance. | Yes |
| Oversized Value Strategy | Determines how the connector handles values that exceed its internal size limits (16 MB) during replication. Possible values are:  - **Fail Table** (default): The table is marked as permanently failed, and replication stops for that table. - **Set Null**: The value is replaced with `NULL` in the destination table.   Use this to prevent table failures when it is acceptable to lose data in tables beyond the oversized value. | No |
| Table Storage Format | Standard Snowflake tables or Iceberg tables. Defaults to **STANDARD**. Don’t change after the connector starts. | Yes |
| Iceberg Version | The Iceberg table version, 2 or 3 (default 3). Ignored unless Table Storage Format is **ICEBERG**. Don’t change this value after ingestion begins. | No |
| Snowflake Warehouse | Snowflake warehouse used to run queries. | Yes |

Expand

Show lessSee more

### SQLServer Ingestion Parameters

| Parameter | Description |
| --- | --- |
| Column Filter JSON | Optional. A JSON array of filter objects specifying which columns to include or exclude per table. For syntax details and examples, see [Replicate a subset of columns in a table](#replicate-a-subset-of-columns-in-a-table). |
| Concurrent Select Queries For Incremental | Maximum number of concurrent SELECT queries to run against the source database during incremental replication. Default: `1`, maximum: `8`. Increasing this can speed up replication when many tables are active, but will also increase the load on the source database. |
| Concurrent Select Queries For Snapshot | Maximum number of concurrent queries to the source database to run in the Snapshot flow. Increasing this can speed up snapshotting large numbers of tables, but will also increase the load on the source database. |
| Included Table Names | A comma-separated list of source table paths, including their databases and schemas, for example:  `database_1.public.table_1, database_2.schema_2.table_2` |
| Included Table Regex | A regular expression to match against table paths, including database and schema names. Every path matching the expression is replicated, and new tables matching the pattern that are created later are also included automatically, for example:  `database_name\.public\.auto_.*` |
| Ingestion Type | Controls whether newly added tables go through a full initial snapshot before switching to incremental CDC replication, or skip the snapshot and begin incremental CDC replication only. Set to `full` (default) for snapshot followed by incremental replication. Set to `incremental` to skip the snapshot for newly added tables and replicate only subsequent changes. Changing this value does not affect tables that have already begun replicating. For usage notes, see [Set up incremental replication without snapshots](/user-guide/data-integration/openflow/connectors/sql-server-cdc/incremental-replication). |
| Merge Task Schedule CRON | CRON expression defining periods when merge operations from Journal to Destination Table will be triggered. Set it to `* * * * * ?` if you want continuous merges, or configure a time schedule to limit warehouse run time. The connector evaluates the schedule in the UTC time zone.  For example:  - The string `* 0 * * * ?` indicates that you want to schedule merges at the full hour for one minute. - The string `* 20 14 ? * MON-FRI` indicates that you want to schedule merges at 2:20 PM every   Monday through Friday.  For additional information and examples, see the cron triggers tutorial in the [Quartz Documentation](https://www.quartz-scheduler.org/documentation/quartz-2.5.x/tutorials/crontrigger.html). |
| Re-read Tables in State | Only applicable when **Starting CDC Position** is `Earliest`.  - `New` (default):   Only new tables, added after the starting position was switched to `Earliest`, will have their CDC   change tables read from the earliest available positions. Tables that started replication before the   configuration change will continue reading from their last positions. - `Any active`: Re-read and re-process changes from any table currently in replication.  For more information, see [Specify load from CDC position](/user-guide/data-integration/openflow/connectors/sql-server-cdc/maintenance#label-sql-server-cdc-connector-start-restart-incremental-load-from-earliest-available-position). |
| Re-snapshot Table Exclusions | A comma-separated list of fully qualified table names that should not be replicated, from among tables matching the included criteria. Use the same format and quoting rules as **Included Table Names**, for example: `database_1.public.table_1`. |
| SQL Server Read Timeout | Read timeout in milliseconds applied to both snapshot and incremental queries. A query that runs longer than this value is closed by SQL Server. Default: `60000`. |
| Starting CDC Position | - `Latest` (default): CDC change table reading starts at the latest available position and continues from there. - `Earliest`: Switches the incremental load to start, or restart reading from the earliest available CDC change table positions.  For more information, see [Specify load from CDC position](/user-guide/data-integration/openflow/connectors/sql-server-cdc/maintenance#label-sql-server-cdc-connector-start-restart-incremental-load-from-earliest-available-position). |
| Table Key Configuration JSON | Optional. A JSON array that declares a logical key for one or more tables. When set, the logical key takes the highest priority and overrides any primary key, unique constraint, or unique index that the connector would otherwise auto-detect. The connector reads this parameter through its `MultiDatabaseJsonTableKeyConfigService` controller service.  For syntax details and examples, see [Specify a logical key for a table](#label-sqlserver-cdc-logical-key). |

Expand

Show lessSee more

## Read the source under SNAPSHOT isolation

During the snapshot phase, the connector reads directly from the source tables to perform the initial full
copy. Under SQL Server’s default READ COMMITTED isolation level, these reads acquire shared locks that can
deadlock with concurrent writes from other database clients. During incremental replication, the connector
reads from dedicated CDC change tables instead of the source tables, so it doesn’t take these locks. To avoid
deadlocks during the snapshot phase without affecting the isolation level that other applications use,
configure the connector to read under
[SNAPSHOT isolation](https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/sql/snapshot-isolation-in-sql-server).
For background, see
[Source database locking behavior](/user-guide/data-integration/openflow/connectors/sql-server-cdc/about#label-sql-server-cdc-source-database-locking-behavior).

Enable SNAPSHOT isolation for the connector in two steps:

1. On each source database, allow snapshot isolation:

   Copy code

   ```
   ALTER DATABASE <database> SET ALLOW_SNAPSHOT_ISOLATION ON;
   ```
2. Add a dynamic property named **Use Snapshot Isolation** with the value `true` to the
   `MultiDatabaseFetchTableSnapshot` processor. Only the snapshot phase takes shared locks on the source
   tables, so incremental replication doesn’t require the **Use Snapshot Isolation** property.

The connector checks each source database when it starts and uses SNAPSHOT isolation only for databases that
have `ALLOW_SNAPSHOT_ISOLATION` enabled. For a database that doesn’t have it enabled, the connector falls back
to the default isolation level. Because this check runs at startup, restart the processor after you change
`ALLOW_SNAPSHOT_ISOLATION`.

Caution

`ALLOW_SNAPSHOT_ISOLATION` only makes SNAPSHOT isolation available to sessions that explicitly request it, such
as the connector. It doesn’t change the default READ COMMITTED isolation level, so other applications that use
the source database are unaffected.

Don’t use `READ_COMMITTED_SNAPSHOT` (RCSI) for this purpose. Although RCSI also removes the shared locks, it
redefines the default READ COMMITTED isolation level for every connection to the database. Applications that
rely on the default lock-based READ COMMITTED behavior (for example, expecting readers to block on concurrent
uncommitted writes) can see different results after the change.

## Replicate a subset of columns in a table

The connector can filter the data replicated per table to a subset of configured columns.
Primary key columns are always included regardless of exclusions.

To apply column filters, set the **Column Filter JSON** parameter in the Ingestion Parameters context
to a JSON array of filter objects, one per table you want to filter.

Columns can be included or excluded by name or by regular expression pattern. You can apply a single condition per table,
or combine multiple conditions, with exclusions always taking precedence over inclusions.

## Syntax

Each object in the array identifies a table and specifies which columns to include or exclude.
Because this connector uses three-part fully qualified names (database, schema, and table), each object
can include a `database` or `databasePattern` field in addition to the schema and table fields.

Copy code

```
[
    {
        "database": "<database>" | "databasePattern": "<regex>",
        "schema": "<schema>" | "schemaPattern": "<regex>",
        "table": "<table>" | "tablePattern": "<regex>",
        "included": ["<column>", "<column>"],
        "excluded": ["<column>", "<column>"],
        "includedPattern": "<regex>",
        "excludedPattern": "<regex>"
    }
]
```

The following rules apply:

- Use `database`, `schema`, and `table` for exact name matching, or `databasePattern`,
  `schemaPattern`, and `tablePattern` for regex matching. You can’t use both a field and its
  pattern variant in the same object (for example, `schema` and `schemaPattern` can’t both appear).
- At least one of `included`, `excluded`, `includedPattern`, or `excludedPattern` must be provided.
- When both included and excluded filters are specified, exclusions take precedence.
- When multiple filters match the same table, the last matching filter is used, with exact matches
  taking precedence over pattern-based filters.
- The value can be an array of objects to apply different filters to different tables.

## Examples

Include specific columns by name:

Copy code

```
[
    {
        "database": "my_db",
        "schema": "dbo",
        "table": "orders",
        "included": ["account_id", "status", "created_at"]
    }
]
```

Exclude specific columns by name:

Copy code

```
[
    {
        "database": "my_db",
        "schema": "dbo",
        "table": "orders",
        "excluded": ["internal_note", "debug_flag"]
    }
]
```

Combine an include pattern with a specific exclusion (for example, include all email columns except `admin_email`):

Copy code

```
[
    {
        "database": "my_db",
        "schema": "dbo",
        "table": "contacts",
        "includedPattern": ".*_email",
        "excluded": ["admin_email"]
    }
]
```

Mix a database pattern with an exact schema and table name to apply a filter across databases:

Copy code

```
[
    {
        "databasePattern": "prod_.*",
        "schema": "dbo",
        "table": "customers",
        "excluded": ["internal_note"]
    }
]
```

Pass multiple filter objects to apply different rules to different tables:

Copy code

```
[
    {"database": "my_db", "schema": "dbo", "table": "orders", "included": ["account_id", "status"]},
    {"database": "my_db", "schema": "dbo", "table": "customers", "excludedPattern": ".*_internal"}
]
```

### Including and excluding the same column

Removing a column from a table’s replicated set (by excluding it or by removing
it from the included list) has the same effect on the destination as dropping
the column at the source: the connector soft-deletes the column on the
destination by renaming it with a suffix (by default, `__SNOWFLAKE_DELETED`).
If you then add the column back to the replicated set and later remove it a
second time, replication for the affected table fails because the soft-deleted
column name is already taken. To recover, restart replication for the affected
table.

## Replicate a partitioned table

The connector supports replication of partitioned tables. A SQL Server
partitioned table is replicated into Snowflake as a single destination table,
containing data from all partitions.

To replicate a partitioned table, ensure that CDC is enabled on the
partitioned table, as described in [Set up your SQL Server instance](#label-sql-server-cdc-connector-setup-instance).

For more information about how the connector handles snapshots of large partitioned tables, see [Snapshot of partitioned tables](/user-guide/data-integration/openflow/connectors/sql-server-cdc/about#label-sql-server-cdc-partitioned-snapshot).

## Specify a logical key for a table

The connector requires a replication key for every table it replicates. By default, the
connector uses the table’s primary key, or falls back to a qualifying unique constraint or
unique index if no primary key exists. For the full priority order the connector uses to
choose a key, see [How the connector chooses a replication key](/user-guide/data-integration/openflow/connectors/sql-server-cdc/about#label-sqlserver-cdc-replication-key-selection).
A *logical key* is a user-declared replacement
for the auto-detected key. Configure a logical key when:

- A table has no primary key, but one or more columns are unique in the data.
- A specific column or set of columns should be used as the replication key, regardless of
  what the connector would auto-detect (for example, to override a synthetic primary key).

A logical key takes the highest priority. When the connector finds a logical key for a
table, it uses that key and ignores any primary key on the table.

### JSON syntax

The **Table Key Configuration JSON** value is a JSON array. Each entry maps one
table to its logical key columns:

Copy code

```
[
    {
        "database": "<database>",
        "schema": "<schema>",
        "table": "<table>",
        "logicalKey": ["<column>", "<column>"]
    }
]
```

The fields are:

| Field | Description |
| --- | --- |
| `database` | Required. The exact source database name. |
| `schema` | Required. The exact source schema name. |
| `table` | Required. The exact source table name. |
| `logicalKey` | Required. A non-empty array of source column names that uniquely identify rows in the table. |

Expand

Show lessSee more

The following rules apply:

- `database`, `schema`, and `table` matching is **case-sensitive**. Use the exact names as reported by
  SQL Server.
- `logicalKey` column names are matched **case-insensitively**: the connector lowercases both the configured
  names and the source column names before comparing them. On a case-sensitive SQL Server collation this
  matching is lenient. A key whose case differs from the actual column is still accepted, and two source
  columns that differ only by letter case are treated as the same key column. Use the exact column case to
  avoid ambiguity.
- An entry whose `database`, `schema`, and `table` don’t match any replicated table is silently ignored.

### Logical key configuration examples

A single-column logical key on a table without a primary key:

Copy code

```
[
    {
        "database": "SalesDB",
        "schema": "dbo",
        "table": "audit_log",
        "logicalKey": ["event_id"]
    }
]
```

A composite logical key:

Copy code

```
[
    {
        "database": "SalesDB",
        "schema": "dbo",
        "table": "order_lines",
        "logicalKey": ["order_id", "line_item_id"]
    }
]
```

Logical keys for several tables in one JSON value:

Copy code

```
[
    {
        "database": "SalesDB",
        "schema": "dbo",
        "table": "audit_log",
        "logicalKey": ["event_id"]
    },
    {
        "database": "SalesDB",
        "schema": "dbo",
        "table": "order_lines",
        "logicalKey": ["order_id", "line_item_id"]
    }
]
```

### Restrictions

The connector rejects the configuration when any of the following is true:

- `logicalKey` is missing, empty, or not an array.
- `logicalKey` contains duplicate column names.
- `logicalKey` contains a nullable column. Logical key columns must be defined as `NOT NULL` to reliably identify rows.
- `logicalKey` contains a column name that doesn’t exist in the source table.

When the configuration is rejected, verification surfaces a clear error and the table stays
in the `NEW` state (never `FAILED`). After you fix the configuration, replication for the
table resumes without resetting state.

### Warnings logged for risky configurations

The connector accepts the following configurations but logs a warning at table
initialization.

When choosing logical-key columns, prefer columns with high cardinality and, where
possible, monotonically increasing values. Low-cardinality or non-monotonic keys can
degrade snapshot performance.

- A logical-key column is a floating-point type (`float`, `real`). Floating-point
  comparisons can produce inconsistent results because of precision differences.
- A logical-key column is a large-object type (`text`, `image`, `varbinary(max)`). Using large
  objects as keys severely degrades MERGE performance.
- The composite logical key includes more than five columns. Long composite keys often
  indicate a design issue and might degrade MERGE performance.
- The logical key overrides an existing primary key on the table. Verify that the
  replacement key is intentional: the connector no longer uses the primary key for
  MERGE operations.

If you observe data divergence after any of these warnings, run a periodic full reload
to reconcile the destination with the source.

### Schema changes that affect a logical key

The connector doesn’t track schema evolution of the unique or logical key columns after
the CDC capture instance exists. Dropping or altering a logical-key column isn’t detected
at runtime:

- If a logical-key column is dropped on the source, replication for the affected table
  fails. Restart table replication to recover. For more information, see
  [Restart table replication](/user-guide/data-integration/openflow/connectors/sql-server-cdc/maintenance#label-of-sql-server-cdc-restart-table-replication).
- If a logical-key column is renamed on the source, the configuration still references
  the old name and replication fails. Update the JSON to use the new name and restart
  table replication.

## Track data changes in tables

The connector replicates the current state of data from the source tables,
as well as detected changes from each polling interval. This data is stored in journal tables
created in the same schema as the destination table.

The journal table names are formatted as: `<source_table_name>_JOURNAL_<timestamp>_<schema_generation>`
where `<timestamp>` is the value of epoch seconds when the source table was added to replication, and `<schema_generation>` is an integer increasing with every schema change on the source table.
As a result, source tables that undergo schema changes will have multiple journal tables.

When you remove a table from replication, then add it back, the `<timestamp>` value changes, and `<schema_generation>` starts again from `1`.

Important

Snowflake recommends not altering the structure of journal tables in any way.
The connector uses them to update the destination table as part of the replication process.

The connector never drops journal tables, but uses the latest
journal for every replicated source table, only reading append-only streams on top of journals.
To reclaim the storage, you can:

- Truncate all journal tables at any time.
- Drop the journal tables related to source tables that were removed from replication.
- Drop all but the latest generation journal tables for actively replicated tables.

For example, if your connector is set to actively replicate source table `orders`,
and you have earlier removed table `customers` from replication, you may have
the following journal tables. In this case you can drop all of them *except* `orders_5678_2`.

```
customers_1234_1
customers_1234_2
orders_5678_1
orders_5678_2
```

## Configure scheduling of merge tasks

The connector uses a warehouse to merge change data capture (CDC) data into destination tables.
The processor named Merge Journal to Destination triggers this operation. When there are no new
changes, or when no new FlowFiles are waiting in the Merge Journal to Destination queue, no merge
is triggered and the warehouse is available for auto-suspension.

To limit warehouse cost and restrict merges to scheduled times, use the CRON expression in the
Merge Task Schedule CRON parameter. It throttles the FlowFiles that reach the Merge Journal to
Destination processor, so merges are triggered only during the specified period. The connector
evaluates the schedule in the UTC time zone.

For additional information and examples, see the cron triggers tutorial in the [Quartz Documentation](https://www.quartz-scheduler.org/documentation/quartz-2.5.x/tutorials/crontrigger.html).

## Run the flow

1. Right-click on the canvas and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.
