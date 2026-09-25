# Set up the Openflow Connector for SQL Server

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes how to set up the Openflow Connector for SQL Server.

For information on the incremental load process, see [Incremental replication](/user-guide/data-integration/openflow/connectors/sql-server/incremental-replication).

## Prerequisites

Before setting up the connector, ensure that you have completed the following prerequisites:

1. Ensure that you have reviewed [About Openflow Connector for SQL Server](/user-guide/data-integration/openflow/connectors/sql-server/about).
2. Ensure that you have reviewed [Supported SQL Server versions](/user-guide/data-integration/openflow/connectors/sql-server/about#label-sql-server-versions).
3. Ensure that you have set up your runtime deployment. For more information, see the following topics:

   - [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs)
   - [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc).
4. If you use Openflow - Snowflake Deployments, ensure that you have reviewed
   [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list) and have granted access to the required domains for the [SQL Server](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-sqlserver) connector.

## Set up your SQL Server instance

Before setting up the connector, perform the following tasks in your SQL Server environment:

Note

You must perform these tasks as a database administrator.

1. Enable change tracking on the
   [databases](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/enable-and-disable-change-tracking-sql-server?view=sql-server-ver16#enable-change-tracking-for-a-database)
   and
   [tables](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/enable-and-disable-change-tracking-sql-server?view=sql-server-ver16#enable-change-tracking-for-a-table)
   that you plan to replicate, as shown in the following SQL Server example:

   Copy code

   ```
   ALTER DATABASE <database>
     SET CHANGE_TRACKING = ON
     (CHANGE_RETENTION = 5 DAYS, AUTO_CLEANUP = ON);

   ALTER TABLE <schema>.<table>
     ENABLE CHANGE_TRACKING
     WITH (TRACK_COLUMNS_UPDATED = OFF);
   ```

   Note

   Run the `ALTER DATABASE` command only once per database to enable change tracking on that database.
   Run the `ALTER TABLE` command for every table that you plan to replicate in that database.

   Important

   Keep the column tracking feature off by setting `TRACK_COLUMNS_UPDATED = OFF` (the default) when you
   enable change tracking on a table. The connector doesn’t use column-level change information, so
   enabling `TRACK_COLUMNS_UPDATED = ON` adds unnecessary storage and per-DML overhead on the source
   without providing any benefit to replication.

   Each table must have change tracking enabled before the connector can replicate it. Enable change
   tracking on every table you want to replicate before you start replication.

   Important

   Set `CHANGE_RETENTION` to a window that’s long enough to keep change data available for data
   continuity. SQL Server removes tracked changes once they’re older than the retention period, so if
   the connector can’t read changes before they expire, it can’t replicate them incrementally and the
   affected tables require a full reload.

   A longer retention window, such as 5 days, gives you time to detect and react to problems, such as
   a paused connector, a network outage, or a failed replication cycle, and to mitigate them without
   reloading entire tables. Choose a value that covers the longest interruption you expect to recover
   from, balanced against the additional storage that retained change data consumes in SQL Server.
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
4. Grant the SELECT and VIEW CHANGE TRACKING permissions to the user for each database that you are
   replicating:

   Copy code

   ```
   GRANT SELECT ON <database>.<schema>.<table> TO <user_name>;
   GRANT VIEW CHANGE TRACKING ON <database>.<schema>.<table> TO <user_name>;
   ```

   Run these commands in each database for every table that you plan to replicate.
   These permissions must be granted to the user of each database that you created in a
   previous step.
5. (Optional) Grant the VIEW DEFINITION privilege on the User Defined Data Types (UDDT).

   If your tables contain columns that use User Defined Data Types (UDDT), and the UDDT is owned by
   a different user than the connector user, you must grant the VIEW DEFINITION permission
   to the connector user as shown in the following SQL Server example:

   Copy code

   ```
   GRANT VIEW DEFINITION TO <user_name>;
   ```

   Without this permission, columns using UDDT are silently excluded from replication.
6. (Optional) Configure SSL connection.

   If you use an SSL connection to connect to SQL Server, create the root certificate for your database
   server. This is required when configuring the connector.

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

For migration instructions, see [Reinstall the connector](/user-guide/data-integration/openflow/connectors/sql-server/maintenance#label-sql-server-reinstall-connector).

## Configure the connector

To configure the connector, do the following as a data engineer:

1. Right-click on the imported process group and select **Parameters**.
2. Populate the required parameter values.

   For more information on the required parameter values, see the following sections:

   - [SQLServer Source Parameters](#label-of-sqlserver-source-parameters): Used to establish a connection with SQL Server.
   - [SQLServer Destination Parameters](#label-of-sqlserver-destination-parameters): Used to establish a connection with Snowflake.
   - [SQLServer Ingestion Parameters](#label-of-sqlserver-ingestion-parameters): Used to specify the tables to replicate.

Start by setting the parameters of the SQLServer Source Parameters context, then the SQLServer Destination Parameters context.
After you complete this, enable the connector. The connector connects to both SQLServer and Snowflake and starts running.
However, the connector doesn’t replicate any data until any tables to be replicated are explicitly added to its configuration.

To configure specific tables for replication, edit the SQLServer Ingestion Parameters context. After you apply the changes to the
SQLServer Ingestion Parameters context, the configuration is picked up by the connector, and the replication lifecycle starts for every table.

To run multiple CDC connector instances on one runtime, see .

Note

**DBCPConnectionPool validation**

Enabling the `DBCPConnectionPool` controller service configures the connection pool but doesn’t open a JDBC connection.

To test the connection from the Openflow runtime, open the controller service configuration and select **Verify**. Confirm that the **Establish Connection** step succeeds. This test opens a connection by using the configured JDBC URL, driver, username, and password.

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

Note

**Azure SQL Managed Instance through a proxy**

If you connect to Azure SQL Managed Instance through a proxy, Nginx route, or another intermediate host, configure Azure SQL Managed Instance to use `Proxy` connection mode.

Don’t use `Redirect` mode when the Openflow runtime must route SQL Server traffic through the proxy host. In `Redirect` mode, Azure SQL Managed Instance can instruct the JDBC driver to reconnect to a different backend host. That redirected host might not be reachable through the proxy route configured for the Openflow runtime.

For example:

1. Openflow connects to `nginx.example.com:10001`.
2. Nginx forwards traffic to `sqlmi.example.database.windows.net:1433`.
3. Azure SQL Managed Instance in `Redirect` mode tells the JDBC driver to reconnect to another backend host.
4. The Openflow runtime tries to connect to that redirected host directly.
5. The connection fails because the redirected host isn’t routed through the proxy.

Use `Proxy` mode when all SQL Server traffic must stay on the original proxy route.

For **SQLServer Username**, enter the SQL login configured on the Azure SQL Managed Instance.

### Always On Availability Groups

Configure the connector to connect through the availability group **listener** (the virtual network name for the group), not through an individual replica node. Set the listener hostname in the **SQLServer Connection URL** parameter in the SQLServer Source Parameters context.

[Always On Availability Groups](https://learn.microsoft.com/sql/database-engine/availability-groups/windows/overview-of-always-on-availability-groups-sql-server) provide high availability through a shared listener and automatic failover between replicas. Always On Availability Groups are separate from SQL Server transactional replication.

Warning

Do not change the connection target after replication has started. Each database maintains its own replication position independently, so switching to a different server or listener can cause the connector to lose track of which changes have already been processed. This might result in data loss.

### Azure Private Link Service for SQL Server

If you connect to SQL Server through a customer-managed Azure Private Link Service (PLS), use the `host` value returned by `SYSTEM$GET_PRIVATELINK_ENDPOINTS_INFO()` as the hostname in **SQLServer Connection URL**. This is the logical hostname supplied when the Snowflake outbound private connectivity endpoint was provisioned. The PLS alias or resource ID identifies the Azure service during provisioning, but it isn’t the JDBC hostname.

For example:

- `jdbc:sqlserver://<host>:1433;databaseName=<db>`

Add the same hostname and port to the Openflow egress network rule:

Copy code

```
TYPE = PRIVATE_HOST_PORT
MODE = EGRESS
VALUE_LIST = ('<host>:1433')
```

Include the `:1433` port explicitly. For a `PRIVATE_HOST_PORT` network rule, if you don’t specify a port it defaults to 443, which doesn’t match the SQL Server listener.

Snowflake routes this registered hostname through the outbound private endpoint. In Azure, configure the PLS and its Standard Load Balancer or Direct Connect destination so that the backend route, health probe, SQL Server listener, and port forwarding deliver traffic for the same port.

This guidance applies to a customer-managed Azure PLS that fronts SQL Server. It doesn’t apply to a native Azure SQL Managed Instance private endpoint.

To provision and approve the endpoint (`SYSTEM$PROVISION_PRIVATELINK_ENDPOINT` and the Azure-side approval), see [External network access and private connectivity on Microsoft Azure](/developer-guide/external-network-access/creating-using-private-azure) and [Private connectivity for outbound network traffic](/user-guide/private-connectivity-outbound).

For failover behavior, see [Always On Availability Groups and source failover](/user-guide/data-integration/openflow/connectors/sql-server/about#label-sqlserver-source-failover-resilience).

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

The following destination parameter controls how the connector handles invalid rows:

| Parameter | Description | Required |
| --- | --- | --- |
| Error Handling Strategy | Determines how the connector handles invalid rows that Snowflake rejects during ingestion. Possible values are:  - **Fail Table** (default): The table is marked as failed on the first invalid row, and replication stops for that table. - **Log Errors and Continue**: The connector keeps replicating the valid rows and records each rejected row in the table’s error table.  For more information, see [Error handling for invalid rows](/user-guide/data-integration/openflow/connectors/sql-server/about#label-sql-server-error-handling). | No |

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
| Ingestion Type | Controls whether newly added tables go through a full initial snapshot before switching to incremental replication, or skip straight to incremental replication. Set to `full` (default) for snapshot followed by incremental replication. Set to `incremental` to skip the snapshot for newly added tables and replicate only subsequent changes. Changing this value does not affect tables that have already begun replicating. For usage notes, see [Set up incremental replication without snapshots](/user-guide/data-integration/openflow/connectors/sql-server/incremental-replication). |
| Max Batch Size | The maximum number of rows to fetch in a single batch. Default: `100000`. |
| Merge Task Schedule CRON | CRON expression defining periods when merge operations from Journal to Destination Table will be triggered. Set it to `* * * * * ?` if you want continuous merges, or configure a time schedule to limit warehouse run time. The connector evaluates the schedule in the UTC time zone.  For example:  - The string `* 0 * * * ?` indicates that you want to schedule merges at the full hour for one minute. - The string `* 20 14 ? * MON-FRI` indicates that you want to schedule merges at 2:20 PM every   Monday through Friday.  For additional information and examples, see the cron triggers tutorial in the [Quartz Documentation](https://www.quartz-scheduler.org/documentation/quartz-2.5.x/tutorials/crontrigger.html). |
| Re-read Tables in State | Only applicable when **Starting Change Tracking Position** is `Earliest`.  - `New` (default):   Only new tables, added after the starting position was switched to `Earliest`, will have their change   tracking tables read from the earliest available positions. Tables that started replication before the   configuration change will continue reading from their last positions. - `Any active`: Re-read and re-process changes from any table currently in replication.  For more information, see [Specify load from change tracking table position](/user-guide/data-integration/openflow/connectors/sql-server/maintenance#label-sql-server-connector-start-restart-incremental-load-from-earliest-available-change-tracking-position). |
| Re-snapshot Table Exclusions | A comma-separated list of fully qualified table names that should not be replicated, from among tables matching the included criteria. Use the same format and quoting rules as **Included Table Names**, for example: `database_1.public.table_1`. |
| SQL Server Read Timeout | Read timeout in milliseconds applied to both snapshot and incremental queries. A query that runs longer than this value is closed by SQL Server. Default: `60000`. |
| Starting Change Tracking Position | - `Latest` (default): Change tracking table reading starts at the latest available position and continues from there. - `Earliest`: Switches the incremental load to start, or restart reading from the earliest available change tracking table positions.  For more information, see [Specify load from change tracking table position](/user-guide/data-integration/openflow/connectors/sql-server/maintenance#label-sql-server-connector-start-restart-incremental-load-from-earliest-available-change-tracking-position). |

Expand

Show lessSee more

## Read the source under SNAPSHOT isolation

The connector reads the source tables during both snapshot and incremental replication. Under SQL Server’s
default READ COMMITTED isolation level, these reads acquire shared locks that can deadlock with concurrent
writes from other database clients. To avoid these deadlocks without affecting the isolation level that other
applications use, configure the connector to read under
[SNAPSHOT isolation](https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/sql/snapshot-isolation-in-sql-server).
For background, see
[Source database locking behavior](/user-guide/data-integration/openflow/connectors/sql-server/about#label-sql-server-source-database-locking-behavior).

Enable SNAPSHOT isolation for the connector in two steps:

1. On each source database, allow snapshot isolation:

   Copy code

   ```
   ALTER DATABASE <database> SET ALLOW_SNAPSHOT_ISOLATION ON;
   ```
2. Add a dynamic property named **Use Snapshot Isolation** with the value `true` to the connector’s processors.
   Because the connector reads the source tables during both snapshot and incremental replication, add this
   dynamic property to both the `MultiDatabaseFetchTableSnapshot` processor and the
   `MultiDatabaseCaptureChangeSqlServer` processor.

The connector checks each source database when it starts and uses SNAPSHOT isolation only for databases that
have `ALLOW_SNAPSHOT_ISOLATION` enabled. For a database that doesn’t have it enabled, the connector falls back
to the default isolation level. Because this check runs at startup, restart the processors after you change
`ALLOW_SNAPSHOT_ISOLATION`.

Caution

`ALLOW_SNAPSHOT_ISOLATION` only makes SNAPSHOT isolation available to sessions that explicitly request it, such
as the connector. It doesn’t change the default READ COMMITTED isolation level, so other applications that use
the source database are unaffected.

Don’t use `READ_COMMITTED_SNAPSHOT` (RCSI) for this purpose. Although RCSI also removes the shared locks, it
redefines the default READ COMMITTED isolation level for every connection to the database. Applications that
rely on the default lock-based READ COMMITTED behavior (for example, expecting readers to block on concurrent
uncommitted writes) can see different results after the change.

## Replicate tables from a SQL Server replica server

The connector can ingest data from a primary server or from a subscriber server using
[transactional replication](https://learn.microsoft.com/en-us/sql/relational-databases/replication/transactional/transactional-replication).
Before configuring the connector to connect to a SQL Server replica, ensure that replication between the primary and replica
nodes works correctly. For instructions on setting up transactional replication, see
[Tutorial: Configure transactional replication](https://learn.microsoft.com/en-us/sql/relational-databases/replication/tutorial-replicating-data-between-continuously-connected-servers).
When investigating issues with missing data in the connector, first ensure that missing rows and
change tracking events are present in the replica server used by the connector.

Note

When using a replica server, the connector setup differs from the standard primary server configuration.
The connection user and change tracking don’t need to be configured on the primary server. Instead, make sure that the
connection user is available on the replica server and has access to the data and change tracking tables there.

To configure the connector to read from a subscriber server instead of the publisher, specify the subscriber server URL in the
**SQLServer Connection URL** parameter.

Warning

Do not change the database server after replication has started. Each database maintains its own change tracking
state independently, so switching to a different server would cause the connector to lose track of which changes
have already been processed, and may result in data loss.

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

To replicate a partitioned table, ensure that change tracking is enabled on the
partitioned table, as described in [Set up your SQL Server instance](#label-sql-server-connector-setup-instance).

For more information about how the connector handles snapshots of large partitioned tables, see [Snapshot of partitioned tables](/user-guide/data-integration/openflow/connectors/sql-server/about#label-sql-server-partitioned-snapshot).

## Track data changes in tables

The connector replicates the current state of data from the source tables,
as well as detected changes from each polling interval. This data is stored in journal tables
created in the same schema as the destination table.

Note

Because the connector uses SQL Server Change Tracking, multiple updates to the same row between
polling intervals are rolled up into a single change. Journal tables reflect the net result of
changes, not every intermediate state. For more information, see [About Openflow Connector for SQL Server](/user-guide/data-integration/openflow/connectors/sql-server/about).

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
