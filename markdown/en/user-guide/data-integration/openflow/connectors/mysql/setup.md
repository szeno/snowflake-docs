# Set up the Openflow Connector for MySQL

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for MySQL.

## Prerequisites

### Before you begin

1. Ensure that you have reviewed [About Openflow Connector for MySQL](/user-guide/data-integration/openflow/connectors/mysql/about).
2. Ensure that you have MySQL 8 or later to synchronize data with Snowflake.
3. Make sure you have an Openflow deployment and runtime for this connector. If you don’t, see
   [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs)
   or [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc).

   A runtime’s size is fixed when you create it, so decide on a size before you create the runtime.
   See [Runtime sizing and packing for CDC connectors](/user-guide/data-integration/openflow/connectors/cdc-runtime-sizing).
4. If using Snowflake deployments, ensure that you’ve reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
   and have granted access to the required domains for the [MySQL](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-mysql) connector.

### Source database setup

As a database administrator, perform the following tasks:

1. Enable [binary logs](https://dev.mysql.com/doc/refman/8.4/en/binary-log.html), then save and configure its format as follows:

   |  |  |
   | --- | --- |
   | `log_bin` | Set to `on`.  This enables the binary log that records structural and data changes. |
   | `binlog_format` | Set to `row`.  The connector supports only row-based replication. MySQL 8.x versions may be the last ones to support this setting, and future versions will only support row-based replication.  Not applicable in GCP Cloud SQL, where it is fixed at the right value. |
   | `binlog_row_metadata` | Set to `full`.  The connector requires all row metadata to operate, most importantly, column names and primary key information.  Under Microsoft Azure Database for MySQL the `binlog_row_metadata` field isn’t user modifiable. Raise a Microsoft support ticket to change this value. |
   | `binlog_row_image` | Set to `full`.  The connector requires that all columns be written into the binary log.  Not applicable in Amazon Aurora, where it is fixed at the right value. |
   | `binlog_row_value_options` | Leave empty.  This option only affects JSON columns, where it can be set to include only the modified parts of JSON documents for `UPDATE` statements. The connector requires that full documents are written into the binary log. |
   | `binlog_expire_logs_seconds` | Snowflake recommends setting the [binary log expiration period (binlog\_expire\_logs\_seconds)](https://dev.mysql.com/doc/refman/8.4/en/replication-options-binary-log.html#sysvar_binlog_expire_logs_seconds) to at least 72 hours (`259200`).  Retention has to cover the entire window between a replication problem starting, someone noticing it, and the fix being applied. Once the expiration period elapses, MySQL can remove binary log files automatically, and Openflow can’t replicate data from files that no longer exist, so the data is lost. Time spent paused counts toward that window, whether the pause is planned maintenance or an unnoticed failure.  If you’re using scheduled replication, the value needs to be longer than the configured schedule. |
   | `binlog_legacy_event_pos` | Set to `ON`.  Required only when the source is MariaDB. The connector requires this flag to track binary log positions correctly during replication.  Not applicable to MySQL. |

   Expand

   Show lessSee more

   For example:

   Copy code

   ```
   log_bin = on
   binlog_format = row
   binlog_row_metadata = full
   binlog_row_image = full
   binlog_row_value_options =
   ```
2. Increase the value of `sort_buffer_size`.

   Copy code

   ```
   sort_buffer_size = 4194304
   ```

   `sort_buffer_size` defines the amount of memory (in bytes) allocated per query thread for in-memory sorting operations, such as ORDER BY.
   If the value is too small, the connector may fail with the following error message:

   `Out of sort memory, consider increasing server sort buffer size`.
   This indicates that `sort_buffer_size` should be raised.
3. If you’re using Amazon RDS databases, then increase the retention period relevant to *binlog\_expire\_logs\_seconds* using *rds\_set\_configuration*.
   For example, if you want to store binlog for 24 hours, then call `mysql.rds_set_configuration('binlog retention hours', 24)`.
4. When using a read replica to connect, binary logging must be enabled on the replica.
5. After binary logging is enabled, configure the replica to log the events received from its source into its own binary log.

   Copy code

   ```
   log_replica_updates = ON
   ```

   `log_replica_updates` allows the replica to write events received from its source to its own binary
   log, making those changes available to any databases that are replicating from it.
6. Connect via SSL. If you’re planning to use an SSL connection to MySQL, prepare the root certificate for your database server.
   It is required during configuration.
7. Create a user for the connector. The connector requires a user with the REPLICATION SLAVE and REPLICATION CLIENT privileges
   for reading the binary logs. Grant these privileges:

   Copy code

   ```
   GRANT REPLICATION SLAVE ON *.* TO '<username>'@'%'
   GRANT REPLICATION CLIENT ON *.* TO '<username>'@'%'
   ```
8. Grant the SELECT privilege on every replicated table:

   Copy code

   ```
   GRANT SELECT ON <schema>.* TO '<username>'@'%'
   GRANT SELECT ON <schema>.<table> TO '<username>'@'%'
   ```

   For more information on replication security, see [Binary log](https://dev.mysql.com/doc/refman/8.4/en/binary-log.html).

### Snowflake account setup

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

## Gather these before you install

You can stop and collect any of these later, but having them on hand first lets you install and
configure the connector in one pass:

- **The MariaDB JDBC driver `.jar` file.** You supply the driver file itself, so download it
  beforehand.
- **A JDBC connection URL**, which must use the `jdbc:mariadb` scheme because the connector
  connects through the MariaDB driver. SSL is configured in the URL itself rather than as a
  separate property, by appending an `sslMode` parameter.
- **A source database user** with the privileges described in
  [Source database setup](#source-database-setup).
- **The source database user’s password.**
- **Decisions on the settings that can’t be changed later.** Destination schema naming, object
  identifier resolution (whether MySQL names are stored case-sensitively or uppercased), and table
  storage format are fixed once the connector has applied its configuration and begun ingesting.
  Changing them afterwards requires a new connector instance and a fresh snapshot.

## Install the connector

### Choose your generation

This connector is available in both gen 1 and gen 2.

|  | Gen 2 (recommended) | Gen 1 |
| --- | --- | --- |
| **Management** | SQL commands + setup wizard | Runtime canvas UI |
| **Configuration** | Versioned config files, CI/CD-friendly | Canvas parameters |
| **Release status** | Public Preview | Generally Available |

Expand

Show lessSee more

If you’re unsure, see [Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations) for a full comparison.

Note

The catalog lists two entries with the same name, **MySQL and MariaDB**. The gen 2 entry is the
one marked with a **Gen 2** tag, and it also carries a **Preview** tag during public preview. The
gen 1 entry has no tag.

Install the connector from the Openflow connector catalog.

To install the connector, do the following as a data engineer:

1. Navigate to the **Connector library** tab in Openflow.
2. On the Openflow connectors page, find the entry for the generation you chose and select
   **Install**.
3. Select the runtime to install the connector on. If you’re prompted to authenticate, sign in with
   your Snowflake account credentials.

What happens next depends on the generation you chose:

- **Gen 2**: the setup wizard opens and collects the connector’s configuration in one guided flow.
  Continue with Configure the connector below, which describes the values this connector needs. If
  you would rather configure the connector programmatically instead of using the wizard, see
  [Configure a gen 2 connector with SQL](/user-guide/data-integration/openflow/gen2/configure-connector-sql).
- **Gen 1**: the Openflow canvas appears with the connector process group added to it.

## Configure the connector

*Using gen 1? [Skip to Configure on the canvas.](#label-mysql-configure-gen1-canvas)*

### Configure with the setup wizard or SQL (gen 2)

Tip

[CoCo](/user-guide/cortex-code/cortex-code) can help you make sure your prerequisites are in place. Try pasting this prompt into CoCo:

> Please help me with the prerequisites for a gen 2 Openflow connector for MySQL and MariaDB. Use skill @(serverSkill:openflow).

Gen 2 references the source database password as a Snowflake secret of type `GENERIC_STRING`
rather than taking the password inline. Create the secret in the same database and schema that
holds your Openflow infrastructure objects (the runtime and connector), keeping infrastructure
separate from the destination database where replicated data is persisted:

Copy code

```
CREATE SECRET <openflow_db>.<openflow_schema>.<secret_name>
  TYPE = GENERIC_STRING
  SECRET_STRING = '<source_db_password>';

GRANT READ ON SECRET <openflow_db>.<openflow_schema>.<secret_name> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
```

If the execute-as role doesn’t already have `USAGE` on the infrastructure database and schema
(for example, if you deviated from the recommended setup path), grant it:

Copy code

```
GRANT USAGE ON DATABASE <openflow_db> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
GRANT USAGE ON SCHEMA <openflow_db>.<openflow_schema> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
```

With the secret in place, configure the connector with the [setup wizard](/user-guide/data-integration/openflow/gen2/setup-connector-wizard) or, for automation, by
editing the connector’s `config.json` with SQL and stage file operations; see
[Configure a gen 2 connector with SQL](/user-guide/data-integration/openflow/gen2/configure-connector-sql).

### Gen 2 parameters

The following table lists the gen 2 connector parameters, grouped by the wizard step where you
configure them. The wizard’s **Step Documentation** panel describes each property in full; this
table gives the parameter name and its purpose so you can prepare before entering the wizard.

| Parameter | Wizard step | Description |
| --- | --- | --- |
| Source Database Connection URL | Source | The JDBC URL to the MySQL or MariaDB source. It must start with `jdbc:mariadb://` and can include the SSL mode. For example: `jdbc:mariadb://db.example.com:3306/?sslMode=verify-full`. |
| Source Database Driver | Source | The [MariaDB JDBC driver](https://mariadb.com/downloads/connectors/connectors-data-access/java8-connector/) `.jar`, uploaded in the wizard. |
| Source Database User | Source | The source database user with `REPLICATION SLAVE`, `REPLICATION CLIENT`, `SELECT`, and `RELOAD` privileges. |
| Source Database Password | Source | A Snowflake secret of type `GENERIC_STRING` holding the source user’s password, with `READ` granted to the execute-as role. |
| Configure Logical Keys | Source | Whether to use default primary-key detection or declare custom logical keys for tables without a usable primary key. |
| Included Source Table Pattern | Replication table schema | The schemas and tables to replicate, selected manually or matched by a regular expression. |
| Replication Columns | Replication columns | Which columns to include per table, and whether newly added columns are included automatically. |
| Snowflake Destination Database | Destination details | The database where replicated data is persisted. The execute-as role needs `USAGE` and `CREATE SCHEMA` on it. |
| Snowflake Warehouse | Destination details | The warehouse used for merge operations. Start with `XSMALL`; for many tables, a multi-cluster warehouse scales better than a larger size. |
| Destination Schema Strategy | Destination details | How destination schemas are named, to avoid collisions when consolidating more than one source database into a single Snowflake database. Fixed after first apply. |
| Object Identifier Resolution | Destination details | Whether source object names are stored case-sensitively (default) or uppercased (recommended). Fixed after first apply. |
| Oversized Value Strategy | Destination details | How values exceeding the 16 MB limit are handled. Defaults to **Set Null**. |
| Error Handling Strategy | Destination details | How invalid rows are handled. Defaults to **Log Errors and Continue**. |
| Table Storage Format | Destination details | Standard Snowflake tables or Iceberg tables. Fixed after first apply. |
| Iceberg Version | Destination details | When using Iceberg, the table version (2 or 3, default 3). |
| Merge Task Schedule CRON | Tuning | CRON expression controlling when journal data is merged into destination tables, which is when warehouse cost accrues. |
| Concurrent Snapshot Queries | Tuning | How many tables to snapshot concurrently (default 2). Each holds a source database connection. |
| Ingestion Type | Migration | Whether new tables get a full snapshot before switching to CDC (default) or go straight to incremental. |
| Starting Binlog Position | Migration | Where in the binlog to start reading: Latest (default) or Earliest. |

Expand

Show lessSee more

*Using gen 2? [Skip to Run the flow.](#label-mysql-run-the-flow)*

### Configure on the canvas (gen 1)

To configure the connector on the canvas, do the following as a data engineer:

1. Right-click on the imported process group and select **Parameters**.
2. Populate the required parameter values.

   For more information on the required parameter values, see the following sections:

   - [MySQL Source Parameters](#label-of-mysql-source-parameters): Used to establish a connection with MySQL.
   - [MySQL Destination Parameters](#label-of-mysql-destination-parameters): Used to establish a connection with Snowflake.
   - [MySQL Ingestion Parameters](#label-of-mysql-ingestion-parameters): Used to specify the tables to replicate.

Start with setting the parameters of the MySQL Source Parameters context, then the MySQL Destination Parameters context.
After this is done, you can enable the connector. The connector should connect to both MySQL and Snowflake and start running.
However, the connector doesn’t replicate any data until any tables to be replicated are explicitly added to its configuration.

To configure specific tables for replication, edit the MySQL Ingestion Parameters context. After you apply the changes to the
MySQL Ingestion Parameters context, the configuration is picked up by the connector, and the replication lifecycle starts for every table.

To run multiple CDC connector instances on one runtime, see .

### MySQL Source Parameters

| Parameter | Description |
| --- | --- |
| MySQL Connection URL | The full JDBC URL to the source database. The connector uses the MariaDB driver, which is compatible with MySQL and requires the `jdbc:mariadb` prefix in the URL. If the SSL is disabled, then the connection URL should have the `allowPublicKeyRetrieval` parameter set to `true`. Examples:   - With SSL enabled: `jdbc:mariadb://example.com:3306` - With SSL disabled: `jdbc:mariadb://example.com:3306?allowPublicKeyRetrieval=true` |
| MySQL JDBC Driver | The absolute path to the [MariaDB JDBC driver jar](https://mariadb.com/downloads/connectors/connectors-data-access/java8-connector/). The connector uses the MariaDB driver, which is compatible with MySQL. Select the **Reference asset** checkbox to upload the MariaDB JDBC driver. Example: `/opt/resources/drivers/mariadb-java-client-3.5.2.jar` |
| MySQL Username | The username for the connector. |
| MySQL Password | The password for the connector. |

Expand

Show lessSee more

### MySQL Destination Parameters

| Parameter | Description | Required |
| --- | --- | --- |
| Destination Database | The database where data is persisted. It must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase. | Yes |
| Destination Schema Pattern | A pattern for the names of destination schemas where data is persisted. The connector creates the schemas if they don’t exist.  You can customize the pattern per ingested table using these optional variables:   - `${source.schema.name}`: the source database (a database in MySQL maps to a schema in Snowflake). - `${source.table.name}`: a source table’s name.   For example, for a table `my_database.users`, the pattern `prefix_${source.schema.name}` evaluates to `prefix_my_database`.  To ingest all tables into a single schema, provide a schema name without any variables, like `destination_schema`.  Important  Don’t change this setting after the connector has begun ingesting data. Changing this setting after ingestion has begun breaks the existing ingestion. If you must change this setting, create a new connector instance. | Yes |
| Snowflake Authentication Strategy | When using:   - **Snowflake Openflow Deployment** or **BYOC**: Use SNOWFLAKE\_MANAGED.   This token is managed automatically by Snowflake.   BYOC deployments must have previously configured   [execute-as roles](/user-guide/data-integration/openflow/setup-openflow-byoc#label-deployment-byoc-setup-runtime-role) to use SNOWFLAKE\_MANAGED. - **BYOC**: Alternatively, BYOC can use KEY\_PAIR as the value for the authentication strategy. | Yes |
| Snowflake Account Identifier | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Snowflake account name formatted as [organization-name]-[account-name]. | Yes |
| Snowflake Connection Strategy | When using KEY\_PAIR, specify the strategy for connecting to Snowflake:   - **STANDARD** (default): Connect using standard public routing to Snowflake services. - **PRIVATE\_CONNECTIVITY**: Connect using private addresses associated with the supporting cloud platform such as AWS PrivateLink. | Required for BYOC with KEY\_PAIR only, otherwise ignored. |
| Snowflake Private Key | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Must be the RSA private key used for authentication, formatted according to PKCS8   standards and including standard PEM headers and footers. Note that either a Snowflake Private   Key File or a Snowflake Private Key must be defined. | No |
| Snowflake Private Key File | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: The private key file must be blank. - **KEY\_PAIR**: Upload the file that contains the RSA private key used for authentication to Snowflake,   formatted according to PKCS8 standards and including standard PEM headers and footers.   The header line begins with `-----BEGIN PRIVATE`.   To upload the private key file, select the **Reference asset** checkbox. | No |
| Snowflake Private Key Password | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the password associated with the Snowflake Private Key File. | No |
| Snowflake Role | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Use the runtime’s execute-as role (or a child role granted to it).   You can find your execute-as role in the Openflow UI by navigating to **View Details** for your runtime. - **KEY\_PAIR**: Use a valid role configured for your service user. | Yes |
| Snowflake Username | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the user name used to connect to the Snowflake instance. | Yes |
| Oversized Value Strategy | Determines how the connector handles values that exceed its internal size limits (16 MB) during replication. Possible values are:  - **Fail Table** (default): The table is marked as permanently failed, and replication stops for that table. - **Set Null**: The value is replaced with `NULL` in the destination table.   Use this to prevent table failures when it is acceptable to lose data in tables beyond the oversized value. | No |
| Error Handling Strategy | Determines how the connector handles invalid rows that Snowflake rejects during ingestion. Possible values are:  - **Fail Table** (default): The table is marked as failed on the first invalid row, and replication stops for that table. - **Log Errors and Continue**: The connector keeps replicating the valid rows and records each rejected row in the table’s error table. | No |
| Table Storage Format | Standard Snowflake tables or Iceberg tables. Defaults to **STANDARD**. Don’t change after the connector starts. | Yes |
| Iceberg Version | The Iceberg table version, 2 or 3 (default 3). Ignored unless Table Storage Format is **ICEBERG**. Don’t change this value after ingestion begins. | No |
| Snowflake Warehouse | Snowflake warehouse used to run queries. | Yes |

Expand

Show lessSee more

### MySQL Ingestion Parameters

| Parameter | Description |
| --- | --- |
| Included Table Names | A comma-separated list of table paths, including their schemas. Example: `public.my_table, other_schema.other_table` |
| Included Table Regex | A regular expression to match against table paths. Every path matching the expression will be replicated, and new tables matching the pattern that get created later will also be included automatically. Example: `public\.auto_.*` |
| Column Filter JSON | Optional. A JSON array of filter objects specifying which columns to include or exclude per table. For syntax details and examples, see [Replicate a subset of columns in a table](#replicate-a-subset-of-columns-in-a-table). |
| Table Key Configuration Service | Optional. A `JsonTableKeyConfigService` controller service that supplies a user-declared logical key for one or more tables. The service exposes a **Table Key Configuration JSON** property where you define the key mappings. When configured, the logical key takes the highest priority and overrides any primary key that the connector would otherwise auto-detect.  For more information, see [Specify a logical key for a table](#label-mysql-logical-key). |
| Merge Task Schedule CRON | A CRON expression defining when the connector merges journal data into destination tables, which is when warehouse cost accrues. The **Merge Journal to Destination** processor performs the merge on this schedule. With no new changes waiting, no merge runs and the warehouse is free to auto-suspend. Set it to `* * * * * ?` for continuous merges (lowest latency, highest cost), or schedule merges to limit warehouse run time. The connector evaluates the schedule in the UTC time zone.  For example:  - The string `* 0 * * * ?` indicates that you want to schedule merges at the full hour for one minute. - The string `* 20 14 ? * MON-FRI` indicates that you want to schedule merges at 2:20 PM every   Monday through Friday.  For additional information and examples, see the cron triggers tutorial in the [Quartz Documentation](https://www.quartz-scheduler.org/documentation/quartz-2.5.x/tutorials/crontrigger.html). |
| Object Identifier Resolution | Specifies how source object identifiers such as the names of schemas, tables, and columns are stored and queried in Snowflake. This setting specifies that you must use double quotes in SQL queries.  Option 1: Default, case-sensitive. For backwards compatibility.   - **Transformation**: Case is preserved.   For example, `My_Table` remains `My_Table`. - **Queries**: SQL queries must use double quotes to match the exact case for database objects.   For example, `SELECT * FROM "My_Table";`.   Note  Snowflake recommends using this option if you must preserve source casing for legacy or compatibility reasons. For example, if the source database includes table names that differ in case only–such as `MY_TABLE` and `my_table`–that would result in a name collision when using when using case-insensitive comparisons. Option 2: Recommended, case-insensitive  - **Transformation**: All identifiers are converted to uppercase. For example, `My_Table` becomes `MY_TABLE`. - **Queries**: SQL queries are case-insensitive and don’t require SQL double quotes.   For example, `SELECT * FROM my_table;` returns the same results as `SELECT * FROM MY_TABLE;`.   Note  Snowflake recommends using this option if database objects are not expected to have mixed case names.  Important  Do not change this setting after the connector has begun ingesting data. Changing this setting after ingestion has begun breaks the existing ingestion. If you must change this setting, create a new connector instance. |
| Concurrent Snapshot Queries | Maximum number of concurrent queries to the source database to run in the Snapshot flow. Increasing this can speed up snapshotting large numbers of tables, but will also increase the load on the source database. |

Expand

Show lessSee more

## Replicate a subset of columns in a table

The following describes the gen 1 `Column Filter JSON` parameter. In gen 2, you
select columns per table in the **Replication columns** step of the setup wizard;
see [Configure with the setup wizard or SQL (gen 2)](#configure-with-the-setup-wizard-or-sql-gen-2) for that step.

The connector can filter the data replicated per table to a subset of configured columns.
Primary key columns are always included regardless of exclusions.

To apply column filters, set the **Column Filter JSON** parameter in the Ingestion Parameters context
to a JSON array of filter objects, one per table you want to filter.

Columns can be included or excluded by name or by regular expression pattern. You can apply a single condition per table,
or combine multiple conditions, with exclusions always taking precedence over inclusions.

## Syntax

Each object in the array identifies a table and specifies which columns to include or exclude.

Copy code

```
[
    {
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

- Use `schema` and `table` for exact name matching, or `schemaPattern` and `tablePattern`
  for regex matching. You can’t use both a field and its pattern variant in the same object
  (for example, `schema` and `schemaPattern` can’t both appear).
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
        "schema": "public",
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
        "schema": "public",
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
        "schema": "public",
        "table": "contacts",
        "includedPattern": ".*_email",
        "excluded": ["admin_email"]
    }
]
```

Mix a schema pattern with an exact table name to apply a filter across schemas:

Copy code

```
[
    {
        "schemaPattern": "data_.*",
        "table": "customers",
        "excluded": ["internal_note"]
    }
]
```

Pass multiple filter objects to apply different rules to different tables:

Copy code

```
[
    {"schema": "public", "table": "orders", "included": ["account_id", "status"]},
    {"schema": "public", "table": "customers", "excludedPattern": ".*_internal"}
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

## Specify a logical key for a table

The connector requires a replication key for every table it replicates. By default, the
connector uses the table’s primary key. A *logical key* is a user-declared replacement
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
        "schema": "<schema>",
        "table": "<table>",
        "logicalKey": ["<column>", "<column>"]
    }
]
```

The fields are:

| Field | Description |
| --- | --- |
| `schema` | Required. The exact source schema name. |
| `table` | Required. The exact source table name. |
| `logicalKey` | Required. A non-empty array of source column names that uniquely identify rows in the table. |

Expand

Show lessSee more

The following rules apply:

- `schema`, `table`, and `logicalKey` column matching is **case-sensitive**. Use the
  exact names as reported by MySQL.
- An entry whose `schema` and `table` don’t match any replicated table is silently ignored.

### Logical key configuration examples

A single-column logical key on a table without a primary key:

Copy code

```
[
    {
        "schema": "sales",
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
        "schema": "sales",
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
        "schema": "sales",
        "table": "audit_log",
        "logicalKey": ["event_id"]
    },
    {
        "schema": "sales",
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

When the configuration is rejected, the connector either fails to enable the
controller service (for structural issues detected at enablement time) or holds the
table in the `NEW` state (for issues detected when the table is initialized). After
you fix the configuration, replication for the table resumes without resetting state.

### Warnings logged for risky configurations

The connector accepts the following configurations but logs a warning at table
initialization.

When choosing logical-key columns, prefer columns with high cardinality and, where
possible, monotonically increasing values. Low-cardinality or non-monotonic keys can
degrade snapshot performance.

- A logical-key column is a large-object type (`blob`, `tinyblob`, `mediumblob`,
  `longblob`, `text`, `tinytext`, `mediumtext`, `longtext`). Using large objects as
  keys severely degrades MERGE performance.
- A logical-key column is a floating-point type (`float`, `double`). Floating-point
  comparisons can produce inconsistent results because of precision differences.
- A logical-key column is a semi-structured type (`json`). Semi-structured values may
  produce non-deterministic equality comparisons.
- The composite logical key includes more than five columns. Long composite keys often
  indicate a design issue and might degrade MERGE performance.
- The logical key overrides an existing primary key on the table. Verify that the
  replacement key is intentional: the connector no longer uses the primary key for
  MERGE operations.

If you observe data divergence after any of these warnings, run a periodic full reload
to reconcile the destination with the source.

### Schema changes that affect a logical key

Logical keys reference column names. The connector doesn’t follow renames or drops of
those columns:

- If a logical-key column is dropped on the source, replication for the affected table
  fails. The table is marked `FAILED`. For more information, see
  [Restart table replication](/user-guide/data-integration/openflow/connectors/mysql/maintenance#label-of-mysql-restart-table-replication).
- If a logical-key column is renamed on the source, the configuration still references
  the old name and replication fails. Update the JSON to use the new name and restart
  table replication.

## Run the flow

### Gen 2

After you apply your configuration in the wizard, the connector’s status moves to **Upgrading** and
then to **Stopped** once upgrading finishes. Start it from the **Installed Connectors** tab: open the
connector’s menu and select **Start**.

If the connector is still in **Draft** when you reach this step, its configuration hasn’t been
applied. Open the setup wizard and select **Apply** so your changes take effect before you start.

After starting, open the connector’s observability dashboard to confirm data is moving and there
are no errors.

To start, stop, or otherwise manage a gen 2 connector programmatically, see
[Manage the gen 2 Openflow connector lifecycle](/user-guide/data-integration/openflow/gen2/manage-connector-lifecycle).

### Gen 1

1. Right-click on the canvas and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.

## Set up alerts

Snowflake recommends setting up alerts so that you’re notified of ingestion errors or stalled
replication without having to check the connector manually. This applies to both gen 1 and gen 2
connectors.

Openflow writes telemetry, including logs and metrics, to an event table. Build an alert on that
telemetry with a scheduled query: see [Monitor Openflow using telemetry data](/user-guide/data-integration/openflow/monitor) for the
available telemetry and example queries, and [Setting up alerts based on data in Snowflake](/user-guide/alerts) for how to create an alert
from a query.
