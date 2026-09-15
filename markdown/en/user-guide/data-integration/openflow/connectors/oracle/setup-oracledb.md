# Openflow Connector for Oracle: Configure the Oracle database

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

Note

The Openflow Connector for Oracle is also subject to additional terms of service beyond the standard
connector terms of service. For more information, see the
[Openflow Connector for Oracle Addendum](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/openflow-oracle-terms/).

This topic describes how to set up the Oracle database for Openflow Connector for Oracle.

Note

Your Oracle database setup depends on your organization’s security policies
and database architecture. For example, if tables reside in a Container
Database (CDB), a Pluggable Database (PDB), multiple PDBs, or a combination.

The steps provided in this topic are examples only. Modify them
as required for your environment.

As an Oracle database administrator, perform the following procedures on your source database:

1. [Configure the retention period for archived redo logs](#label-set-up-archived-redo-logs-retention-period)
2. [Enable XStream and supplemental logging](#label-enable-xstream-and-supplemental-logging)
3. [Create the XStream administrator user](#label-create-xstream-administrator-user)
4. [Grant XStream administrator privileges](#label-granting-xstream-administrator-privileges)
5. [Configure XStream server connect user](#label-configure-xstream-server-connect-user)
6. [Create XStream Outbound Server](#label-create-xstream-outbound-server)
7. [Set up the XStream Outbound Server Connect User](#label-set-xstream-outbound-server-connect-user)
8. [Set up the XStream Outbound Server Capture User](#label-set-xstream-outbound-server-capture-user)
9. (Optional) [Data Guard or standby capture (optional)](#label-oracle-standby-setup)
10. (Optional) [Configure SSL connections (optional)](#label-configure-ssl-connections)

Note

The steps in this topic are written for a multi-tenant architecture with a Container
Database (CDB) and one or more Pluggable Databases (PDB). If your Oracle database uses a single-tenant
architecture, see [Set up XStream for single-tenant databases](#label-setup-xstream-single-tenant).

## Configure the retention period for archived redo logs

You must enable the `ARCHIVELOG` mode to ensure that change data is available for replication.

If you use AWS RDS for Oracle, you must also configure the retention period for archived redo logs.
Determine this period based on the volume of changes in the source database and your storage capacity.

To set the retention period, for example to 24 hours, follow the procedures in the following table:

| Database version | Procedure |
| --- | --- |
| AWS RDS (Standard) | Run the following:  Copy code  ``` begin     rdsadmin.rdsadmin_util.set_configuration(         name  => 'archivelog retention hours',         value => '24'); end; / commit; ```  For more information, see [Retaining archived redo logs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.Oracle.CommonDBATasks.RetainRedoLogs.html). |
| AWS RDS Custom | 1. Create a text file named `/opt/aws/rdscustomagent/config/redo_logs_custom_configuration.json`. 2. Add a JSON object to this file in the following format: `{"archivedLogRetentionHours" : "24"}`.   For more information, see [Restoring an RDS Custom for Oracle instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/custom-backup.pitr.html). |

Expand

Show lessSee more

## Enable XStream and supplemental logging

Note

XStream is included with Oracle Database and doesn’t require any additional software.

To enable and configure XStream replication to capture and stream change data, run the following commands:

1. Enable XStream replication:

Copy code

```
ALTER SYSTEM SET enable_goldengate_replication=TRUE SCOPE=BOTH;

ALTER SYSTEM SET STREAMS_POOL_SIZE = 2560M;
```

Note

Snowflake recommends setting the streams pool size to 2.5 GB. This allocation covers the following:

- 1 GB for Capture
- 1 GB for Apply
- An additional 25% buffer

To enable supplemental logging to ensure that the redo logs capture the information required for logical
replication, run the following commands:

1. Confirm that the database is in ARCHIVELOG mode as shown in the following example:

   Copy code

   ```
   SELECT LOG_MODE, FORCE_LOGGING FROM V$DATABASE;
   ```

   Snowflake recommends forcing logging at the database or tablespace level.
2. Set the container to the root container and add supplemental logging to the database:

   Copy code

   ```
   ALTER SESSION SET CONTAINER = CDB$ROOT;
   ALTER DATABASE ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS;
   ```

   Alternatively, you can enable logging only on specific tables as shown in the following example:

   Copy code

   ```
   ALTER TABLE schema_name.table_name ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS;
   ```

## Create the XStream administrator user

An XStream administrator user is required to manage XStream components, including the
creation and alteration of outbound servers.
You can either create a dedicated user for this purpose or use an existing user,
provided that the necessary XStream administration privileges are granted (see the next section).

The following example details the setup of a dedicated XStream administrator user in the root container of a CDB.

Note

The following example assumes that the database also has a PDB containing tables to be replicated.

Connect as SYSDBA or a user with appropriate privileges and run the following commands:

Copy code

```
-- Switch to the root container.
ALTER SESSION SET CONTAINER = CDB$ROOT;

--  Create a tablespace for the XStream administrator user.
CREATE TABLESPACE xstream_adm_tbs DATAFILE '/path/to/your/cdb/xstream_adm_tbs.dbf'
   SIZE 25M REUSE AUTOEXTEND ON MAXSIZE UNLIMITED;

-- Switch to the Pluggable Database (PDB) and create a tablespace there.
ALTER SESSION SET CONTAINER = YOUR_PDB_NAME;

CREATE TABLESPACE xstream_adm_tbs DATAFILE '/path/to/your/pdb/xstream_adm_tbs.dbf'
   SIZE 25M REUSE AUTOEXTEND ON MAXSIZE UNLIMITED;

-- Switch back to the root container to create the common user.
ALTER SESSION SET CONTAINER = CDB$ROOT;

-- Create the XStream administrator user.
-- Note: the 'c##' prefix indicates a common user in a CDB environment, and CONTAINER=ALL grants privileges across all containers.
-- Replace "YOUR_XSTREAM_ADMIN_PASSWORD" with a strong, secure password.

CREATE USER c##xstreamadmin IDENTIFIED BY "YOUR_XSTREAM_ADMIN_PASSWORD"
   DEFAULT TABLESPACE xstream_adm_tbs
   QUOTA UNLIMITED ON xstream_adm_tbs
   CONTAINER=ALL;
```

## Grant XStream administrator privileges

Connect as SYSDBA or a user with appropriate privileges and grant the required privileges
to the XStream administrator user.

1. Grant the CREATE SESSION privilege to the XStream administrator:

   Copy code

   ```
   GRANT CREATE SESSION TO c##xstreamadmin CONTAINER=ALL;
   ```
2. Grant XStream capture privileges using one of the following commands, depending on your Oracle Database version:

   | Database version | Command |
   | --- | --- |
   | Oracle Database 21c and earlier | Run the following:  Copy code  ``` BEGIN   DBMS_XSTREAM_AUTH.GRANT_ADMIN_PRIVILEGE(  grantee                 => 'c##xstreamadmin',  privilege_type          => 'CAPTURE',  grant_select_privileges => TRUE,  container               => 'ALL'); END; / ``` |
   | Oracle Database 23c and later | Oracle Database 23c introduced a dedicated `XSTREAM_CAPTURE` system privilege. Run the following:  Copy code  ``` GRANT XSTREAM_CAPTURE TO c##xstreamadmin CONTAINER=ALL; ``` |

   Expand

   Show lessSee more

## Configure XStream server connect user

The Snowflake Openflow Connector uses a dedicated connect user to establish a connection to the XStream Outbound Server and receive change data.
This user requires specific privileges to facilitate replication:

- **Read from XStream Outbound Server**: The user must be able to access the change data stream from the configured XStream Outbound Server.
- **Select from Data Dictionary Views**: The connect user needs SELECT access to various data dictionary views.
  This can be achieved by granting SELECT\_CATALOG\_ROLE or SELECT ANY DICTIONARY.
  If granting SELECT ANY DICTIONARY isn’t desired due to company policy, the user specifically needs SELECT access to the following views:

  - ALL\_USERS
  - ALL\_TABLES
  - ALL\_TAB\_COLS
  - ALL\_CONS\_COLUMNS
  - ALL\_CONSTRAINTS
  - ALL\_INDEXES
  - ALL\_IND\_COLUMNS
  - V\_$DATABASE

  If you’re replicating data from multiple PDBs, also grant SELECT access to:

  - V\_$CONTAINERS
  - V\_$PARAMETER
  - CDB\_TABLES
  - CDB\_USERS

  `ALL_INDEXES` and `ALL_IND_COLUMNS` are required so the connector can detect
  unique constraints and unique indexes as replication keys when a table has no
  primary key. For more information on the selection algorithm, see
  [How the connector chooses a replication key](/user-guide/data-integration/openflow/connectors/oracle/about#label-oracle-replication-key-selection).
- **Select from Source Tables**: The user must have SELECT privileges on all tables that are intended for replication.

The following is an example of how to set up such a user in the root container of the CDB.
The example assumes that the database also has a PDB containing tables to be replicated.

Copy code

```
-- Connect as SYSDBA or a user with appropriate privileges
-- Switch to the root container.

ALTER SESSION SET CONTAINER = CDB$ROOT;

-- Create the connect user.
-- Replace "YOUR_CAPTURE_USER_PASSWORD" with a strong, secure password.
CREATE USER c##connectuser IDENTIFIED BY "YOUR_CAPTURE_USER_PASSWORD"
    CONTAINER=ALL;

-- Grant necessary privileges to the connect user.
-- You can choose to grant access to specific tables
-- instead of SELECT ANY TABLE for more granular control,
-- for example, GRANT SELECT ON schema.table TO c##connectuser;
GRANT CREATE SESSION, SELECT_CATALOG_ROLE, SELECT ANY TABLE TO c##connectuser CONTAINER=ALL;
```

Note

If your database is multi-tenant and the connector is connected to a CDB to replicate
data from multiple PDBs, grant the connect user the additional privileges needed to
switch between containers and read data dictionary information across all of them:

Copy code

```
ALTER USER c##connectuser SET CONTAINER_DATA = ALL CONTAINER = CURRENT;

GRANT SET CONTAINER TO c##connectuser CONTAINER=ALL;
```

If you granted SELECT on individual data dictionary views instead of
SELECT\_CATALOG\_ROLE or SELECT ANY DICTIONARY, also grant SELECT on
`V_$CONTAINERS`, `V_$PARAMETER`, `CDB_TABLES`, and `CDB_USERS`.

## Create XStream Outbound Server

The XStream Outbound Server captures changes from redo logs for consumption by the Openflow Connector. Define which schemas or tables to replicate.
For more information, see [DBMS\_XSTREAM\_ADM.CREATE\_OUTBOUND Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_XSTREAM_ADM.html#GUID-A602ED86-0F5A-4A27-92A0-55D5ADC0AF0D).

Create the outbound server on a writable database: the primary, a logical
standby, or a downstream capture database. You can’t create it on an Active
Data Guard physical standby. For supported standby topologies, see
[Data Guard and standby support](/user-guide/data-integration/openflow/connectors/oracle/about#label-oracle-standby-data-guard-support)
and [Data Guard or standby capture (optional)](#label-oracle-standby-setup).

Important considerations for replication scope:

- If a table is included in the XStream Outbound filtering rules command, it won’t be replicated.
- A table or schema included here must also be defined in the connector parameters for it to be replicated.
  You can include an entire schema in the server filtering rules and later, in the connector parameters,
  specify only certain tables within that schema for replication.

Note

The XStream Outbound Server can only be created from the root container. However,
starting with Oracle Database version 23ai, it can also be created on the PDB level.

To avoid a significant hit to your CPU and network, and to prevent your queues from being filled with irrelevant data, it’s essential to use a granular approach. The best way to do this is with the DBMS\_XSTREAM\_ADM.ADD\_TABLE\_RULES procedure, which lets you choose only the specific tables
you need.

The following examples show how to set up the XStream Outbound Server based on different replication needs. In practice, when setting up your XStream Outbound Server on your production environment, you should be selective about what changes you capture. Capturing everything can have serious consequences for your database’s performance and resource usage.

For information on how to configure XStream Outbound Server, see
[Configuring XStream Out](https://docs.oracle.com/en/database/oracle/oracle-database/19/xstrm/configuring-xstream-out.html#GUID-A1C8430E-565B-4F66-8E00-495F283AAAFB).

**Example 1:** Capture all tables from all schemas in the root container and all PDBs

Copy code

```
-- Connect as a user with XStream admin privileges to the root container.
-- Ensure serveroutput is enabled to see messages from the PL/SQL block.
SET SERVEROUTPUT ON;

DECLARE
    tables  DBMS_UTILITY.UNCL_ARRAY;
    schemas DBMS_UTILITY.UNCL_ARRAY;
BEGIN
   -- To replicate all tables in all schemas across all containers, set both to NULL.
   tables(1) := NULL;
   schemas(1) := NULL;
   DBMS_XSTREAM_ADM.CREATE_OUTBOUND(
       server_name => 'XOUT1',
       table_names => tables,
       schema_names => schemas,
       include_ddl => TRUE
   );
   DBMS_OUTPUT.PUT_LINE('XStream Outbound Server created.');
   EXCEPTION
   WHEN OTHERS THEN
       DBMS_OUTPUT.PUT_LINE('Error creating XStream Outbound Server: ' || SQLERRM);
       RAISE;
END;
/
```

**Example 2:** Capture all tables from a single schema in a Pluggable Database (PDB)

Copy code

```
-- Connect as a user with XStream admin privileges to the root container.
-- Ensure serveroutput is enabled to see messages from the PL/SQL block.
SET SERVEROUTPUT ON;

DECLARE
    tables  DBMS_UTILITY.UNCL_ARRAY;
    schemas DBMS_UTILITY.UNCL_ARRAY;
BEGIN
    -- To replicate all tables in a schema in the single PDB, set source_container_name.
    tables(1) := NULL;
    schemas(1) := 'schema_name';
    DBMS_XSTREAM_ADM.CREATE_OUTBOUND(
        server_name => 'XOUT1',
        table_names => tables,
        schema_names => schemas,
        include_ddl => TRUE,
        source_container_name => 'YOUR_PDB_NAME'
    );
    DBMS_OUTPUT.PUT_LINE('XStream Outbound Server created.');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error creating XStream Outbound Server: ' || SQLERRM);
      RAISE;
END;
/
```

## Set up the XStream Outbound Server Connect User

Set the connect user on the XStream Outbound Server. This ensures that the previously created connect user is associated with the XStream Outbound Server (XOUT1), allowing it to receive change data.

Note

The following example assumes that the connect user is c##connectuser.

Copy code

```
BEGIN
    DBMS_XSTREAM_ADM.ALTER_OUTBOUND(
        server_name  => 'XOUT1',
        connect_user => 'c##connectuser');
   END;
/
```

## Set up the XStream Outbound Server Capture User

Note

If you want the data to be captured by the same user that created the server (the administrator), skip this section.

If you configured a separate capture user, configure the XStream Outbound Server to run
as this user. This ensures that the dedicated capture user is associated with the XStream Outbound Server (XOUT1), allowing that user to capture change data.

Copy code

```
BEGIN
    DBMS_XSTREAM_ADM.ALTER_OUTBOUND(
        server_name  => 'XOUT1',
      capture_user => 'yourcaptureuser');
END;
/
```

## Set up XStream for single-tenant databases

The default architecture for Oracle 12c and later is a multi-tenant architecture with
a Container Database (CDB) and one or more Pluggable Databases (PDB). Oracle 11g uses
a single-tenant (non-CDB) architecture.

If your Oracle database uses a single-tenant architecture, note the following
differences in setting up XStream:

- Do not use `ALTER SESSION SET CONTAINER` commands. In a single-tenant
  database, there is only one instance, so container switching doesn’t apply.
- Create only one `xstream_adm_tbs` tablespace. Do not create a second
  tablespace in a PDB.
- Do not use the `C##` prefix on user names. For example, create
  `xstreamadmin` instead of `c##xstreamadmin` and `connectuser` instead
  of `c##connectuser`. The `C##` prefix is required only in multi-tenant
  environments.
- Do not include `CONTAINER=ALL` or `container => 'ALL'` in any commands.
  These clauses grant privileges across multiple containers and don’t apply
  in a single-tenant database.

## Data Guard or standby capture (optional)

By default, the procedures in this topic create the XStream outbound server on
the primary (source) database. If you want to keep replication load off the primary, review
[Data Guard and standby support](/user-guide/data-integration/openflow/connectors/oracle/about#label-oracle-standby-data-guard-support)
and choose a supported topology before you create the outbound server.

### Logical standby requirements

On a logical standby, create the XStream outbound server and connect the
connector to that standby the same way you would for a primary. Before you
create the outbound server or start the connector, set Database Guard to
`STANDBY`.

Logical standbys default to Database Guard `ALL`, which blocks the XStream
client from reading the outbound server and raises
`ORA-16224: Database Guard is enabled`.

1. Check the current guard status:

   Copy code

   ```
   SELECT guard_status FROM v$database;
   ```
2. If the result is `ALL`, set Database Guard to `STANDBY`:

   Copy code

   ```
   ALTER DATABASE GUARD STANDBY;
   ```

Then complete the XStream setup procedures in this topic on the logical
standby, and point the connector’s Oracle connection URL and XStream Out Server
URL at that standby.

### Active Data Guard requirements for snapshot load

You can run the connector’s snapshot load against an Active Data Guard physical
standby to avoid reading application tables on the primary. Because the standby
is read-only:

- Set **Snapshot Fetching Strategy** to `SEQUENTIAL_BY_PRIMARY_KEY` in the
  connector parameters. `CONCURRENT_BY_ROWID` requires creating a parallel
  task, which isn’t allowed on a read-only standby.
- Don’t create the XStream outbound server on the Active Data Guard standby.
  For CDC, create it on the primary, a logical standby, or a downstream
  capture database instead.

Point the connector’s Oracle connection URL at the Active Data Guard standby
for snapshot reads. Point the XStream Out Server URL at the writable database
that hosts the outbound server (for example, the primary or a downstream
capture database).

### Downstream capture for CDC

To run CDC off the primary, configure Oracle downstream capture so that a
separate database receives redo from the primary, then create the XStream
outbound server on that downstream database by using the procedures in this
topic.

Downstream capture provides redo only. It can’t serve snapshot queries. If you
also need an initial snapshot without reading the primary, combine Active Data
Guard for the snapshot with downstream capture for CDC, or use a logical
standby for both stages.

For Oracle’s downstream capture concepts and setup, see
[XStream Out Concepts](https://docs.oracle.com/en/database/oracle/oracle-database/19/xstrm/xstream-out-concepts.html)
in the Oracle documentation.

## Configure SSL connections (optional)

The Openflow Connector for Oracle supports encrypted SSL connections to the Oracle database using the TCPS
(TCP with SSL) protocol. When SSL is enabled, both the database connection and the XStream connection use encrypted communication.

To use SSL, you must:

1. [Enable TCPS on the Oracle database](#label-enable-tcps-on-oracle-database)
2. [Create a client wallet](#label-create-client-wallet)

### Enable TCPS on the Oracle database

You must configure the Oracle database to accept connections using the TCPS protocol.
Follow the procedure for your database environment.

#### On-premises / OCI

1. Create an SSL server wallet with the server certificate.
2. Configure the `listener.ora` to include a TCPS endpoint (default port 2484).
3. Configure the `sqlnet.ora` to reference the server wallet.
4. Restart the listener.

For more information, see
[Configuring Transport Layer Security Encryption](https://docs.oracle.com/en/database/oracle/oracle-database/23/dbseg/configuring-transport-layer-security-encryption.html).

#### AWS RDS (Standard)

1. Add the Oracle SSL option to the option group associated with the DB instance.
2. Specify the SSL port (for example, 2484).

For more information, see
[Oracle Secure Sockets Layer](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.Oracle.Options.SSL.html).

### Create a client wallet

After TCPS is enabled on the database, create an Oracle auto-login wallet (`cwallet.sso`)
containing the server’s trusted certificate. This wallet is provided to the connector so
that it can verify the server during the SSL handshake.

1. Export the server certificate from the Oracle database server as a PEM file.
2. Use the Oracle `orapki` utility to create a client wallet and import the server certificate:

   Copy code

   ```
   orapki wallet create -wallet /path/to/client/wallet -pwd <wallet_password> -auto_login

   orapki wallet add -wallet /path/to/client/wallet -pwd <wallet_password> \
   -trusted_cert -cert /path/to/server-cert.pem
   ```
3. Copy the generated `cwallet.sso` file to a location accessible by the Openflow runtime.

Note

For AWS RDS, download the root certificate from AWS instead of exporting it from the
database server. For more information, see
[Connecting to an RDS for Oracle DB instance using SSL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.Oracle.Options.SSL.Connecting.html).

For more information, see
[Using the orapki Utility to Manage PKI Elements](https://docs.oracle.com/en/database/oracle/oracle-database/23/dbseg/using-the-orapki-utility-to-manage-pki-elements.html).

## Next steps

[Configure the connector](/user-guide/data-integration/openflow/connectors/oracle/setup-connector).
